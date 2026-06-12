#!/usr/bin/env python3
"""
MudMixer Cross-Specification Engineering Analysis

Independent physics checks that test whether the published MudMixer
specifications are mutually consistent, and quantify the operating
parameters the manufacturer does not publish. Each function returns a
dict so results can be tested and reported.

Discoveries produced by this module are documented in
docs/DESIGN_INSIGHTS.md.

Usage:
    python mixer_analysis.py

Dependencies: none (standard library only)
"""

import math
from typing import Dict, Optional

from auger_optimizer import AugerGeometry, AugerOptimizer

# Bulk density of dry bagged concrete mix (consolidated), lb/ft³
DRY_MIX_DENSITY_LB_FT3 = 105.0
# Yield of an 80 lb bag of concrete mix, ft³ (industry standard)
BAG_80LB_YIELD_FT3 = 0.60
# Mixing water per 80 lb bag, quarts (manufacturer range 2.8-4)
WATER_QT_PER_BAG = 3.5


def throughput_analysis(
    geometry: Optional[AugerGeometry] = None,
    rpm: float = 27.0,
    fill_efficiency: float = 0.35,
    claimed_bags_hr: float = 45.0,
) -> Dict[str, float]:
    """
    Validate the claimed 45 bags/hr (~1 yd³/hr) against screw-conveyor
    physics (CEMA-style volumetric flow, docs/AUGER_DESIGN.md):

        Q = (π/4) × D² × P × N × η

    using the chute-section pitch, where conveyance is flow-limiting.
    Also solves for the fill efficiency the claim implies.
    """
    if geometry is None:
        design = AugerOptimizer(6.0).generate_optimized_design()
        geometry = design["objects"]["geometry"]

    diameter = geometry.outer_diameter
    pitch = geometry.pitch_chute

    flow_in3_min = (math.pi / 4) * diameter**2 * pitch * rpm * fill_efficiency
    flow_ft3_hr = flow_in3_min * 60 / 1728
    bags_hr = flow_ft3_hr / BAG_80LB_YIELD_FT3
    yd3_hr = flow_ft3_hr / 27

    claimed_flow_ft3_hr = claimed_bags_hr * BAG_80LB_YIELD_FT3
    implied_eta = fill_efficiency * claimed_flow_ft3_hr / flow_ft3_hr

    return {
        "auger_diameter_in": diameter,
        "pitch_chute_in": pitch,
        "rpm": rpm,
        "fill_efficiency": fill_efficiency,
        "flow_ft3_hr": flow_ft3_hr,
        "throughput_bags_hr": bags_hr,
        "throughput_yd3_hr": yd3_hr,
        "claimed_bags_hr": claimed_bags_hr,
        "implied_fill_efficiency": implied_eta,
        # CEMA fill efficiency for inclined screws is typically 0.30-0.45
        "claim_consistent": 0.20 <= implied_eta <= 0.45,
    }


def implied_auger_size(
    claimed_bags_hr: float = 45.0,
    rpm: float = 27.0,
    fill_efficiency: float = 0.35,
    pd_ratio_chute: float = 0.85,
    clearance_per_side: float = 0.75,
) -> Dict[str, float]:
    """
    Invert the throughput equation to estimate the REAL auger diameter
    from the manufacturer's performance claim.

    With P = (P/D)·D, the flow equation becomes Q = (π/4)·D³·(P/D)·N·η,
    so the claimed throughput pins down D — and therefore the housing
    bore, the repo's #1 unknown (docs/DATA_REQUIREMENTS.md).
    """
    flow_in3_min = claimed_bags_hr * BAG_80LB_YIELD_FT3 * 1728 / 60
    d_cubed = flow_in3_min / (
        (math.pi / 4) * pd_ratio_chute * rpm * fill_efficiency
    )
    diameter = d_cubed ** (1 / 3)
    housing_id = diameter + 2 * clearance_per_side

    return {
        "claimed_bags_hr": claimed_bags_hr,
        "implied_auger_od_in": diameter,
        "implied_housing_id_in": housing_id,
        "assumed_housing_id_in": 6.0,
        "assumption_consistent": abs(housing_id - 6.0) < 0.25,
    }


