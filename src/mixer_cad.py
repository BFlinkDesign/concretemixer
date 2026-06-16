#!/usr/bin/env python3
"""
MudMixer Full-Machine Parametric CAD Model

Builds the complete mixer assembly as watertight triangle meshes from the
reverse-engineered specifications (docs/SPECIFICATIONS.md, docs/ASSEMBLIES.md):

    frame rails / cross members / handles / legs    1" steel pipe
    wheels + axle                                   Marathon flat-free, 5/8" axle
    hopper                                          14 ga steel funnel, top at 35"
    chute housing                                   14 ga steel tube, 6" bore
    shaftless auger + fingers                       from auger_cad / auger_optimizer
    motor + transformer box                         0.5 HP DC drive

The assembly is laid out at the 15-degree tilt preset with the discharge
opening at the specified 16" height. Every component is independently
watertight, carries a material density, and contributes to the mass /
center-of-gravity / stability validation in validate_assembly().

Usage:
    python mixer_cad.py --report
    python mixer_cad.py --stl-dir cad_out --render assembly.png --exploded exploded.png

Dependencies:
    - none for geometry, STL export, and validation (standard library only)
    - matplotlib (optional, for rendering)
"""

import argparse
import math
import os
from dataclasses import dataclass
from typing import Any

from auger_cad import build_auger_mesh, render_mesh  # noqa: F401  (render_mesh re-exported)
from auger_optimizer import AugerOptimizer
from geometry import (
    Triangle,
    Vec3,
    bounding_box,
    box,
    cross,
    cylinder,
    is_watertight,
    mesh_centroid,
    mesh_volume,
    normalize,
    pipe_between,
    rect_funnel,
    rot_x,
    rot_y,
    sub,
    transform,
    tube,
    write_binary_stl,
)

# ---------------------------------------------------------------------------
# Specification targets (docs/SPECIFICATIONS.md)
# ---------------------------------------------------------------------------

SPEC = {
    "overall_length_in": 66.5,
    "overall_width_in": 27.5,
    "overall_height_in": 35.0,
    "discharge_height_in": 16.0,
    "dry_weight_lb": 145.0,
    "hopper_capacity_lb": 120.0,
    "max_lift_height_in": 42.0,
    "tilt_preset_deg": 15.0,        # using the shallow preset (15/25/35)
    "housing_id_in": 6.0,
}

# Material densities, lb/in³. Pipe members are modeled as solid rods with an
# effective density scaled by the 1" sch-40 pipe wall/solid area ratio (~0.42).
DENSITY = {
    "steel": 0.284,
    "pipe_effective": 0.284 * 0.42,
    "rubber_wheel": 0.0255,
    "motor_average": 0.110,        # ~15 lb right-angle gearmotor over envelope
    "electronics": 0.033,          # ~8 lb transformer + controls over enclosure
}

# Mass allowance for items not modeled as solids: auger guard, pivot
# plates, water plumbing, wiring, fasteners (docs/BOM.md categories).
UNMODELED_ALLOWANCE_LB = (8.0, 22.0)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

@dataclass
class Component:
    """One rigid part of the mixer with material and render metadata."""
    name: str
    triangles: list[Triangle]
    density: float                       # lb/in³
    color: tuple[float, float, float]
    explode_dir: Vec3 = (0.0, 0.0, 0.0)  # unit offset for exploded views

    @property
    def volume(self) -> float:
        return mesh_volume(self.triangles)

    @property
    def weight_lb(self) -> float:
        return self.volume * self.density

    @property
    def centroid(self) -> Vec3:
        return mesh_centroid(self.triangles)


