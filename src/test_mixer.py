"""Tests for the full-machine CAD model and cross-specification analysis."""

import math
import os

import pytest

import mixer_analysis
from geometry import (
    bounding_box,
    box,
    cylinder,
    flip,
    is_watertight,
    mesh_centroid,
    mesh_volume,
    rect_funnel,
    transform,
    tube,
)
from mixer_cad import SPEC, build_mixer, export_stls, validate_assembly


class TestPrimitives:
    def test_box_volume_and_integrity(self):
        mesh = box(2.0, 3.0, 4.0)
        assert is_watertight(mesh)
        assert mesh_volume(mesh) == pytest.approx(24.0)
        assert mesh_centroid(mesh) == pytest.approx((0.0, 0.0, 0.0), abs=1e-9)

    def test_cylinder_volume(self):
        mesh = cylinder(radius=2.0, height=5.0, segments=128)
        assert is_watertight(mesh)
        # Polygonal area converges to πr² from below
        assert mesh_volume(mesh) == pytest.approx(math.pi * 4 * 5, rel=0.002)

    def test_tube_volume(self):
        mesh = tube(outer_radius=3.0, inner_radius=2.5, height=10.0, segments=128)
        assert is_watertight(mesh)
        expected = math.pi * (3.0**2 - 2.5**2) * 10.0
        assert mesh_volume(mesh) == pytest.approx(expected, rel=0.002)

    def test_rect_funnel_shell(self):
        mesh = rect_funnel(20.0, 18.0, 8.0, 6.0, 10.0, wall=0.075)
        assert is_watertight(mesh)
        assert mesh_volume(mesh) > 0

    def test_flip_inverts_volume(self):
        mesh = box(1.0, 1.0, 1.0)
        assert mesh_volume(flip(mesh)) == pytest.approx(-mesh_volume(mesh))

    def test_transform_preserves_volume(self):
        from mixer_cad import rot_y
        mesh = cylinder(1.0, 4.0, 32)
        moved = transform(mesh, rot_y(105.0), (3.0, -2.0, 7.0))
        assert mesh_volume(moved) == pytest.approx(mesh_volume(mesh), rel=1e-9)
        assert is_watertight(moved)


class TestAssembly:
    @pytest.fixture(scope="class")
    def components(self):
        return build_mixer()

    @pytest.fixture(scope="class")
    def report(self, components):
        return validate_assembly(components)

    def test_every_component_watertight(self, report):
        for name, data in report["components"].items():
            assert data["watertight"], f"{name} is not watertight"
            assert data["volume_in3"] > 0, f"{name} has non-positive volume"

    def test_all_validation_checks_pass(self, report):
        failures = [c for c in report["checks"] if c["status"] != "OK"]
        assert failures == [], f"failed checks: {failures}"

    def test_envelope_matches_spec(self, report):
        length, width, height = report["envelope_in"]
        assert length == pytest.approx(SPEC["overall_length_in"], rel=0.10)
        assert width == pytest.approx(SPEC["overall_width_in"], rel=0.10)
        assert height == pytest.approx(SPEC["overall_height_in"], rel=0.10)

    def test_discharge_height(self, report):
        assert report["discharge_height_in"] == pytest.approx(
            SPEC["discharge_height_in"], abs=1.0
        )

    def test_mass_budget_brackets_spec(self, report):
        low, high = report["reconciled_weight_range_lb"]
        assert low <= SPEC["dry_weight_lb"] <= high + 10

    def test_machine_sits_on_ground(self, components):
        everything = [t for c in components.values() for t in c.triangles]
        (_, _, z0), _ = bounding_box(everything)
        assert z0 == pytest.approx(0.0, abs=1e-6)

    def test_stability_margins(self, report):
        assert report["cg_loaded_x"] < 20.0          # never tips over the axle
        assert 0.3 < report["wheel_load_fraction"] < 0.9
        assert report["handle_lift_empty_lb"] < 60.0

    def test_lateral_symmetry(self, report):
        assert report["cg_empty"][1] == pytest.approx(0.0, abs=0.5)

    def test_converged_design_point_also_validates(self):
        """The machine must validate at BOTH the 6.0\" baseline and the
        6.5\" self-consistent design point (DESIGN_INSIGHTS D11)."""
        components = build_mixer(housing_id=6.5)
        report = validate_assembly(components, housing_id=6.5)
        failures = [c for c in report["checks"] if c["status"] != "OK"]
        assert failures == [], f"failed at 6.5\" bore: {failures}"
        assert report["measured_bore_clearance_in"] >= 0.6

    def test_stl_export(self, components, tmp_path):
        paths = export_stls(components, str(tmp_path))
        # One STL per component plus the combined assembly
        assert len(paths) == len(components) + 1
        for path in paths:
            size = os.path.getsize(path)
            assert size > 84 and (size - 84) % 50 == 0


