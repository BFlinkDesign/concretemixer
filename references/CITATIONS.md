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
| CEMA-350 | CEMA | ANSI/CEMA Standard No. 350 | 2021 (6th) | Screw conveyor design |
| KWS-CAP | KWS Mfg | Screw Conveyor Capacity Engineering Guide | Current | Capacity calculation |
| KWS-HP | KWS Mfg | Screw Conveyor Horsepower Engineering Guide | Current | Power calculation |
| KWS-TQ | KWS Mfg | Screw Conveyor Torque Engineering Guide | Current | Torque calculation |
| KWS-SL | KWS Mfg | Shaftless Screw Conveyor Engineering Guide | Current | Shaftless design |
| MARTIN | Martin Sprocket | Pocket Guide to Screw Conveyor | Current | Material factors |
| NEC-2023 | NFPA | National Electrical Code | 2023 | Electrical design |

---

## Electrical Standards

| Ref ID | Standard | Title | Used For |
|--------|----------|-------|----------|
| NEC-310.16 | NEC Table 310.16 | Conductor Ampacity | Wire sizing |
| NEC-430.32 | NEC 430.32 | Motor Overload Protection | Overload sizing |
| NEC-430.52 | NEC 430.52 | Motor Branch Circuit OCPD | Breaker sizing |
| NEC-250.122 | NEC Table 250.122 | EGC Sizing | Ground conductor |
| NEC-590.6 | NEC 590.6 | Temporary Installations | GFCI requirements |
| UL-943 | UL 943 | GFCI Devices | Class A trip level |
| UL-62 | UL 62 | Flexible Cords | SOOW rating |

---

## Motor/Gearmotor Specifications

| Ref ID | Manufacturer | Model | Source URL |
|--------|--------------|-------|------------|
| LEESON-107013 | Leeson/Regal | 107013.00 | globalindustrial.com |
| LEESON-107015 | Leeson/Regal | 107015.00 | industrialmotors.com |
| DAYTON-1LPU5 | Dayton | 1LPU5 | zoro.com |
| DAYTON-6Z414 | Dayton | 6Z414 | grainger.com |
| BODINE-HG | Bodine Electric | HG/CG Series | bodine-electric.com |

---

## Electrical Component Datasheets

| Ref ID | Manufacturer | Part Number | Component |
|--------|--------------|-------------|-----------|
| HUBBELL-GFCI | Hubbell | GFPST6C15M | GFCI Portable Cord |
| LEVITON-GFCI | Leviton | GFWT1-W | GFCI Receptacle |
| CARLING-SW | Carling Technologies | 2GO53-73/TABS | DPDT Toggle Switch |
| HUBBELL-PLUG | Hubbell | HBL5266C | NEMA 5-15P Plug |
| KEMET-CAP | KEMET | R46KN3100JCK1M | X2 Capacitor |
| LITTELFUSE-MOV | Littelfuse | V150LA10AP | MOV Surge Suppressor |

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
| CALC-AUGER-001 | Auger/Conveyor Design (CEMA) | ✅ COMPLETE | /references/calculations/AUGER_CEMA_CALCULATIONS.md |
| CALC-MOTOR-001 | Motor Selection | ✅ COMPLETE | /references/calculations/MOTOR_SELECTION.md |
| CALC-ELEC-001 | Electrical Design (NEC) | ✅ COMPLETE | /references/calculations/ELECTRICAL_DESIGN.md |
| CALC-HYDRO-001 | Water System | ⏳ PENDING | |

---

## Critical Finding Log

| Date | Finding | Impact | Resolution |
|------|---------|--------|------------|
| 2026-05-17 | 1" Sch 40 frame tube undersized (SF=1.24) | Safety | ✅ Upgraded to 1-1/4" Sch 40 (SF=2.19) |
| 2026-05-17 | CEMA auger calc: 25 RPM optimal | Performance | Validated vs patent specs |
| 2026-05-17 | Motor torque marginal at starting | Reliability | Recommend 375-500W motor for margin |
| 2026-05-17 | AR400 steel required for flight | Durability | Per CEMA abrasive material specs |
| 2026-05-17 | NEC electrical design validated | Compliance | 12 AWG SOOW, 15A GFCI per NEC 2023 |

---

## Validated CAD Models

| File | Status | Source Calculations |
|------|--------|---------------------|
| src/mudmixer_auger.step | ✅ VALIDATED | CALC-AUGER-001 (CEMA 350) |
| src/mudmixer_frame.step | ✅ VALIDATED | CALC-STRUCT-001 (ASTM/AISC) |
| src/parametric_auger.py | ✅ VALIDATED | Patent specs + CEMA |
| src/frame_model.py | ✅ VALIDATED | 1-1/4" Sch 40 per SF analysis |

---

## Files Pending Validation/Deletion

Files created without engineering validation - to be replaced:
- docs/PRODUCTION_BOM.md (needs real part numbers from validated motors/components)
- docs/DFMEA.md (needs validated failure modes from CEMA analysis)
- docs/PFMEA.md (needs validated process from actual fab sequence)

*BOM requires specific part numbers from motor selection (CALC-MOTOR-001)*
