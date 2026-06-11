"""Tests for the MudMixer auger design framework engineering calculations."""

import math

import pytest

from auger_optimizer import (
    AugerGeometry,
    AugerOptimizer,
    CFDParameters,
    DutyCycle,
    FingerConfig,
    FingerMaterial,
    OperatingConditions,
    PowerSystem,
    ThermalAnalyzer,
)


class TestOperatingConditions:
    def test_motor_torque_from_hp_and_rpm(self):
        # HP = T(ft-lb) × RPM / 5252  →  T = 0.5 × 5252 / 27
        conditions = OperatingConditions(motor_power_hp=0.5, motor_rpm=27.0)
        assert conditions.motor_torque_ft_lb == pytest.approx(97.26, abs=0.01)

    def test_torque_metric_conversion(self):
        conditions = OperatingConditions(motor_power_hp=0.5, motor_rpm=27.0)
        assert conditions.motor_torque_nm == pytest.approx(
            conditions.motor_torque_ft_lb * 1.3558
        )


class TestAugerGeometry:
    def _geometry(self, **overrides):
        params = dict(
            outer_diameter=4.5,
            inner_diameter=3.69,
            length_hopper=10.0,
            length_chute=14.0,
            pitch_hopper=2.925,   # P/D = 0.65
            pitch_chute=3.825,    # P/D = 0.85
        )
        params.update(overrides)
        return AugerGeometry(**params)

    def test_valid_geometry_passes_patent_checks(self):
        assert self._geometry().validate() == []

    def test_pd_ratios(self):
        geometry = self._geometry()
        assert geometry.pd_ratio_hopper == pytest.approx(0.65)
        assert geometry.pd_ratio_chute == pytest.approx(0.85)

    def test_hopper_pd_out_of_patent_range_flagged(self):
        issues = self._geometry(pitch_hopper=0.5).validate()  # P/D = 0.11
        assert any("Hopper P/D" in issue for issue in issues)

    def test_chute_pitch_must_exceed_hopper_pitch(self):
        issues = self._geometry(pitch_hopper=3.9, pitch_chute=3.0).validate()
        assert any("variable pitch" in issue for issue in issues)


class TestClearance:
    def test_adequate_clearance(self):
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_clearance(auger_od=4.5)
        assert result["clearance_per_side"] == pytest.approx(0.75)
        assert result["status"] == "OK"

    def test_insufficient_clearance_fails(self):
        # 0.4" per side < 1.2 × 0.5" aggregate
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_clearance(auger_od=5.2)
        assert result["status"] == "FAIL"
        assert "jamming" in result["warning"]


class TestFingerShear:
    def _fingers(self, material):
        return FingerConfig(material=material, diameter=0.375, length=2.0, count=8)

    def test_single_finger_jam_governs(self):
        """Worst case is one finger reacting full torque, not torque/count."""
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_finger_shear(self._fingers(FingerMaterial.STEEL_1045))
        assert result["jam_force_lbf"] == pytest.approx(
            result["force_per_finger_lbf"] * 8
        )
        assert result["jam_pressure_psi"] > result["pressure_psi"]

    def test_steel_survives_jam(self):
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_finger_shear(self._fingers(FingerMaterial.STEEL_1045))
        assert result["status"] == "OK"

    def test_uhmw_fails_jam_case(self):
        """UHMW passes the distributed-load check but fails a single-finger jam."""
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_finger_shear(self._fingers(FingerMaterial.UHMW_STANDARD))
        assert result["pressure_psi"] < result["design_strength_psi"]
        assert result["status"] == "FAIL"


class TestSkeletonSizing:
    def test_safety_factor_applied_once(self):
        """SF lives in the allowable stress; torque must not be scaled again."""
        optimizer = AugerOptimizer(housing_id=6.0)
        result = optimizer.calculate_skeleton_diameter()

        torque_in_lb = optimizer.conditions.motor_torque_ft_lb * 12
        allowable = 31000 / optimizer.safety_factor
        expected = ((16 * torque_in_lb) / (math.pi * allowable)) ** (1 / 3)

        assert result["min_diameter_in"] == pytest.approx(expected)
        assert result["recommended_diameter_in"] >= result["min_diameter_in"]


