#!/usr/bin/env python3
"""
Comprehensive Digital Twin Test Suite

Tests for 95%+ accuracy validation of the concrete mixer digital twin.
Includes:
- Dimensional accuracy tests
- Physics model validation
- Flow rate calculations
- Torque/power verification
- Thermal analysis validation
- Water system accuracy
- Component geometry verification

Run with: pytest test_digital_twin.py -v
"""

import pytest
import numpy as np
import sys
import os

# Add simulation directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))

from auger_physics import (
    AugerSpecs, HousingSpecs, MotorSpecs,
    AugerFlowSimulation, ThermalSimulation, ParticleSimulation,
    ConcreteType, ConcreteProperties
)
from water_mixing import (
    WaterSystemSpecs, ConcreteWaterRequirements,
    SprayPatternSimulation, WaterCementController, MixingEfficiencyModel
)


# =============================================================================
# TEST CONFIGURATION - Known Reference Values
# =============================================================================

# From DATA_REQUIREMENTS.md - CONFIRMED specifications
REFERENCE_SPECS = {
    # Overall Dimensions (CONFIRMED)
    "overall_length_in": 66.5,
    "overall_width_in": 27.5,
    "overall_height_in": 35.0,
    "chute_height_in": 16.0,
    "dry_weight_lb": 145.0,

    # Auger (CONFIRMED 4" OD)
    "auger_od_in": 4.0,
    "auger_od_mm": 102.0,

    # Housing (5" Sch 40 pipe)
    "housing_od_in": 5.563,
    "housing_id_in": 5.047,

    # Clearance
    "clearance_per_side_in": 0.523,  # (5.047 - 4.0) / 2

    # Motor
    "motor_power_hp": 0.5,
    "motor_power_w": 373.0,
    "motor_rpm": 27.0,
    "motor_voltage": 120.0,
    "motor_current_a": 2.6,

    # Capacity
    "hopper_capacity_lb": 120.0,
    "throughput_bags_per_hr": 45.0,  # Target: 45+ bags/hr

    # Water System
    "min_water_pressure_psi": 30.0,
    "nozzle_count": 2,

    # Pitch-to-Diameter ratios
    "pd_ratio_hopper_min": 0.5,
    "pd_ratio_hopper_max": 0.8,
    "pd_ratio_chute_min": 0.6,
    "pd_ratio_chute_max": 1.0,

    # Max aggregate size
    "max_aggregate_in": 0.5,
}

# Tolerance for accuracy tests (95% = 5% tolerance)
TOLERANCE_PERCENT = 5.0


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def within_tolerance(actual: float, expected: float, tolerance_pct: float = TOLERANCE_PERCENT) -> bool:
    """Check if actual value is within tolerance of expected."""
    if expected == 0:
        return abs(actual) < 0.001
    return abs((actual - expected) / expected) * 100 <= tolerance_pct


def accuracy_score(actual: float, expected: float) -> float:
    """Calculate accuracy score (0-100%)."""
    if expected == 0:
        return 100.0 if abs(actual) < 0.001 else 0.0
    error = abs((actual - expected) / expected) * 100
    return max(0, 100 - error)


# =============================================================================
# DIMENSIONAL ACCURACY TESTS
# =============================================================================