def converged_design(
    claimed_bags_hr: float = 45.0,
    tolerance: float = 0.01,
    max_iterations: int = 10,
) -> Dict[str, object]:
    """
    Close the D1 discovery loop: iterate the housing bore until the
    generative design's own geometry reproduces the manufacturer's
    throughput claim at CEMA mid-range fill efficiency.

    Fixed-point iteration: bore → optimized auger OD/pitch → predicted
    throughput → implied bore correction → repeat until self-consistent.
    """
    housing_id = 6.0
    history = []
    for _ in range(max_iterations):
        design = AugerOptimizer(housing_id).generate_optimized_design()
        geometry = design["objects"]["geometry"]
        flow = throughput_analysis(geometry=geometry)
        history.append((housing_id, flow["throughput_bags_hr"]))

        implied = implied_auger_size(
            claimed_bags_hr=claimed_bags_hr,
            pd_ratio_chute=geometry.pd_ratio_chute,
        )
        next_id = implied["implied_housing_id_in"]
        if abs(next_id - housing_id) < tolerance:
            housing_id = next_id
            break
        housing_id = next_id

    design = AugerOptimizer(housing_id).generate_optimized_design()
    geometry = design["objects"]["geometry"]
    flow = throughput_analysis(geometry=geometry)

    return {
        "converged_housing_id_in": housing_id,
        "auger_od_in": geometry.outer_diameter,
        "pitch_hopper_in": geometry.pitch_hopper,
        "pitch_chute_in": geometry.pitch_chute,
        "predicted_bags_hr": flow["throughput_bags_hr"],
        "claimed_bags_hr": claimed_bags_hr,
        "iterations": len(history),
        "history": history,
        "self_consistent": abs(
            flow["throughput_bags_hr"] - claimed_bags_hr
        ) / claimed_bags_hr < 0.05,
        "patent_validation_issues": design["validation"],
    }


def water_demand(
    bags_hr: float = 45.0,
    water_qt_per_bag: float = WATER_QT_PER_BAG,
    supply_psi: float = 30.0,
    nozzle_count: int = 2,
    discharge_coefficient: float = 0.9,
) -> Dict[str, float]:
    """
    Water mass balance at rated throughput, and the spray-nozzle orifice
    size that delivers it at the specified 30 PSI minimum supply.

    Orifice flow (fire-stream form of Torricelli):
        q_gpm = 29.84 × Cd × d² × √P(psi)
    """
    gpm_required = bags_hr * water_qt_per_bag / 4 / 60
    gpm_per_nozzle = gpm_required / nozzle_count

    orifice_d = math.sqrt(
        gpm_per_nozzle / (29.84 * discharge_coefficient * math.sqrt(supply_psi))
    )

    water_lb_hr = bags_hr * water_qt_per_bag * 2.085  # 1 qt water ≈ 2.085 lb
    mix_lb_hr = bags_hr * 80.0
    water_fraction = water_lb_hr / (water_lb_hr + mix_lb_hr)

    return {
        "bags_hr": bags_hr,
        "gpm_required": gpm_required,
        "gpm_per_nozzle": gpm_per_nozzle,
        "orifice_diameter_in": orifice_d,
        "water_lb_hr": water_lb_hr,
        "water_mass_fraction": water_fraction,
        # A garden hose at 30 PSI delivers ~4-6 GPM; demand must fit easily
        "supply_adequate": gpm_required < 4.0,
    }


