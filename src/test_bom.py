"""Tests for the CAD-reconciled BOM and procurement audit."""

import pytest

import bom_generator


class TestProcurementAudit:
    @pytest.mark.parametrize("bore", [6.0, 6.5])
    def test_audit_passes_at_design_points(self, bore):
        failures = [c for c in bom_generator.procurement_audit(bore)
                    if c["status"] != "OK"]
        assert failures == []

    def test_legacy_bom_combination_is_flagged(self):
        """The original 5.5\" auger / 6\" chute pair must be identified
        as a jam hazard (DESIGN_INSIGHTS D14)."""
        audit = {c["name"]: c for c in bom_generator.procurement_audit(6.0)}
        assert "would jam" in audit["legacy_bom_auger_rejected"]["detail"]

    def test_fuse_sized_above_bus_current(self):
        audit = {c["name"]: c for c in bom_generator.procurement_audit(6.0)}
        assert audit["fuse_rating"]["status"] == "OK"
        assert "18" in audit["fuse_rating"]["detail"]


class TestQuantitiesFromCAD:
    def test_raw_stock_quantities_sane(self):
        materials = {m["item"]: m for m in bom_generator.cad_derived_materials()}
        sheet_ft2 = float(materials["Steel sheet, 14 ga"]["qty"].split()[0])
        pipe_ft = float(materials["Steel pipe, 1\" OD"]["qty"].split()[0])
        # One 4x8 sheet (32 ft²) must cover the sheet-metal demand
        assert 10 < sheet_ft2 < 32
        # Frame uses tens of feet of pipe, not hundreds
        assert 15 < pipe_ft < 35

    def test_auger_stock_scales_with_bore(self):
        small = bom_generator.cad_derived_materials(6.0)
        large = bom_generator.cad_derived_materials(6.5)

        def flight_weight(mats):
            return float(
                next(m for m in mats if "flight" in m["item"])["qty"].split()[0]
            )

        assert flight_weight(large) > flight_weight(small)


class TestOutputs:
    def test_cost_rollup(self):
        bom = bom_generator.full_bom(6.5)
        rollup = bom_generator.cost_rollup(bom)
        assert rollup["total"] == rollup["raw stock"] + rollup["purchased"]
        assert 800 < rollup["total"] < 1500

    def test_csv_and_markdown(self, tmp_path):
        csv_path = tmp_path / "bom.csv"
        md_path = tmp_path / "bom.md"
        bom_generator.write_csv(bom_generator.full_bom(6.5), str(csv_path))
        bom_generator.write_markdown(6.5, str(md_path))
        csv_text = csv_path.read_text()
        assert csv_text.startswith("category,item,qty,spec,source,est_cost")
        assert "CORRECTED" in csv_text
        md_text = md_path.read_text()
        assert "Procurement Audit" in md_text
        assert "| OK |" in md_text and "| FAIL |" not in md_text

    def test_cli(self, tmp_path, capsys):
        code = bom_generator.main(["--housing-id", "6.5",
                                   "--csv", str(tmp_path / "b.csv"),
                                   "--md", str(tmp_path / "b.md")])
        assert code == 0
        assert "ALL CHECKS PASS" in capsys.readouterr().out