def build_mixer(housing_id: float = SPEC["housing_id_in"]) -> dict[str, Component]:
    """
    Build the full machine in world coordinates:
    +x toward discharge, +y left, +z up, ground plane at z=0.

    The hopper aperture seats directly on the chute housing, which runs
    the full auger length from the swivel discharge to the motor coupling
    bell — matching the patent's rigid hopper/chute coupling.
    """
    tilt = math.radians(SPEC["tilt_preset_deg"])
    # Unit vector pointing rearward/up along the auger axis
    u_rear = (-math.cos(tilt), 0.0, math.sin(tilt))
    discharge = (21.0, 0.0, SPEC["discharge_height_in"])

    def along_axis(s: float) -> Vec3:
        """Point s inches rearward of the discharge opening, on the axis."""
        return (
            discharge[0] + s * u_rear[0],
            discharge[1] + s * u_rear[1],
            discharge[2] + s * u_rear[2],
        )

    # Rotation taking +z to the discharge direction (-u_rear)
    axis_rotation = rot_y(90.0 + SPEC["tilt_preset_deg"])
    wall = 0.075  # 14 gauge

    components: dict[str, Component] = {}

    def add(component: Component):
        components[component.name] = component

    # --- Auger inside the full-length chute housing -----------------------
    design = AugerOptimizer(housing_id).generate_optimized_design()
    geometry = design["objects"]["geometry"]
    fingers = design["objects"]["fingers"]

    auger_local = build_auger_mesh(geometry, fingers, segments_per_turn=48)
    add(Component(
        "auger", transform(auger_local, axis_rotation,
                           along_axis(geometry.total_length + 0.5)),
        DENSITY["steel"], (0.72, 0.74, 0.78), explode_dir=(0.97, 0.0, -0.26),
    ))

    housing_len = 26.0
    housing_local = tube(housing_id / 2 + wall, housing_id / 2, housing_len, 64)
    add(Component(
        "chute_housing",
        transform(housing_local, axis_rotation, along_axis(housing_len)),
        DENSITY["steel"], (0.85, 0.55, 0.15),
    ))

    # Swivel discharge spout: steeper drop for placement, with collar ring
    spout_rotation = rot_y(140.0)
    add(Component(
        "discharge_spout",
        transform(tube(housing_id / 2 + 0.2, housing_id / 2 + 0.05, 4.0, 48),
                  spout_rotation, discharge),
        DENSITY["steel"], (0.55, 0.58, 0.62), explode_dir=(0.77, 0.0, -0.64),
    ))
    add(Component(
        "swivel_collar",
        transform(tube(housing_id / 2 + 0.45, housing_id / 2 + 0.21, 1.8, 48),
                  spout_rotation, discharge),
        DENSITY["steel"], (0.30, 0.32, 0.36), explode_dir=(0.77, 0.0, -0.64),
    ))

    # Water injection manifold with dual spray nozzles at the aperture zone
    manifold_center = along_axis(14.0)
    add(Component(
        "water_manifold",
        transform(tube(housing_id / 2 + 0.45, housing_id / 2 + 0.08, 1.4, 48),
                  axis_rotation, along_axis(14.7)),
        DENSITY["steel"], (0.72, 0.45, 0.20), explode_dir=(0.26, 0.0, 0.97),
    ))
    nozzles = []
    for sy in (1, -1):
        n_hat = (0.0, sy * 0.643, 0.766)
        base = (manifold_center[0] + 2.8 * n_hat[0],
                manifold_center[1] + 2.8 * n_hat[1],
                manifold_center[2] + 2.8 * n_hat[2])
        tip = (manifold_center[0] + 4.6 * n_hat[0],
               manifold_center[1] + 4.6 * n_hat[1],
               manifold_center[2] + 4.6 * n_hat[2])
        nozzles += pipe_between(base, tip, radius=0.28, segments=12)
    add(Component(
        "spray_nozzles", nozzles, DENSITY["steel"], (0.78, 0.55, 0.25),
        explode_dir=(0.26, 0.0, 0.97),
    ))

    # Motor coupling bell and water-sealed gearmotor at the rear
    add(Component(
        "motor_bell",
        transform(tube(housing_id / 2 + 0.1, 2.6, 2.5, 48),
                  axis_rotation, along_axis(28.5)),
        DENSITY["steel"], (0.45, 0.47, 0.50), explode_dir=(-0.97, 0.0, 0.26),
    ))
    add(Component(
        "motor", transform(cylinder(2.5, 7.0, 48), axis_rotation, along_axis(35.5)),
        DENSITY["motor_average"], (0.22, 0.22, 0.25), explode_dir=(-0.97, 0.0, 0.26),
    ))

    # --- Hopper seated on the housing over the low-pitch auger section ----
    seat = along_axis(18.0)
    hopper_base_z = seat[2] + (housing_id / 2 + wall) / math.cos(tilt) - 0.25
    hopper_local = rect_funnel(22.0, 20.0, 10.0, 8.0,
                               SPEC["overall_height_in"] - hopper_base_z, wall)
    add(Component(
        "hopper", transform(hopper_local, None, (seat[0], 0.0, hopper_base_z)),
        DENSITY["steel"], (0.88, 0.78, 0.25), explode_dir=(0.0, 0.0, 1.0),
    ))

    # --- Transformer / control enclosure on the body floor ----------------
    add(Component(
        "control_box", transform(box(8.0, 6.0, 5.0), None, (-14.0, 0.0, 12.0)),
        DENSITY["electronics"], (0.3, 0.5, 0.35), explode_dir=(-0.5, 0.0, 0.87),
    ))

    # --- Frame: rails, cross members, handles, legs, posts, braces --------
    # Joint endpoints are staggered slightly into the mating member so no
    # two end caps share a plane and center (coincident cap fans would
    # create duplicate edges and break the manifold check).
    rail_z, rail_y = 10.0, 10.0
    frame_members = []
    for sy in (1, -1):
        frame_members += pipe_between((-32.0, sy * rail_y, rail_z), (24.0, sy * rail_y, rail_z))
        frame_members += pipe_between((-31.5, sy * rail_y, rail_z), (-41.5, sy * rail_y, 16.5))
        frame_members += pipe_between(
            (-28.0, sy * rail_y, rail_z + 0.45), (-28.0, sy * rail_y, 0.55)
        )
        frame_members += pipe_between((6.5, sy * rail_y, rail_z + 0.45), (6.5, sy * 4.0, 19.5))
        frame_members += pipe_between((18.0, sy * rail_y, rail_z + 0.42), (7.0, sy * 4.4, 19.0))
    frame_members += pipe_between((-28.0, -rail_y - 0.48, rail_z), (-28.0, rail_y + 0.48, rail_z))
    frame_members += pipe_between((18.0, -rail_y - 0.48, rail_z), (18.0, rail_y + 0.48, rail_z))
    add(Component(
        "frame", frame_members, DENSITY["pipe_effective"], (0.35, 0.38, 0.42),
    ))

    # Handle grips
    grips = []
    for sy in (1, -1):
        grips += pipe_between((-38.3, sy * rail_y, 14.6), (-42.0, sy * rail_y, 16.8),
                               radius=0.7, segments=16)
    add(Component("handle_grips", grips, DENSITY["rubber_wheel"],
                  (0.10, 0.10, 0.10)))

    # 14 ga body panels (sides + floor) between the rails
    panels = []
    panels += transform(box(30.0, wall, 5.5), None, (-8.0, 9.4, 9.2))
    panels += transform(box(30.0, wall, 5.5), None, (-8.0, -9.4, 9.2))
    panels += transform(box(30.0, 18.7, wall), None, (-8.0, 0.0, 9.42))
    add(Component(
        "body_panels", panels, DENSITY["steel"], (0.55, 0.58, 0.62),
        explode_dir=(0.0, 0.0, -1.0),
    ))

    # Support feet pads under the legs
    feet = []
    for sy in (1, -1):
        feet += transform(box(3.0, 2.5, 0.6), None, (-28.0, sy * rail_y, 0.3))
    add(Component("support_feet", feet, DENSITY["steel"], (0.25, 0.27, 0.30)))

    # --- Running gear ------------------------------------------------------
    axle_y = 13.75
    axle = transform(cylinder(0.3125, 2 * axle_y, 16), rot_x(-90.0), (20.0, -axle_y, 5.0))
    add(Component("axle", axle, DENSITY["steel"], (0.5, 0.5, 0.5)))

    brackets = []
    for sy in (1, -1):
        brackets += transform(box(2.0, 0.8, 4.8), None, (20.0, sy * rail_y, 7.3))
    add(Component("axle_brackets", brackets, DENSITY["steel"], (0.4, 0.42, 0.45)))

    wheels = []
    for sy in (1, -1):
        wheel_local = cylinder(5.0, 3.5, 48)
        wheels += transform(wheel_local, rot_x(-90.0),
                            (20.0, sy * axle_y - (3.5 if sy > 0 else 0.0), 5.0))
    add(Component(
        "wheels", wheels, DENSITY["rubber_wheel"], (0.12, 0.12, 0.12),
        explode_dir=(0.0, 1.0, 0.0),
    ))

    return components


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_assembly(
    components: dict[str, Component],
    housing_id: float = SPEC["housing_id_in"],
) -> dict[str, Any]:
    """
    Validate the modeled machine against docs/SPECIFICATIONS.md.

    Checks: per-component mesh integrity, mass budget vs 145 lb dry weight,
    overall envelope, discharge height, hopper lift height, auger clearance,
    center of gravity, axle/leg load split, and handle lift effort.

    Args:
        components: assembly from build_mixer()
        housing_id: bore used to build it (6.0 baseline or the 6.5
            self-consistent design point from DESIGN_INSIGHTS D11)
    """
    report: dict[str, Any] = {"components": {}, "checks": []}

    def check(name: str, ok: bool, detail: str):
        report["checks"].append(
            {"name": name, "status": "OK" if ok else "FAIL", "detail": detail}
        )

    # Per-component integrity and mass
    total_weight = 0.0
    moment = [0.0, 0.0, 0.0]
    for component in components.values():
        watertight = is_watertight(component.triangles)
        volume = component.volume
        weight = component.weight_lb
        centroid = component.centroid
        report["components"][component.name] = {
            "triangles": len(component.triangles),
            "watertight": watertight,
            "volume_in3": volume,
            "weight_lb": weight,
            "centroid": centroid,
        }
        check(f"mesh:{component.name}", watertight and volume > 0,
              f"{len(component.triangles)} tris, {volume:.1f} in³, {weight:.1f} lb")
        total_weight += weight
        for i in range(3):
            moment[i] += weight * centroid[i]

    cg_empty = tuple(m / total_weight for m in moment)
    report["modeled_weight_lb"] = total_weight
    report["cg_empty"] = cg_empty

    # Mass budget vs spec
    low, high = UNMODELED_ALLOWANCE_LB
    reconciled = (total_weight + low, total_weight + high)
    report["unmodeled_allowance_lb"] = UNMODELED_ALLOWANCE_LB
    report["reconciled_weight_range_lb"] = reconciled
    check("mass_budget",
          reconciled[0] <= SPEC["dry_weight_lb"] <= reconciled[1] + 10,
          f"modeled {total_weight:.0f} lb + {low:.0f}-{high:.0f} lb panels/guard/"
          f"hardware = {reconciled[0]:.0f}-{reconciled[1]:.0f} lb vs spec "
          f"{SPEC['dry_weight_lb']:.0f} lb")

    # Envelope
    everything = [t for c in components.values() for t in c.triangles]
    (x0, y0, z0), (x1, y1, z1) = bounding_box(everything)
    length, width, height = x1 - x0, y1 - y0, z1 - z0
    report["envelope_in"] = (length, width, height)
    for axis_name, measured, spec_key in (
        ("length", length, "overall_length_in"),
        ("width", width, "overall_width_in"),
        ("height", height, "overall_height_in"),
    ):
        check(f"envelope_{axis_name}",
              abs(measured - SPEC[spec_key]) / SPEC[spec_key] < 0.10,
              f"{measured:.1f}\" vs spec {SPEC[spec_key]}\"")
    check("ground_plane", abs(z0) < 1e-6, f"lowest point at z={z0:.3f}\"")

    # Only the running gear and support feet may touch the ground
    ground_contact = {"wheels", "support_feet"}
    floating_min = min(
        v[2] for name, c in components.items() if name not in ground_contact
        for tri in c.triangles for v in tri
    )
    check("ground_contact_discipline", floating_min > 0.4,
          f"non-wheel/foot components clear ground by {floating_min:.2f}\"")

    # Discharge height: centroid of the housing's discharge-end face,
    # found by projecting vertices onto the chute axis direction
    tilt_rad = math.radians(SPEC["tilt_preset_deg"])
    u_dis = (math.cos(tilt_rad), 0.0, -math.sin(tilt_rad))
    housing_verts = {v for tri in components["chute_housing"].triangles for v in tri}
    s_max = max(v[0] * u_dis[0] + v[2] * u_dis[2] for v in housing_verts)
    face = [v for v in housing_verts
            if v[0] * u_dis[0] + v[2] * u_dis[2] > s_max - 0.01]
    discharge_z = sum(v[2] for v in face) / len(face)
    report["discharge_height_in"] = discharge_z
    check("discharge_height", abs(discharge_z - SPEC["discharge_height_in"]) < 1.0,
          f"discharge centerline at {discharge_z:.1f}\" "
          f"(spec {SPEC['discharge_height_in']}\")")

    # Hopper lift height (patent claim 12: < 42")
    _, (_, _, hopper_top) = bounding_box(components["hopper"].triangles)
    check("hopper_lift_height", hopper_top < SPEC["max_lift_height_in"],
          f"hopper rim at {hopper_top:.1f}\" < {SPEC['max_lift_height_in']}\"")

    # Auger-to-housing clearance, MEASURED from the meshes: every auger
    # vertex must lie inside the housing bore with aggregate clearance.
    u = (-math.cos(tilt_rad), 0.0, math.sin(tilt_rad))
    origin = (
        sum(v[0] for v in face) / len(face),
        sum(v[1] for v in face) / len(face),
        discharge_z,
    )

    def radial_distance(v: Vec3) -> float:
        w = sub(v, origin)
        t = w[0] * u[0] + w[1] * u[1] + w[2] * u[2]
        perp = (w[0] - t * u[0], w[1] - t * u[1], w[2] - t * u[2])
        return math.sqrt(perp[0] ** 2 + perp[1] ** 2 + perp[2] ** 2)

    max_auger_radius = max(
        radial_distance(v)
        for tri in components["auger"].triangles for v in tri
    )
    bore_radius = housing_id / 2
    measured_clearance = bore_radius - max_auger_radius
    min_clearance = 0.5 * 1.2  # 0.5" aggregate + 20%
    report["measured_bore_clearance_in"] = measured_clearance
    check("auger_clearance_measured", measured_clearance >= min_clearance,
          f"mesh-measured {measured_clearance:.2f}\"/side vs min "
          f"{min_clearance:.2f}\" for 0.5\" aggregate")

    # Stability: supports at the axle (x=20) and the legs (x=-28)
    x_axle, x_leg, x_handle = 20.0, -28.0, -43.0
    payload = SPEC["hopper_capacity_lb"]
    hopper_cg = components["hopper"].centroid

    w_loaded = total_weight + payload
    cg_loaded_x = (total_weight * cg_empty[0] + payload * hopper_cg[0]) / w_loaded
    report["cg_loaded_x"] = cg_loaded_x

    check("no_forward_tip_loaded", cg_loaded_x < x_axle,
          f"loaded CG at x={cg_loaded_x:.1f}\" is {x_axle - cg_loaded_x:.1f}\" "
          "behind the axle")
    check("no_rearward_tip", cg_empty[0] > x_leg,
          f"empty CG at x={cg_empty[0]:.1f}\" is {cg_empty[0] - x_leg:.1f}\" "
          "ahead of the support legs")

    # Load split and wheelbarrow lift effort (pivot about the axle)
    wheel_share = (cg_empty[0] - x_leg) / (x_axle - x_leg)
    lift_empty = total_weight * (x_axle - cg_empty[0]) / (x_axle - x_handle)
    lift_loaded = w_loaded * (x_axle - cg_loaded_x) / (x_axle - x_handle)
    report["wheel_load_fraction"] = wheel_share
    report["handle_lift_empty_lb"] = lift_empty
    report["handle_lift_loaded_lb"] = lift_loaded
    check("handle_lift_effort", lift_empty < 60.0,
          f"{lift_empty:.0f} lb empty / {lift_loaded:.0f} lb loaded "
          "(two-handed wheelbarrow lift)")

    report["all_ok"] = all(c["status"] == "OK" for c in report["checks"])
    return report