def drivetrain_analysis(
    motor_base_rpm: float = 1800.0,
    output_rpm: float = 27.0,
    motor_power_hp: float = 0.5,
    gearbox_efficiency: float = 0.85,
) -> Dict[str, float]:
    """
    The spec sheet says "direct drive", yet a 0.5 HP DC motor natively
    runs 1750-3600 RPM. Quantify the reduction stage that must exist
    inside the "direct drive" gearmotor, and the resulting output torque.
    """
    ratio = motor_base_rpm / output_rpm
    motor_torque_ft_lb = motor_power_hp * 5252 / motor_base_rpm
    output_torque_ft_lb = motor_torque_ft_lb * ratio * gearbox_efficiency

    return {
        "motor_base_rpm": motor_base_rpm,
        "output_rpm": output_rpm,
        "required_ratio": ratio,
        "motor_torque_ft_lb": motor_torque_ft_lb,
        "output_torque_ft_lb": output_torque_ft_lb,
        # Left-hand Acme coupling (patent 10,259,140): forward rotation
        # tightens the joint; a RH thread would unscrew under load.
        "coupling": "LH Acme — self-tightening under forward drive",
    }


def power_audit(
    rated_hp: float = 0.5,
    input_volts: float = 120.0,
    rated_amps: float = 2.6,
    drivetrain_efficiency: float = 0.75,
) -> Dict[str, float]:
    """
    Cross-check the published electrical ratings against each other.

    The spec sheet claims 0.5 HP (373 W mechanical) AND 2.6 A at 120 V
    (312 W electrical input). Output cannot exceed input: these two
    numbers cannot both describe continuous full-load operation.
    """
    input_watts = input_volts * rated_amps
    rated_output_watts = rated_hp * 746
    implied_efficiency = rated_output_watts / input_watts

    honest_amps = rated_output_watts / (drivetrain_efficiency * input_volts)
    max_hp_at_rated_amps = input_watts * drivetrain_efficiency / 746

    return {
        "rated_output_watts": rated_output_watts,
        "input_watts_at_rated_amps": input_watts,
        "implied_efficiency": implied_efficiency,
        "specs_consistent": implied_efficiency <= 1.0,
        "amps_needed_at_full_load": honest_amps,
        "max_continuous_hp_at_rated_amps": max_hp_at_rated_amps,
    }


def hopper_capacity_check(
    hopper_volume_in3: float,
    rated_capacity_lb: float = 120.0,
    bulk_density_lb_ft3: float = DRY_MIX_DENSITY_LB_FT3,
) -> Dict[str, float]:
    """
    Does the modeled hopper geometry actually hold the rated 120 lb
    (2 × 60 lb bags) of dry mix?
    """
    volume_ft3 = hopper_volume_in3 / 1728
    holds_lb = volume_ft3 * bulk_density_lb_ft3
    required_ft3 = rated_capacity_lb / bulk_density_lb_ft3

    return {
        "hopper_volume_ft3": volume_ft3,
        "holds_lb_struck_level": holds_lb,
        "required_ft3_for_rating": required_ft3,
        "fill_fraction_at_rating": required_ft3 / volume_ft3,
        "capacity_adequate": holds_lb >= rated_capacity_lb,
    }


def hopper_cavity_volume_in3(
    top_lx: float = 22.0, top_ly: float = 20.0,
    bottom_lx: float = 10.0, bottom_ly: float = 8.0,
    height: float = 11.0,
) -> float:
    """Interior volume of the rectangular hopper frustum (prismatoid rule)."""
    a_top = top_lx * top_ly
    a_bot = bottom_lx * bottom_ly
    a_mid = ((top_lx + bottom_lx) / 2) * ((top_ly + bottom_ly) / 2)
    return height / 6 * (a_top + 4 * a_mid + a_bot)


