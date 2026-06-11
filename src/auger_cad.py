#!/usr/bin/env python3
"""
MudMixer Auger CAD Export

Generates a watertight 3D triangle mesh of the shaftless variable-pitch
helical auger (per US 10,259,140 / US 11,285,639) and exports it as a
binary STL file suitable for CAD import, 3D printing, or CFD meshing.

The flight is modeled as a rectangular-section helical ribbon swept from
the hopper section (low pitch) into the chute section (high pitch) with a
step-wise pitch transition at the aperture, matching the patent's
"step-wise increase" embodiment. Mixing fingers are added as octagonal
prisms projecting from the flight inner edge into the interior volume.

Usage:
    python auger_cad.py --stl auger.stl --render auger.png

Dependencies:
    - none for mesh generation and STL export (standard library only)
    - matplotlib (optional, for PNG rendering)
"""

import argparse
import math
import struct
from typing import List, Optional, Tuple

from auger_optimizer import AugerGeometry, FingerConfig, FingerMaterial

Vec3 = Tuple[float, float, float]
Triangle = Tuple[Vec3, Vec3, Vec3]

# Minimum open-center radius preserved at finger tips. The shaftless
# design's aggregate-handling advantage depends on keeping the center open.
MIN_OPEN_CENTER_RADIUS = 0.3  # inches


def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _normalize(v: Vec3) -> Vec3:
    mag = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if mag == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / mag, v[1] / mag, v[2] / mag)


def _sweep_rings(
    geometry: AugerGeometry,
    segments_per_turn: int,
) -> List[Tuple[float, float]]:
    """
    Integrate the helix axial position over sweep angle.

    The local pitch sets dz/dθ = pitch(z) / 2π, so the hopper section
    advances slowly (more mixing time) and the chute section advances
    quickly (accelerated conveyance), exactly as the patent describes.

    Returns:
        List of (theta, z) pairs for each ring station.
    """
    d_theta = 2 * math.pi / segments_per_turn
    rings = [(0.0, 0.0)]
    theta, z = 0.0, 0.0

    while z < geometry.total_length:
        pitch = (
            geometry.pitch_hopper
            if z < geometry.length_hopper
            else geometry.pitch_chute
        )
        theta += d_theta
        z = min(z + pitch * d_theta / (2 * math.pi), geometry.total_length)
        rings.append((theta, z))

    return rings


def _ring_corners(
    theta: float, z: float, r_inner: float, r_outer: float, thickness: float
) -> List[Vec3]:
    """
    Cross-section corners at one sweep station.

    Ordered counterclockwise in the local (radial, axial) plane:
    inner-bottom, outer-bottom, outer-top, inner-top.
    """
    c, s = math.cos(theta), math.sin(theta)
    return [
        (r_inner * c, r_inner * s, z),
        (r_outer * c, r_outer * s, z),
        (r_outer * c, r_outer * s, z + thickness),
        (r_inner * c, r_inner * s, z + thickness),
    ]


def build_flight_mesh(
    geometry: AugerGeometry,
    segments_per_turn: int = 64,
) -> List[Triangle]:
    """
    Build a watertight triangle mesh of the helical flight ribbon.

    Args:
        geometry: Auger geometry from the optimizer
        segments_per_turn: Angular resolution (64 ≈ 5.6° facets)

    Returns:
        List of triangles with consistent outward-facing winding
    """
    r_outer = geometry.outer_diameter / 2
    r_inner = geometry.inner_diameter / 2
    thickness = geometry.flight_thickness

    stations = _sweep_rings(geometry, segments_per_turn)
    rings = [
        _ring_corners(theta, z, r_inner, r_outer, thickness)
        for theta, z in stations
    ]

    triangles: List[Triangle] = []

    # Side surfaces: one quad strip per cross-section edge.
    # Winding (u_i, u_j, v_j, v_i) yields outward normals for a CCW section.
    for ring_a, ring_b in zip(rings, rings[1:]):
        for k in range(4):
            u_a, v_a = ring_a[k], ring_a[(k + 1) % 4]
            u_b, v_b = ring_b[k], ring_b[(k + 1) % 4]
            triangles.append((u_a, u_b, v_b))
            triangles.append((u_a, v_b, v_a))

    # End caps: start cap faces against the sweep, end cap faces along it.
    a, b, c, d = rings[0]
    triangles.append((a, b, c))
    triangles.append((a, c, d))
    a, b, c, d = rings[-1]
    triangles.append((a, c, b))
    triangles.append((a, d, c))

    return triangles


