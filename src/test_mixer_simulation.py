"""Tests for the converged design point and 12-hour operational simulation."""

import pytest

import mixer_analysis
from mixer_simulation import (
    STEEL_MAX_CONTINUOUS_F,
    UHMW_DEFLECTION_F,
    UHMW_MAX_CONTINUOUS_F,
    SimulationConfig,
    simulate,
)


@pytest.fixture(scope="module")
def result():
    # 5 s steps keep the suite fast; dynamics are minute-scale
    return simulate(SimulationConfig(dt_s=5.0))


class TestConvergedDesign:
    def test_fixed_point_converges(self):
        converged = mixer_analysis.converged_design()
        assert converged["self_consistent"]
        assert converged["iterations"] <= 4

    def test_converged_bore_near_6_5(self):
        converged = mixer_analysis.converged_design()
        assert converged["converged_housing_id_in"] == pytest.approx(6.5, abs=0.15)

    def test_converged_design_satisfies_patents(self):
        converged = mixer_analysis.converged_design()
        assert converged["patent_validation_issues"] == []

    def test_converged_throughput_reproduces_claim(self):
        converged = mixer_analysis.converged_design()
        assert converged["predicted_bags_hr"] == pytest.approx(45.0, rel=0.05)


class TestMassConservation:
    def test_mass_balance_closes(self, result):
        """Initial charge + bags dumped = material mixed + hopper residue."""
        material_in = 120.0 + result.totals["bags"] * 80.0
        material_out = result.totals["consumed_lb"] + result.hopper_lb[-1]
        assert material_in == pytest.approx(material_out, rel=0.01)

    def test_water_proportional_to_bags(self, result):
        assert result.totals["water_gal"] == pytest.approx(
            result.totals["bags"] * 3.5 / 4
        )

    def test_volume_accounting(self, result):
        assert result.totals["volume_yd3"] == pytest.approx(
            result.totals["bags"] * 0.60 / 27
        )

    def test_dayrate_matches_duty_cycle_definition(self, result):
        """Independent cross-check: the simulated day lands near the 500
        bags/session the repo's JOBSITE_12HR duty cycle was defined with."""
        assert 470 <= result.totals["bags"] <= 560


class TestThermalOutcomes:
    def test_steel_fingers_survive(self, result):
        assert result.totals["max_temp_steel_f"] < STEEL_MAX_CONTINUOUS_F
        assert result.totals["steel_margin_f"] > 500

    def test_uhmw_exceeds_deflection_but_not_melt(self, result):
        assert result.totals["max_temp_uhmw_f"] > UHMW_DEFLECTION_F
        assert result.totals["max_temp_uhmw_f"] < UHMW_MAX_CONTINUOUS_F + 50

    def test_enclosure_needs_fan(self, result):
        """Quantifies the 'active cooling required' design requirement."""
        assert result.totals["max_temp_enclosure_f"] > 140.0
        assert result.totals["enclosure_with_fan_f"] < 140.0

    def test_lunch_break_thermal_recovery(self, result):
        """Temperatures must dip during the hour-6 break."""
        in_break = [
            temp for t, temp in zip(result.time_hr, result.temp_steel_f)
            if 6.3 < t < 6.5
        ]
        running = [
            temp for t, temp in zip(result.time_hr, result.temp_steel_f)
            if 5.0 < t < 6.0
        ]
        assert min(in_break) < min(running) - 10


class TestElectricalOutcomes:
    def test_full_load_current_exceeds_published(self, result):
        assert result.totals["full_load_amps"] > 2.6  # D2

    def test_energy_integral(self, result):
        """kWh must equal full-load power times running hours (within the
        lunch break and feed-gap tolerance)."""
        running_hr = 12.0 - 0.5
        expected = result.totals["full_load_amps"] * 120 * running_hr / 1000
        assert result.totals["energy_kwh"] == pytest.approx(expected, rel=0.05)

    def test_current_drops_during_break(self, result):
        break_amps = [
            a for t, a in zip(result.time_hr, result.amps) if 6.1 < t < 6.4
        ]
        assert max(break_amps) == 0.0


class TestDrawingSheet:
    def test_drawing_sheet_renders(self, tmp_path):
        from mixer_cad import build_mixer, render_drawing_sheet
        path = tmp_path / "sheet.png"
        render_drawing_sheet(build_mixer(), str(path))
        assert path.exists() and path.stat().st_size > 50_000


class TestSimulationCLI:
    def test_main_prints_summary(self, capsys):
        from mixer_simulation import main
        main(["--hours", "1"])
        output = capsys.readouterr().out
        assert "JOBSITE SIMULATION" in output
        assert "Bags mixed" in output