def main():
    print("=" * 72)
    print("MUDMIXER CROSS-SPECIFICATION ANALYSIS")
    print("=" * 72)

    throughput = throughput_analysis()
    print("\n[1] THROUGHPUT vs CLAIM")
    print(f"    Q = (π/4)D²PNη with D={throughput['auger_diameter_in']:.2f}\", "
          f"P={throughput['pitch_chute_in']:.2f}\", N={throughput['rpm']:.0f} RPM")
    print(f"    At η=0.35: {throughput['throughput_bags_hr']:.0f} bags/hr "
          f"({throughput['throughput_yd3_hr']:.2f} yd³/hr)")
    print(f"    Claimed 45 bags/hr implies η = "
          f"{throughput['implied_fill_efficiency']:.2f} "
          f"→ {'CONSISTENT with CEMA inclined-screw range' if throughput['claim_consistent'] else 'INCONSISTENT'}")

    size = implied_auger_size()
    print("\n[1b] IMPLIED TRUE AUGER SIZE (inverting the claim at η=0.35)")
    print(f"    Claim is satisfied by auger OD ≈ {size['implied_auger_od_in']:.1f}\" "
          f"→ housing ID ≈ {size['implied_housing_id_in']:.1f}\"")
    print(f"    Repo assumption is {size['assumed_housing_id_in']:.1f}\" (UNMEASURED) — "
          "the claim suggests the real bore is ~6.5\"; verify with a bore gauge")

    converged = converged_design()
    print("\n[1c] SELF-CONSISTENT DESIGN POINT (fixed-point iteration)")
    print(f"    Converged in {converged['iterations']} iterations: "
          f"bore {converged['converged_housing_id_in']:.2f}\", "
          f"auger OD {converged['auger_od_in']:.2f}\", "
          f"pitches {converged['pitch_hopper_in']:.2f}\"/"
          f"{converged['pitch_chute_in']:.2f}\"")
    print(f"    Predicted throughput {converged['predicted_bags_hr']:.1f} bags/hr "
          f"vs claimed {converged['claimed_bags_hr']:.0f} → "
          f"{'SELF-CONSISTENT' if converged['self_consistent'] else 'NOT CONVERGED'}; "
          f"patent P/D checks: "
          f"{'PASS' if not converged['patent_validation_issues'] else converged['patent_validation_issues']}")

    water = water_demand()
    print("\n[2] WATER MASS BALANCE")
    print(f"    {water['gpm_required']:.2f} GPM total "
          f"({water['gpm_per_nozzle']:.2f} GPM/nozzle), "
          f"water fraction {water['water_mass_fraction']*100:.1f}% of wet mix")
    print(f"    Orifice for 30 PSI supply: ~{water['orifice_diameter_in']:.3f}\" "
          f"→ supply {'ADEQUATE' if water['supply_adequate'] else 'MARGINAL'}")

    drive = drivetrain_analysis()
    print("\n[3] DRIVETRAIN (\"direct drive\" claim)")
    print(f"    {drive['motor_base_rpm']:.0f} RPM motor → {drive['output_rpm']:.0f} RPM "
          f"auger requires {drive['required_ratio']:.0f}:1 reduction")
    print(f"    Output torque ≈ {drive['output_torque_ft_lb']:.0f} ft-lb; "
          f"{drive['coupling']}")

    power = power_audit()
    print("\n[4] ELECTRICAL SPEC AUDIT")
    print(f"    Claimed: 0.5 HP out ({power['rated_output_watts']:.0f} W) on "
          f"2.6 A × 120 V in ({power['input_watts_at_rated_amps']:.0f} W)")
    print(f"    Implied efficiency {power['implied_efficiency']*100:.0f}% → "
          f"{'physically possible' if power['specs_consistent'] else 'IMPOSSIBLE (output exceeds input)'}")
    print(f"    Full 0.5 HP at 75% drive efficiency needs "
          f"{power['amps_needed_at_full_load']:.1f} A; at 2.6 A the motor "
          f"delivers at most {power['max_continuous_hp_at_rated_amps']:.2f} HP")

    capacity = hopper_capacity_check(hopper_cavity_volume_in3())
    print("\n[5] HOPPER CAPACITY")
    print(f"    Modeled cavity {capacity['hopper_volume_ft3']:.2f} ft³ holds "
          f"{capacity['holds_lb_struck_level']:.0f} lb struck level "
          f"(rating 120 lb at "
          f"{capacity['fill_fraction_at_rating']*100:.0f}% fill) → "
          f"{'ADEQUATE' if capacity['capacity_adequate'] else 'UNDERSIZED'}")


if __name__ == "__main__":
    main()
