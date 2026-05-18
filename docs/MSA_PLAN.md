# Measurement System Analysis (MSA) Plan

> **Standard**: AIAG MSA Manual, 4th Edition  
> **Document Control**: REV A  
> **Date**: 2026-05-17

---

## 1. PURPOSE

This document defines the Measurement System Analysis requirements for the MudMixer production validation per PPAP Element 8.

---

## 2. MSA STUDY INDEX

| Study ID | Characteristic | Gage | Study Type | Required For |
|----------|----------------|------|------------|--------------|
| MSA-001 | Auger OD | Calipers | Gage R&R | PPAP |
| MSA-002 | Auger Pitch | Tape + fixture | Gage R&R | PPAP |
| MSA-003 | Auger Runout | Dial indicator | Gage R&R | PPAP |
| MSA-004 | Tube Length | Tape measure | Gage R&R | PPAP |
| MSA-005 | Sheet Thickness | Micrometer | Gage R&R | PPAP |
| MSA-006 | Weld Fillet Size | Fillet gauge | Gage R&R | PPAP |
| MSA-007 | Torque | Torque wrench | Gage R&R | PPAP |
| MSA-008 | Pressure | Test gauge | Linearity/Bias | PPAP |
| MSA-009 | Angle | Protractor/DRO | Gage R&R | PPAP |
| MSA-010 | Thread | Thread gauge | Attribute | PPAP |

---

## 3. ACCEPTANCE CRITERIA

### 3.1 Variable Gage R&R

| %GRR | Disposition |
|------|-------------|
| < 10% | Acceptable |
| 10-30% | Marginal - may be acceptable based on application |
| > 30% | Unacceptable - requires corrective action |

### 3.2 Number of Distinct Categories (ndc)

| ndc | Disposition |
|-----|-------------|
| ≥ 5 | Acceptable |
| < 5 | Inadequate discrimination |

### 3.3 Attribute Gage

| Metric | Requirement |
|--------|-------------|
| Effectiveness | ≥ 90% |
| Miss Rate | ≤ 2% |
| False Alarm Rate | ≤ 5% |

---

## 4. MSA-001: AUGER OUTER DIAMETER

### 4.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Digital Caliper |
| Make/Model | Mitutoyo 500-196-30 |
| Range | 0-6" |
| Resolution | 0.0005" |
| Calibration | Annual, NIST traceable |

### 4.2 Study Parameters
| Parameter | Value |
|-----------|-------|
| Study Type | Gage R&R (Crossed) |
| Operators | 3 |
| Parts | 10 |
| Trials | 3 |
| Total measurements | 90 |

### 4.3 Specification
| Parameter | Value |
|-----------|-------|
| Nominal | 2.500" |
| Tolerance | ±0.010" |
| Total tolerance | 0.020" |

### 4.4 Data Collection Form

**Operator A:**
| Part | Trial 1 | Trial 2 | Trial 3 |
|------|---------|---------|---------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

*(Repeat for Operators B and C)*

### 4.5 Analysis Method
- ANOVA method (preferred)
- Calculate: Repeatability, Reproducibility, Part-to-Part variation
- Report: %GRR, ndc

### 4.6 Acceptance
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| %GRR | < 10% | | |
| ndc | ≥ 5 | | |

---

## 5. MSA-003: AUGER RUNOUT

### 5.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Dial Indicator + V-Block fixture |
| Make/Model | Starrett 25-131J |
| Range | 0-0.250" |
| Resolution | 0.0001" |
| Calibration | Annual |

### 5.2 Study Parameters
| Parameter | Value |
|-----------|-------|
| Study Type | Gage R&R (Crossed) |
| Operators | 2 |
| Parts | 10 |
| Trials | 3 |
| Total measurements | 60 |

### 5.3 Specification
| Parameter | Value |
|-----------|-------|
| Maximum TIR | 0.030" |
| Measurement location | 6" from each end |

### 5.4 Setup Procedure
1. Place auger in V-blocks on surface plate
2. Position dial indicator at measurement location
3. Zero indicator
4. Rotate auger 360°
5. Record total indicator reading (TIR)
6. Repeat at second location

---

## 6. MSA-006: WELD FILLET SIZE

### 6.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Fillet Weld Gauge Set |
| Make/Model | GAL Gage FWG-1 |
| Range | 1/8" - 1/2" |
| Resolution | 1/32" |
| Calibration | Annual |

### 6.2 Study Parameters
| Parameter | Value |
|-----------|-------|
| Study Type | Gage R&R (Crossed) |
| Operators | 3 |
| Parts (welds) | 10 |
| Trials | 3 |
| Total measurements | 90 |

### 6.3 Specification
| Weld Location | Size | Tolerance |
|---------------|------|-----------|
| Frame joints | 3/16" | +1/32", -0 |
| Hopper to frame | 1/8" | +1/32", -0 |
| Motor mount | 1/4" | +1/32", -0 |

---

