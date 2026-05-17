# Test Procedures - MudMixer Production Validation

> **Standards**: ASTM C685, ASTM C143, IEC 60335, OSHA 1926.702  
> **Document Control**: REV A  
> **Date**: 2026-05-17

---

## 1. TEST PROCEDURE INDEX

| Test ID | Test Name | Phase | Required For |
|---------|-----------|-------|--------------|
| TP-001 | Incoming Material Inspection | Receiving | All materials |
| TP-002 | Dimensional Inspection | In-Process | All fabricated parts |
| TP-003 | Weld Inspection | In-Process | All welded assemblies |
| TP-004 | Motor Run-In Test | Subassembly | Motor assembly |
| TP-005 | Water System Pressure Test | Subassembly | Water system |
| TP-006 | Electrical Safety Test | Final Assembly | Complete unit |
| TP-007 | Functional Test | Final Assembly | Complete unit |
| TP-008 | Throughput Validation | Final Assembly | First Article |
| TP-009 | Mixing Quality Test | Final Assembly | First Article |
| TP-010 | Endurance Test | Qualification | First Article |

---

## 2. TP-001: INCOMING MATERIAL INSPECTION

### 2.1 Purpose
Verify raw materials meet specifications before use in production.

### 2.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Calipers | 0.001" resolution, calibrated |
| Micrometer | 0.0001" resolution, calibrated |
| Thickness gauge | 0-0.250" range |
| Hardness tester | Rockwell B/C scale |

### 2.3 Procedure

