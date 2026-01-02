#!/usr/bin/env python3
"""
MudMixer Auger Generative Design Framework

This module provides computational tools for optimizing the design of a
shaftless helical auger for continuous concrete mixing.

Usage:
    python auger_optimizer.py --housing-id 6.0 --torque 95 --aggregate 0.5

Dependencies:
    - numpy
    - scipy (optional, for advanced optimization)
    - matplotlib (optional, for visualization)
"""

import math
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict
from enum import Enum


class FingerMaterial(Enum):
    """Available finger materials with mechanical properties."""
    STEEL_1045 = ("1045 Steel", 12000, 250)           # (name, shear_psi, max_temp_F)
    STAINLESS_304 = ("304 SS", 10000, 1500)
    UHMW_STANDARD = ("UHMW-PE", 2000, 180)
    UHMW_HIGH_TEMP = ("High-Temp UHMW", 1800, 275)
    PTFE = ("PTFE/Teflon", 600, 500)

    def __init__(self, display_name: str, shear_strength_psi: int, max_temp_f: int):
        self.display_name = display_name
        self.shear_strength_psi = shear_strength_psi
        self.max_temp_f = max_temp_f


class DutyCycle(Enum):
    """Operating duty cycle classifications."""
    LIGHT = ("light", 5, 10)      # (name, bags_per_session, sessions_per_day)
    MEDIUM = ("medium", 20, 5)
    HEAVY = ("heavy", 50, 3)
    CONTINUOUS = ("continuous", 100, 1)

    def __init__(self, name: str, bags_per_session: int, sessions_per_day: int):
        self._name = name
        self.bags_per_session = bags_per_session
        self.sessions_per_day = sessions_per_day


@dataclass
class AugerGeometry:
    """Defines the geometric parameters of the shaftless auger."""
    outer_diameter: float           # inches
    inner_diameter: float           # inches (open center)
    length_hopper: float            # inches (section 1)
    length_chute: float             # inches (section 2)
    pitch_hopper: float             # inches (section 1 pitch)
    pitch_chute: float              # inches (section 2 pitch)
    flight_thickness: float = 0.1875  # inches (3/16")

    @property
    def total_length(self) -> float:
        return self.length_hopper + self.length_chute

    @property
    def pd_ratio_hopper(self) -> float:
        return self.pitch_hopper / self.outer_diameter

    @property
    def pd_ratio_chute(self) -> float:
        return self.pitch_chute / self.outer_diameter

    def validate(self) -> List[str]:
        """Validate geometry against patent specifications."""
        issues = []

        # Patent 10,259,140: P/D ratio 0.2-0.9 for hopper
        if not (0.2 <= self.pd_ratio_hopper <= 0.9):
            issues.append(f"Hopper P/D ratio {self.pd_ratio_hopper:.2f} outside range 0.2-0.9")

        # Patent 11,285,639: P/D ratio 0.6-1.0 for chute
        if not (0.6 <= self.pd_ratio_chute <= 1.0):
            issues.append(f"Chute P/D ratio {self.pd_ratio_chute:.2f} outside range 0.6-1.0")

        # Chute pitch must be greater than hopper pitch
        if self.pitch_chute <= self.pitch_hopper:
            issues.append("Chute pitch must be greater than hopper pitch (variable pitch design)")

        return issues


@dataclass
class FingerConfig:
    """Defines the finger (mixing element) configuration."""
    material: FingerMaterial
    diameter: float                 # inches
    length: float                   # inches (how far into interior)
    count: int                      # total number of fingers
    angle: float = 90.0             # degrees from flight surface

    @property
    def cross_section_area(self) -> float:
        """Cross-sectional area in square inches."""
        return math.pi * (self.diameter / 2) ** 2


