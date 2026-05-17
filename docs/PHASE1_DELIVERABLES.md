# APQP Phase 1 Deliverables - MudMixer Reverse Engineering Project

> **Document Number**: APQP-P1-001  
> **Revision**: 1.0  
> **Date**: 2026-05-17  
> **Project**: Portable Continuous Concrete Mixer (MudMixer Equivalent)  
> **Phase**: Plan and Define Program

---

## Document Control

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2026-05-17 | Engineering Team | Initial Phase 1 Release |

---

## 1. DESIGN GOALS

### 1.1 Performance Targets (Based on Competitor Analysis)

| Parameter | MudMixer Evolution (Benchmark) | Target Specification | Stretch Goal | Acceptance Criteria |
|-----------|-------------------------------|---------------------|--------------|---------------------|
| Throughput | 45+ bags (80 lb)/hr | >= 45 bags/hr | >= 50 bags/hr | Verified via timed test with Quikrete 80 lb bags |
| Cubic Yard Rate | ~1 yd³/hr | >= 1 yd³/hr | >= 1.2 yd³/hr | Continuous operation, 2-person crew |
| Hopper Capacity | 120 lbs | >= 120 lbs | >= 150 lbs | Weighed capacity without spillage |
| Motor Power | 0.5 HP (250W Evolution) | 0.5 HP (373W) | 0.75 HP | Nameplate rating |
| Auger Speed | ~118 RPM | 115-125 RPM | Adjustable | Tachometer measurement |
| Output Torque | 95-129 N-m | >= 95 N-m | >= 110 N-m | Calculated from power/speed |
| Maximum Aggregate | 1/2" (12.7 mm) | >= 1/2" | >= 5/8" | No jamming during 100-bag test |
| Water Pressure (Min) | 30 PSI | <= 30 PSI | <= 25 PSI | Functional test at minimum pressure |
| Chute Swivel | 330 degrees | >= 330 degrees | 360 degrees | Measured arc of rotation |
| Chute Tilt Range | -5 deg to +30 deg | -5 deg to +30 deg | -10 deg to +35 deg | Protractor measurement |
| Weight (Dry) | 145 lbs | <= 150 lbs | <= 140 lbs | Calibrated scale |
| Overall Length | 66.5 in | 65-68 in | <= 65 in | Tape measurement |
| Overall Width | 27.5 in | 26-29 in | <= 27 in | Tape measurement |

### 1.2 Competitive Improvement Targets

Based on documented MudMixer design flaws, the following improvements are targeted:

| Known Issue | Competitor Status | Target Improvement | Verification Method |
|-------------|------------------|-------------------|---------------------|
| Water not linked to motor | Water continues during jams | Auto water shutoff on motor stop | Induced jam test - water must stop within 1 second |
| Hopper clogging/bridging | Requires constant agitation | Self-feeding hopper design | 50-bag continuous test without manual agitation |
| Inconsistent water dial | "Finicky" per user reports | Linear flow response (R² >= 0.95) | Flow rate measurement at 10%, 50%, 90% dial settings |
| Paint finish | Paint (not powder coat) | Powder coat finish | Adhesion test per ASTM D3359 (5B rating) |
| GFCI reliability | Intermittent failures reported | Zero GFCI nuisance trips | 100 on/off cycle test in wet environment |

---

## 2. RELIABILITY GOALS

### 2.1 Mean Time Between Failures (MTBF) Targets

| Component/System | MTBF Target | Calculation Basis | Verification Method |
|------------------|-------------|-------------------|---------------------|
| Complete System | >= 500 operating hours | 2-year warranty equiv. @ 250 hrs/yr | Accelerated life test or field data |
| Motor Assembly | >= 2,000 operating hours | High-cost component, critical | Motor endurance test per IEC 60034 |
| Auger Assembly | >= 1,000 operating hours | Primary wear item | Wear measurement at 100, 250, 500 hrs |
| Water Solenoid | >= 5,000 cycles | 100 cycles/job x 50 jobs | Cycle endurance test |
| Electrical System | >= 1,500 operating hours | GFCI, switches, wiring | Environmental chamber cycling |
| Bearings | >= 1,000 operating hours | Sealed bearing, concrete environment | Vibration analysis trending |
| Frame/Welds | >= 2,500 operating hours | Structural components | Fatigue test, dye penetrant inspection |