def print_report(report: dict[str, Any]) -> None:
    print("=" * 72)
    print("MUDMIXER FULL-MACHINE CAD VALIDATION")
    print("=" * 72)
    print(f"\n{'Component':<16}{'Tris':>7}{'Vol in³':>10}{'Weight lb':>11}  Watertight")
    print("-" * 72)
    for name, data in report["components"].items():
        print(f"{name:<16}{data['triangles']:>7}{data['volume_in3']:>10.1f}"
              f"{data['weight_lb']:>11.1f}  {'yes' if data['watertight'] else 'NO'}")
    print("-" * 72)
    print(f"{'modeled total':<33}{report['modeled_weight_lb']:>11.1f}")
    low, high = report["reconciled_weight_range_lb"]
    print(f"{'with panels/guard/hardware':<33}{low:>6.0f}-{high:.0f} lb "
          f"(spec: {SPEC['dry_weight_lb']:.0f} lb)")

    length, width, height = report["envelope_in"]
    print(f"\nEnvelope: {length:.1f} × {width:.1f} × {height:.1f} in "
          f"(spec {SPEC['overall_length_in']} × {SPEC['overall_width_in']} × "
          f"{SPEC['overall_height_in']})")
    cg = report["cg_empty"]
    print(f"Empty CG: ({cg[0]:.1f}, {cg[1]:.1f}, {cg[2]:.1f}) in   "
          f"wheel load {report['wheel_load_fraction']*100:.0f}%   "
          f"lift {report['handle_lift_empty_lb']:.0f} lb empty / "
          f"{report['handle_lift_loaded_lb']:.0f} lb loaded")

    print(f"\n{'Check':<26}{'Status':<8}Detail")
    print("-" * 72)
    for c in report["checks"]:
        print(f"{c['name']:<26}{c['status']:<8}{c['detail']}")
    print("-" * 72)
    print("RESULT:", "ALL CHECKS PASS" if report["all_ok"] else "FAILURES PRESENT")


