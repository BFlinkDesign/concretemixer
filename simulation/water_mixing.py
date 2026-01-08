#!/usr/bin/env python3
"""
Water Injection and Mixing Simulation

Models the dual-nozzle water injection system and mixing zone
physics for the concrete mixer auger.

Key Parameters:
- Min water pressure: 30 PSI (40 PSI recommended)
- Nozzle count: 2
- Flow control: Adjustable dial
- Water/cement ratio targets based on product type
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum


# =============================================================================
# WATER SYSTEM SPECIFICATIONS
# =============================================================================

@dataclass
class WaterSystemSpecs:
    """Water injection system specifications"""
    min_pressure_psi: float = 30.0
    recommended_pressure_psi: float = 40.0
    nozzle_count: int = 2
    nozzle_orifice_dia_inch: float = 0.125  # 1/8" orifice
    spray_angle_deg: float = 65.0  # Full cone spray
    nozzle_spacing_inch: float = 10.0
    manifold_dia_inch: float = 0.75  # 3/4" copper

    @property
    def nozzle_cv(self) -> float:
        """Flow coefficient Cv (GPM/sqrt(PSI))"""
        # Empirical for 1/8" full cone nozzle
        return 0.5

    def flow_rate_gpm(self, pressure_psi: float) -> float:
        """Calculate flow rate per nozzle at given pressure"""
        return self.nozzle_cv * np.sqrt(pressure_psi)

    def total_flow_gpm(self, pressure_psi: float) -> float:
        """Total flow from all nozzles"""
        return self.nozzle_count * self.flow_rate_gpm(pressure_psi)


@dataclass
class ConcreteWaterRequirements:
    """Water requirements for different concrete products"""
    product_name: str
    water_per_80lb_bag_pints: float
    target_wc_ratio: float  # Water/cement ratio
    slump_target_inch: float

    @property
    def water_per_bag_gallons(self) -> float:
        return self.water_per_80lb_bag_pints / 8.0

    @classmethod
    def get_requirements(cls, product_type: str) -> 'ConcreteWaterRequirements':
        products = {
            "standard": cls("Standard Concrete Mix", 6.0, 0.50, 3.0),
            "high_strength": cls("High-Strength Mix", 5.5, 0.45, 2.5),
            "fast_setting": cls("Fast-Setting Mix", 5.0, 0.42, 2.0),
            "mortar": cls("Mortar Mix", 5.0, 0.55, 4.0),
            "sand_mix": cls("Sand Mix", 4.0, 0.48, 2.0),
            "grout": cls("Non-Shrink Grout", 3.75, 0.40, 6.0),  # Flowable
        }
        return products.get(product_type, products["standard"])


# =============================================================================
# SPRAY PATTERN SIMULATION
# =============================================================================

class SprayPatternSimulation:
    """
    Simulates the water spray pattern from dual nozzles
    into the mixing zone.
    """

    def __init__(self, water_system: WaterSystemSpecs):
        self.ws = water_system

    def spray_coverage(self, distance_inch: float) -> Tuple[float, float]:
        """
        Calculate spray coverage diameter at a given distance.

        Returns: (coverage_diameter, intensity_factor)
        """
        half_angle_rad = np.radians(self.ws.spray_angle_deg / 2)
        diameter = 2 * distance_inch * np.tan(half_angle_rad)

        # Intensity decreases with distance squared
        intensity = 1.0 / (1.0 + (distance_inch / 5.0) ** 2)

        return diameter, intensity

    def mixing_zone_coverage(self, housing_id: float = 5.047) -> dict:
        """
        Analyze spray coverage in the mixing zone.

        Args:
            housing_id: Housing internal diameter (inches)

        Returns:
            Coverage analysis dict
        """
        # Distance from nozzle to auger surface
        nozzle_standoff = 2.0  # inches from housing
        distance_to_auger = nozzle_standoff + (housing_id - 4.0) / 2

        coverage_dia, intensity = self.spray_coverage(distance_to_auger)

        # Overlap between two nozzles
        overlap = max(0, coverage_dia - self.ws.nozzle_spacing_inch / 2)

        return {
            "coverage_diameter_inch": coverage_dia,
            "intensity_factor": intensity,
            "nozzle_overlap_inch": overlap,
            "coverage_percentage": min(100, (2 * coverage_dia / self.ws.nozzle_spacing_inch) * 100),
            "uniform_zone_length": self.ws.nozzle_spacing_inch + coverage_dia
        }


# =============================================================================
# WATER/CEMENT RATIO CONTROL
# =============================================================================

class WaterCementController:
    """
    Models the water flow control for achieving target W/C ratios.
    """

    def __init__(self, water_system: WaterSystemSpecs):
        self.ws = water_system

    def required_flow_rate(self, bags_per_hour: float,
                           requirements: ConcreteWaterRequirements) -> float:
        """
        Calculate required water flow rate for target throughput.

        Args:
            bags_per_hour: Throughput in 80-lb bags per hour
            requirements: Water requirements for the product

        Returns:
            Required flow rate in GPM
        """
        gallons_per_hour = bags_per_hour * requirements.water_per_bag_gallons
        return gallons_per_hour / 60.0  # GPM

    def dial_setting(self, target_gpm: float, pressure_psi: float) -> float:
        """
        Calculate dial setting (0-100%) for target flow rate.

        Assumes linear relationship between dial and flow.
        """
        max_flow = self.ws.total_flow_gpm(pressure_psi)
        setting = (target_gpm / max_flow) * 100
        return min(100, max(0, setting))

    def actual_wc_ratio(self, dial_setting_pct: float, pressure_psi: float,
                        cement_rate_lb_per_min: float) -> float:
        """
        Calculate actual W/C ratio for given settings.

        Args:
            dial_setting_pct: Dial setting 0-100%
            pressure_psi: Water supply pressure
            cement_rate_lb_per_min: Cement flow rate

        Returns:
            Actual water/cement ratio by weight
        """
        max_flow_gpm = self.ws.total_flow_gpm(pressure_psi)
        actual_flow_gpm = max_flow_gpm * (dial_setting_pct / 100)

        # Convert GPM to lb/min (water density ~8.34 lb/gal)
        water_lb_per_min = actual_flow_gpm * 8.34

        if cement_rate_lb_per_min > 0:
            return water_lb_per_min / cement_rate_lb_per_min
        return 0


# =============================================================================
# MIXING EFFICIENCY MODEL
# =============================================================================

class MixingEfficiencyModel:
    """
    Models the mixing efficiency based on water injection,
    auger action, and residence time.
    """

    def __init__(self, auger_rpm: float = 27.0, housing_length: float = 44.0):
        self.auger_rpm = auger_rpm
        self.housing_length = housing_length

    def residence_time(self, pitch_avg: float = 2.75) -> float:
        """
        Calculate material residence time in mixing zone (seconds).
        """
        # Axial velocity = pitch * RPM / 60
        axial_velocity = pitch_avg * self.auger_rpm / 60  # inch/sec
        return self.housing_length / axial_velocity

    def mixing_intensity(self, finger_count: int = 8) -> float:
        """
        Calculate mixing intensity index based on auger design.

        Higher = more aggressive mixing.
        """
        # Shear events per revolution
        shear_events = finger_count

        # Events per second
        events_per_sec = shear_events * self.auger_rpm / 60

        # Normalize to 0-1 scale (100 events/sec = 1.0)
        return min(1.0, events_per_sec / 100)

    def water_integration_efficiency(self, spray_coverage: dict,
                                     residence_time: float) -> float:
        """
        Estimate water integration efficiency (0-1 scale).

        Based on spray coverage and residence time.
        """
        coverage_factor = spray_coverage["coverage_percentage"] / 100
        time_factor = min(1.0, residence_time / 10)  # 10 sec = full integration

        # Combined efficiency
        return coverage_factor * time_factor * 0.95  # 95% max due to losses


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_water_system_analysis(pressure_range: Tuple[float, float] = (20, 60)):
    """Generate water system analysis plots."""
    ws = WaterSystemSpecs()
    spray_sim = SprayPatternSimulation(ws)
    wc_controller = WaterCementController(ws)
    mixing = MixingEfficiencyModel()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Water Injection System Analysis", fontsize=14, fontweight='bold')

    # 1. Flow rate vs pressure
    ax1 = axes[0, 0]
    pressures = np.linspace(pressure_range[0], pressure_range[1], 50)
    flows = [ws.total_flow_gpm(p) for p in pressures]

    ax1.plot(pressures, flows, 'b-', linewidth=2)
    ax1.axvline(x=30, color='r', linestyle='--', label='Min: 30 PSI')
    ax1.axvline(x=40, color='g', linestyle='--', label='Recommended: 40 PSI')
    ax1.axhline(y=0.56, color='orange', linestyle=':', label='Req @ 45 bags/hr')
    ax1.set_xlabel('Supply Pressure (PSI)')
    ax1.set_ylabel('Total Flow Rate (GPM)')
    ax1.set_title('Water Flow vs Supply Pressure')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Spray coverage pattern
    ax2 = axes[0, 1]
    distances = np.linspace(0.5, 6, 50)
    coverages = [spray_sim.spray_coverage(d)[0] for d in distances]
    intensities = [spray_sim.spray_coverage(d)[1] for d in distances]

    ax2.plot(distances, coverages, 'b-', linewidth=2, label='Coverage Diameter')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(distances, intensities, 'r--', linewidth=2, label='Intensity')

    ax2.axvline(x=2.5, color='g', linestyle=':', label='Auger Distance')
    ax2.set_xlabel('Distance from Nozzle (inches)')
    ax2.set_ylabel('Coverage Diameter (inches)', color='b')
    ax2_twin.set_ylabel('Intensity Factor', color='r')
    ax2.set_title('Spray Pattern Characteristics')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    # 3. Dial setting vs W/C ratio
    ax3 = axes[1, 0]
    dial_settings = np.linspace(10, 100, 50)

    for product in ["standard", "high_strength", "mortar", "grout"]:
        req = ConcreteWaterRequirements.get_requirements(product)
        # Assume 1.5 lb/min cement rate at 45 bags/hr
        wc_ratios = [wc_controller.actual_wc_ratio(d, 40, 1.5) for d in dial_settings]
        ax3.plot(dial_settings, wc_ratios, linewidth=2, label=req.product_name)
        ax3.axhline(y=req.target_wc_ratio, linestyle=':', alpha=0.5)

    ax3.set_xlabel('Dial Setting (%)')
    ax3.set_ylabel('Water/Cement Ratio')
    ax3.set_title('W/C Ratio Control')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Mixing efficiency vs residence time
    ax4 = axes[1, 1]
    pitches = np.linspace(1.5, 4.0, 50)
    res_times = [mixing.residence_time(p) for p in pitches]

    coverage = spray_sim.mixing_zone_coverage()
    efficiencies = [mixing.water_integration_efficiency(coverage, t) for t in res_times]

    ax4.plot(res_times, [e * 100 for e in efficiencies], 'b-', linewidth=2)
    ax4.axvline(x=mixing.residence_time(2.75), color='r', linestyle='--',
                label=f'Design: {mixing.residence_time(2.75):.1f}s')
    ax4.set_xlabel('Residence Time (seconds)')
    ax4.set_ylabel('Water Integration Efficiency (%)')
    ax4.set_title('Mixing Efficiency vs Residence Time')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def print_system_summary():
    """Print water system summary."""
    ws = WaterSystemSpecs()
    spray_sim = SprayPatternSimulation(ws)
    wc_controller = WaterCementController(ws)
    mixing = MixingEfficiencyModel()

    print("=" * 60)
    print("WATER INJECTION SYSTEM SUMMARY")
    print("=" * 60)

    print(f"\n[Water System Specs]")
    print(f"  Nozzle count: {ws.nozzle_count}")
    print(f"  Nozzle orifice: {ws.nozzle_orifice_dia_inch}\"")
    print(f"  Spray angle: {ws.spray_angle_deg}°")
    print(f"  Min pressure: {ws.min_pressure_psi} PSI")

    print(f"\n[Flow Rates]")
    for psi in [30, 40, 50]:
        print(f"  @ {psi} PSI: {ws.total_flow_gpm(psi):.2f} GPM")

    coverage = spray_sim.mixing_zone_coverage()
    print(f"\n[Spray Coverage]")
    print(f"  Coverage diameter: {coverage['coverage_diameter_inch']:.2f}\"")
    print(f"  Nozzle overlap: {coverage['nozzle_overlap_inch']:.2f}\"")
    print(f"  Coverage %: {coverage['coverage_percentage']:.1f}%")

    print(f"\n[Mixing Zone]")
    print(f"  Residence time: {mixing.residence_time():.1f} seconds")
    print(f"  Mixing intensity: {mixing.mixing_intensity():.2f}")
    print(f"  Integration efficiency: {mixing.water_integration_efficiency(coverage, mixing.residence_time())*100:.1f}%")

    print(f"\n[Dial Settings for 45 bags/hr @ 40 PSI]")
    for product in ["standard", "high_strength", "mortar", "grout"]:
        req = ConcreteWaterRequirements.get_requirements(product)
        target_gpm = wc_controller.required_flow_rate(45, req)
        dial = wc_controller.dial_setting(target_gpm, 40)
        print(f"  {req.product_name}: {dial:.0f}%")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print_system_summary()

    print("\n[Generating plots...]")
    fig = plot_water_system_analysis()
    fig.savefig("/home/user/concretemixer/simulation/water_system_analysis.png",
                dpi=150, bbox_inches='tight')
    print("Saved: water_system_analysis.png")

    plt.close()
