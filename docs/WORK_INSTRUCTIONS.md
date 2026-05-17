# Work Instructions - MudMixer Production

> **Document Control**: REV A  
> **Date**: 2026-05-17  
> **Standard**: ISO 9001:2015 §7.5.1

---

## WI-001: FRAME TUBE CUTTING

### 1.1 Purpose
Cut 1" steel tubing to specified lengths for frame assembly.

### 1.2 Required Materials
| Item | Specification | Qty |
|------|---------------|-----|
| Steel tubing | 1" Sch 40, ASTM A513 | Per BOM |
| Cutting fluid | Water-soluble | As needed |

### 1.3 Required Equipment
| Equipment | Specification |
|-----------|---------------|
| Cold saw | 14" blade, carbide tip |
| Tape measure | Calibrated ±1/16" |
| Marker | Industrial |
| Deburring tool | Handheld |

### 1.4 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Verify material against BOM | ASTM A513 cert |
| 2 | Measure and mark cut length | ±1/16" |
| 3 | Secure tube in saw fixture | Tube cannot rotate |
| 4 | Apply cutting fluid | Continuous flow |
| 5 | Cut at marked location | Blade speed per chart |
| 6 | Deburr both ends | Remove all burrs |
| 7 | Verify length | Per drawing ±1/16" |
| 8 | Mark part number on tube | Permanent marker |

### 1.5 Quality Checks
| Check | Frequency | Accept Criteria |
|-------|-----------|-----------------|
| Length | 100% | ±1/16" |
| Squareness | 100% | ≤1/32" deviation |
| Burr removal | 100% | No sharp edges |

---

## WI-002: SHEET METAL LASER CUTTING

### 2.1 Purpose
Laser cut 14 ga sheet metal parts per DXF files.

### 2.2 Required Materials
| Item | Specification | Qty |
|------|---------------|-----|
| Sheet steel | 14 ga ASTM A1008 | Per nest |
| Lens cleaner | Laser grade | As needed |

### 2.3 Required Equipment
| Equipment | Specification |
|-----------|---------------|
| Fiber laser | 2kW minimum |
| CAM software | Current version |
| Calipers | 0.001" resolution |