### 2.2 Duty Cycle Requirements

| Operating Mode | Definition | Duration Target | Thermal Limit |
|----------------|------------|-----------------|---------------|
| Continuous | Uninterrupted operation | >= 2 hours | Motor temp rise <= 80K above ambient |
| Intermittent (S3) | 10 min ON / 5 min OFF | 8-hour workday | Motor temp rise <= 100K |
| Peak Load | Aggregate jam clearing | 15 seconds forward/reverse cycling | No thermal trip |
| Startup | Cold start, fully loaded hopper | Motor must start within 3 seconds | Inrush current <= 25A |

### 2.3 Environmental Reliability Requirements

| Environmental Factor | Test Condition | Acceptance Criteria |
|---------------------|----------------|---------------------|
| Operating Temperature | 32 deg F to 104 deg F (0 deg C to 40 deg C) | Full functionality, no derating |
| Storage Temperature | -4 deg F to 140 deg F (-20 deg C to 60 deg C) | No permanent damage |
| Humidity | 95% RH non-condensing | IP55 motor, watertight boxes maintain function |
| Water Spray | IPX4 (splashing water) | Electrical system maintains operation |
| Dust/Cement | IP5X (dust protected) | Motor ventilation maintains airflow |
| UV Exposure | 1000 hours UV-B per ASTM G154 | No visible cracking, color fade <= Delta E 3 |
| Vibration | 2g, 10-500 Hz, 3 axes | No fastener loosening, no structural cracks |

### 2.4 Warranty Alignment

| Warranty Period | Target Reliability | Field Failure Rate Target |
|-----------------|-------------------|---------------------------|
| 2 years (match Evolution) | 95% survive warranty period | <= 5% warranty claims |
| Extended 3-year option | 85% survive extended period | <= 15% claims by year 3 |

---

## 3. QUALITY GOALS

### 3.1 Process Capability Targets (Cpk)

| Critical Dimension | Nominal | Tolerance | Cpk Target | Measurement System |
|-------------------|---------|-----------|------------|-------------------|
| Auger OD | 2.500 in | +/- 0.010 in | >= 1.67 | CMM or precision calipers |
| Housing ID | 2.600 in | +/- 0.015 in | >= 1.33 | Bore gauge |
| Auger-Housing Clearance | 0.050 in | +0.030/-0.020 in | >= 1.33 | Calculated from measured values |
| Pitch-to-Diameter Ratio (Hopper) | 0.50 | +/- 0.05 | >= 1.33 | Pitch gauge |
| Pitch-to-Diameter Ratio (Chute) | 0.80 | +/- 0.10 | >= 1.33 | Pitch gauge |
| Motor Shaft Concentricity | 0.000 in | 0.002 in TIR max | >= 1.67 | Dial indicator on V-blocks |
| Frame Tube Perpendicularity | 90.0 deg | +/- 0.5 deg | >= 1.33 | Digital protractor |
| Weld Throat (Fillet) | 0.125 in | -0 / +0.0625 in | >= 1.33 | Weld gauge |

### 3.2 Defect Rate Targets

| Category | Target | Measurement | Reporting Period |
|----------|--------|-------------|------------------|
| Assembly Defects | <= 1,000 ppm | Defects per million units assembled | Monthly |
| Supplier Defects (Incoming) | <= 500 ppm | Incoming inspection reject rate | Monthly |
| Field Failures (0-90 days) | <= 2% | DOA + early field returns | Quarterly |
| Field Failures (0-1 year) | <= 3% | Warranty claims | Annually |
| Field Failures (0-2 year) | <= 5% | Total warranty claims | Warranty period |
| Customer Complaints | <= 1% | Complaints per units shipped | Quarterly |