@dataclass
class OperatingConditions:
    """Defines the operating environment and constraints."""
    motor_power_hp: float = 0.5
    motor_rpm: float = 27.0
    max_aggregate_size: float = 0.5     # inches (CONFIRMED for MudMixer)
    duty_cycle: DutyCycle = DutyCycle.MEDIUM
    ambient_temp_f: float = 70.0
    water_pressure_psi: float = 40.0

    @property
    def motor_torque_ft_lb(self) -> float:
        """Calculate motor output torque from power and RPM."""
        # HP = Torque(ft-lb) × RPM / 5252
        return (self.motor_power_hp * 5252) / self.motor_rpm

    @property
    def motor_torque_nm(self) -> float:
        """Motor torque in Newton-meters."""
        return self.motor_torque_ft_lb * 1.3558


class AugerOptimizer:
    """
    Generative design optimizer for shaftless helical auger.

    This class performs engineering calculations to validate and optimize
    auger geometry, finger configuration, and material selection.
    """

    def __init__(
        self,
        housing_id: float,
        conditions: Optional[OperatingConditions] = None
    ):
        """
        Initialize optimizer with housing internal diameter.

        Args:
            housing_id: Internal diameter of chute housing (inches)
            conditions: Operating conditions (uses defaults if None)
        """
        self.housing_id = housing_id
        self.conditions = conditions or OperatingConditions()
        self.safety_factor = 2.5

    def calculate_clearance(self, auger_od: float) -> Dict[str, float]:
        """
        Calculate clearance between auger and housing.

        Args:
            auger_od: Outer diameter of auger (inches)

        Returns:
            Dict with clearance analysis results
        """
        clearance_per_side = (self.housing_id - auger_od) / 2
        clearance_ratio = clearance_per_side / self.conditions.max_aggregate_size

        # Determine if clearance is adequate
        min_clearance = self.conditions.max_aggregate_size * 1.2  # 20% safety

        result = {
            "housing_id": self.housing_id,
            "auger_od": auger_od,
            "clearance_per_side": clearance_per_side,
            "clearance_total": clearance_per_side * 2,
            "clearance_ratio": clearance_ratio,
            "min_required": min_clearance,
            "status": "OK" if clearance_per_side >= min_clearance else "FAIL"
        }

        if clearance_per_side < min_clearance:
            result["warning"] = (
                f"Clearance {clearance_per_side:.3f}\" < minimum {min_clearance:.3f}\". "
                f"Risk of aggregate jamming with {self.conditions.max_aggregate_size}\" stone."
            )
        elif clearance_per_side > self.conditions.max_aggregate_size * 2:
            result["warning"] = (
                f"Clearance {clearance_per_side:.3f}\" may be excessive. "
                "Reduced shear efficiency and material bypass possible."
            )

        return result

    def calculate_finger_shear(self, fingers: FingerConfig) -> Dict[str, any]:
        """
        Determine if fingers can shear aggregate based on torque and geometry.

        Args:
            fingers: Finger configuration

        Returns:
            Dict with shear analysis results
        """
        # Force at finger tip = Torque / Radius
        # Assume fingers at average radius
        avg_radius = (self.housing_id / 2) * 0.7  # 70% of housing radius
        avg_radius_ft = avg_radius / 12

        force_per_finger = (
            self.conditions.motor_torque_ft_lb /
            (avg_radius_ft * fingers.count)
        )
        force_per_finger_lbf = force_per_finger

        # Contact area: finger diameter × aggregate size (worst case)
        contact_area = fingers.diameter * self.conditions.max_aggregate_size

        # Pressure on finger
        pressure_psi = force_per_finger_lbf / contact_area

        # Compare to material shear strength
        material_strength = fingers.material.shear_strength_psi
        design_strength = material_strength / self.safety_factor

        result = {
            "force_per_finger_lbf": force_per_finger_lbf,
            "contact_area_sq_in": contact_area,
            "pressure_psi": pressure_psi,
            "material": fingers.material.display_name,
            "material_strength_psi": material_strength,
            "design_strength_psi": design_strength,
            "utilization": pressure_psi / design_strength,
        }

        if pressure_psi > design_strength:
            result["status"] = "FAIL"
            result["recommendation"] = (
                f"Finger stress {pressure_psi:.0f} psi > allowable {design_strength:.0f} psi. "
                "Options: increase finger diameter, add more fingers, or use stronger material."
            )
        elif pressure_psi < design_strength * 0.3:
            result["status"] = "OVER-DESIGNED"
            result["recommendation"] = (
                f"Finger utilization only {result['utilization']*100:.0f}%. "
                "Consider smaller fingers or fewer count for weight reduction."
            )
        else:
            result["status"] = "OK"
            result["recommendation"] = "Finger geometry adequate for shear requirements."

        return result

    def calculate_skeleton_diameter(self) -> Dict[str, float]:
        """
        Calculate minimum stainless steel skeleton wire diameter for torsion.

        For a shaftless auger with SS skeleton + UHMW flighting, the skeleton
        must resist the full motor torque.

        Returns:
            Dict with skeleton sizing results
        """
        torque_in_lb = self.conditions.motor_torque_ft_lb * 12  # ft-lb to in-lb

        # Shear stress formula for solid round bar in torsion:
        # τ = 16T / (π × d³)
        # Solving for d: d = ∛(16T / (π × τ_allow))

        # 304 Stainless Steel shear allowable (with safety factor)
        ss_shear_ultimate = 31000  # psi
        ss_shear_allow = ss_shear_ultimate / self.safety_factor

        d_cubed = (16 * torque_in_lb * self.safety_factor) / (math.pi * ss_shear_allow)
        min_diameter = d_cubed ** (1/3)

        # Round up to standard wire sizes
        standard_sizes = [0.125, 0.1875, 0.25, 0.3125, 0.375, 0.5, 0.625, 0.75]
        recommended_size = next((s for s in standard_sizes if s >= min_diameter), standard_sizes[-1])

        return {
            "torque_in_lb": torque_in_lb,
            "min_diameter_in": min_diameter,
            "recommended_diameter_in": recommended_size,
            "material": "304 Stainless Steel",
            "shear_allowable_psi": ss_shear_allow,
            "safety_factor": self.safety_factor,
        }

    def calculate_thermal_rise(
        self,
        fingers: FingerConfig,
        runtime_minutes: float = 60
    ) -> Dict[str, any]:
        """
        Estimate temperature rise in fingers due to friction.

        Args:
            fingers: Finger configuration
            runtime_minutes: Continuous operation time

        Returns:
            Dict with thermal analysis results
        """
        # Friction power = coefficient × normal force × velocity
        # This is a simplified model

        friction_coeff = 0.3  # Concrete on UHMW estimate
        avg_radius = self.housing_id / 2 * 0.7
        velocity = 2 * math.pi * (avg_radius / 12) * self.conditions.motor_rpm / 60  # ft/s

        # Assume 10% of motor power goes to finger friction
        friction_power_watts = self.conditions.motor_power_hp * 746 * 0.10
        friction_power_btu_hr = friction_power_watts * 3.412

        # Simplified heat rise (very rough estimate)
        # Assumes adiabatic conditions (no cooling)
        heat_capacity = 0.5  # BTU/(lb·°F) for UHMW
        finger_weight_lb = (
            fingers.cross_section_area * fingers.length *
            0.034 * fingers.count  # UHMW density ~0.034 lb/in³
        )

        temp_rise = (friction_power_btu_hr * runtime_minutes / 60) / (finger_weight_lb * heat_capacity)
        final_temp = self.conditions.ambient_temp_f + temp_rise

        result = {
            "friction_power_watts": friction_power_watts,
            "runtime_minutes": runtime_minutes,
            "estimated_temp_rise_f": temp_rise,
            "final_temp_f": final_temp,
            "material_max_temp_f": fingers.material.max_temp_f,
        }

        if final_temp > fingers.material.max_temp_f:
            result["status"] = "FAIL"
            result["recommendation"] = (
                f"Estimated temp {final_temp:.0f}°F exceeds {fingers.material.display_name} "
                f"limit of {fingers.material.max_temp_f}°F. Use high-temp material or add cooling."
            )
        else:
            margin = fingers.material.max_temp_f - final_temp
            result["status"] = "OK"
            result["temp_margin_f"] = margin

        return result

    def generate_optimized_design(
        self,
        target_throughput_bags_hr: float = 45
    ) -> Dict[str, any]:
        """
        Generate an optimized auger design based on constraints.

        Args:
            target_throughput_bags_hr: Target throughput in 80-lb bags/hour

        Returns:
            Complete design specification
        """
        # Calculate optimal auger diameter (leave clearance for aggregate)
        optimal_clearance = self.conditions.max_aggregate_size * 1.5
        auger_od = self.housing_id - (2 * optimal_clearance)
        auger_id = auger_od * 0.82  # ~18% wall for shaftless flight

        # Calculate pitch based on P/D ratios
        pd_hopper = 0.65  # Middle of 0.5-0.8 preferred range
        pd_chute = 0.85   # Middle of 0.6-1.0 range

        pitch_hopper = pd_hopper * auger_od
        pitch_chute = pd_chute * auger_od

        # Estimate lengths (based on 16-30" chute range)
        length_hopper = 10.0  # inches
        length_chute = 14.0   # inches

        geometry = AugerGeometry(
            outer_diameter=auger_od,
            inner_diameter=auger_id,
            length_hopper=length_hopper,
            length_chute=length_chute,
            pitch_hopper=pitch_hopper,
            pitch_chute=pitch_chute,
        )

        # Optimize finger configuration
        fingers = FingerConfig(
            material=FingerMaterial.STEEL_1045,  # Default to steel for durability
            diameter=0.375,  # 3/8" standard
            length=2.0,      # 2" inward projection
            count=8,         # 8 fingers total
        )

        # Run all analyses
        clearance = self.calculate_clearance(auger_od)
        shear = self.calculate_finger_shear(fingers)
        skeleton = self.calculate_skeleton_diameter()
        thermal = self.calculate_thermal_rise(fingers, runtime_minutes=30)

        return {
            "geometry": {
                "auger_od": auger_od,
                "auger_id": auger_id,
                "housing_id": self.housing_id,
                "clearance_per_side": optimal_clearance,
                "pitch_hopper": pitch_hopper,
                "pitch_chute": pitch_chute,
                "length_total": geometry.total_length,
                "pd_ratio_hopper": pd_hopper,
                "pd_ratio_chute": pd_chute,
            },
            "fingers": {
                "material": fingers.material.display_name,
                "diameter": fingers.diameter,
                "length": fingers.length,
                "count": fingers.count,
            },
            "skeleton": skeleton,
            "analysis": {
                "clearance": clearance,
                "shear": shear,
                "thermal": thermal,
            },
            "validation": geometry.validate(),
        }