class TestDimensionalAccuracy:
    """Test dimensional accuracy of the digital twin."""

    def test_auger_outer_diameter(self):
        """Verify auger OD matches confirmed 4.0 inch specification."""
        auger = AugerSpecs()
        expected = REFERENCE_SPECS["auger_od_in"]
        actual = auger.outer_diameter

        assert actual == expected, f"Auger OD: {actual} != {expected}"
        assert accuracy_score(actual, expected) >= 95.0

    def test_auger_od_metric(self):
        """Verify auger OD in metric (102mm)."""
        auger = AugerSpecs()
        expected_mm = REFERENCE_SPECS["auger_od_mm"]
        actual_mm = auger.outer_diameter * 25.4

        assert within_tolerance(actual_mm, expected_mm, 2.0)  # Tighter tolerance for conversion

    def test_housing_id(self):
        """Verify housing ID matches 5" Sch 40 pipe."""
        housing = HousingSpecs()
        expected = REFERENCE_SPECS["housing_id_in"]
        actual = housing.inner_diameter

        assert within_tolerance(actual, expected)
        assert accuracy_score(actual, expected) >= 95.0

    def test_housing_od(self):
        """Verify housing OD matches 5" Sch 40 pipe."""
        housing = HousingSpecs()
        expected = REFERENCE_SPECS["housing_od_in"]
        actual = housing.outer_diameter

        assert within_tolerance(actual, expected)

    def test_clearance_calculation(self):
        """Verify auger-to-housing clearance calculation."""
        housing = HousingSpecs()
        expected = REFERENCE_SPECS["clearance_per_side_in"]
        actual = housing.clearance

        assert within_tolerance(actual, expected, 2.0)  # Tighter tolerance
        assert accuracy_score(actual, expected) >= 95.0

    def test_pitch_to_diameter_ratios(self):
        """Verify P/D ratios are within patent specifications."""
        auger = AugerSpecs()

        # Hopper P/D ratio
        pd_hopper = auger.pitch_hopper / auger.outer_diameter
        assert REFERENCE_SPECS["pd_ratio_hopper_min"] <= pd_hopper <= REFERENCE_SPECS["pd_ratio_hopper_max"], \
            f"Hopper P/D {pd_hopper} out of range"

        # Chute P/D ratio
        pd_chute = auger.pitch_chute / auger.outer_diameter
        assert REFERENCE_SPECS["pd_ratio_chute_min"] <= pd_chute <= REFERENCE_SPECS["pd_ratio_chute_max"], \
            f"Chute P/D {pd_chute} out of range"


# =============================================================================
# MOTOR & POWER TESTS
# =============================================================================