### 3.3 Quality System Requirements

| Requirement | Standard | Compliance Target |
|-------------|----------|-------------------|
| Quality Management System | ISO 9001:2015 | Full certification (match Prince Mfg) |
| Environmental Management | ISO 14001:2015 | Full certification |
| Supplier Quality | AIAG PPAP Level 3 | All critical component suppliers |
| Measurement System Analysis | AIAG MSA 4th Edition | GR&R <= 10% for critical characteristics |
| Statistical Process Control | AIAG SPC 2nd Edition | Control charts on all SC characteristics |

### 3.4 First Pass Yield Targets

| Assembly Stage | FPY Target | Rework Limit |
|----------------|------------|--------------|
| Frame Welding | >= 98% | <= 2% rework |
| Motor Assembly | >= 99% | <= 1% rework |
| Electrical Assembly | >= 99% | <= 1% rework |
| Water System Assembly | >= 98% | <= 2% rework |
| Final Assembly | >= 97% | <= 3% rework |
| Functional Test | >= 99% | <= 1% retest |
| Overall Assembly Line | >= 92% | Product of all stages |

---

## 4. PRELIMINARY SPECIAL CHARACTERISTICS LIST

### 4.1 Safety-Critical Characteristics (SC - Diamond Symbol)

These characteristics directly affect operator safety and require enhanced process controls.

| ID | Characteristic | Specification | Control Method | Verification |
|----|---------------|---------------|----------------|--------------|
| SC-001 | GFCI Function | Trip within 25ms at 5mA | 100% functional test | Electrical safety test per UL 943 |
| SC-002 | Ground Continuity | <= 0.1 ohm resistance | 100% functional test | Hi-pot tester |
| SC-003 | Motor Enclosure Integrity | IP55 rating maintained | Visual + pressure test | Water ingress test per IEC 60529 |
| SC-004 | Emergency Stop Function | Motor stop within 0.5 sec | 100% functional test | Timed response test |
| SC-005 | Auger Guard/Shield Presence | Guards installed, no gaps > 6mm | Visual inspection | Go/no-go gauge |
| SC-006 | Pinch Point Labeling | Warning labels present and legible | Visual inspection | Label checklist |
| SC-007 | Handle Grip Security | No rotation under 25 ft-lb torque | Torque test (sample) | Torque wrench test |
| SC-008 | Wheel Axle Retention | Nylock nut torqued to 135 ft-lb | Torque verification | Calibrated torque wrench |
| SC-009 | Frame Weld Integrity | No cracks, full penetration | Visual + sample dye penetrant | AWS D1.3 inspection criteria |
| SC-010 | Tip-Over Stability | Stable at 15 deg angle, full load | Tilt table test | Angle measurement |

### 4.2 Significant Characteristics (CC - Shield Symbol)

These characteristics significantly affect product function, fit, or customer satisfaction.

| ID | Characteristic | Specification | Control Method | Verification |
|----|---------------|---------------|----------------|--------------|
| CC-001 | Auger-Housing Clearance | 0.050 +0.030/-0.020 in | SPC with control charts | Bore gauge measurement |
| CC-002 | Motor Torque Output | >= 95 N-m at 118 RPM | Sample dynamometer test | Motor test stand |
| CC-003 | Throughput Rate | >= 45 bags/hr | End-of-line functional test | Timed throughput test |
| CC-004 | Water Flow at 30 PSI | 0.5-2.0 GPM adjustable | Functional test | Calibrated flow meter |
| CC-005 | Chute Swivel Free Movement | 330 deg min, smooth rotation | Manual inspection | Protractor + feel test |
| CC-006 | Hopper Capacity | >= 120 lbs without overflow | Sample weight test | Calibrated scale |
| CC-007 | Auger Finger Weld Strength | >= 500 lbf shear | Destructive sample test | Tensile tester |
| CC-008 | Motor Coupling Thread Engagement | >= 4 threads (min 0.5 in) | Visual + gauge | Thread engagement gauge |
| CC-009 | Solenoid Response Time | <= 1 second open/close | Functional test | Timed test with stopwatch |
| CC-010 | Paint/Coating Adhesion | 5B per ASTM D3359 | Sample cross-hatch test | Tape pull test |
| CC-011 | Auger Helix Direction | Right-hand helix | Visual inspection | Inspection checklist |
| CC-012 | Motor Rotation Direction | Forward = material advance | 100% functional test | Direction verification |