def build_finger_mesh(
    geometry: AugerGeometry,
    fingers: FingerConfig,
    segments_per_turn: int = 64,
    sides: int = 8,
) -> List[Triangle]:
    """
    Build mixing fingers as closed octagonal prisms projecting inward
    from the flight inner edge, distributed evenly along the auger.

    Finger length is clamped so tips never close off the open center
    (the shaftless design's defining feature).
    """
    r_inner = geometry.inner_diameter / 2
    radius = fingers.diameter / 2
    stations = _sweep_rings(geometry, segments_per_turn)

    # Embed the base slightly into the flight ribbon so the shells fuse.
    base_radius = r_inner + min(0.2, (geometry.outer_diameter / 2 - r_inner) / 2)
    max_reach = base_radius - MIN_OPEN_CENTER_RADIUS
    length = min(fingers.length + (base_radius - r_inner), max_reach)

    triangles: List[Triangle] = []
    total = geometry.total_length

    for k in range(fingers.count):
        z_target = total * (k + 0.5) / fingers.count
        theta, z = min(stations, key=lambda st: abs(st[1] - z_target))
        cos_t, sin_t = math.cos(theta), math.sin(theta)

        # Radially-inward axis with an orthonormal section basis.
        axis = (-cos_t, -sin_t, 0.0)
        e1 = (0.0, 0.0, 1.0)
        e2 = _cross(axis, e1)

        center = (
            base_radius * cos_t,
            base_radius * sin_t,
            z + geometry.flight_thickness / 2,
        )

        base_ring = []
        tip_ring = []
        for j in range(sides):
            phi = 2 * math.pi * j / sides
            offset = (
                radius * (math.cos(phi) * e1[0] + math.sin(phi) * e2[0]),
                radius * (math.cos(phi) * e1[1] + math.sin(phi) * e2[1]),
                radius * (math.cos(phi) * e1[2] + math.sin(phi) * e2[2]),
            )
            base = (center[0] + offset[0], center[1] + offset[1], center[2] + offset[2])
            tip = (
                base[0] + length * axis[0],
                base[1] + length * axis[1],
                base[2] + length * axis[2],
            )
            base_ring.append(base)
            tip_ring.append(tip)

        for j in range(sides):
            jn = (j + 1) % sides
            triangles.append((base_ring[j], base_ring[jn], tip_ring[jn]))
            triangles.append((base_ring[j], tip_ring[jn], tip_ring[j]))

        for j in range(1, sides - 1):
            triangles.append((base_ring[0], base_ring[j + 1], base_ring[j]))
            triangles.append((tip_ring[0], tip_ring[j], tip_ring[j + 1]))

    return triangles


def build_auger_mesh(
    geometry: AugerGeometry,
    fingers: Optional[FingerConfig] = None,
    segments_per_turn: int = 64,
) -> List[Triangle]:
    """Build the complete auger mesh: flight ribbon plus mixing fingers."""
    mesh = build_flight_mesh(geometry, segments_per_turn)
    if fingers is not None and fingers.count > 0:
        mesh += build_finger_mesh(geometry, fingers, segments_per_turn)
    return mesh


def mesh_volume(triangles: List[Triangle]) -> float:
    """
    Signed volume via divergence theorem (cubic inches).

    Positive for consistently outward-wound watertight meshes.
    """
    volume = 0.0
    for v0, v1, v2 in triangles:
        cross = _cross(v1, v2)
        volume += (v0[0] * cross[0] + v0[1] * cross[1] + v0[2] * cross[2]) / 6.0
    return volume