## 7. MSA-007: TORQUE WRENCH

### 7.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Click-type Torque Wrench |
| Make/Model | CDI 2502MRMH |
| Range | 30-250 in-lb |
| Accuracy | ±4% |
| Calibration | Annual + after drop |

### 7.2 Study Parameters
| Parameter | Value |
|-----------|-------|
| Study Type | Gage R&R (Crossed) |
| Operators | 3 |
| Joints | 10 |
| Trials | 3 |

### 7.3 Critical Torque Values
| Application | Torque | Tolerance |
|-------------|--------|-----------|
| Motor mount bolts | 25 ft-lb | ±10% |
| Auger coupling | 35 ft-lb | ±10% |
| Frame bolts | 17 ft-lb | ±10% |

---

## 8. MSA-008: PRESSURE GAUGE (LINEARITY & BIAS)

### 8.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Pressure Gauge |
| Make/Model | Ashcroft 1009AW |
| Range | 0-100 PSI |
| Resolution | 1 PSI |
| Calibration | Annual |

### 8.2 Study Type: Linearity & Bias
Reference standard: Certified pressure calibrator (±0.1% accuracy)

### 8.3 Test Points
| Reference PSI | Reading 1 | Reading 2 | Reading 3 | Avg | Bias |
|---------------|-----------|-----------|-----------|-----|------|
| 0 | | | | | |
| 20 | | | | | |
| 40 | | | | | |
| 60 | | | | | |
| 80 | | | | | |
| 100 | | | | | |

### 8.4 Acceptance Criteria
| Metric | Requirement |
|--------|-------------|
| Linearity | ≤ 5% of tolerance |
| Bias | ≤ 5% of tolerance at each point |

---

## 9. MSA-010: THREAD GAUGE (ATTRIBUTE)

### 9.1 Gage Information
| Item | Value |
|------|-------|
| Gage | Acme Thread Gauge Set (LH) |
| Specification | 5/8-8 LH Acme |
| Go gauge | Must enter freely |
| No-Go gauge | Must not enter > 2 threads |

### 9.2 Study Type: Attribute Agreement Analysis

### 9.3 Study Parameters
| Parameter | Value |
|-----------|-------|
| Operators | 3 |
| Parts | 30 (mix of good/bad) |
| Trials | 2 |
| Reference decision | Master evaluation |

### 9.4 Data Collection
| Part | Reference | Op A-T1 | Op A-T2 | Op B-T1 | Op B-T2 | Op C-T1 | Op C-T2 |
|------|-----------|---------|---------|---------|---------|---------|---------|
| 1 | G/NG | | | | | | |
| 2 | G/NG | | | | | | |
| ... | | | | | | | |

### 9.5 Analysis Metrics
| Metric | Calculation | Target |
|--------|-------------|--------|
| Effectiveness | Correct decisions / Total | ≥ 90% |
| Miss Rate | Missed defects / Total defects | ≤ 2% |
| False Alarm | False rejects / Total good | ≤ 5% |
| Kappa | Agreement statistic | ≥ 0.75 |

---

## 10. CALIBRATION REQUIREMENTS

### 10.1 Gage List
| Gage ID | Description | Cal Interval | Due Date | Status |
|---------|-------------|--------------|----------|--------|
| CAL-001 | Digital Caliper 6" | 12 months | | |
| CAL-002 | Micrometer 0-1" | 12 months | | |
| CAL-003 | Dial Indicator | 12 months | | |
| CAL-004 | Fillet Gauge Set | 12 months | | |
| CAL-005 | Torque Wrench | 12 months | | |
| CAL-006 | Pressure Gauge | 12 months | | |
| CAL-007 | Thread Gauge Set | 12 months | | |
| CAL-008 | Tape Measure 25' | 24 months | | |
| CAL-009 | Angle Gauge | 12 months | | |
| CAL-010 | Hipot Tester | 12 months | | |

### 10.2 Calibration Requirements
- All gages calibrated to NIST-traceable standards
- Calibration certificates on file
- Out-of-tolerance gages: quarantine and assess impact
- Calibration stickers visible on all gages

---

## 11. MSA SUMMARY STATUS

| Study | Gage | %GRR / Result | ndc | Status |
|-------|------|---------------|-----|--------|
| MSA-001 | Caliper | | | Pending |
| MSA-002 | Tape/Fixture | | | Pending |
| MSA-003 | Dial Indicator | | | Pending |
| MSA-004 | Tape Measure | | | Pending |
| MSA-005 | Micrometer | | | Pending |
| MSA-006 | Fillet Gauge | | | Pending |
| MSA-007 | Torque Wrench | | | Pending |
| MSA-008 | Pressure Gauge | | | Pending |
| MSA-009 | Angle Gauge | | | Pending |
| MSA-010 | Thread Gauge | | | Pending |

---

## 12. APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Engineer | | | |
| Manufacturing Engineer | | | |
| Metrology | | | |