class TestThroughputAnalysis:
    def test_flow_equation(self):
        result = mixer_analysis.throughput_analysis(fill_efficiency=0.35)
        d, p = result["auger_diameter_in"], result["pitch_chute_in"]
        expected_in3_min = (math.pi / 4) * d**2 * p * 27.0 * 0.35
        assert result["flow_ft3_hr"] == pytest.approx(
            expected_in3_min * 60 / 1728
        )

    def test_implied_efficiency_scales_inversely(self):
        base = mixer_analysis.throughput_analysis(fill_efficiency=0.35)
        # Implied η is a property of the claim and geometry, not the assumed η
        other = mixer_analysis.throughput_analysis(fill_efficiency=0.20)
        assert base["implied_fill_efficiency"] == pytest.approx(
            other["implied_fill_efficiency"]
        )

    def test_implied_auger_size_roundtrip(self):
        """The implied diameter must reproduce the claimed flow exactly."""
        size = mixer_analysis.implied_auger_size(claimed_bags_hr=45.0)
        d = size["implied_auger_od_in"]
        flow = (math.pi / 4) * d**3 * 0.85 * 27.0 * 0.35  # in³/min
        bags = flow * 60 / 1728 / mixer_analysis.BAG_80LB_YIELD_FT3
        assert bags == pytest.approx(45.0, rel=1e-9)

    def test_claim_implies_larger_bore_than_assumed(self):
        size = mixer_analysis.implied_auger_size()
        assert size["implied_housing_id_in"] > 6.0
        assert not size["assumption_consistent"]


class TestWaterAndPower:
    def test_water_demand_balances(self):
        water = mixer_analysis.water_demand(bags_hr=45.0)
        assert water["gpm_required"] == pytest.approx(45 * 3.5 / 4 / 60)
        assert water["supply_adequate"]
        assert 0.05 < water["water_mass_fraction"] < 0.15

    def test_published_electrical_specs_are_inconsistent(self):
        """0.5 HP out on 312 W in violates conservation of energy."""
        audit = mixer_analysis.power_audit()
        assert audit["implied_efficiency"] > 1.0
        assert not audit["specs_consistent"]
        assert audit["amps_needed_at_full_load"] > 2.6

    def test_drivetrain_requires_reduction(self):
        drive = mixer_analysis.drivetrain_analysis()
        assert drive["required_ratio"] == pytest.approx(1800 / 27)
        assert 60 < drive["output_torque_ft_lb"] < 100


class TestHopperCapacity:
    def test_modeled_hopper_holds_rating(self):
        volume = mixer_analysis.hopper_cavity_volume_in3()
        capacity = mixer_analysis.hopper_capacity_check(volume)
        assert capacity["capacity_adequate"]
        assert capacity["fill_fraction_at_rating"] < 1.0

    def test_prismatoid_volume(self):
        # Degenerate case: straight box 10×8×11 → exactly 880 in³
        volume = mixer_analysis.hopper_cavity_volume_in3(10, 8, 10, 8, 11)
        assert volume == pytest.approx(880.0)


class TestCLI:
    def test_report_runs_clean(self, capsys):
        from mixer_cad import main
        main(["--report"])
        output = capsys.readouterr().out
        assert "ALL CHECKS PASS" in output

    def test_analysis_main(self, capsys):
        mixer_analysis.main()
        output = capsys.readouterr().out
        assert "CROSS-SPECIFICATION" in output
        assert "IMPLIED TRUE AUGER SIZE" in output
