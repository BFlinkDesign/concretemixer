# PPAP Package - MudMixer Production Part Approval

> **Standard**: AIAG PPAP Manual, 4th Edition  
> **Submission Level**: Level 3 (Full submission)  
> **Date**: 2026-05-17  
> **Document Control**: REV A

---

## 1. PART INFORMATION

| Field | Value |
|-------|-------|
| Part Name | MudMixer Continuous Concrete Mixer |
| Part Number | MM-0001-A |
| Customer | Internal / Distribution |
| Drawing Number | MM-0001-A |
| Drawing Revision | A |
| Engineering Change Level | - |
| PPAP Submission Date | |
| Production Site | TBD |

---

## 2. PPAP ELEMENT CHECKLIST

### 18 Elements Status

| Element | Description | Document | Status | Location |
|---------|-------------|----------|--------|----------|
| **1** | Design Records | Engineering drawings | ✅ READY | /drawings/ |
| **2** | Engineering Change Documents | ECN log | ⏳ N/A | - |
| **3** | Customer Engineering Approval | (Internal approval) | ⏳ PENDING | - |
| **4** | Design FMEA | DFMEA.md | ✅ READY | /docs/DFMEA.md |
| **5** | Process Flow Diagram | PROCESS_FLOW.md | ✅ READY | /docs/PROCESS_FLOW.md |
| **6** | Process FMEA | PFMEA.md | ⏳ IN PROGRESS | /docs/PFMEA.md |
| **7** | Control Plan | CONTROL_PLAN.md | ✅ READY | /docs/CONTROL_PLAN.md |
| **8** | MSA Studies | MSA_PLAN.md | ✅ READY (plan) | /docs/MSA_PLAN.md |
| **9** | Dimensional Results | (Requires production) | ⏳ PENDING | - |
| **10** | Material/Performance Tests | (Requires production) | ⏳ PENDING | - |
| **11** | Initial Process Studies | (Requires production) | ⏳ PENDING | - |
| **12** | Qualified Lab Documentation | Calibration certs | ⏳ PENDING | - |
| **13** | Appearance Approval Report | (If applicable) | ⏳ N/A | - |
| **14** | Sample Production Parts | (Requires production) | ⏳ PENDING | - |
| **15** | Master Sample | (Requires production) | ⏳ PENDING | - |
| **16** | Checking Aids | Gage list in MSA_PLAN.md | ✅ READY | /docs/MSA_PLAN.md |
| **17** | Customer-Specific Reqs | (None specified) | ⏳ N/A | - |
| **18** | Part Submission Warrant | PSW form below | ⏳ PENDING | This document |

---

## 3. ELEMENT 1: DESIGN RECORDS

### 3.1 Drawing List
| Drawing No. | Title | Rev | Status |
|-------------|-------|-----|--------|
| MM-0001-A | Complete Assembly | A | Defined |
| MM-0010-A | Frame Assembly | A | Defined |
| MM-0020-A | Hopper Assembly | A | Defined |
| MM-0030-A | Auger Assembly | A | Defined |
| MM-0040-A | Motor Assembly | A | Defined |
| MM-0050-A | Water System | A | Defined |
| MM-0060-A | Electrical System | A | Defined |
| MM-0070-A | Chute Assembly | A | Defined |

### 3.2 Specifications Referenced
| Spec | Title |
|------|-------|
| ASTM A513 | Steel tubing |
| ASTM A1008 | Sheet steel |
| AWS D1.3 | Sheet steel welding |
| ASME Y14.5 | Dimensioning & tolerancing |

---

## 4. ELEMENT 4: DESIGN FMEA SUMMARY

| Metric | Value |
|--------|-------|
| Document | DFMEA.md |
| Total Failure Modes | 32 |
| High Priority (AP=H) | 3 |
| Medium Priority (AP=M) | 16 |
| Low Priority (AP=L) | 13 |

### High Priority Actions Required
| Item | Failure Mode | Recommended Action | Status |
|------|--------------|-------------------|--------|
| 3.1 | Water not linked to motor | Add motor-interlock solenoid | Open |
| 1.1 | Auger jam from aggregate | Add aggregate screen | Open |
| 1.2 | Material bridging | Add hopper vibrator | Open |

---

## 5. ELEMENT 5: PROCESS FLOW SUMMARY

| Metric | Value |
|--------|-------|
| Document | PROCESS_FLOW.md |
| Total Operations | 89 |
| Inspection Points | 19 |
| Critical Path Operations | 10 |

### Process Categories
| Category | Operation Range |
|----------|-----------------|
| Receiving | 10-50 |
| Frame Fabrication | 60-140 |
| Sheet Metal | 150-240 |
| Auger Manufacturing | 250-340 |
| Motor Subassembly | 350-400 |
| Water System | 410-470 |
| Welded Assembly | 480-550 |
| Surface Finishing | 560-620 |
| Final Assembly | 630-720 |
| Testing | 730-790 |
| Packaging | 800-880 |

---

## 6. ELEMENT 7: CONTROL PLAN SUMMARY

| Metric | Value |
|--------|-------|
| Document | CONTROL_PLAN.md |
| Control Plan Type | Pre-Launch |
| Critical Characteristics (CC) | 12 |
| Significant Characteristics (SC) | 7 |