### 4.3 Special Characteristics Summary Matrix

| Type | Symbol | Quantity | Control Plan Level | Documentation Required |
|------|--------|----------|-------------------|----------------------|
| Safety-Critical (SC) | Diamond | 10 | Level 3 (Enhanced) | PFMEA RPN <= 80, Cpk >= 1.67 |
| Significant (CC) | Shield | 12 | Level 2 (Standard) | PFMEA RPN <= 120, Cpk >= 1.33 |
| Standard | None | All others | Level 1 (Basic) | Work instructions |

---

## 5. PRODUCT ASSURANCE PLAN

### 5.1 Verification and Validation Approach

#### 5.1.1 Design Verification (DVP&R) Overview

| Phase | Activities | Exit Criteria |
|-------|------------|---------------|
| DV1 - Component | Individual component testing | All components meet specifications |
| DV2 - Subsystem | Integrated subsystem testing | Motor, water, frame subsystems validated |
| DV3 - System | Full system verification | All design requirements verified |
| PV - Production Validation | Production-representative samples | Process capable of meeting requirements |

#### 5.1.2 Design Verification Test Matrix

| Test Category | Test Name | Sample Size | Test Standard/Method | Acceptance Criteria |
|---------------|-----------|-------------|---------------------|---------------------|
| **Performance** | | | | |
| | Throughput Verification | 3 units | Timed bag count (80 lb Quikrete) | >= 45 bags/hr for all units |
| | Mixing Quality | 3 units | Visual + slump test per ASTM C143 | Homogeneous mix, slump within spec |
| | Aggregate Compatibility | 3 units | Test with 1/2" max aggregate | No jams in 100-bag continuous test |
| | Water Flow Calibration | 5 units | Flow meter at dial positions | Linear response R² >= 0.95 |
| **Durability** | | | | |
| | Motor Endurance | 3 motors | 500 hr continuous per IEC 60034 | No failure, temp rise <= 80K |
| | Auger Wear | 3 augers | 500 hr with abrasive media | Wear <= 0.010 in on flight OD |
| | Frame Fatigue | 2 frames | 100,000 cycles at 1.5x load | No cracks (dye penetrant) |
| | Weld Strength | 10 coupons | Tensile test per AWS D1.3 | >= 60 ksi ultimate strength |
| **Environmental** | | | | |
| | Temperature Cycling | 2 units | -20 deg C to +60 deg C, 50 cycles | Functional after cycling |
| | Water Ingress (Motor) | 3 motors | IPX5 spray test per IEC 60529 | No water in motor cavity |
| | Corrosion Resistance | 3 units | 240 hr salt spray per ASTM B117 | No red rust on frame |
| | UV Exposure | 3 panels | 1000 hr UV-B per ASTM G154 | Delta E <= 3, no cracking |
| **Electrical Safety** | | | | |
| | GFCI Functional | 100% | UL 943 test protocol | Trip <= 25ms at 5mA |
| | Dielectric Strength | 100% | Hi-pot 1500V AC for 1 min | No breakdown |
| | Ground Continuity | 100% | Ground bond test | <= 0.1 ohm |
| | Leakage Current | 5 units | Per UL 987 | <= 0.5 mA |
| **Structural** | | | | |
| | Static Load | 3 units | 1.5x max hopper load | No permanent deformation |
| | Dynamic Load | 3 units | 2x load, 1000 cycles | No cracks or fastener loosening |
| | Tip-Over Stability | 3 units | Tilt table test | Stable at 15 deg, full load |
| | Handle Strength | 3 handles | 200 lbf vertical pull | No failure or excessive deflection |

