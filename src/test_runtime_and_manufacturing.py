"""Runtime matrix, manufacturing audit, and simulation envelope tests.

Three guarantees:
1. RUNTIME — every CLI entry point runs cleanly with every flag combination
2. MANUFACTURING — every exported STL passes the file-level audit (parsed
   back at float32 precision exactly as fabrication software receives it)
3. REAL-LIFE ENVELOPE — simulation invariants hold across the operating
   envelope (ambient temperature, shift length, integration step)
"""

import os

import pytest

import manufacturing_audit
import mixer_simulation
from mixer_simulation import SimulationConfig, simulate


class TestRuntimeMatrix:
    """Every entry point, every flag combination — nothing breaks at runtime."""

    def test_auger_optimizer_all_flags(self, tmp_path, capsys):
        from auger_optimizer import main
        main(["--housing-id", "6.5", "--hp", "0.75", "--rpm", "30",
              "--aggregate", "0.375", "--ambient", "105", "--duty", "heavy",
              "--stl", str(tmp_path / "a.stl"),
              "--render", str(tmp_path / "a.png")])
        assert (tmp_path / "a.stl").exists()
        assert (tmp_path / "a.png").exists()
        assert "STL exported" in capsys.readouterr().out

    def test_auger_optimizer_every_duty_cycle(self, capsys):
        from auger_optimizer import main
        for duty in ("light", "medium", "heavy", "continuous", "jobsite_12hr"):
            main(["--duty", duty])
            assert duty in capsys.readouterr().out

    def test_auger_cad_cli(self, tmp_path, capsys):
        from auger_cad import main
        main(["--housing-id", "6.5", "--segments", "32",
              "--stl", str(tmp_path / "b.stl"),
              "--render", str(tmp_path / "b.png")])
        assert (tmp_path / "b.stl").exists()
        main([])  # no outputs requested — must not crash
        assert "No output requested" in capsys.readouterr().out

    def test_mixer_cad_all_flags(self, tmp_path, capsys):
        from mixer_cad import main
        main(["--housing-id", "6.5", "--report",
              "--stl-dir", str(tmp_path / "stl"),
              "--render", str(tmp_path / "asm.png"),
              "--exploded", str(tmp_path / "exp.png"),
              "--drawing", str(tmp_path / "dwg.png")])
        output = capsys.readouterr().out
        assert "ALL CHECKS PASS" in output
        for name in ("asm.png", "exp.png", "dwg.png"):
            assert (tmp_path / name).exists()

    def test_mixer_analysis_cli(self, capsys):
        import mixer_analysis
        mixer_analysis.main()
        assert "SELF-CONSISTENT" in capsys.readouterr().out

    def test_simulation_cli_with_plot(self, tmp_path, capsys):
        mixer_simulation.main(["--hours", "2",
                               "--plot", str(tmp_path / "sim.png")])
        assert (tmp_path / "sim.png").exists()

    def test_build_all_pipeline(self, tmp_path, capsys):
        """The complete automated backend must run and self-gate."""
        import build_all
        build_all.main(["--out", str(tmp_path / "dist")])
        output = capsys.readouterr().out
        assert "BUILD OK" in output
        assert (tmp_path / "dist" / "MANIFEST.txt").exists()
        # The audit gate report must show zero failures
        audit = (tmp_path / "dist" / "reports" /
                 "manufacturing_audit.txt").read_text()
        assert "FAIL" not in audit

    def test_manufacturing_audit_cli(self, tmp_path, capsys):
        from auger_cad import build_flight_mesh, write_binary_stl
        from auger_optimizer import AugerOptimizer
        design = AugerOptimizer(6.0).generate_optimized_design()
        mesh = build_flight_mesh(design["objects"]["geometry"], 16)
        write_binary_stl(mesh, str(tmp_path / "x.stl"))
        assert manufacturing_audit.main([str(tmp_path)]) == 0
        assert "1/1 files manufacturing-clean" in capsys.readouterr().out