class TestMotorSpecifications:
    """Test motor and power calculations."""

    def test_motor_power_hp(self):
        """Verify motor power matches 0.5 HP specification."""
        motor = MotorSpecs()
        expected = REFERENCE_SPECS["motor_power_hp"]
        actual = motor.power_hp

        assert actual == expected

    def test_motor_power_watts(self):
        """Verify motor power in watts."""
        motor = MotorSpecs()
        expected = REFERENCE_SPECS["motor_power_w"]
        actual = motor.power_watts

        assert within_tolerance(actual, expected)

    def test_motor_rpm(self):
        """Verify motor RPM."""
        motor = MotorSpecs()
        expected = REFERENCE_SPECS["motor_rpm"]
        actual = motor.rpm

        assert actual == expected

    def test_torque_calculation(self):
        """Verify torque calculation from power and RPM."""
        motor = MotorSpecs()

        # Torque = Power / (2π × RPM/60)
        expected_nm = motor.power_watts / (2 * np.pi * motor.rpm / 60)
        actual_nm = motor.torque_nm

        assert within_tolerance(actual_nm, expected_nm, 1.0)  # Very tight tolerance

    def test_torque_ftlb_conversion(self):
        """Verify torque conversion to ft-lb."""
        motor = MotorSpecs()

        expected_ftlb = motor.torque_nm * 0.7376
        actual_ftlb = motor.torque_ftlb

        assert within_tolerance(actual_ftlb, expected_ftlb, 1.0)

    def test_motor_adequacy(self):
        """Verify motor has adequate torque margin for all concrete types."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()

        for concrete_type in ConcreteType:
            sim = AugerFlowSimulation(auger, housing, motor, concrete_type)
            result = sim.check_motor_adequacy()

            assert result["adequate"], f"Motor inadequate for {concrete_type.value}"
            assert result["torque_margin"] > 50, f"Torque margin too low for {concrete_type.value}"


# =============================================================================
# FLOW & THROUGHPUT TESTS
# =============================================================================

class TestFlowCalculations:
    """Test flow rate and throughput calculations."""

    def test_volumetric_flow_positive(self):
        """Verify volumetric flow is positive."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

        flow = sim.calculate_volumetric_flow()
        assert flow > 0, "Volumetric flow must be positive"

    def test_mass_flow_positive(self):
        """Verify mass flow is positive."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

        mass_flow = sim.calculate_mass_flow()
        assert mass_flow > 0, "Mass flow must be positive"

    def test_throughput_reasonable(self):
        """Verify throughput is in reasonable range."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

        throughput = sim.calculate_throughput_bags_per_hour()

        # Should be > 0 and < 100 bags/hr for this design
        assert 5 < throughput < 100, f"Throughput {throughput} out of reasonable range"

    def test_shear_rate_positive(self):
        """Verify shear rate is positive."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

        shear_rate = sim.calculate_shear_rate()
        assert shear_rate > 0, "Shear rate must be positive"


# =============================================================================
# CONCRETE PROPERTIES TESTS
# =============================================================================

class TestConcreteProperties:
    """Test concrete rheological properties."""

    def test_all_concrete_types_have_properties(self):
        """Verify all concrete types have defined properties."""
        for concrete_type in ConcreteType:
            props = ConcreteProperties.get_properties(concrete_type)
            assert props is not None
            assert props.density > 0
            assert props.yield_stress >= 0
            assert props.plastic_viscosity > 0

    def test_density_range(self):
        """Verify concrete densities are in realistic range."""
        for concrete_type in ConcreteType:
            props = ConcreteProperties.get_properties(concrete_type)
            # Fresh concrete: 2000-2500 kg/m³
            assert 2000 <= props.density <= 2500, \
                f"{concrete_type.value} density {props.density} out of range"

    def test_max_aggregate_within_spec(self):
        """Verify all products have aggregate <= 0.5 inch."""
        for concrete_type in ConcreteType:
            props = ConcreteProperties.get_properties(concrete_type)
            assert props.max_aggregate_size <= REFERENCE_SPECS["max_aggregate_in"], \
                f"{concrete_type.value} aggregate {props.max_aggregate_size} exceeds max"

    def test_bingham_plastic_model(self):
        """Verify Bingham plastic viscosity model."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

        apparent_visc = sim.calculate_apparent_viscosity()

        # Apparent viscosity should be > plastic viscosity (due to yield stress)
        assert apparent_visc >= sim.concrete.plastic_viscosity


# =============================================================================
# THERMAL ANALYSIS TESTS
# =============================================================================

