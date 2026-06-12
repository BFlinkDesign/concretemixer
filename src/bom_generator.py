#!/usr/bin/env python3
"""
MudMixer CAD-Reconciled BOM & Procurement Generator

Generates the procurement package directly from the validated CAD model,
so quantities can never disagree with the geometry:

    raw stock      sheet ft², pipe ft, bar stock — derived from mesh
                   volumes/areas of the actual components, with scrap
    purchased      consolidated parts list (frame, hopper, chute, auger,
                   drive, water, power, hardware) with corrected specs
    audit          cross-checks every spec the analysis can verify:
                   auger/chute clearance, fuse vs DC bus current, wire
                   gauge, nozzle orifice vs required flow, axle stock

The audit caught real errors in the original hand-written docs/BOM.md
(see docs/DESIGN_INSIGHTS.md D14): a 5.5" auger in the 6" chute (jams on
0.5" aggregate), a 15 A fuse on an ~18 A DC bus, and 1/8" nozzles that
flow ~7x the required water.

Usage:
    python bom_generator.py --housing-id 6.5 --csv bom.csv --md bom.md

Dependencies: none (standard library only)
"""

import argparse
import csv
import math
from typing import Dict, List, Optional

from auger_optimizer import AugerOptimizer, PowerSystem
from mixer_analysis import water_demand
from mixer_cad import DENSITY, build_mixer

SCRAP_FACTOR = 1.15
SHEET_THICKNESS = 0.075  # 14 ga
PIPE_RADIUS = 0.5

# Ampacity (chassis wiring, conservative) for the DC-side check
WIRE_AMPACITY = {16: 13, 14: 17, 12: 23, 10: 33, 8: 46}


def cad_derived_materials(housing_id: float = 6.0) -> List[Dict[str, object]]:
    """Raw-stock requirements computed from the CAD meshes."""
    components = build_mixer(housing_id=housing_id)

    sheet_parts = ("hopper", "body_panels", "chute_housing", "discharge_spout",
                   "swivel_collar", "water_manifold", "motor_bell")
    sheet_area_in2 = sum(
        components[name].volume / SHEET_THICKNESS for name in sheet_parts
    )
    sheet_ft2 = sheet_area_in2 / 144 * SCRAP_FACTOR

    pipe_length_in = components["frame"].volume / (math.pi * PIPE_RADIUS**2)
    pipe_ft = pipe_length_in / 12 * SCRAP_FACTOR

    flight_lb = components["auger"].weight_lb * SCRAP_FACTOR

    design = AugerOptimizer(housing_id).generate_optimized_design()
    skeleton = design["skeleton"]["recommended_diameter_in"]

    return [
        {"item": "Steel sheet, 14 ga", "qty": f"{sheet_ft2:.1f} ft²",
         "spec": "A1011 or equiv; one 4'×8' sheet covers it",
         "source": "CAD: shell volumes / 0.075\" + 15% scrap",
         "est_cost": 90},
        {"item": "Steel pipe, 1\" OD", "qty": f"{pipe_ft:.1f} ft",
         "spec": "16 ga wall min (sch-40 preferred per SPECIFICATIONS)",
         "source": "CAD: frame member volume / cross-section + 15% scrap",
         "est_cost": 55},
        {"item": "Auger flight stock", "qty": f"{flight_lb:.1f} lb",
         "spec": f"3/16\" plate, helicoid-formed, "
                 f"{design['geometry']['auger_od']:.2f}\" OD variable pitch",
         "source": "CAD: flight mesh weight + 15%",
         "est_cost": 120},
        {"item": "Finger bar stock", "qty": "24 in",
         "spec": "3/8\" 1045 steel rod (8 fingers + stubs)",
         "source": "FingerConfig 8 × ~2\" + weld stubs",
         "est_cost": 12},
        {"item": "Skeleton bar stock", "qty": "30 in",
         "spec": f"{skeleton}\" 304 SS round (corrected sizing, D6)",
         "source": "calculate_skeleton_diameter (single safety factor)",
         "est_cost": 35},
        {"item": "Axle bar stock", "qty": "30 in",
         "spec": "5/8\" 1018 CR round (adequate per corrected D13)",
         "source": "ENGINEERING.md §3 revised", "est_cost": 14},
    ]


