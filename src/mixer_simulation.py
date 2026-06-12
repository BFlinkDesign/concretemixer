#!/usr/bin/env python3
"""
MudMixer 12-Hour Jobsite Operational Simulation (digital twin)

Time-domain simulation of a full continuous-duty workday at the
self-consistent design point (6.5" bore — see docs/DESIGN_INSIGHTS.md D1):

    feed loop      operator dumps an 80 lb bag whenever hopper ≤ 40 lb
                   (minimum 45 s operator cycle); mixer consumes at the
                   screw-conveyor rate; 30 min lunch break at hour 6
    electrical     honest full-load current from the D2 power audit
                   (~4.1 A at 120 V, not the published 2.6 A)
    finger thermal first-order lag toward a load-dependent steady state;
                   when material is flowing, the wet mix itself is the
                   dominant heat sink (h ≈ 15 BTU/hr·ft²·°F granular
                   contact vs 2 for natural convection when idle);
                   5% of motor power is dissipated at the fingers
    electronics    transformer/controller enclosure temperature with and
                   without a ventilation fan

Assumptions are deliberately conservative and stated inline; every output
is checked in test_mixer_simulation.py.

Usage:
    python mixer_simulation.py --plot ../drawings/SIMULATION_12HR.png

Dependencies: none for simulation (standard library); matplotlib for --plot
"""

import argparse
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from mixer_analysis import throughput_analysis, power_audit, WATER_QT_PER_BAG
from auger_optimizer import AugerOptimizer

# Thermal model constants
FINGER_FRICTION_SHARE = 0.05      # fraction of motor power heating fingers
H_MIX_CONTACT = 15.0              # BTU/(hr·ft²·°F), flowing wet-mix contact
H_NATURAL = 2.0                   # BTU/(hr·ft²·°F), idle natural convection
FINGER_AREA_FT2 = 10.0 / 144      # 10 in² exposed per finger set
FINGER_MASS_LB = 0.5

UHMW_DEFLECTION_F = 116.0         # heat-deflection temp under load
UHMW_MAX_CONTINUOUS_F = 180.0
STEEL_MAX_CONTINUOUS_F = 800.0

ENCLOSURE_LOSS_W = 50.0           # transformer + controller dissipation
ENCLOSURE_AREA_FT2 = 236.0 / 144  # 8×6×5 box surface
ENCLOSURE_H_FAN = 6.0             # forced ventilation
ENCLOSURE_THERMAL_MASS = 8.0 * 0.2  # lb × BTU/(lb·°F)


@dataclass
class SimulationConfig:
    duration_hr: float = 12.0
    dt_s: float = 1.0
    housing_id_in: float = 6.5        # D1 self-consistent design point
    rpm: float = 27.0
    fill_efficiency: float = 0.35
    bag_lb: float = 80.0
    bag_yield_ft3: float = 0.60
    hopper_capacity_lb: float = 120.0
    reload_threshold_lb: float = 40.0
    operator_cycle_s: float = 45.0    # minimum seconds between bag dumps
    lunch_start_hr: float = 6.0
    lunch_minutes: float = 30.0
    ambient_f: float = 95.0
    idle_load_fraction: float = 0.35  # motor load with no material


@dataclass
class SimulationResult:
    time_hr: List[float] = field(default_factory=list)
    hopper_lb: List[float] = field(default_factory=list)
    bags_cumulative: List[int] = field(default_factory=list)
    amps: List[float] = field(default_factory=list)
    kwh_cumulative: List[float] = field(default_factory=list)
    temp_steel_f: List[float] = field(default_factory=list)
    temp_uhmw_f: List[float] = field(default_factory=list)
    temp_enclosure_f: List[float] = field(default_factory=list)
    totals: Dict[str, float] = field(default_factory=dict)


def _finger_thermal_params(material_cp: float, h: float):
    """First-order lag parameters: steady-state rise and time constant."""
    cooling = h * FINGER_AREA_FT2                      # BTU/(hr·°F)
    tau_hr = FINGER_MASS_LB * material_cp / cooling    # hours
    return cooling, tau_hr