class TestThermalRise:
    def test_uses_material_properties(self):
        """Steel fingers have ~10× the thermal mass of UHMW; the adiabatic
        temperature rise must reflect the actual material, not assume UHMW."""
        optimizer = AugerOptimizer(housing_id=6.0)
        steel = FingerConfig(FingerMaterial.STEEL_1045, 0.375, 2.0, 8)
        uhmw = FingerConfig(FingerMaterial.UHMW_STANDARD, 0.375, 2.0, 8)

        steel_rise = optimizer.calculate_thermal_rise(steel)["estimated_temp_rise_f"]
        uhmw_rise = optimizer.calculate_thermal_rise(uhmw)["estimated_temp_rise_f"]

        # mass×cp ratio: (0.284×0.12) / (0.034×0.55) ≈ 1.82
        assert uhmw_rise / steel_rise == pytest.approx(
            (0.284 * 0.12) / (0.034 * 0.55), rel=0.01
        )


class TestPowerSystem:
    def test_single_battery_runtime(self):
        power = PowerSystem(motor_power_watts=373, efficiency=0.85)
        result = power.calculate_battery_runtime("DCB612", count=1)
        assert result["energy_wh"] == pytest.approx(54 * 12.0)
        assert result["runtime_hours"] == pytest.approx(648 / (373 / 0.85), rel=1e-3)

    def test_series_doubles_voltage_not_capacity(self):
        power = PowerSystem()
        result = power.calculate_battery_runtime("DCB612", count=2, series=True)
        assert result["voltage_nominal"] == 108
        assert result["capacity_ah"] == 12.0

    def test_unknown_battery_rejected(self):
        with pytest.raises(ValueError):
            PowerSystem().calculate_battery_runtime("DCB999")


class TestThermalAnalyzer:
    def test_steady_state_energy_balance(self):
        """At steady state, generated heat equals convective rejection."""
        analyzer = ThermalAnalyzer(motor_power_hp=0.5, friction_loss_pct=0.15)
        result = analyzer.calculate_steady_state_temp(
            material="STEEL_1045",
            component_mass_lb=0.5,
            surface_area_in2=10.0,
            runtime_hours=100.0,
        )
        rejection = result["cooling_rate_btu_hr_f"] * result["temp_rise_at_runtime_f"]
        assert rejection == pytest.approx(result["heat_generation_btu_hr"], rel=0.01)

    def test_12hr_duty_recommends_metal(self):
        analyzer = ThermalAnalyzer()
        rec = analyzer.recommend_finger_material(DutyCycle.JOBSITE_12HR)
        assert rec["recommended_material"] in ("STEEL_1045", "STAINLESS_304")
        assert rec["thermal_severity"] == "EXTREME"


class TestCFDParameters:
    def test_yield_stress_from_slump(self):
        assert CFDParameters(slump_inches=4.0).yield_stress_pa == pytest.approx(1800)

    def test_viscosity_decreases_with_water(self):
        wet = CFDParameters(water_cement_ratio=0.6).plastic_viscosity_pa_s
        dry = CFDParameters(water_cement_ratio=0.4).plastic_viscosity_pa_s
        assert wet < dry


class TestOptimizedDesign:
    def test_generated_design_satisfies_patents(self):
        design = AugerOptimizer(housing_id=6.0).generate_optimized_design()
        assert design["validation"] == []
        assert design["analysis"]["clearance"]["status"] == "OK"
        assert design["analysis"]["shear"]["status"] == "OK"

    def test_design_exposes_geometry_objects(self):
        design = AugerOptimizer(housing_id=6.0).generate_optimized_design()
        geometry = design["objects"]["geometry"]
        assert isinstance(geometry, AugerGeometry)
        assert geometry.outer_diameter == design["geometry"]["auger_od"]


class TestCLI:
    def test_main_runs_with_defaults(self, capsys):
        from auger_optimizer import main
        main([])
        output = capsys.readouterr().out
        assert "OPTIMIZED GEOMETRY" in output
        assert "jobsite_12hr" in output

    def test_main_accepts_custom_parameters(self, capsys):
        from auger_optimizer import main
        main(["--housing-id", "8.0", "--duty", "light", "--ambient", "70"])
        output = capsys.readouterr().out
        assert "8.0" in output
        assert "light" in output