### 2.4 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Load DXF file to CAM | Correct revision |
| 2 | Verify material thickness | 14 ga (0.0747") |
| 3 | Set cutting parameters | Per material chart |
| 4 | Load sheet to bed | Flat, no warping |
| 5 | Set origin | Reference corner |
| 6 | Run cutting program | Monitor for pierce issues |
| 7 | Remove parts from skeleton | Avoid scratching |
| 8 | Deburr all edges | Remove dross |
| 9 | Verify critical dimensions | Per drawing |
| 10 | Label parts | Part number + date |

### 2.5 Cutting Parameters (14 ga Mild Steel)
| Parameter | Value |
|-----------|-------|
| Power | 1500W |
| Speed | 200 ipm |
| Assist gas | Nitrogen, 150 PSI |
| Focus | -1.0mm |
| Pierce delay | 0.3 sec |

### 2.6 Quality Checks
| Check | Frequency | Accept Criteria |
|-------|-----------|-----------------|
| Dimensions | First piece + 10% | Per drawing |
| Edge quality | 100% | No excessive dross |
| Flatness | 100% | ≤0.030"/ft |

---

## WI-003: BRAKE FORMING

### 3.1 Purpose
Form sheet metal parts to specified angles.

### 3.2 Required Equipment
| Equipment | Specification |
|-----------|---------------|
| Press brake | 60 ton minimum |
| V-die | Per material thickness |
| Back gauge | Digital readout |
| Angle gauge | ±0.5° accuracy |

### 3.3 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Select die per thickness | V = 8× material |
| 2 | Set back gauge | Per drawing |
| 3 | Verify bend sequence | Inside to outside |
| 4 | Position part against gauge | Firm contact |
| 5 | Form bend | Controlled stroke |
| 6 | Measure angle | ±1° tolerance |
| 7 | Adjust tonnage if needed | Spring-back compensation |
| 8 | Complete all bends | Per sequence |
| 9 | Verify final dimensions | Per drawing |

### 3.4 Bend Allowance (14 ga)
| Angle | Inside Radius | K-Factor |
|-------|---------------|----------|
| 90° | 0.075" | 0.33 |
| 45° | 0.075" | 0.33 |
| 135° | 0.075" | 0.33 |

### 3.5 Quality Checks
| Check | Frequency | Accept Criteria |
|-------|-----------|-----------------|
| Angle | 100% | ±1° |
| Bend location | 100% | ±0.030" |
| No cracking | 100% | Visual, no cracks |

---

## WI-004: FRAME WELDING

### 4.1 Purpose
Weld frame tube assembly per drawing.

### 4.2 Required Materials
| Item | Specification | Qty |
|------|---------------|-----|
| Welding wire | ER70S-6, 0.030" | As needed |
| Shielding gas | 75% Ar / 25% CO₂ | As needed |
| Anti-spatter | Spray | As needed |

### 4.3 Required Equipment
| Equipment | Specification |
|-----------|---------------|
| MIG welder | 200A minimum |
| Welding fixture | Per assembly |
| Fillet gauge | 1/8" - 1/2" |
| Wire brush | Stainless steel |
| Angle grinder | 4.5" |

### 4.4 Welder Qualification
- Certified to AWS D1.3
- Current certification on file

### 4.5 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Verify parts against BOM | All parts present |
| 2 | Clean joint areas | Wire brush, no oil |
| 3 | Load parts in fixture | Tight fit-up |
| 4 | Tack weld at corners | 1/2" tacks |
| 5 | Verify alignment | Per fixture |
| 6 | Complete fillet welds | Per drawing symbol |
| 7 | Clean spatter | Wire brush |
| 8 | Inspect welds | Per WI-010 |
| 9 | Remove from fixture | Careful handling |
| 10 | Mark weld date/welder | Per traceability |

### 4.6 Welding Parameters
| Parameter | Value |
|-----------|-------|
| Wire feed speed | 280-320 ipm |
| Voltage | 19-21V |
| Travel speed | 12-18 ipm |
| Stick-out | 3/8" - 1/2" |
| Gas flow | 30-35 CFH |

### 4.7 Quality Checks
| Check | Frequency | Accept Criteria |
|-------|-----------|-----------------|
| Fillet size | 100% | Per drawing ±1/32" |
| Visual inspection | 100% | Per AWS D1.3 |
| Overall dimensions | 100% | Per drawing |

---

## WI-005: AUGER ASSEMBLY

### 5.1 Purpose
Assemble shaftless auger with fingers and coupling.

### 5.2 Required Materials
| Item | Specification | Qty |
|------|---------------|-----|
| Auger helix | MM-3001 | 1 |
| Fingers | MM-3003 | 4 |
| Coupling | MM-3002 | 1 |
| Thread locker | Loctite 242 | As needed |

### 5.3 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Inspect auger helix | Per TP-002 |
| 2 | Position fingers at marked locations | Per drawing |
| 3 | Weld fingers | Per WI-004 |
| 4 | Clean coupling threads | Solvent wipe |
| 5 | Apply thread locker | Light coat |
| 6 | Thread coupling onto auger | Hand tight + wrench |
| 7 | Torque coupling | 35 ft-lb |
| 8 | Verify runout | ≤0.030" TIR |
| 9 | Apply witness mark | Paint pen |

### 5.4 Critical Dimensions
| Feature | Specification | Check Method |
|---------|---------------|--------------|
| Overall length | 36.00" ±0.125" | Tape measure |
| Finger position | Per drawing ±0.25" | Tape measure |
| Coupling engagement | ≥0.75" | Visual |
| Runout | ≤0.030" TIR | Dial indicator |

---

## WI-006: MOTOR INSTALLATION

### 6.1 Purpose
Install motor assembly to frame.

### 6.2 Required Materials
| Item | Specification | Qty |
|------|---------------|-----|
| Motor assembly | MMXR-P209 | 1 |
| Mounting bolts | 5/16-18 × 1", Gr 8 | 4 |
| Lock washers | 5/16" split | 4 |
| Flat washers | 5/16" SAE | 4 |

### 6.3 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Verify motor orientation | Shaft toward auger |
| 2 | Position motor on bracket | Align bolt holes |
| 3 | Install bolts hand tight | All 4 bolts |
| 4 | Align motor shaft to auger axis | ±0.010" |
| 5 | Torque bolts in cross pattern | 25 ft-lb |
| 6 | Verify alignment | No binding |
| 7 | Connect auger coupling | Thread onto shaft |
| 8 | Torque coupling | 35 ft-lb |
| 9 | Install coupling guard | Secure with screws |

### 6.4 Critical Checks
| Check | Specification |
|-------|---------------|
| Bolt torque | 25 ft-lb ±10% |
| Shaft alignment | ≤0.010" TIR |
| Coupling secure | Witness mark aligned |

---

## WI-007: WATER SYSTEM ASSEMBLY

### 7.1 Purpose
Assemble and install water system components.

### 7.2 Required Materials
| Item | Part Number | Qty |
|------|-------------|-----|
| Solenoid valve | MMXR-P114 | 1 |
| Flow control | MMXR-P118 | 1 |
| Tubing 34.25" | MMXR-P108 | 1 |
| Nozzle adapter | MMXR-P122 | 2 |
| Teflon tape | 1/2" width | As needed |

### 7.3 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Inspect all components | No damage |
| 2 | Apply Teflon tape to threads | 3 wraps clockwise |
| 3 | Install inlet fitting | Hand tight + 1 turn |
| 4 | Mount solenoid valve | Orientation per drawing |
| 5 | Connect flow control | After solenoid |
| 6 | Route tubing | No kinks |
| 7 | Connect nozzle adapters | Hand tight + 1/4 turn |
| 8 | Position nozzles | Spray toward auger |
| 9 | Perform leak test | Per TP-005 |
| 10 | Document test results | Test report |

### 7.4 Quality Checks
| Check | Specification |
|-------|---------------|
| Leak test | No leaks at 60 PSI |
| Flow test | Per TP-005 |
| Nozzle spray pattern | Both nozzles active |

---

## WI-008: ELECTRICAL WIRING

### 8.1 Purpose
Install and connect electrical components.

### 8.2 Required Materials
| Item | Part Number | Qty |
|------|-------------|-----|
| Power cord | MMXR-P201 | 1 |
| Switch | MMXR-P203 | 1 |
| Wire terminals | Ring, 14 AWG | As needed |
| Wire ties | 6" nylon | As needed |
| Heat shrink | 1/4" | As needed |

### 8.3 Procedure
| Step | Action | Critical Parameter |
|------|--------|-------------------|
| 1 | Mount switch in panel | Secure mounting |
| 2 | Route power cord | Away from moving parts |
| 3 | Strip wire ends | 1/4" exposed |
| 4 | Crimp terminals | Full compression |
| 5 | Connect per schematic | L, N, G correct |
| 6 | Apply heat shrink | Cover all connections |
| 7 | Connect solenoid leads | Per schematic |
| 8 | Secure wiring | Wire ties every 6" |
| 9 | Perform electrical test | Per TP-006 |

### 8.4 Wire Color Code
| Color | Function |
|-------|----------|
| Black | Line (hot) |
| White | Neutral |
| Green | Ground |
| Red | Switched hot |
| Blue | Solenoid |

### 8.5 Critical Checks
| Check | Specification |
|-------|---------------|
| Ground continuity | ≤0.1Ω |
| Insulation resistance | ≥2 MΩ |
| GFCI function | Trips ≤6 mA |

---

## WI-009: FINAL ASSEMBLY

### 9.1 Purpose
Complete final assembly and prepare for testing.

### 9.2 Assembly Sequence
| Step | Operation | Reference |
|------|-----------|-----------|
| 1 | Install wheels to frame | MM-0010 |
| 2 | Attach hopper assembly | MM-0020 |
| 3 | Install auger | WI-005 |
| 4 | Mount motor | WI-006 |
| 5 | Install water system | WI-007 |
| 6 | Complete electrical | WI-008 |
| 7 | Install chute assembly | MM-0070 |
| 8 | Install guards | All guards |
| 9 | Apply labels | Safety, rating, serial |
| 10 | Final inspection | TP-007 |

### 9.3 Serial Number Application
Format: `MM-YYWW-NNNN`
- YY = Year (26)
- WW = Week (01-52)
- NNNN = Sequential (0001-9999)

### 9.4 Required Labels
| Label | Location |
|-------|----------|
| Rating plate | Motor cover |
| Safety warnings | Hopper, guards |
| Serial number | Frame |
| Operating instructions | Handle |

---

## WI-010: WELD INSPECTION

### 10.1 Purpose
Inspect welds per AWS D1.3 requirements.

### 10.2 Visual Inspection Criteria
| Defect | Acceptance |
|--------|------------|
| Cracks | None |
| Incomplete fusion | None |
| Undercut | ≤1/32" |
| Porosity | ≤3/32" dia, ≤3/inch |
| Overlap | None |
| Weld size | Per drawing ±1/32" |

### 10.3 Procedure
| Step | Action |
|------|--------|
| 1 | Clean weld surface |
| 2 | Inspect with adequate lighting (50+ fc) |
| 3 | Check weld size with fillet gauge |
| 4 | Examine for defects |
| 5 | Mark any rejectable welds |
| 6 | Document findings |

### 10.4 Disposition
| Finding | Action |
|---------|--------|
| Acceptable | Proceed |
| Minor defect | Repair and reinspect |
| Major defect | Scrap or MRB |

---

## REVISION HISTORY

| Rev | Date | Description | By |
|-----|------|-------------|-----|
| A | 2026-05-17 | Initial release | |

---

## APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Manufacturing Engineer | | | |
| Quality Engineer | | | |
| Production Supervisor | | | |