def simulate(config: Optional[SimulationConfig] = None) -> SimulationResult:
    """Run the 12-hour duty-cycle simulation."""
    cfg = config or SimulationConfig()
    result = SimulationResult()

    # Mixing rate from the screw-conveyor model at this design point
    design = AugerOptimizer(cfg.housing_id_in).generate_optimized_design()
    flow = throughput_analysis(
        geometry=design["objects"]["geometry"],
        rpm=cfg.rpm,
        fill_efficiency=cfg.fill_efficiency,
    )
    consume_lb_s = flow["throughput_bags_hr"] * cfg.bag_lb / 3600

    # Honest electrical operating point (D2)
    audit = power_audit()
    full_load_amps = audit["amps_needed_at_full_load"]
    motor_watts = audit["rated_output_watts"]

    # Thermal lags (mix-contact cooling while material flows)
    dt_hr = cfg.dt_s / 3600
    heat_btu_hr = motor_watts * FINGER_FRICTION_SHARE * 3.412

    hopper = cfg.hopper_capacity_lb
    bags = 0
    consumed_lb = 0.0
    kwh = 0.0
    since_bag_s = 1e9
    t_steel = t_uhmw = t_box = cfg.ambient_f

    lunch_start = cfg.lunch_start_hr
    lunch_end = cfg.lunch_start_hr + cfg.lunch_minutes / 60

    steps = int(cfg.duration_hr * 3600 / cfg.dt_s)
    sample_every = max(1, int(30 / cfg.dt_s))  # log every ~30 s

    for step in range(steps):
        t_hr = step * cfg.dt_s / 3600
        on_break = lunch_start <= t_hr < lunch_end
        running = not on_break
        mixing = running and hopper > 0

        # Operator feed loop
        since_bag_s += cfg.dt_s
        if (running and since_bag_s >= cfg.operator_cycle_s
                and hopper <= cfg.reload_threshold_lb + cfg.bag_lb / 2
                and hopper + cfg.bag_lb <= cfg.hopper_capacity_lb + 1):
            hopper += cfg.bag_lb
            bags += 1
            since_bag_s = 0.0

        # Material consumption
        if mixing:
            delta = min(consume_lb_s * cfg.dt_s, hopper)
            hopper -= delta
            consumed_lb += delta

        # Electrical
        load = (1.0 if mixing else cfg.idle_load_fraction) if running else 0.0
        amps = full_load_amps * load
        kwh += amps * 120.0 * cfg.dt_s / 3600 / 1000

        # Finger temperatures: first-order lag toward load-dependent target
        h = H_MIX_CONTACT if mixing else H_NATURAL
        cooling = h * FINGER_AREA_FT2
        target = cfg.ambient_f + (heat_btu_hr * load) / cooling
        for name, cp in (("steel", 0.12), ("uhmw", 0.55)):
            tau = FINGER_MASS_LB * cp / cooling
            alpha = 1 - math.exp(-dt_hr / tau)
            if name == "steel":
                t_steel += (target - t_steel) * alpha
            else:
                t_uhmw += (target - t_uhmw) * alpha

        # Electronics enclosure (no fan — worst case)
        box_cooling = H_NATURAL * ENCLOSURE_AREA_FT2
        box_target = cfg.ambient_f + (
            ENCLOSURE_LOSS_W * 3.412 * (1.0 if running else 0.0) / box_cooling
        )
        box_tau = ENCLOSURE_THERMAL_MASS / box_cooling
        t_box += (box_target - t_box) * (1 - math.exp(-dt_hr / box_tau))

        if step % sample_every == 0:
            result.time_hr.append(t_hr)
            result.hopper_lb.append(hopper)
            result.bags_cumulative.append(bags)
            result.amps.append(amps)
            result.kwh_cumulative.append(kwh)
            result.temp_steel_f.append(t_steel)
            result.temp_uhmw_f.append(t_uhmw)
            result.temp_enclosure_f.append(t_box)

    water_gal = bags * WATER_QT_PER_BAG / 4
    enclosure_fan_rise = (
        ENCLOSURE_LOSS_W * 3.412 / (ENCLOSURE_H_FAN * ENCLOSURE_AREA_FT2)
    )

    result.totals = {
        "bags": bags,
        "consumed_lb": consumed_lb,
        "volume_ft3": bags * cfg.bag_yield_ft3,
        "volume_yd3": bags * cfg.bag_yield_ft3 / 27,
        "water_gal": water_gal,
        "energy_kwh": kwh,
        "throughput_bags_hr": flow["throughput_bags_hr"],
        "full_load_amps": full_load_amps,
        "max_temp_steel_f": max(result.temp_steel_f),
        "max_temp_uhmw_f": max(result.temp_uhmw_f),
        "max_temp_enclosure_f": max(result.temp_enclosure_f),
        "enclosure_with_fan_f": cfg.ambient_f + enclosure_fan_rise,
        "uhmw_exceeds_deflection": max(result.temp_uhmw_f) > UHMW_DEFLECTION_F,
        "uhmw_exceeds_continuous": max(result.temp_uhmw_f) > UHMW_MAX_CONTINUOUS_F,
        "steel_margin_f": STEEL_MAX_CONTINUOUS_F - max(result.temp_steel_f),
    }
    return result


