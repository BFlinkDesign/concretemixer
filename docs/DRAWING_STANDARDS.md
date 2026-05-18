# Engineering Drawing Standards - MudMixer Project

> **Applicable Standards**: ASME Y14.5-2018, ASME Y14.100, AWS A2.4  
> **Document Control**: REV A  
> **Date**: 2026-05-17

---

## 1. DRAWING FORMAT

### 1.1 Sheet Sizes (ANSI)
| Size | Dimensions | Use |
|------|------------|-----|
| A (8.5×11) | Detail drawings, single parts |
| B (11×17) | Subassembly drawings |
| C (17×22) | Major assembly drawings |
| D (22×34) | Full machine assembly |

### 1.2 Title Block Required Fields
| Field | Content |
|-------|---------|
| Drawing Number | MM-XXXX-REV |
| Title | Descriptive part/assembly name |
| Material | Per ASTM/SAE specification |
| Scale | As noted (1:1 preferred for details) |
| Weight | Calculated or measured |
| Drawn By | Initials + date |
| Checked By | Initials + date |
| Approved By | Initials + date |
| Sheet | X of Y |

### 1.3 Drawing Number Convention
```
MM - XXXX - YY - REV
│    │      │    │
│    │      │    └── Revision letter (A, B, C...)
│    │      └─────── Variant/option (01, 02, etc.)
│    └────────────── Sequential number (0001-9999)
└──────────────────── Project prefix (MudMixer)
```

**Number Blocks:**
| Range | Category |
|-------|----------|
| 0001-0999 | Assembly drawings |
| 1000-1999 | Frame components |
| 2000-2999 | Hopper components |
| 3000-3999 | Auger components |
| 4000-4999 | Motor/drive components |
| 5000-5999 | Water system components |
| 6000-6999 | Electrical components |
| 7000-7999 | Chute components |
| 8000-8999 | Hardware/fasteners |
| 9000-9999 | Tooling/fixtures |

---

## 2. DIMENSIONING STANDARDS (ASME Y14.5-2018)

### 2.1 General Tolerances
| Feature Type | Tolerance |
|--------------|-----------|
| Linear dimensions ≤ 6" | ±0.010" |
| Linear dimensions > 6" | ±0.015" |
| Angular dimensions | ±0.5° |
| Bend radii | ±0.030" |
| Hole locations | ±0.010" |

### 2.2 Precision Tolerances (When Specified)
| Class | Tolerance | Application |
|-------|-----------|-------------|
| Fine | ±0.005" | Bearing fits, shaft diameters |
| Medium | ±0.010" | Mating parts, assembly interfaces |
| Coarse | ±0.030" | Non-critical features |

### 2.3 GD&T Feature Control Frames
Required for all critical features:

| Symbol | Tolerance | Application |
|--------|-----------|-------------|
| ⌖ Position | 0.010" DIA | Hole patterns, mounting features |
| ⊥ Perpendicularity | 0.005" | Shaft to bearing face |
| ∥ Parallelism | 0.005" | Mating surfaces |
| ○ Circularity | 0.003" | Auger OD, shaft diameters |
| ⌓ Cylindricity | 0.005" | Bearing journals |
| ↗ Runout | 0.005" TIR | Rotating components |
| ⊕ Concentricity | 0.005" DIA | Auger to shaft |

### 2.4 Datum Structure
| Datum | Feature | Use |
|-------|---------|-----|
| A | Motor mounting face | Primary reference |
| B | Auger centerline | Rotational axis |
| C | Frame base plane | Vertical reference |

---

## 3. MATERIAL SPECIFICATIONS

### 3.1 Steel Specifications
| Application | Specification | Grade |
|-------------|---------------|-------|
| Frame tubing | ASTM A513 | 1020 |
| Sheet metal (body) | ASTM A1008 | CS Type B |
| Auger flight | ASTM A36 | - |
| Shaft | ASTM A108 | 1045 |

### 3.2 Material Callout Format
```
MATERIAL: ASTM A1008 CS TYPE B
         14 GA (0.0747")
         HOT DIP GALVANIZED PER ASTM A653 G90
```

### 3.3 Hardness Requirements (When Specified)
| Component | Hardness | Test Method |
|-----------|----------|-------------|
| Auger shaft | 28-32 HRC | ASTM E18 |
| Fingers | 45-50 HRC | ASTM E18 |
| Wear surfaces | 58-62 HRC | ASTM E18 |

---

## 4. WELD SPECIFICATIONS (AWS A2.4)

### 4.1 Weld Symbol Requirements
All welds shall include:
- Weld type (fillet, groove, etc.)
- Size (leg dimension for fillets)
- Length and pitch (if intermittent)
- Process (GMAW, GTAW, etc.)
- Weld all around symbol where applicable