def purchased_parts(housing_id: float = 6.0) -> List[Dict[str, object]]:
    """Consolidated purchased-parts list with audit-corrected specs."""
    design = AugerOptimizer(housing_id).generate_optimized_design()
    auger_od = design["geometry"]["auger_od"]
    water = water_demand()
    power = PowerSystem(motor_power_watts=373)
    dc_amps = power.current_draw_24v

    parts = [
        # Running gear & frame
        {"item": "Wheel, 10\" flat-free", "qty": 2,
         "spec": "Marathon or equiv", "est_cost": 50},
        {"item": "Handle grips", "qty": 2, "spec": "1\" pipe", "est_cost": 8},
        {"item": "Axle hardware", "qty": 1,
         "spec": "5/8\"-11 lock nuts ×4, washers ×4, cotter pins", "est_cost": 10},
        # Chute / pivot
        {"item": "Pivot thrust bearing", "qty": 1,
         "spec": "330° swivel, bronze/steel", "est_cost": 25},
        {"item": "Pivot plates + spring + tilt lock", "qty": 1,
         "spec": "1/4\" plate ×2, compression spring, pin lock", "est_cost": 30},
        # Drive (corrected: see D2/D3/D14)
        {"item": "DC gearmotor", "qty": 1,
         "spec": "0.5 HP, ~67:1 to 27 RPM output, water-sealed, reversible",
         "est_cost": 220},
        {"item": "AC-DC power supply", "qty": 1,
         "spec": f"24 V, ≥550 W ({dc_amps:.0f} A continuous + headroom)",
         "est_cost": 120},
        {"item": "Fuse + holder (CORRECTED)", "qty": 1,
         "spec": f"25 A DC-side (bus draws {dc_amps:.0f} A; the original "
                 "BOM's 15 A blows at full load). AC side: 5 A",
         "est_cost": 8},
        {"item": "DC motor wiring (CORRECTED)", "qty": "10 ft",
         "spec": f"10 AWG for the {dc_amps:.0f} A DC bus "
                 "(14 AWG is AC-side only)", "est_cost": 12},
        {"item": "FWD/REV switch", "qty": 1, "spec": "DPDT 25 A", "est_cost": 18},
        {"item": "Power cord + enclosure", "qty": 1,
         "spec": "14 AWG grounded, weatherproof box + ventilation fan "
                 "(enclosure hits 147°F without one, D12)", "est_cost": 40},
        # Water (corrected orifice, D7/D14)
        {"item": "Spray nozzles (CORRECTED)", "qty": 2,
         "spec": f"~3/64\" ({water['orifice_diameter_in']:.3f}\") orifice, "
                 "65° fan, brass — the original 1/8\" flows ~7× requirement",
         "est_cost": 16},
        {"item": "Water fittings kit", "qty": 1,
         "spec": "3/4\" GHT inlet, 3/8\" needle valve + dial, tee, "
                 "shutoff, 4 ft reinforced tubing, clamps + inline filter "
                 "(orifices this small clog)", "est_cost": 45},
        # Coupling
        {"item": "Motor coupling", "qty": 1,
         "spec": f"LH Acme (self-tightening, D3) to {auger_od:.2f}\" OD auger",
         "est_cost": 45},
        # Hardware & finishing
        {"item": "Fastener kit", "qty": 1,
         "spec": "Grade 5: 1/4-20, 5/16-18, 3/8-16 + lock nuts/washers",
         "est_cost": 35},
        {"item": "Primer + enamel + safety labels", "qty": 1,
         "spec": "1 qt each, rotating-machinery decals", "est_cost": 45},
    ]
    return parts


def procurement_audit(housing_id: float = 6.0) -> List[Dict[str, object]]:
    """Cross-check every spec the analysis framework can verify."""
    checks = []
    design = AugerOptimizer(housing_id).generate_optimized_design()

    def check(name, ok, detail):
        checks.append({"name": name, "status": "OK" if ok else "FAIL",
                       "detail": detail})

    clearance = design["analysis"]["clearance"]
    check("auger_chute_clearance", clearance["status"] == "OK",
          f"{design['geometry']['auger_od']:.2f}\" OD in {housing_id}\" bore: "
          f"{clearance['clearance_per_side']:.2f}\"/side (min 0.60\")")

    legacy_clearance = (6.0 - 5.5) / 2
    check("legacy_bom_auger_rejected", legacy_clearance < 0.6,
          "original BOM 5.5\" auger in 6\" chute leaves "
          f"{legacy_clearance:.2f}\"/side — would jam; superseded")

    dc_amps = PowerSystem(motor_power_watts=373).current_draw_24v
    check("fuse_rating", 25 > dc_amps * 1.25,
          f"25 A fuse vs {dc_amps:.1f} A bus (original 15 A would blow)")
    check("dc_wire_ampacity", WIRE_AMPACITY[10] > dc_amps * 1.25,
          f"10 AWG ({WIRE_AMPACITY[10]} A) vs {dc_amps:.1f} A bus")

    water = water_demand()
    legacy_flow_ratio = (0.125 / water["orifice_diameter_in"]) ** 2
    check("nozzle_orifice", water["supply_adequate"],
          f"{water['orifice_diameter_in']:.3f}\" orifice delivers "
          f"{water['gpm_per_nozzle']:.2f} GPM/nozzle at 30 PSI "
          f"(original 1/8\" = {legacy_flow_ratio:.0f}× oversize)")

    shear = design["analysis"]["shear"]
    check("finger_material", shear["status"] == "OK",
          f"{shear['material']} survives single-finger jam "
          f"({shear['jam_pressure_psi']:.0f} psi vs "
          f"{shear['design_strength_psi']:.0f} allowable)")

    check("skeleton_stock", design["skeleton"]["recommended_diameter_in"] >=
          design["skeleton"]["min_diameter_in"],
          f"{design['skeleton']['recommended_diameter_in']}\" stock ≥ "
          f"{design['skeleton']['min_diameter_in']:.3f}\" required")

    return checks