### Special Characteristics
| Char # | Feature | Class | Spec | Control |
|--------|---------|-------|------|---------|
| SC-001 | Auger OD | CC | 2.500" ±0.010" | 100% inspect |
| SC-002 | Auger Pitch | CC | 0.6/0.85 P/D | 100% inspect |
| SC-003 | Coupling Torque | CC | 35 ft-lb | Torque wrench |
| SC-004 | Motor Alignment | CC | <0.015" TIR | Dial indicator |
| SC-005 | Ground Continuity | CC | <0.1Ω | 100% test |
| SC-006 | GFCI Function | CC | <6mA trip | 100% test |
| SC-007 | Weld Integrity | CC | AWS D1.3 | 100% visual |

---

## 7. ELEMENT 8: MSA SUMMARY

| Metric | Value |
|--------|-------|
| Document | MSA_PLAN.md |
| Total Studies Required | 10 |
| Studies Completed | 0 |
| Acceptance Criteria | %GRR <10% (variable), Effectiveness >90% (attribute) |

### Gage List
| Gage | Characteristic | Cal Status |
|------|----------------|------------|
| Digital Caliper | Auger OD, lengths | Pending |
| Dial Indicator | Runout | Pending |
| Fillet Gauge | Weld size | Pending |
| Torque Wrench | Bolt torque | Pending |
| Thread Gauge | Coupling threads | Pending |

---

## 8. ELEMENT 9: DIMENSIONAL RESULTS (Template)

### First Article Inspection - Auger (MM-3001)
| Char # | Feature | Specification | Actual | Pass/Fail |
|--------|---------|---------------|--------|-----------|
| 1 | Overall length | 36.00" ±0.125" | | |
| 2 | Outer diameter | 2.500" ±0.010" | | |
| 3 | Pitch (hopper) | 1.50" ±0.06" | | |
| 4 | Pitch (chute) | 2.125" ±0.09" | | |
| 5 | Flight thickness | 0.188" ±0.015" | | |
| 6 | Coupling thread | 5/8-8 LH Acme | | |
| 7 | Runout TIR | 0.030" max | | |

*To be completed with production parts*

---

## 9. ELEMENT 11: INITIAL PROCESS CAPABILITY (Template)

### Cpk Study Requirements
| Characteristic | Spec | LSL | USL | Cpk Target |
|----------------|------|-----|-----|------------|
| Auger OD | 2.500" ±0.010" | 2.490" | 2.510" | ≥1.33 |
| Auger Pitch | P/D = 0.6 ±0.04 | 0.56 | 0.64 | ≥1.33 |
| Motor Torque | 25 ft-lb ±10% | 22.5 | 27.5 | ≥1.33 |
| Throughput | ≥45 bags/hr | 45 | - | ≥1.33 |

### Sample Size
- Minimum 30 consecutive parts from production run
- All parts measured by same operator, same gage

*Data to be collected during production trial*

---

## 10. ELEMENT 18: PART SUBMISSION WARRANT (PSW)

### Part Information
| Field | Value |
|-------|-------|
| Customer Name | (Internal) |
| Part Name | MudMixer Continuous Mixer |
| Part Number | MM-0001-A |
| Drawing Number | MM-0001-A |
| Drawing Revision | A |
| Drawing Date | 2026-05-17 |
| Additional Engineering Changes | None |

### Organization Information
| Field | Value |
|-------|-------|
| Organization Name | |
| Address | |
| Supplier Code | |
| DUNS Number | |

### Submission Information
| Field | Value |
|-------|-------|
| Submission Level | 3 |
| Submission Reason | □ Initial □ Engineering Change □ Tooling □ Other |
| Customer Purchase Order | |

### Materials Declaration
| Declaration | Status |
|-------------|--------|
| IMDS/CMDS submitted | □ Yes □ No □ N/A |
| RoHS compliant | □ Yes □ No |
| REACH compliant | □ Yes □ No |
| Conflict minerals reported | □ Yes □ No □ N/A |

### Certification
I hereby certify that the samples represented by this warrant are representative of our parts, which were made by a process that meets all Production Part Approval Process Manual requirements. I further certify that these samples were produced at the production rate of _____ parts per hour.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Manager | | | |
| Title | | | |
| Phone | | | |
| Email | | | |

### Customer Decision
| Decision | Status |
|----------|--------|
| □ Approved | Parts meet all requirements |
| □ Interim Approval | Parts may ship with limitations |
| □ Rejected | Parts do not meet requirements |

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Customer Representative | | | |

---

## 11. PPAP READINESS SUMMARY

### Pre-Production Complete
| Item | Status |
|------|--------|
| Design records complete | ✅ |
| DFMEA complete | ✅ |
| Process Flow complete | ✅ |
| PFMEA | ⏳ In Progress |
| Control Plan complete | ✅ |
| MSA Plan complete | ✅ |
| Work Instructions complete | ✅ |
| Test Procedures complete | ✅ |

### Production Required
| Item | Status |
|------|--------|
| Production trial run | ⏳ Not started |
| Dimensional results | ⏳ Requires production |
| Cpk studies | ⏳ Requires production |
| MSA execution | ⏳ Requires production |
| Material test results | ⏳ Requires production |
| Sample parts | ⏳ Requires production |
| Master sample | ⏳ Requires production |

---

## 12. APPROVAL

### Document Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Engineer | | | |
| Manufacturing Engineer | | | |
| Design Engineer | | | |
| Program Manager | | | |

### PPAP Submission Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Manager | | | |
| Customer Representative | | | |