class TestThermalAnalysis:
    """Test thermal simulation accuracy."""

    def test_heat_generation_positive(self):
        """Verify heat generation is positive."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        flow_sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)
        thermal_sim = ThermalSimulation(flow_sim)

        heat = thermal_sim.calculate_heat_generation()

        assert heat["motor_heat_w"] > 0
        assert heat["total_heat_w"] > 0

    def test_temperature_rise_reasonable(self):
        """Verify temperature rise is in reasonable range."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        flow_sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)
        thermal_sim = ThermalSimulation(flow_sim)

        temp = thermal_sim.estimate_temperature_rise(ambient_temp_c=25)

        # Should be < 100°C for normal operation
        assert 25 < temp < 100, f"Temperature {temp}°C unreasonable"

    def test_motor_efficiency_loss(self):
        """Verify motor heat is ~20% of input power."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        flow_sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)
        thermal_sim = ThermalSimulation(flow_sim)

        heat = thermal_sim.calculate_heat_generation()

        # Motor heat should be ~20% of power (80% efficient)
        expected_motor_heat = motor.power_watts * 0.20
        assert within_tolerance(heat["motor_heat_w"], expected_motor_heat, 10)


# =============================================================================
# WATER SYSTEM TESTS
# =============================================================================

class TestWaterSystem:
    """Test water injection system accuracy."""

    def test_water_system_specs(self):
        """Verify water system specifications."""
        ws = WaterSystemSpecs()

        assert ws.min_pressure_psi == REFERENCE_SPECS["min_water_pressure_psi"]
        assert ws.nozzle_count == REFERENCE_SPECS["nozzle_count"]

    def test_flow_rate_calculation(self):
        """Verify flow rate calculation at various pressures."""
        ws = WaterSystemSpecs()

        # Flow should increase with pressure
        flow_30 = ws.total_flow_gpm(30)
        flow_40 = ws.total_flow_gpm(40)
        flow_50 = ws.total_flow_gpm(50)

        assert flow_30 < flow_40 < flow_50
        assert flow_30 > 0

    def test_spray_coverage(self):
        """Verify spray pattern coverage calculation."""
        ws = WaterSystemSpecs()
        spray_sim = SprayPatternSimulation(ws)

        # Coverage should increase with distance
        cov_1, _ = spray_sim.spray_coverage(1.0)
        cov_3, _ = spray_sim.spray_coverage(3.0)

        assert cov_3 > cov_1

    def test_mixing_zone_coverage(self):
        """Verify mixing zone coverage analysis."""
        ws = WaterSystemSpecs()
        spray_sim = SprayPatternSimulation(ws)

        coverage = spray_sim.mixing_zone_coverage()

        assert coverage["coverage_diameter_inch"] > 0
        assert 0 <= coverage["coverage_percentage"] <= 200  # Can exceed 100 with overlap

    def test_water_requirements_all_products(self):
        """Verify water requirements for all product types."""
        for product in ["standard", "high_strength", "fast_setting", "mortar", "sand_mix", "grout"]:
            req = ConcreteWaterRequirements.get_requirements(product)
            assert req is not None
            assert req.water_per_80lb_bag_pints > 0
            assert req.target_wc_ratio > 0

    def test_dial_setting_range(self):
        """Verify dial settings are in valid range."""
        ws = WaterSystemSpecs()
        controller = WaterCementController(ws)

        for product in ["standard", "high_strength", "mortar", "grout"]:
            req = ConcreteWaterRequirements.get_requirements(product)
            target_gpm = controller.required_flow_rate(45, req)
            dial = controller.dial_setting(target_gpm, 40)

            assert 0 <= dial <= 100, f"Dial setting {dial}% out of range for {product}"


# =============================================================================
# PARTICLE SIMULATION TESTS
# =============================================================================

class TestParticleSimulation:
    """Test DEM particle simulation."""

    def test_particle_initialization(self):
        """Verify particles initialize correctly."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        particle_sim = ParticleSimulation(auger, housing, num_particles=50)

        assert len(particle_sim.particles) == 50

    def test_particle_sizes_within_spec(self):
        """Verify particle sizes are within aggregate spec."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        particle_sim = ParticleSimulation(auger, housing, num_particles=100)

        for p in particle_sim.particles:
            assert p["size"] <= REFERENCE_SPECS["max_aggregate_in"], \
                f"Particle size {p['size']} exceeds max aggregate"

    def test_particle_step_advances(self):
        """Verify particles move during simulation step."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        particle_sim = ParticleSimulation(auger, housing, num_particles=10)

        initial_positions = particle_sim.get_particle_positions().copy()

        for _ in range(10):
            particle_sim.step(dt=0.01, auger_rpm=27)

        final_positions = particle_sim.get_particle_positions()

        # At least some particles should have moved
        assert not np.allclose(initial_positions, final_positions)


# =============================================================================
# MIXING EFFICIENCY TESTS
# =============================================================================