### 5.2 Validation Test Plan

#### 5.2.1 Design Validation (Customer-Focused)

| Test | Description | Sample Size | Duration | Success Criteria |
|------|-------------|-------------|----------|------------------|
| Beta Field Trial | Units deployed to 10 contractor sites | 10 units | 90 days | >= 90% satisfaction, <= 2 failures |
| Usability Assessment | Ergonomic evaluation by users | 20 users | 1 day each | Task completion >= 95%, no safety incidents |
| Competitor Benchmark | Side-by-side test vs MudMixer | 3 pairs | 1 week | Meet or exceed all benchmark metrics |
| Extreme Use Case | 8-hour continuous operation | 3 units | 1 day | No thermal trip, consistent output |
| Solo Operation | One-person workflow evaluation | 5 users | 4 hours each | Achievable throughput >= 25 bags/hr |

#### 5.2.2 Production Validation (Process-Focused)

| Activity | Sample Size | Timing | Acceptance Criteria |
|----------|-------------|--------|---------------------|
| PPAP Submission | Per AIAG PPAP Level 3 | Pre-production | Full approval from customer |
| Initial Process Study | 30 consecutive units | First production run | Cpk >= 1.33 for CC, >= 1.67 for SC |
| Measurement System Analysis | Per AIAG MSA | Pre-production | GR&R <= 10% for SC, <= 20% for CC |
| Run @ Rate | 300 units | Production ramp | Meet takt time, FPY >= 92% |
| Process Capability Study | 300 units | Steady-state production | Cpk >= 1.33 sustained |

### 5.3 Supplier Quality Requirements

| Requirement | Critical Components | Standard Components |
|-------------|--------------------|--------------------|
| PPAP Level | Level 3 (Full) | Level 2 (Standard) |
| Cpk Requirement | >= 1.67 | >= 1.33 |
| Incoming Inspection | 100% for SC characteristics | AQL sampling per Z1.4 |
| Supplier Audit | Annual on-site | Self-assessment questionnaire |
| Corrective Action Response | 24-hour acknowledgment, 5 days containment | 48-hour acknowledgment, 10 days containment |

### 5.4 Risk-Based Testing Priority

Based on KNOWN_ISSUES.md analysis, prioritize testing for identified failure modes:

| Risk Area | Known Issue | Test Priority | Mitigation Validation |
|-----------|-------------|---------------|----------------------|
| Water-Motor Interlock | Water continues during jam | HIGH | Verify auto-shutoff under simulated jam |
| Hopper Bridging | Material clogs in hopper | HIGH | Continuous feed test without agitation |
| Aggregate Jamming | >1/2" aggregate causes jam | HIGH | Edge-case aggregate size testing |
| GFCI Reliability | Intermittent trip issues | HIGH | Extended wet environment cycling |
| Solenoid Durability | Reported early failures | MEDIUM | Accelerated cycle life test |
| Paint Durability | Users expect powder coat | MEDIUM | Enhanced adhesion and corrosion testing |

### 5.5 Certification and Compliance Requirements

| Requirement | Standard | Applicability | Timeline |
|-------------|----------|---------------|----------|
| Electrical Safety (US) | UL 987 (Stationary and Fixed Electric Tools) | Mandatory for US market | Before production |
| Electrical Safety (Canada) | CSA C22.2 No. 60335-2-45 | Mandatory for Canada | Before production |
| EMC Compliance | FCC Part 15 Class B | Mandatory for US | Before production |
| RoHS Compliance | EU 2015/863 | Required for EU export | Design phase |
| California Prop 65 | If lead/cadmium present | Required for CA sales | Labeling if applicable |
| OSHA Compliance | 29 CFR 1910 | Design guidance | Design phase |