class CFDParameters:
    """
    Boundary conditions for Computational Fluid Dynamics simulation.

    Concrete is modeled as a Bingham Plastic fluid:
    τ = τ_y + μ_p × γ̇

    Where:
        τ = shear stress
        τ_y = yield stress (concrete acts solid below this)
        μ_p = plastic viscosity
        γ̇ = shear rate
    """

    def __init__(
        self,
        slump_inches: float = 4.0,
        water_cement_ratio: float = 0.5,
        aggregate_fraction: float = 0.65,
    ):
        self.slump = slump_inches
        self.wc_ratio = water_cement_ratio
        self.aggregate_fraction = aggregate_fraction

    @property
    def yield_stress_pa(self) -> float:
        """Estimate yield stress from slump (empirical correlation)."""
        # τ_y ≈ 300 × (10 - slump) for slump in inches
        return 300 * (10 - self.slump)

    @property
    def plastic_viscosity_pa_s(self) -> float:
        """Estimate plastic viscosity from w/c ratio."""
        # Higher w/c = lower viscosity
        base_viscosity = 30  # Pa·s at w/c = 0.5
        return base_viscosity * (0.5 / self.wc_ratio) ** 1.5

    def generate_cfd_setup(self) -> Dict[str, any]:
        """Generate CFD simulation parameters."""
        return {
            "material_model": "Bingham Plastic",
            "density_kg_m3": 2400,
            "yield_stress_pa": self.yield_stress_pa,
            "plastic_viscosity_pa_s": self.plastic_viscosity_pa_s,
            "inlet": {
                "type": "mass_flow",
                "material": "dry_premix",
                "moisture_content": 0.0,
            },
            "water_injection": {
                "type": "spray_nozzle",
                "count": 2,
                "pressure_psi": 40,
                "angle_degrees": 65,
                "location": "aperture_zone",
            },
            "outlet": {
                "type": "pressure_outlet",
                "target_moisture": 0.12,  # ~12% by weight
            },
            "mesh": {
                "type": "polyhedral",
                "base_size_mm": 5,
                "prism_layers": 5,
                "wall_y_plus": 30,
            },
            "solver": {
                "type": "unsteady_rans",
                "turbulence_model": "k-omega-sst",
                "time_step_s": 0.001,
                "max_iterations": 50,
            },
        }


