"""Tests for the auger CAD mesh generation and STL export."""

import math
import os
import struct
from collections import Counter

import pytest

from auger_cad import (
    _sweep_rings,
    build_auger_mesh,
    build_flight_mesh,
    mesh_volume,
    write_binary_stl,
)
from auger_optimizer import AugerGeometry, AugerOptimizer, FingerConfig, FingerMaterial


@pytest.fixture
def geometry():
    return AugerGeometry(
        outer_diameter=4.5,
        inner_diameter=3.69,
        length_hopper=10.0,
        length_chute=14.0,
        pitch_hopper=2.925,
        pitch_chute=3.825,
    )


@pytest.fixture
def fingers():
    return FingerConfig(FingerMaterial.STEEL_1045, diameter=0.375, length=2.0, count=8)


def assert_watertight(triangles):
    """Every directed edge must appear exactly once, paired with its reverse.

    This guarantees the mesh is closed (no holes), manifold, and
    consistently oriented — the requirements for a printable STL.
    """
    edges: Counter[tuple] = Counter()
    for v0, v1, v2 in triangles:
        edges[(v0, v1)] += 1
        edges[(v1, v2)] += 1
        edges[(v2, v0)] += 1

    for edge, count in edges.items():
        assert count == 1, f"directed edge {edge} appears {count} times"
        assert edges[(edge[1], edge[0])] == 1, f"unpaired edge {edge}"


class TestFlightMesh:
    def test_watertight(self, geometry):
        assert_watertight(build_flight_mesh(geometry, segments_per_turn=32))

    def test_volume_matches_analytic(self, geometry):
        """A helical ribbon of thickness t swept through total angle θ covers
        each angular column once per turn, so V = t·(Ro²−Ri²)/2·θ exactly."""
        segments = 64
        mesh = build_flight_mesh(geometry, segments_per_turn=segments)
        theta_total = _sweep_rings(geometry, segments)[-1][0]

        r_outer = geometry.outer_diameter / 2
        r_inner = geometry.inner_diameter / 2
        expected = (
            geometry.flight_thickness * (r_outer**2 - r_inner**2) / 2 * theta_total
        )

        assert mesh_volume(mesh) == pytest.approx(expected, rel=0.02)

    def test_outward_orientation(self, geometry):
        assert mesh_volume(build_flight_mesh(geometry, segments_per_turn=32)) > 0

    def test_extents(self, geometry):
        mesh = build_flight_mesh(geometry, segments_per_turn=32)
        xs = [v[0] for tri in mesh for v in tri]
        zs = [v[2] for tri in mesh for v in tri]
        assert max(xs) == pytest.approx(geometry.outer_diameter / 2, rel=1e-6)
        assert max(zs) == pytest.approx(
            geometry.total_length + geometry.flight_thickness, rel=1e-6
        )

    def test_variable_pitch_sweep(self, geometry):
        """The hopper section (low pitch) must take more turns per inch
        than the chute section (high pitch)."""
        rings = _sweep_rings(geometry, 64)
        aperture_theta = next(t for t, z in rings if z >= geometry.length_hopper)
        hopper_turns = aperture_theta / (2 * math.pi)
        chute_turns = rings[-1][0] / (2 * math.pi) - hopper_turns

        assert hopper_turns / geometry.length_hopper > chute_turns / geometry.length_chute
        assert hopper_turns == pytest.approx(
            geometry.length_hopper / geometry.pitch_hopper, rel=0.05
        )


class TestFullMesh:
    def test_watertight_with_fingers(self, geometry, fingers):
        assert_watertight(build_auger_mesh(geometry, fingers, segments_per_turn=32))

    def test_fingers_preserve_open_center(self, geometry, fingers):
        """Finger tips must never close off the shaftless open center."""
        from auger_cad import MIN_OPEN_CENTER_RADIUS, build_finger_mesh

        mesh = build_finger_mesh(geometry, fingers, segments_per_turn=32)
        min_radius = min(
            math.hypot(v[0], v[1]) for tri in mesh for v in tri
        )
        # Allow for octagon corner offset around the finger axis
        assert min_radius >= MIN_OPEN_CENTER_RADIUS - fingers.diameter / 2

    def test_optimizer_design_meshes_cleanly(self):
        design = AugerOptimizer(housing_id=6.0).generate_optimized_design()
        mesh = build_auger_mesh(
            design["objects"]["geometry"],
            design["objects"]["fingers"],
            segments_per_turn=32,
        )
        assert_watertight(mesh)
        assert mesh_volume(mesh) > 0


class TestSTLExport:
    def test_binary_stl_structure(self, geometry, tmp_path):
        mesh = build_flight_mesh(geometry, segments_per_turn=16)
        path = tmp_path / "auger.stl"
        write_binary_stl(mesh, str(path))

        # Binary STL: 80-byte header + 4-byte count + 50 bytes/triangle
        assert os.path.getsize(path) == 84 + 50 * len(mesh)

        with open(path, "rb") as f:
            header = f.read(80)
            (count,) = struct.unpack("<I", f.read(4))
        assert b"MudMixer" in header
        assert count == len(mesh)

    def test_stl_normals_are_unit_length(self, geometry, tmp_path):
        mesh = build_flight_mesh(geometry, segments_per_turn=16)
        path = tmp_path / "auger.stl"
        write_binary_stl(mesh, str(path))

        with open(path, "rb") as f:
            f.seek(84)
            for _ in range(min(50, len(mesh))):
                values = struct.unpack("<12fH", f.read(50))
                normal_mag = math.sqrt(sum(x**2 for x in values[:3]))
                assert normal_mag == pytest.approx(1.0, abs=1e-5)