# ---------------------------------------------------------------------------
# Rendering and export
# ---------------------------------------------------------------------------

def render_assembly(
    components: dict[str, Component],
    path: str,
    explode: float = 0.0,
    views: list[tuple[str, float, float]] | None = None,
) -> None:
    """Render the assembly (optionally exploded) to PNG. Needs matplotlib."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    light = normalize((0.4, -0.6, 0.7))
    all_triangles: list[Triangle] = []
    face_colors: list[tuple[float, ...]] = []

    for component in components.values():
        offset = (explode * component.explode_dir[0],
                  explode * component.explode_dir[1],
                  explode * component.explode_dir[2])
        triangles = transform(component.triangles, None, offset)
        all_triangles += triangles
        for v0, v1, v2 in triangles:
            normal = normalize(cross(sub(v1, v0), sub(v2, v0)))
            intensity = abs(sum(n * lt for n, lt in zip(normal, light, strict=True)))
            scale = 0.40 + 0.60 * intensity
            face_colors.append(tuple(ch * scale for ch in component.color))

    xs = [v[0] for tri in all_triangles for v in tri]
    ys = [v[1] for tri in all_triangles for v in tri]
    zs = [v[2] for tri in all_triangles for v in tri]
    ranges = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))

    if views is None:
        views = [
            ("Isometric (front-right)", 22.0, -55.0),
            ("Isometric (rear-left)", 18.0, 140.0),
            ("Side elevation", 0.0, -90.0),
            ("Plan view", 90.0, -90.0),
        ]

    ncols = 2 if len(views) > 1 else 1
    nrows = (len(views) + ncols - 1) // ncols
    fig = plt.figure(figsize=(7.5 * ncols, 6 * nrows))
    for i, (title, elev, azim) in enumerate(views, start=1):
        ax = fig.add_subplot(nrows, ncols, i, projection="3d")
        ax.add_collection3d(
            Poly3DCollection(all_triangles, facecolors=face_colors, linewidths=0)
        )
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(ys), max(ys))
        ax.set_zlim(min(zs), max(zs))
        ax.set_box_aspect(ranges, zoom=1.25)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title)
        ax.set_axis_off()

    label = "exploded view" if explode else "assembly"
    fig.suptitle(f"MudMixer MMXR-3221 — full machine {label} (generated CAD)",
                 fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)


def render_drawing_sheet(components: dict[str, Component], path: str) -> None:
    """
    Generate a dimensioned 2D engineering drawing sheet (side and front
    elevations with dimension callouts and a title block). Requires
    matplotlib.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    def silhouette(ax, plane: str):
        polys, colors = [], []
        for component in components.values():
            for v0, v1, v2 in component.triangles:
                if plane == "side":
                    polys.append([(v0[0], v0[2]), (v1[0], v1[2]), (v2[0], v2[2])])
                else:
                    polys.append([(v0[1], v0[2]), (v1[1], v1[2]), (v2[1], v2[2])])
                colors.append(tuple(ch * 0.85 for ch in component.color))
        ax.add_collection(
            PolyCollection(polys, facecolors=colors, linewidths=0, alpha=0.9)
        )
        ax.axhline(0, color="black", lw=1.2)  # ground line
        ax.set_aspect("equal")
        ax.set_axisbelow(True)
        ax.grid(True, lw=0.3, alpha=0.4)

    def dim_h(ax, x0, x1, y, label, offset=2.0):
        for x in (x0, x1):
            ax.plot([x, x], [y - 0.8, y + 0.8], color="#1a4d8f", lw=0.8)
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<->", color="#1a4d8f", lw=1.0))
        ax.text((x0 + x1) / 2, y + offset, label, ha="center", fontsize=9,
                color="#1a4d8f")

    def dim_v(ax, x, y0, y1, label, offset=1.5):
        for y in (y0, y1):
            ax.plot([x - 0.8, x + 0.8], [y, y], color="#1a4d8f", lw=0.8)
        ax.annotate("", xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle="<->", color="#1a4d8f", lw=1.0))
        ax.text(x + offset, (y0 + y1) / 2, label, va="center", fontsize=9,
                color="#1a4d8f", rotation=90)

    everything = [t for c in components.values() for t in c.triangles]
    (x0, y0, _), (x1, y1, z1) = bounding_box(everything)

    fig, (ax_side, ax_front) = plt.subplots(
        1, 2, figsize=(16, 8), gridspec_kw={"width_ratios": [2.2, 1]}
    )

    silhouette(ax_side, "side")
    dim_h(ax_side, x0, x1, -6, f'{x1 - x0:.1f}" OVERALL')
    dim_v(ax_side, x1 + 4, 0, z1, f'{z1:.1f}" OVERALL')
    dim_v(ax_side, x1 + 9, 0, SPEC["discharge_height_in"],
          f'{SPEC["discharge_height_in"]:.0f}" DISCHARGE')
    dim_v(ax_side, x0 - 4, 0, 10.0, '10.0" RAIL')
    dim_h(ax_side, 15.0, 25.0, -2.5, 'Ø10" WHEEL')
    ax_side.set_xlim(x0 - 10, x1 + 14)
    ax_side.set_ylim(-9, z1 + 4)
    ax_side.set_title("SIDE ELEVATION", fontsize=11)

    silhouette(ax_front, "front")
    dim_h(ax_front, y0, y1, -6, f'{y1 - y0:.1f}" OVERALL')
    dim_h(ax_front, -10.0, 10.0, z1 + 2.5, '20.0" HOPPER RIM')
    dim_v(ax_front, y1 + 3.5, 0, z1, f'{z1:.1f}"')
    ax_front.annotate(
        f'Ø{SPEC["housing_id_in"]:.1f}" BORE\n(see DESIGN_INSIGHTS D1:\n'
        'measured value may be ~6.5")',
        xy=(0, 17), xytext=(y1 + 2, 22), fontsize=8, color="#1a4d8f",
        arrowprops=dict(arrowstyle="->", color="#1a4d8f", lw=0.8),
    )
    ax_front.set_xlim(y0 - 6, y1 + 12)
    ax_front.set_ylim(-9, z1 + 6)
    ax_front.set_title("FRONT ELEVATION", fontsize=11)

    for ax in (ax_side, ax_front):
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("MUDMIXER MMXR-3221 — GENERAL ARRANGEMENT", fontsize=14,
                 fontweight="bold")
    fig.text(
        0.99, 0.01,
        "DWG MM-001  |  UNITS: INCHES  |  GENERATED BY src/mixer_cad.py  |  "
        "REVERSE-ENGINEERED — VERIFY CRITICAL DIMS BEFORE FABRICATION",
        ha="right", fontsize=8, color="#555",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)


