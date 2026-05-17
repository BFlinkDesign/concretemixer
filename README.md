# MudMixer Reverse Engineering Project

## Overview

This project contains reverse-engineered documentation of the MudMixer portable continuous concrete/mortar mixer. The MudMixer is a patented continuous-feed mixing system that uses a shaftless helical auger to hydrate and mix bagged cementitious materials.

## Product Summary

| Attribute | Value |
|-----------|-------|
| **Manufacturer** | MudMixer, LLC (formerly Red Dog Mobile Shelters, LLC) |
| **Models** | MMXR-3221 (discontinued), MMXR-3225 (Evolution), **MudMixer Pro (NEW 2026)** |
| **Type** | Continuous-feed portable electric mixer |
| **Patents** | US 10,259,140 B1, US 11,285,639 B2, D943,639 |

### MudMixer Pro (Announced January 2026)

> **NEW**: Unveiled at World of Concrete 2026 (Jan 20-22, Las Vegas)

| Spec | MudMixer Pro | Evolution |
|------|--------------|-----------|
| Throughput | **3+ yd³/hour** | 1 yd³/hour |
| Motor | **1.5 HP** | 0.5 HP |
| Hopper | **250 lbs** | 120 lbs |
| Wheels | 4 all-terrain | 2 flat-free |
| Swivel | 360° | 330° |

## Key Features

- **Continuous Mixing**: Unlike batch mixers, material flows through continuously
- **Shaftless Helical Auger**: Variable-pitch design for optimal mixing and conveyance
- **Dual Spray Nozzles**: Water injection system with adjustable flow control
- **330° Swivel**: Precision placement capability
- **Portable Design**: Flat-free tires, lightweight frame (145 lbs)

## Design Requirements (Optimized Version)

| Requirement | Specification | Rationale |
|-------------|---------------|-----------|
| **Duty Cycle** | 12+ hours/day continuous | Jobsite commercial operation |
| **Primary Power** | 120V AC | Unlimited runtime, standard outlet |
| **Secondary Power** | DeWalt 20V/60V FlexVolt | Portable runs (1.5-3 hr) |
| **Finger Material** | Steel (not UHMW) | 12-hr thermal exceeds UHMW limits |
| **Thermal Management** | Active cooling required | Electronics need ventilation |

## Project Status: PRODUCTION-READY TDP

**Technical Data Package (TDP) Level 3 Complete** per MIL-STD-31000

| Phase | Status | Documents |
|-------|--------|-----------|
| Design Documentation | ✅ Complete | 10 files |
| Manufacturing Documentation | ✅ Complete | 5 files |
| Quality Documentation | ✅ Complete | 8 files |
| CAD Models | ✅ Complete | 9 files |
| **Production Trial** | ⏳ Required | - |

---

## Documentation Structure

### Technical Data Package Summary
- [**TDP Summary**](./docs/TDP_SUMMARY.md) - Executive overview, readiness checklist

### Design Documentation (`docs/`)
- [Technical Specifications](./docs/SPECIFICATIONS.md) - Dimensions, power, capacity
- [Validated Specifications](./docs/VALIDATED_SPECIFICATIONS.md) - Confirmed specs with sources
- [Main Assemblies](./docs/ASSEMBLIES.md) - Frame, hopper, chute, drive system
- [Auger Design](./docs/AUGER_DESIGN.md) - Shaftless auger geometry
- [Water System](./docs/WATER_SYSTEM.md) - Spray nozzle and flow control
- [Power System](./docs/POWER_SYSTEM.md) - Dual power: 120V AC + DeWalt FlexVolt
- [Engineering Calculations](./docs/ENGINEERING.md) - Design calculations
- [Drawing Standards](./docs/DRAWING_STANDARDS.md) - ASME Y14.5 compliance

### APQP/PPAP Documentation (`docs/`)
- [Phase 1 Deliverables](./docs/PHASE1_DELIVERABLES.md) - Design/reliability/quality goals
- [DFMEA](./docs/DFMEA.md) - Design Failure Mode Analysis (32 failure modes)
- [PFMEA](./docs/PFMEA.md) - Process Failure Mode Analysis (47 failure modes)
- [Process Flow](./docs/PROCESS_FLOW.md) - 89 manufacturing operations
- [Control Plan](./docs/CONTROL_PLAN.md) - AIAG format, CC/SC characteristics
- [PPAP Package](./docs/PPAP_PACKAGE.md) - 18 elements checklist

### Manufacturing Documentation (`docs/`)
- [Production BOM](./docs/PRODUCTION_BOM.md) - 105 parts, sourcing, $1,821 material cost
- [Work Instructions](./docs/WORK_INSTRUCTIONS.md) - 10 detailed work instructions

### Quality Documentation (`docs/`)
- [Test Procedures](./docs/TEST_PROCEDURES.md) - 10 test procedures (TP-001 to TP-010)
- [MSA Plan](./docs/MSA_PLAN.md) - 10 Gage R&R studies
- [AS9102 FAI Forms](./docs/AS9102_FAI_FORMS.md) - 46 characteristics