def main():
    """Example usage of the optimizer."""
    print("=" * 70)
    print("MudMixer Auger Generative Design Framework")
    print("=" * 70)
    print()

    # Initialize with known/assumed housing ID
    housing_id = 6.0  # inches (ASSUMED - needs measurement)

    conditions = OperatingConditions(
        motor_power_hp=0.5,
        motor_rpm=27,
        max_aggregate_size=0.5,  # CONFIRMED
        duty_cycle=DutyCycle.MEDIUM,
    )

    optimizer = AugerOptimizer(housing_id, conditions)

    print(f"Housing Internal Diameter: {housing_id}\" (ASSUMED)")
    print(f"Motor: {conditions.motor_power_hp} HP @ {conditions.motor_rpm} RPM")
    print(f"Torque: {conditions.motor_torque_ft_lb:.1f} ft-lb ({conditions.motor_torque_nm:.1f} N·m)")
    print(f"Max Aggregate: {conditions.max_aggregate_size}\" (CONFIRMED)")
    print()

    # Generate optimized design
    design = optimizer.generate_optimized_design()

    print("-" * 70)
    print("OPTIMIZED GEOMETRY")
    print("-" * 70)
    for key, value in design["geometry"].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}\"")
        else:
            print(f"  {key}: {value}")

    print()
    print("-" * 70)
    print("FINGER CONFIGURATION")
    print("-" * 70)
    for key, value in design["fingers"].items():
        print(f"  {key}: {value}")

    print()
    print("-" * 70)
    print("SKELETON SIZING")
    print("-" * 70)
    skeleton = design["skeleton"]
    print(f"  Minimum diameter: {skeleton['min_diameter_in']:.3f}\"")
    print(f"  Recommended: {skeleton['recommended_diameter_in']}\" SS wire")

    print()
    print("-" * 70)
    print("ANALYSIS RESULTS")
    print("-" * 70)

    clearance = design["analysis"]["clearance"]
    print(f"  Clearance: {clearance['status']}")
    print(f"    Per side: {clearance['clearance_per_side']:.3f}\"")
    if "warning" in clearance:
        print(f"    Warning: {clearance['warning']}")

    shear = design["analysis"]["shear"]
    print(f"  Finger Shear: {shear['status']}")
    print(f"    Utilization: {shear['utilization']*100:.0f}%")
    print(f"    {shear['recommendation']}")

    thermal = design["analysis"]["thermal"]
    print(f"  Thermal: {thermal['status']}")
    print(f"    Est. temp rise: {thermal['estimated_temp_rise_f']:.0f}°F")

    if design["validation"]:
        print()
        print("  VALIDATION ISSUES:")
        for issue in design["validation"]:
            print(f"    ⚠️  {issue}")

    print()
    print("=" * 70)
    print("CFD SIMULATION PARAMETERS")
    print("=" * 70)
    cfd = CFDParameters(slump_inches=4.0)
    params = cfd.generate_cfd_setup()
    print(f"  Material Model: {params['material_model']}")
    print(f"  Yield Stress: {params['yield_stress_pa']:.0f} Pa")
    print(f"  Plastic Viscosity: {params['plastic_viscosity_pa_s']:.1f} Pa·s")
    print()


if __name__ == "__main__":
    main()