def export_stls(components: dict[str, Component], directory: str) -> list[str]:
    """Write one STL per component plus the combined assembly."""
    os.makedirs(directory, exist_ok=True)
    paths = []
    combined: list[Triangle] = []
    for component in components.values():
        path = os.path.join(directory, f"mudmixer_{component.name}.stl")
        write_binary_stl(component.triangles, path, f"MudMixer {component.name}")
        paths.append(path)
        combined += component.triangles
    assembly_path = os.path.join(directory, "mudmixer_assembly.stl")
    write_binary_stl(combined, assembly_path, "MudMixer full assembly")
    paths.append(assembly_path)
    return paths


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="MudMixer full-machine CAD model: build, validate, export"
    )
    parser.add_argument("--housing-id", type=float,
                        default=SPEC["housing_id_in"],
                        help="Chute housing bore, inches (6.0 baseline; "
                             "6.5 = self-consistent design point, see "
                             "DESIGN_INSIGHTS D11)")
    parser.add_argument("--report", action="store_true",
                        help="Print the validation report")
    parser.add_argument("--stl-dir", metavar="DIR",
                        help="Export per-component and assembly STLs to DIR")
    parser.add_argument("--render", metavar="PATH",
                        help="Render assembly views to PNG")
    parser.add_argument("--exploded", metavar="PATH",
                        help="Render exploded view to PNG")
    parser.add_argument("--drawing", metavar="PATH",
                        help="Render dimensioned drawing sheet to PNG")
    args = parser.parse_args(argv)

    components = build_mixer(args.housing_id)
    report = validate_assembly(components, args.housing_id)

    if args.report or not (args.stl_dir or args.render or args.exploded):
        print_report(report)

    if args.stl_dir:
        for path in export_stls(components, args.stl_dir):
            print(f"STL exported: {path}")
    if args.render:
        render_assembly(components, args.render)
        print(f"Render saved: {args.render}")
    if args.exploded:
        render_assembly(components, args.exploded, explode=9.0,
                        views=[("Exploded isometric", 20.0, -50.0)])
        print(f"Exploded render saved: {args.exploded}")
    if args.drawing:
        render_drawing_sheet(components, args.drawing)
        print(f"Drawing sheet saved: {args.drawing}")

    if not report["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