### Analysis Documentation (`docs/`)
- [Gap Analysis](./docs/GAP_ANALYSIS.md) - TRL/MRL assessment, FMEA
- [Technology Selection](./docs/TECHNOLOGY_SELECTION.md) - Tool selection matrices
- [Professional Task List](./docs/PROFESSIONAL_TASK_LIST.md) - Industry workflow per MIL-HDBK-115C
- [Data Requirements](./docs/DATA_REQUIREMENTS.md) - Known vs unknown specs
- [Known Issues](./docs/KNOWN_ISSUES.md) - Field problems and workarounds

### Technical Drawings (`drawings/`)
- [Assembly Drawing](./drawings/ASSEMBLY_DRAWING.md) - Side/front/top views
- [Auger Drawing](./drawings/AUGER_DRAWING.md) - Shaftless auger geometry
- [Electrical Schematic](./drawings/ELECTRICAL_SCHEMATIC.md) - Drive system wiring

### CAD Models and Tools (`src/`)
- [parametric_auger.py](./src/parametric_auger.py) - Parametric auger with STEP export (CadQuery/build123d)
- [frame_model.py](./src/frame_model.py) - Parametric frame with STEP export
- [assembly_spec.json](./src/assembly_spec.json) - Complete assembly relationships
- [auger_spec.json](./src/auger_spec.json) - Auger dimensions JSON
- [frame_spec.json](./src/frame_spec.json) - Frame dimensions JSON
- [mudmixer_auger.scad](./src/mudmixer_auger.scad) - OpenSCAD auger model
- [mudmixer_frame.scad](./src/mudmixer_frame.scad) - OpenSCAD frame model
- [auger_optimizer.py](./src/auger_optimizer.py) - Generative design framework
- [requirements.txt](./src/requirements.txt) - Python dependencies

### 3D Visualization (`src/visualization/`)
- [index.html](./src/visualization/index.html) - WebGL visualization with Three.js
- [package.json](./src/visualization/package.json) - Node.js dependencies

## Operation Principle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DRY MIX ──▶ HOPPER ──▶ AUGER + WATER ──▶ CHUTE ──▶ OUTPUT │
│              (120 lbs)    (dual spray)     (16")            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

1. Dry bagged mix (concrete, mortar, stucco) is loaded into the hopper
2. Material flows by gravity into the shaftless auger
3. Water is injected via dual spray nozzles at adjustable rate
4. Auger rotates, mixing and conveying material through chute
5. Mixed material exits through 330° swivel chute for placement

## Performance

- **Throughput**: 45+ bags (80 lb) per hour
- **Output Rate**: ~1 cubic yard per hour
- **Mix Rate**: ~1 bag (60 lb) per minute

## Key Confirmed Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| Max Aggregate Size | **0.5 inch** | MudMixer Specs |
| Motor Coupling | **Left-Hand Acme Thread** | Patent 10,259,140 |
| Hopper P/D Ratio | 0.2 - 0.9 (preferred 0.5-0.8) | Patent Claims |
| Chute P/D Ratio | 0.6 - 1.0 | Patent Claims |
| Chute Length | 16 - 30 inches | Patent Claims |

## Critical Unknown Dimensions

> ⚠️ **The following must be measured before replication:**

| Parameter | Impact | Acquisition Method |
|-----------|--------|-------------------|
| Housing Internal Diameter | Clearance calculation, CFD | Bore gauge |
| Auger Outer Diameter | Clearance, flow rate | Caliper |
| Acme Thread Size | Motor coupling adapter | Thread gauge |
| Bearing Specifications | Load path analysis | Disassembly |

See [DATA_REQUIREMENTS.md](./docs/DATA_REQUIREMENTS.md) for complete analysis.

## Patents Referenced

| Patent | Title | Filed | Issued |
|--------|-------|-------|--------|
| US 10,259,140 B1 | Portable concrete mixer for hydrating and mixing concrete mix containing gravel aggregate in a continuous process | Oct 19, 2018 | Apr 16, 2019 |
| US 11,285,639 B2 | Portable mixer for hydrating and mixing cementitious mix in a continuous process | Mar 13, 2019 | Mar 29, 2022 |
| D943,639 | Design Patent (Mixer appearance) | - | Feb 15, 2022 |

## Sources

- [MudMixer Official Website](https://mudmixer.com/)
- [MudMixer Specifications](https://mudmixer.com/pages/specs)
- [US Patent 10,259,140](https://patents.justia.com/patent/10259140)
- [Freepatentsonline US 11,285,639](https://www.freepatentsonline.com/11285639.html)

## Disclaimer

This reverse engineering documentation is for educational and research purposes only. The MudMixer design is protected by the patents listed above. Any commercial use or manufacture must respect applicable intellectual property rights.