**2.3.1 Steel Tubing (1" Schedule 40)**
| Check | Specification | Method | Accept/Reject |
|-------|---------------|--------|---------------|
| OD | 1.315" ±0.010" | Caliper | |
| Wall | 0.133" ±0.010" | Micrometer | |
| Length | Per PO ±1/4" | Tape measure | |
| Surface | No rust, scale, defects | Visual | |
| Mill cert | ASTM A513, 1020 steel | Document review | |

**2.3.2 Sheet Steel (14 Gauge)**
| Check | Specification | Method | Accept/Reject |
|-------|---------------|--------|---------------|
| Thickness | 0.0747" ±0.004" | Micrometer | |
| Dimensions | Per PO ±1/8" | Tape measure | |
| Surface | No rust, scratches, dents | Visual | |
| Mill cert | ASTM A1008 CS Type B | Document review | |

**2.3.3 Motor Assembly**
| Check | Specification | Method | Accept/Reject |
|-------|---------------|--------|---------------|
| Model number | Per BOM | Visual | |
| Voltage rating | 120V AC | Nameplate | |
| Power rating | 250W (Evolution) | Nameplate | |
| Shaft diameter | Per spec | Caliper | |
| COC/COA | Received | Document review | |

### 2.4 Records
- Complete inspection report form
- Attach mill certifications
- Tag material with lot number
- File in lot history folder

---

## 3. TP-002: DIMENSIONAL INSPECTION

### 3.1 Purpose
Verify fabricated parts meet drawing specifications.

### 3.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| CMM or height gauge | 0.0001" resolution |
| Calipers | 0.001" resolution |
| Thread gauges | Acme LH set |
| Radius gauges | 1/64" - 1/2" |
| Surface plate | Grade B minimum |

### 3.3 Procedure - Auger (MM-3001)

**Critical Dimensions:**
| Char # | Feature | Specification | Actual | Pass/Fail |
|--------|---------|---------------|--------|-----------|
| 1 | Overall length | 36.00" ±0.125" | | |
| 2 | Outer diameter | 2.500" ±0.010" | | |
| 3 | Pitch (hopper section) | 1.25" ±0.030" | | |
| 4 | Pitch (chute section) | 2.00" ±0.030" | | |
| 5 | Flight thickness | 0.188" ±0.015" | | |
| 6 | Coupling thread | 5/8-8 LH Acme | | |
| 7 | Runout (TIR) | 0.030" max | | |
| 8 | Finger length | 2.00" ±0.030" | | |

**GD&T Verification:**
| Feature | Symbol | Tolerance | Actual | Pass/Fail |
|---------|--------|-----------|--------|-----------|
| Coupling axis to helix axis | Concentricity | ⌀0.010" | | |
| Helix OD | Circularity | 0.010" | | |
| Overall | Runout | 0.030" TIR | | |

### 3.4 First Article Requirements
- Measure 100% of dimensions on first 3 pieces
- Complete AS9102 forms (Form 1, 2, 3)
- Production: Sample per Control Plan

---

## 4. TP-003: WELD INSPECTION

### 4.1 Purpose
Verify weld quality meets AWS D1.3 requirements.

### 4.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Fillet gauge | 1/8" - 1/2" |
| Flashlight | LED |
| Magnifier | 10x |
| Dye penetrant kit | Per ASTM E1417 |

### 4.3 Visual Inspection Criteria (AWS D1.3)

| Defect | Acceptance Criteria |
|--------|---------------------|
| Cracks | None allowed |
| Incomplete fusion | None allowed |
| Undercut | ≤ 1/32" depth |
| Overlap | None allowed |
| Porosity | ≤ 3/32" dia, ≤ 3 per inch |
| Spatter | Minimal, removable |
| Weld size | Per drawing ±1/32" |

### 4.4 Inspection Points
| Location | Weld Type | Size | Inspection Level |
|----------|-----------|------|------------------|
| Frame tube joints | Fillet | 3/16" | 100% visual |
| Hopper to frame | Fillet | 1/8" | 100% visual |
| Motor mount | Fillet | 1/4" | 100% visual + 10% PT |
| Auger flights | Fillet | 1/8" | 100% visual |

### 4.5 Dye Penetrant Test (Critical Welds)
1. Clean surface with solvent
2. Apply penetrant, dwell 10 minutes
3. Remove excess penetrant
4. Apply developer
5. Inspect under adequate lighting
6. Accept: No linear indications
7. Reject: Any crack indications

---

## 5. TP-004: MOTOR RUN-IN TEST

### 5.1 Purpose
Verify motor assembly operates within specifications.

### 5.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Clamp ammeter | 0-10A AC, 1% accuracy |
| Tachometer | 0-200 RPM, ±1 RPM |
| Infrared thermometer | -20°C to 200°C |
| Timer | ±1 second |
| Variable transformer | 0-140V AC |

### 5.3 Test Setup
1. Mount motor assembly in test fixture
2. Connect to 120V AC power via GFCI
3. Install tachometer on output shaft
4. Allow 5-minute warm-up

### 5.4 Test Sequence

**5.4.1 No-Load Test**
| Parameter | Specification | Actual | Pass/Fail |
|-----------|---------------|--------|-----------|
| Voltage | 120V AC ±5% | | |
| Current (no load) | ≤ 1.0A | | |
| Speed (no load) | 118 RPM ±10% | | |
| Noise | No grinding, squealing | | |
| Vibration | Smooth operation | | |

**5.4.2 Loaded Test (with brake)**
| Parameter | Specification | Actual | Pass/Fail |
|-----------|---------------|--------|-----------|
| Current (full load) | ≤ 2.6A | | |
| Speed (full load) | ≥ 100 RPM | | |
| Temperature rise (30 min) | ≤ 40°C above ambient | | |

**5.4.3 Direction Test**
| Parameter | Specification | Actual | Pass/Fail |
|-----------|---------------|--------|-----------|
| Forward rotation | Clockwise (from motor end) | | |
| Reverse rotation | Counter-clockwise | | |
| Switch operation | Smooth engagement | | |

### 5.5 Acceptance Criteria
- All parameters within specification
- No abnormal noise or vibration
- Temperature stable after 30 minutes

---

## 6. TP-005: WATER SYSTEM PRESSURE TEST

### 6.1 Purpose
Verify water system is leak-free and operates correctly.

### 6.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Pressure gauge | 0-100 PSI, 2% accuracy |
| Water supply | 40-60 PSI adjustable |
| Flow meter | 0-5 GPM |
| Timer | ±1 second |

### 6.3 Test Procedure

**6.3.1 Leak Test**
1. Connect water supply at 60 PSI
2. Open flow control to 100%
3. Visually inspect all connections for 2 minutes
4. Close flow control
5. Hold pressure for 5 minutes

| Check Point | Acceptance | Result |
|-------------|------------|--------|
| Inlet fitting | No leaks | |
| Solenoid valve | No leaks | |
| Flow control valve | No leaks | |
| Tubing connections | No leaks | |
| Nozzle adapters | No leaks | |
| Pressure drop (5 min hold) | ≤ 2 PSI | |

**6.3.2 Flow Test**
| Dial Setting | Min Flow | Max Flow | Actual | Pass/Fail |
|--------------|----------|----------|--------|-----------|
| 0 | 0 GPM | 0 GPM | | |
| 25 | 0.3 GPM | 0.6 GPM | | |
| 50 | 0.6 GPM | 1.2 GPM | | |
| 75 | 1.0 GPM | 1.8 GPM | | |
| 100 | 1.5 GPM | 2.5 GPM | | |

**6.3.3 Solenoid Test**
| Test | Specification | Result |
|------|---------------|--------|
| Response time (open) | ≤ 1 second | |
| Response time (close) | ≤ 1 second | |
| Cycles (10x) | No leaks, consistent | |

---

## 7. TP-006: ELECTRICAL SAFETY TEST

### 7.1 Purpose
Verify electrical safety per IEC 60335-1.

### 7.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Hipot tester | 0-1500V AC |
| Ground continuity tester | 25A, 0-1Ω |
| Insulation resistance tester | 500V DC |
| GFCI tester | UL listed |

### 7.3 Test Sequence

**7.3.1 Ground Continuity**
| Test Point | Specification | Actual | Pass/Fail |
|------------|---------------|--------|-----------|
| Plug ground to frame | ≤ 0.1Ω | | |
| Plug ground to motor case | ≤ 0.1Ω | | |
| Plug ground to hopper | ≤ 0.1Ω | | |

**7.3.2 Insulation Resistance**
| Test | Specification | Actual | Pass/Fail |
|------|---------------|--------|-----------|
| Line to ground | ≥ 2 MΩ | | |
| Neutral to ground | ≥ 2 MΩ | | |

**7.3.3 Dielectric Withstand (Hipot)**
| Test | Specification | Actual | Pass/Fail |
|------|---------------|--------|-----------|
| Line/Neutral to ground | 1000V AC, 1 min, no breakdown | | |

**7.3.4 GFCI Function**
| Test | Specification | Actual | Pass/Fail |
|------|---------------|--------|-----------|
| Trip current | ≤ 6 mA | | |
| Trip time | ≤ 25 ms | | |
| Reset function | Operational | | |

### 7.4 Safety
- Performed by trained personnel only
- Follow lockout/tagout procedures
- Use insulated tools

---

## 8. TP-007: FUNCTIONAL TEST

### 8.1 Purpose
Verify complete unit operates as designed.

### 8.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Test stand | Level surface |
| Water supply | 40 PSI minimum |
| Dry mix (mortar) | 50 lb bag |
| Wheelbarrow | For output |
| Timer | ±1 second |
| Scale | 0-100 lb |

### 8.3 Test Procedure

**8.3.1 Pre-Start Checks**
| Check | Specification | Result |
|-------|---------------|--------|
| Hopper clear | No obstructions | |
| Chute aligned | Points to wheelbarrow | |
| Water connected | 40+ PSI confirmed | |
| Power connected | 120V via GFCI | |
| Guards in place | All guards secure | |

**8.3.2 Dry Run (No Material)**
| Check | Specification | Result |
|-------|---------------|--------|
| Motor starts | Smooth start | |
| Auger rotates freely | No binding | |
| Water spray pattern | Both nozzles active | |
| Chute swivel | Full range, smooth | |
| Chute tilt | All 3 positions | |
| E-stop function | Immediate stop | |

**8.3.3 Wet Run (With Material)**
1. Set water dial to 40
2. Start motor
3. Add 25 lb dry mix slowly
4. Observe mixing action
5. Collect output in wheelbarrow
6. Stop motor after hopper empty

| Check | Specification | Result |
|-------|---------------|--------|
| Material flow | Continuous, no bridging | |
| Mix consistency | Homogeneous | |
| Output rate | ≥ 30 lb/min | |
| Water integration | No dry spots | |
| Cleanup | Auger clears in reverse | |

---

## 9. TP-008: THROUGHPUT VALIDATION

### 9.1 Purpose
Verify production throughput meets specification (45+ bags/hr).

### 9.2 Test Setup
- 10 bags × 80 lb mortar mix
- Water supply at 40 PSI
- 2-person crew (loader + monitor)
- Timer
- Scale (verified)

### 9.3 Procedure
1. Stage all 10 bags at hopper
2. Record start time
3. Feed bags continuously (max sustainable rate)
4. Record completion time
5. Calculate throughput

### 9.4 Calculations
```
Throughput (bags/hr) = (10 bags) / (elapsed time in hours)
Throughput (lb/hr) = (800 lb) / (elapsed time in hours)
Throughput (yd³/hr) = (lb/hr) / (3200 lb/yd³)
```

### 9.5 Acceptance Criteria
| Metric | Minimum | Target |
|--------|---------|--------|
| Bags/hour | 40 | 45+ |
| Pounds/hour | 3200 | 3600+ |
| Cubic yards/hour | 1.0 | 1.1+ |

---

## 10. TP-009: MIXING QUALITY TEST

### 10.1 Purpose
Verify mix uniformity per ASTM C685 requirements.

### 10.2 Equipment Required
| Equipment | Specification |
|-----------|---------------|
| Slump cone | ASTM C143 |
| Tamping rod | 5/8" × 24" |
| Measuring tape | 1/16" resolution |
| Sample containers | 6" × 12" cylinders |

### 10.3 Procedure (ASTM C143 Slump Test)
1. Collect output sample at beginning, middle, end of batch
2. Fill slump cone in 3 layers, rod each layer 25 times
3. Strike off top, remove cone vertically
4. Measure slump (cone height minus concrete height)

### 10.4 Acceptance Criteria
| Sample | Target Slump | Tolerance | Actual | Pass/Fail |
|--------|--------------|-----------|--------|-----------|
| Beginning | Per mix spec | ±1" | | |
| Middle | Per mix spec | ±1" | | |
| End | Per mix spec | ±1" | | |

**Uniformity Requirement:**
- Variation between samples ≤ 1.5" (indicates consistent mixing)

---

## 11. TP-010: ENDURANCE TEST (First Article Only)

### 11.1 Purpose
Verify durability under continuous operation.

### 11.2 Test Duration
- 40 hours total operation
- 8 hours per day × 5 days
- Simulate 1-month production use

### 11.3 Test Protocol
| Day | Hours | Material | Inspection Points |
|-----|-------|----------|-------------------|
| 1 | 8 | Sand/cement 50/50 | Baseline measurements |
| 2 | 8 | Mortar mix | Temperature monitoring |
| 3 | 8 | Concrete mix (≤1/2" agg) | Vibration check |
| 4 | 8 | Stucco mix | Auger wear measurement |
| 5 | 8 | Sand/cement 50/50 | Final inspection |

### 11.4 Monitoring During Test
| Parameter | Frequency | Limit |
|-----------|-----------|-------|
| Motor temperature | Every hour | ≤ 80°C |
| Motor current | Every hour | ≤ 2.6A |
| Auger speed | Every 2 hours | ≥ 100 RPM |
| Unusual noise | Continuous | None |
| Leaks | Every 2 hours | None |

### 11.5 Post-Test Inspection
| Check | Specification | Result |
|-------|---------------|--------|
| Auger OD wear | ≤ 0.010" reduction | |
| Finger wear | ≤ 0.020" reduction | |
| Weld integrity | No cracks | |
| Motor function | Passes TP-004 | |
| Water system | Passes TP-005 | |

### 11.6 Acceptance Criteria
- All parameters within limits throughout test
- No component failures
- Wear within acceptable limits
- Unit passes all functional tests post-endurance

---

## 12. APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Engineer | | | |
| Manufacturing Engineer | | | |
| Design Engineer | | | |
| Program Manager | | | |