---

## 6. PHASE 1 DELIVERABLES CHECKLIST

| Deliverable | Status | Document Reference |
|-------------|--------|-------------------|
| Voice of Customer (VOC) | Complete | KNOWN_ISSUES.md (User feedback analysis) |
| Business Plan / Marketing Strategy | Pending | Not in scope for reverse engineering |
| Product/Process Benchmark Data | Complete | SPECIFICATIONS.md, VALIDATED_SPECIFICATIONS.md |
| Product/Process Assumptions | Complete | DATA_REQUIREMENTS.md Section 6 |
| Product Reliability Studies | Complete | Section 2 of this document |
| Customer Inputs | Complete | KNOWN_ISSUES.md (User reports, forums) |
| Design Goals | Complete | Section 1 of this document |
| Reliability and Quality Goals | Complete | Sections 2, 3 of this document |
| Preliminary Bill of Materials | Partial | VALIDATED_SPECIFICATIONS.md (Parts list) |
| Preliminary Process Flow Chart | Pending | Phase 2 deliverable |
| Preliminary Special Characteristics | Complete | Section 4 of this document |
| Product Assurance Plan | Complete | Section 5 of this document |
| Management Support | Pending | Project approval required |

---

## 7. PHASE 1 EXIT CRITERIA

| Criterion | Requirement | Status |
|-----------|-------------|--------|
| Design goals documented and approved | Complete with measurable targets | COMPLETE |
| Reliability goals established | MTBF targets for all major systems | COMPLETE |
| Quality goals defined | Cpk and defect rate targets set | COMPLETE |
| Special characteristics identified | SC and CC list with control methods | COMPLETE |
| Product assurance plan approved | DVP&R framework established | COMPLETE |
| Customer requirements confirmed | VOC captured from user feedback | COMPLETE |
| Feasibility assessment | Technical feasibility confirmed | COMPLETE |
| Resource plan | Engineering team assigned | PENDING |
| Management commitment | Phase gate approval | PENDING |

---

## 8. NEXT PHASE (PHASE 2) PREVIEW

Phase 2 - Product Design and Development will address:

1. **Design FMEA (DFMEA)** - Failure mode analysis for all subsystems
2. **Design for Manufacturability (DFM)** - Optimize for production at Prince Mfg or equivalent
3. **Design Verification Plan (DVP&R)** - Detailed test procedures
4. **Prototype Build Plan** - Alpha and beta prototype specifications
5. **Supplier Selection** - RFQ and qualification of critical suppliers
6. **CAD Model Completion** - Full parametric 3D models
7. **Engineering Drawings** - GD&T per ASME Y14.5

---

## APPROVAL SIGNATURES

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Program Manager | _________________ | _________________ | ________ |
| Design Engineer | _________________ | _________________ | ________ |
| Quality Engineer | _________________ | _________________ | ________ |
| Manufacturing Engineer | _________________ | _________________ | ________ |
| Supplier Quality | _________________ | _________________ | ________ |

---

## REVISION HISTORY

| Rev | Date | Description | Author |
|-----|------|-------------|--------|
| 1.0 | 2026-05-17 | Initial Phase 1 release | Engineering Team |

---

## REFERENCES

- VALIDATED_SPECIFICATIONS.md - Technical specifications with confidence levels
- SPECIFICATIONS.md - Product line overview and competitor data
- DATA_REQUIREMENTS.md - Known vs unknown specifications gap analysis
- KNOWN_ISSUES.md - User-reported issues and design flaws
- US Patent 10,259,140 B1 - Primary patent reference
- US Patent 11,285,639 B2 - Secondary patent reference
- AIAG APQP Manual, 2nd Edition
- AIAG PPAP Manual, 4th Edition
- AIAG FMEA Handbook, 4th Edition