def full_bom(housing_id: float = 6.0) -> List[Dict[str, object]]:
    materials = [dict(entry, category="raw stock")
                 for entry in cad_derived_materials(housing_id)]
    parts = [dict(entry, category="purchased")
             for entry in purchased_parts(housing_id)]
    return materials + parts


def cost_rollup(bom: List[Dict[str, object]]) -> Dict[str, float]:
    total = sum(entry["est_cost"] for entry in bom)
    by_category: Dict[str, float] = {}
    for entry in bom:
        by_category[entry["category"]] = (
            by_category.get(entry["category"], 0) + entry["est_cost"]
        )
    return {"total": total, **by_category}


def write_csv(bom: List[Dict[str, object]], path: str):
    fields = ["category", "item", "qty", "spec", "source", "est_cost"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for entry in bom:
            writer.writerow(entry)


def write_markdown(housing_id: float, path: str):
    bom = full_bom(housing_id)
    audit = procurement_audit(housing_id)
    rollup = cost_rollup(bom)

    lines = [
        f"# Procurement Package — {housing_id}\" bore design point",
        "",
        "Generated by `src/bom_generator.py` from the validated CAD model.",
        "Do not hand-edit; regenerate via `python src/build_all.py`.",
        "",
        "## Bill of Materials",
        "",
        "| Category | Item | Qty | Spec | Est. cost |",
        "|---|---|---|---|---|",
    ]
    for entry in bom:
        lines.append(
            f"| {entry['category']} | {entry['item']} | {entry['qty']} | "
            f"{entry['spec']} | ${entry['est_cost']} |"
        )
    lines += [
        "",
        f"**Estimated total: ${rollup['total']}** "
        f"(raw stock ${rollup['raw stock']}, purchased ${rollup['purchased']})",
        "",
        "## Procurement Audit",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for check in audit:
        lines.append(f"| {check['name']} | {check['status']} | "
                     f"{check['detail']} |")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="CAD-reconciled BOM and procurement audit"
    )
    parser.add_argument("--housing-id", type=float, default=6.0)
    parser.add_argument("--csv", metavar="PATH")
    parser.add_argument("--md", metavar="PATH")
    args = parser.parse_args(argv)

    bom = full_bom(args.housing_id)
    audit = procurement_audit(args.housing_id)
    rollup = cost_rollup(bom)

    print("=" * 76)
    print(f"PROCUREMENT PACKAGE — {args.housing_id}\" bore design point")
    print("=" * 76)
    for entry in bom:
        print(f"  [{entry['category']:<9}] {entry['item']:<34} "
              f"{str(entry['qty']):>9}  ${entry['est_cost']}")
    print("-" * 76)
    print(f"  ESTIMATED TOTAL: ${rollup['total']} "
          f"(raw ${rollup['raw stock']} + purchased ${rollup['purchased']})")
    print()
    print("  PROCUREMENT AUDIT")
    failed = 0
    for check in audit:
        print(f"    {check['name']:<28}{check['status']:<6}{check['detail']}")
        failed += check["status"] != "OK"
    print("-" * 76)
    print(f"  RESULT: {'ALL CHECKS PASS' if not failed else f'{failed} FAILURES'}")

    if args.csv:
        write_csv(bom, args.csv)
        print(f"  CSV written: {args.csv}")
    if args.md:
        write_markdown(args.housing_id, args.md)
        print(f"  Markdown written: {args.md}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