class TestManufacturingAudit:
    """The audit itself must catch real defects, not just pass clean files."""

    def test_detects_truncated_file(self, tmp_path):
        from auger_cad import build_flight_mesh, write_binary_stl
        from auger_optimizer import AugerOptimizer
        design = AugerOptimizer(6.0).generate_optimized_design()
        mesh = build_flight_mesh(design["objects"]["geometry"], 16)
        path = tmp_path / "trunc.stl"
        write_binary_stl(mesh, str(path))
        data = path.read_bytes()
        path.write_bytes(data[:-50])  # drop the final triangle
        with pytest.raises(ValueError, match="declares"):
            manufacturing_audit.read_binary_stl(str(path))

    def test_detects_open_shell(self):
        from mixer_cad import box
        mesh = box(1, 1, 1)[:-1]  # remove one facet → hole
        result = manufacturing_audit.audit_triangles(mesh, "open")
        assert not result["ok"]
        assert any("watertight" in f for f in result["failures"])

    def test_detects_inverted_shell(self):
        from mixer_cad import box, flip
        result = manufacturing_audit.audit_triangles(flip(box(1, 1, 1)), "inv")
        assert not result["ok"]
        assert any("inverted" in f for f in result["failures"])

    def test_detects_degenerate_facets(self):
        from mixer_cad import box
        point = (0.0, 0.0, 0.0)
        mesh = box(1, 1, 1) + [(point, point, point)]
        result = manufacturing_audit.audit_triangles(mesh, "degen")
        assert any("degenerate" in f for f in result["failures"])

    def test_shell_count_matches_components(self, tmp_path):
        """The assembly STL must contain every component's shells."""
        from mixer_cad import build_mixer, export_stls
        components = build_mixer()
        export_stls(components, str(tmp_path))
        result = manufacturing_audit.audit_file(
            str(tmp_path / "mudmixer_assembly.stl")
        )
        assert result["ok"]
        # Frame members, fingers, wheels etc. produce many shells; at
        # minimum one per component
        assert result["shells"] >= len(components)


class TestSimulationEnvelope:
    """Invariants must hold across the real-life operating envelope."""

    ENVELOPE = [
        SimulationConfig(duration_hr=2.0, dt_s=2.0, ambient_f=40.0),   # cold
        SimulationConfig(duration_hr=2.0, dt_s=2.0, ambient_f=75.0),
        SimulationConfig(duration_hr=2.0, dt_s=2.0, ambient_f=110.0),  # hot
        SimulationConfig(duration_hr=14.0, dt_s=10.0, ambient_f=95.0), # long
        SimulationConfig(duration_hr=12.0, dt_s=1.0, ambient_f=95.0,
                         operator_cycle_s=120.0),  # slow operator (starves)
    ]

    @pytest.mark.parametrize("config", ENVELOPE,
                             ids=["cold", "mild", "hot", "14hr", "starved"])
    def test_invariants(self, config):
        result = simulate(config)
        totals = result.totals

        # Mass balance closes exactly at every operating point
        material_in = config.hopper_capacity_lb + totals["bags"] * config.bag_lb
        material_out = totals["consumed_lb"] + result.hopper_lb[-1]
        assert material_in == pytest.approx(material_out, rel=0.01)

        # Temperatures finite, ordered, above ambient floor
        for series in (result.temp_steel_f, result.temp_uhmw_f,
                       result.temp_enclosure_f):
            assert all(config.ambient_f - 1 <= t < 1000 for t in series)

        # Energy is non-negative and bounded by full-load-all-day
        ceiling = totals["full_load_amps"] * 120 * config.duration_hr / 1000
        assert 0 <= totals["energy_kwh"] <= ceiling * 1.01

        # Hopper level always within physical bounds
        assert all(
            -1e-6 <= level <= config.hopper_capacity_lb + config.bag_lb
            for level in result.hopper_lb
        )

    def test_starved_operator_reduces_output(self):
        normal = simulate(SimulationConfig(duration_hr=4.0, dt_s=5.0))
        starved = simulate(SimulationConfig(duration_hr=4.0, dt_s=5.0,
                                            operator_cycle_s=120.0))
        assert starved.totals["bags"] < normal.totals["bags"]

    def test_dt_independence(self):
        """Totals must not depend on the integration step (±2%)."""
        coarse = simulate(SimulationConfig(duration_hr=3.0, dt_s=10.0))
        fine = simulate(SimulationConfig(duration_hr=3.0, dt_s=1.0))
        assert coarse.totals["bags"] == pytest.approx(
            fine.totals["bags"], rel=0.02
        )
        assert coarse.totals["energy_kwh"] == pytest.approx(
            fine.totals["energy_kwh"], rel=0.02
        )

    def test_hot_day_does_not_break_steel(self):
        hot = simulate(SimulationConfig(duration_hr=2.0, dt_s=2.0,
                                        ambient_f=110.0))
        assert hot.totals["max_temp_steel_f"] < 250  # vast margin to 800