def plot(result: SimulationResult, path: str):
    """Render the workday timeline. Requires matplotlib."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    t = result.time_hr

    ax = axes[0]
    ax.fill_between(t, result.hopper_lb, color="#d9b514", alpha=0.6,
                    label="Hopper level (lb)")
    ax.set_ylabel("Hopper (lb)")
    ax2 = ax.twinx()
    ax2.plot(t, result.bags_cumulative, color="#7a4b12", lw=2,
             label="Bags mixed")
    ax2.set_ylabel("Bags (cumulative)")
    ax.set_title(
        f"Material: {result.totals['bags']} bags, "
        f"{result.totals['volume_yd3']:.1f} yd³, "
        f"{result.totals['water_gal']:.0f} gal water"
    )

    ax = axes[1]
    ax.plot(t, result.temp_steel_f, color="#3a6ea5", lw=2, label="Steel fingers")
    ax.plot(t, result.temp_uhmw_f, color="#c0392b", lw=2, label="UHMW fingers")
    ax.plot(t, result.temp_enclosure_f, color="#27764a", lw=2,
            label="Electronics enclosure (no fan)")
    ax.axhline(UHMW_DEFLECTION_F, color="#c0392b", ls="--", lw=1,
               label="UHMW heat deflection (116°F)")
    ax.axhline(140, color="#27764a", ls="--", lw=1,
               label="Electronics derating (140°F)")
    ax.set_ylabel("Temperature (°F)")
    ax.legend(loc="lower right", fontsize=8, ncol=2)
    ax.set_title(
        f"Thermal: UHMW peaks {result.totals['max_temp_uhmw_f']:.0f}°F "
        f"(deflection limit exceeded), steel margin "
        f"{result.totals['steel_margin_f']:.0f}°F; enclosure "
        f"{result.totals['max_temp_enclosure_f']:.0f}°F without fan vs "
        f"{result.totals['enclosure_with_fan_f']:.0f}°F with fan"
    )

    ax = axes[2]
    ax.plot(t, result.amps, color="#444", lw=1, label="Motor current (A)")
    ax.set_ylabel("Current (A)")
    ax.set_xlabel("Time (hours)")
    ax2 = ax.twinx()
    ax2.plot(t, result.kwh_cumulative, color="#8e44ad", lw=2, label="Energy")
    ax2.set_ylabel("Energy (kWh)")
    ax.set_title(
        f"Electrical: {result.totals['full_load_amps']:.1f} A full load "
        f"(not the published 2.6 A), {result.totals['energy_kwh']:.1f} kWh total"
    )

    fig.suptitle("MudMixer 12-hour jobsite duty cycle — operational simulation",
                 fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="Simulate a 12-hour MudMixer jobsite day"
    )
    parser.add_argument("--hours", type=float, default=12.0)
    parser.add_argument("--plot", metavar="PATH", help="Save timeline PNG")
    args = parser.parse_args(argv)

    result = simulate(SimulationConfig(duration_hr=args.hours))
    totals = result.totals

    print("=" * 70)
    print(f"MUDMIXER {args.hours:.0f}-HOUR JOBSITE SIMULATION "
          f"(6.5\" bore design point)")
    print("=" * 70)
    print(f"  Bags mixed:        {totals['bags']} "
          f"({totals['throughput_bags_hr']:.1f} bags/hr capacity)")
    print(f"  Concrete placed:   {totals['volume_yd3']:.1f} yd³ "
          f"({totals['volume_ft3']:.0f} ft³)")
    print(f"  Water used:        {totals['water_gal']:.0f} gal")
    print(f"  Energy:            {totals['energy_kwh']:.1f} kWh at "
          f"{totals['full_load_amps']:.1f} A full load")
    print(f"  Steel fingers:     peak {totals['max_temp_steel_f']:.0f}°F "
          f"(margin {totals['steel_margin_f']:.0f}°F)")
    print(f"  UHMW fingers:      peak {totals['max_temp_uhmw_f']:.0f}°F — "
          f"{'EXCEEDS' if totals['uhmw_exceeds_deflection'] else 'within'} "
          f"116°F heat-deflection limit")
    print(f"  Enclosure:         {totals['max_temp_enclosure_f']:.0f}°F no fan / "
          f"{totals['enclosure_with_fan_f']:.0f}°F with fan "
          f"(140°F derating threshold)")

    if args.plot:
        plot(result, args.plot)
        print(f"\nTimeline saved: {args.plot}")


if __name__ == "__main__":
    main()
