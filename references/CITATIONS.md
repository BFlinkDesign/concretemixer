# Engineering Citations Database

> **Purpose**: Single source of truth for all engineering references  
> **Status**: ACTIVE - Updated as research completes

---

## Standards Organizations

| Ref ID | Standard | Title | Used For |
|--------|----------|-------|----------|
| ASTM-A513 | ASTM A513 | Electric-Resistance-Welded Carbon Steel Tubing | Frame material |
| ASTM-A36 | ASTM A36 | Carbon Structural Steel | Auger material |
| ASTM-A1008 | ASTM A1008 | Cold-Rolled Steel Sheet | Sheet metal body |
| AWS-D1.1 | AWS D1.1 | Structural Welding Code - Steel | Weld sizing |
| AWS-D1.3 | AWS D1.3 | Sheet Steel Welding Code | Thin material welds |
| AISC-15 | AISC Manual 15th Ed | Steel Construction Manual | Section properties |

---

## Engineering Textbooks

| Ref ID | Author | Title | Edition | Used For |
|--------|--------|-------|---------|----------|
| ROARK | Young, Budynas | Roark's Formulas for Stress and Strain | 8th | Beam formulas |
| SHIGLEY | Budynas, Nisbett | Shigley's Mechanical Engineering Design | 11th | Safety factors |
| CEMA | CEMA | Screw Conveyor Engineering Manual | 2019 | Auger design |
| KWS | KWS Mfg | Shaftless Screw Conveyor Design Guide | Current | Shaftless specific |

---

## Component Datasheets (To Be Added)

| Ref ID | Manufacturer | Part Number | Component | URL |
|--------|--------------|-------------|-----------|-----|
| | | | | |

---

## Validated Calculations

| Calc ID | Title | Status | Location |
|---------|-------|--------|----------|
| CALC-STRUCT-001 | Frame Structural Analysis | ✅ COMPLETE | /references/calculations/STRUCTURAL_ANALYSIS.md |
| CALC-AUGER-001 | Auger/Conveyor Design | ⏳ PENDING | |
| CALC-MOTOR-001 | Motor Selection | ⏳ PENDING | |
| CALC-ELEC-001 | Electrical Design | ⏳ PENDING | |
| CALC-HYDRO-001 | Water System | ⏳ PENDING | |

---

## Critical Finding Log

| Date | Finding | Impact | Resolution |
|------|---------|--------|------------|
| 2026-05-17 | 1" Sch 40 frame tube undersized (SF=1.24) | Safety | Upgrade to 1-1/4" Sch 40 |

---

## Files Pending Validation/Deletion

Files created without engineering validation - to be replaced:
- docs/PRODUCTION_BOM.md (needs real part numbers)
- docs/DFMEA.md (needs validated failure modes)
- docs/PFMEA.md (needs validated process)
- src/parametric_auger.py (needs validated dimensions)
- src/frame_model.py (needs validated dimensions)

*These will be updated or deleted as validated engineering completes.*