### 4.2 Standard Weld Sizes
| Material Thickness | Minimum Fillet |
|-------------------|----------------|
| 14 ga (0.075") | 1/8" |
| 12 ga (0.105") | 1/8" |
| 11 ga (0.120") | 5/32" |
| 3/16" | 3/16" |
| 1/4" | 1/4" |

### 4.3 Weld Process Specifications
| Process | Wire | Gas | Application |
|---------|------|-----|-------------|
| GMAW | ER70S-6, 0.030" | 75% Ar / 25% CO₂ | Sheet metal, tubing |
| GTAW | ER70S-2 | 100% Ar | Critical joints |

### 4.4 Weld Quality Requirements
Per AWS D1.3 (Sheet Steel):
- No cracks, incomplete fusion, or overlap
- Undercut ≤ 1/32" depth
- Porosity ≤ 3/32" diameter, ≤ 3 per inch
- Visual inspection 100%
- Dimensional inspection per Control Plan

---

## 5. SURFACE FINISH

### 5.1 Standard Finishes
| Ra (μin) | Application |
|----------|-------------|
| 250 | As-machined, non-critical |
| 125 | Mating surfaces |
| 63 | Bearing surfaces |
| 32 | Sealing surfaces |

### 5.2 Coating Specifications
| Finish | Specification | Application |
|--------|---------------|-------------|
| Powder coat | Per MIL-PRF-32348 | Frame, external surfaces |
| Zinc plate | ASTM B633, SC2 | Hardware |
| Hot dip galvanize | ASTM A653, G90 | Sheet metal |
| None (bare) | - | Internal auger surfaces |

---

## 6. SPECIAL CHARACTERISTICS

### 6.1 Classification Symbols
| Symbol | Classification | Definition |
|--------|---------------|------------|
| ◇ (CC) | Critical Characteristic | Affects safety or regulatory compliance |
| ◆ (SC) | Significant Characteristic | Affects fit, function, or durability |

### 6.2 Critical Characteristics (CC)
| Feature | Drawing | Rationale |
|---------|---------|-----------|
| Motor mounting bolt pattern | MM-4001 | Safety - prevents detachment |
| Auger-to-shaft coupling | MM-3001 | Safety - prevents separation |
| E-stop wiring | MM-6001 | Safety - emergency function |
| Guard mounting | MM-1005 | Safety - OSHA compliance |

### 6.3 Significant Characteristics (SC)
| Feature | Drawing | Rationale |
|---------|---------|-----------|
| Auger pitch | MM-3001 | Function - throughput |
| Auger OD | MM-3001 | Function - clearance |
| Water nozzle position | MM-5001 | Function - mixing quality |
| Hopper angle | MM-2001 | Function - material flow |

---

## 7. REVISION CONTROL

### 7.1 Revision Levels
| Level | Description |
|-------|-------------|
| - (dash) | Preliminary/development |
| A | First release |
| B, C, D... | Subsequent revisions |
| NC | Non-conformance revision |

### 7.2 Revision Block Format
| Rev | Description | Date | By |
|-----|-------------|------|-----|
| A | Initial release | | |
| B | Updated per ECN-001 | | |

### 7.3 Engineering Change Notice (ECN) Required For:
- Any dimensional change
- Material change
- Process change affecting form/fit/function
- Tolerance change
- Addition/removal of features

---

## 8. DRAWING CHECKLIST

### 8.1 Before Release
| Check | Item |
|-------|------|
| □ | All dimensions complete |
| □ | All tolerances specified or default noted |
| □ | Material specification complete |
| □ | Surface finish specified |
| □ | All welds specified with symbols |
| □ | GD&T applied to critical features |
| □ | Special characteristics identified (CC, SC) |
| □ | Title block complete |
| □ | BOM matches assembly (if applicable) |
| □ | Drawing number follows convention |
| □ | Scale appropriate and noted |
| □ | Section views labeled correctly |
| □ | Notes block complete |

### 8.2 Standard Notes Block
```
NOTES:
1. INTERPRET DRAWING PER ASME Y14.5-2018
2. REMOVE ALL BURRS AND SHARP EDGES
3. DIMENSIONS IN INCHES UNLESS NOTED
4. TOLERANCES UNLESS NOTED:
   .XX = ±0.01
   .XXX = ±0.005
   ANGULAR = ±0.5°
5. WELD PER AWS D1.3
6. SURFACE FINISH 125 μin UNLESS NOTED
7. DO NOT SCALE DRAWING
```

---

## 9. DRAWING LIST

### 9.1 Assembly Drawings
| Drawing No. | Title | Sheet Size |
|-------------|-------|------------|
| MM-0001-A | Complete Machine Assembly | D |
| MM-0010-A | Frame Assembly | C |
| MM-0020-A | Hopper Assembly | B |
| MM-0030-A | Auger Assembly | B |
| MM-0040-A | Motor/Drive Assembly | B |
| MM-0050-A | Water System Assembly | B |
| MM-0060-A | Electrical Assembly | B |
| MM-0070-A | Chute Assembly | B |

### 9.2 Detail Drawings (Partial List)
| Drawing No. | Title | Sheet Size |
|-------------|-------|------------|
| MM-1001-A | Frame - Main Tube | A |
| MM-1002-A | Frame - Cross Member | A |
| MM-1003-A | Handle Assembly | A |
| MM-2001-A | Hopper - Body | B |
| MM-2002-A | Hopper - Grate | A |
| MM-3001-A | Auger - Shaftless Helix | B |
| MM-3002-A | Auger - Motor Coupling | A |
| MM-3003-A | Auger - Finger Detail | A |
| MM-4001-A | Motor Mount Bracket | A |
| MM-5001-A | Water Manifold | A |
| MM-7001-A | Chute - Tube | A |
| MM-7002-A | Chute - Swivel Bracket | A |

---

## 10. APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Design Engineer | | | |
| Quality Engineer | | | |
| Manufacturing Engineer | | | |
| Program Manager | | | |