def write_binary_stl(
    triangles: List[Triangle],
    path: str,
    solid_name: str = "MudMixer shaftless auger",
) -> None:
    """Write triangles to a binary STL file."""
    header = solid_name.encode("ascii", errors="replace")[:80].ljust(80, b"\0")
    with open(path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(triangles)))
        for v0, v1, v2 in triangles:
            normal = _normalize(_cross(_sub(v1, v0), _sub(v2, v0)))
            f.write(struct.pack("<12fH", *normal, *v0, *v1, *v2, 0))


def render_mesh(
    triangles: List[Triangle],
    path: str,
    elev: float = 18.0,
    azim: float = -55.0,
) -> None:
    """
    Render the mesh to a PNG with isometric and end-on views.

    Requires matplotlib (optional dependency).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Flat-shade each facet against a fixed light direction.
    light = _normalize((0.4, -0.6, 0.7))
    base = (0.54, 0.61, 0.67)  # steel grey
    face_colors = []
    for v0, v1, v2 in triangles:
        normal = _normalize(_cross(_sub(v1, v0), _sub(v2, v0)))
        intensity = abs(
            normal[0] * light[0] + normal[1] * light[1] + normal[2] * light[2]
        )
        scale = 0.35 + 0.65 * intensity
        face_colors.append(tuple(channel * scale for channel in base))

    xs = [v[0] for tri in triangles for v in tri]
    ys = [v[1] for tri in triangles for v in tri]
    zs = [v[2] for tri in triangles for v in tri]
    ranges = (
        max(xs) - min(xs),
        max(ys) - min(ys),
        max(zs) - min(zs),
    )

    fig = plt.figure(figsize=(11, 6))
    views = [
        ("Isometric view", elev, azim, 1.0),
        ("End-on view (open center)", 90.0, -90.0, 2.4),
    ]
    for i, (title, view_elev, view_azim, zoom) in enumerate(views, start=1):
        ax = fig.add_subplot(1, 2, i, projection="3d")
        collection = Poly3DCollection(
            triangles, facecolors=face_colors, linewidths=0
        )
        ax.add_collection3d(collection)
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(ys), max(ys))
        ax.set_zlim(min(zs), max(zs))
        ax.set_box_aspect(ranges, zoom=zoom)
        ax.view_init(elev=view_elev, azim=view_azim)
        ax.set_title(title)
        ax.set_axis_off()

    fig.suptitle(
        "MudMixer Shaftless Variable-Pitch Auger (generated geometry)",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)


def main(argv: Optional[List[str]] = None):
    """Generate STL/render for the default optimized geometry."""
    parser = argparse.ArgumentParser(
        description="Export MudMixer auger mesh as STL and/or PNG render"
    )
    parser.add_argument("--housing-id", type=float, default=6.0,
                        help="Housing internal diameter, inches (default: 6.0)")
    parser.add_argument("--segments", type=int, default=64,
                        help="Mesh segments per turn (default: 64)")
    parser.add_argument("--stl", metavar="PATH", help="Output STL path")
    parser.add_argument("--render", metavar="PATH", help="Output PNG path")
    args = parser.parse_args(argv)

    from auger_optimizer import AugerOptimizer

    design = AugerOptimizer(args.housing_id).generate_optimized_design()
    geometry = design["objects"]["geometry"]
    fingers = design["objects"]["fingers"]

    mesh = build_auger_mesh(geometry, fingers, segments_per_turn=args.segments)
    print(f"Mesh: {len(mesh)} triangles, "
          f"flight volume {mesh_volume(mesh):.1f} in³, "
          f"OD {geometry.outer_diameter:.2f}\", "
          f"length {geometry.total_length:.1f}\"")

    if args.stl:
        write_binary_stl(mesh, args.stl)
        print(f"STL exported: {args.stl}")
    if args.render:
        render_mesh(mesh, args.render)
        print(f"Render saved: {args.render}")
    if not args.stl and not args.render:
        print("No output requested; use --stl and/or --render.")


if __name__ == "__main__":
    main()