class TestMixingEfficiency:
    """Test mixing efficiency model."""

    def test_residence_time_positive(self):
        """Verify residence time is positive."""
        mixing = MixingEfficiencyModel()
        res_time = mixing.residence_time()

        assert res_time > 0

    def test_residence_time_reasonable(self):
        """Verify residence time is in reasonable range."""
        mixing = MixingEfficiencyModel()
        res_time = mixing.residence_time()

        # Should be 10-60 seconds for this design
        assert 10 < res_time < 60, f"Residence time {res_time}s out of range"

    def test_mixing_intensity_range(self):
        """Verify mixing intensity is in valid range."""
        mixing = MixingEfficiencyModel()
        intensity = mixing.mixing_intensity()

        assert 0 <= intensity <= 1

    def test_integration_efficiency_range(self):
        """Verify integration efficiency is in valid range."""
        ws = WaterSystemSpecs()
        spray_sim = SprayPatternSimulation(ws)
        mixing = MixingEfficiencyModel()

        coverage = spray_sim.mixing_zone_coverage()
        res_time = mixing.residence_time()
        efficiency = mixing.water_integration_efficiency(coverage, res_time)

        assert 0 <= efficiency <= 1


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for the complete digital twin."""

    def test_full_simulation_runs(self):
        """Verify complete simulation runs without errors."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()

        for concrete_type in ConcreteType:
            sim = AugerFlowSimulation(auger, housing, motor, concrete_type)

            # All calculations should complete without error
            _ = sim.calculate_volumetric_flow()
            _ = sim.calculate_mass_flow()
            _ = sim.calculate_throughput_bags_per_hour()
            _ = sim.calculate_shear_rate()
            _ = sim.calculate_apparent_viscosity()
            _ = sim.calculate_required_torque()
            _ = sim.check_motor_adequacy()

    def test_thermal_integration(self):
        """Verify thermal simulation integrates with flow simulation."""
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()
        flow_sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)
        thermal_sim = ThermalSimulation(flow_sim)

        _ = thermal_sim.calculate_heat_generation()
        _ = thermal_sim.estimate_temperature_rise()

    def test_water_system_integration(self):
        """Verify water system integrates with mixing model."""
        ws = WaterSystemSpecs()
        spray_sim = SprayPatternSimulation(ws)
        controller = WaterCementController(ws)
        mixing = MixingEfficiencyModel()

        coverage = spray_sim.mixing_zone_coverage()
        res_time = mixing.residence_time()
        _ = mixing.water_integration_efficiency(coverage, res_time)


# =============================================================================
# ACCURACY SUMMARY TEST
# =============================================================================

class TestOverallAccuracy:
    """Test overall digital twin accuracy score."""

    def test_minimum_95_percent_accuracy(self):
        """
        Verify digital twin achieves minimum 95% accuracy
        across all measured parameters.
        """
        accuracy_scores = []

        # Dimensional accuracy
        auger = AugerSpecs()
        housing = HousingSpecs()
        motor = MotorSpecs()

        accuracy_scores.append(accuracy_score(auger.outer_diameter, REFERENCE_SPECS["auger_od_in"]))
        accuracy_scores.append(accuracy_score(housing.inner_diameter, REFERENCE_SPECS["housing_id_in"]))
        accuracy_scores.append(accuracy_score(housing.outer_diameter, REFERENCE_SPECS["housing_od_in"]))
        accuracy_scores.append(accuracy_score(motor.power_hp, REFERENCE_SPECS["motor_power_hp"]))
        accuracy_scores.append(accuracy_score(motor.power_watts, REFERENCE_SPECS["motor_power_w"]))
        accuracy_scores.append(accuracy_score(motor.rpm, REFERENCE_SPECS["motor_rpm"]))

        # Water system accuracy
        ws = WaterSystemSpecs()
        accuracy_scores.append(accuracy_score(ws.min_pressure_psi, REFERENCE_SPECS["min_water_pressure_psi"]))
        accuracy_scores.append(accuracy_score(ws.nozzle_count, REFERENCE_SPECS["nozzle_count"]))

        # Calculate overall accuracy
        overall_accuracy = np.mean(accuracy_scores)

        print(f"\n{'='*60}")
        print(f"DIGITAL TWIN ACCURACY REPORT")
        print(f"{'='*60}")
        print(f"Individual scores: {[f'{s:.1f}%' for s in accuracy_scores]}")
        print(f"Overall accuracy: {overall_accuracy:.1f}%")
        print(f"{'='*60}\n")

        assert overall_accuracy >= 95.0, \
            f"Overall accuracy {overall_accuracy:.1f}% below 95% threshold"


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
