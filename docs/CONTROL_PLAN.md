# Pre-Launch Control Plan - MudMixer Concrete Mixer

**Document Number:** CP-MM-001  
**Revision:** A  
**Date:** 2026-05-17  
**Product:** MudMixer MMXR-3225 Continuous Concrete Mixer  
**Control Plan Type:** Pre-Launch  
**Prepared By:** Quality Engineering  
**AIAG Reference:** APQP Manual, Section 6

---

## Control Plan Header

| Field | Information |
|-------|-------------|
| **Part Number** | MMXR-3225 |
| **Part Name** | Continuous Concrete Mixer Assembly |
| **Supplier/Plant** | Manufacturing Facility |
| **Supplier Code** | TBD |
| **Core Team** | Mfg Eng, Quality, Production |
| **Customer Engineering Approval** | ________ Date: ________ |
| **Supplier/Plant Approval** | ________ Date: ________ |
| **Customer Quality Approval** | ________ Date: ________ |
| **Other Approval** | ________ Date: ________ |

---

## Special Characteristics Legend

| Classification | Symbol | Description |
|----------------|--------|-------------|
| Critical Characteristic | **CC** | May affect safety or regulatory compliance |
| Significant Characteristic | **SC** | May affect fit, function, or customer satisfaction |

---

## Control Plan Matrix

### Section 1: Incoming Material Inspection

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 20 | Incoming Inspection - Steel Sheet | Micrometer, Calipers | Thickness | Material certification | SC | 14 ga: 0.0747" +/-0.005" | Micrometer measurement | 3 per lot | Each receipt | Inspection record; COC review | Reject lot; notify supplier |
| 20 | Incoming Inspection - Steel Sheet | Visual | Surface condition | Mill scale, rust, damage | - | No excessive scale, rust, or damage | Visual inspection | 100% | Each receipt | Visual acceptance | Reject affected material |
| 20 | Incoming Inspection - Steel Tube | Calipers, Tape | OD, Wall thickness | - | - | 1" OD +/-0.010"; Wall 0.133" +/-0.010" | Dimensional measurement | 3 per lot | Each receipt | Inspection record | Reject lot; notify supplier |
| 40 | Incoming Inspection - Motor | Test bench | Power rating, Current | Motor performance | CC | 250W; 1.6A running | Electrical test | 100% | Each receipt | Motor test record | Reject; return to supplier |
| 40 | Incoming Inspection - Motor | Visual, Multimeter | IP55 rating, GFCI function | Electrical safety | CC | GFCI trips within spec | GFCI trip test | 100% | Each receipt | Test record | Reject; return to supplier |
| 40 | Incoming Inspection - Solenoid Valve | Pressure test fixture | Pressure rating | Valve function | SC | Holds 145 PSI; No leaks | Pressure test | 5 per lot | Each receipt | Pressure test record | Reject lot |
| 40 | Incoming Inspection - Wheels | Visual, Scale | Load capacity | Wheel integrity | - | 300 lbs per wheel | Visual/Documentation | 3 per lot | Each receipt | Inspection record | Reject lot |

---

### Section 2: Frame Fabrication

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 70 | Cut Frame Tubes | Cold cut saw | Cut length | Blade condition, feed rate | - | Per drawing +/-0.125" | Tape measure | First 3 + 1/10 | Each setup; per batch | Cut length log | Adjust saw; re-cut |
| 70 | Cut Frame Tubes | Cold cut saw | Cut squareness | Blade alignment | - | +/-1 degree | Square/protractor | First 3 | Each setup | Setup sheet | Re-align blade |
| 90 | Bend Handle Tubes | Tube bender | Bend angle | Bender dies, pressure | SC | Per drawing +/-2 deg | Protractor, template | First 2 + 1/20 | Each setup; per batch | Bend log | Adjust bender; re-work |
| 90 | Bend Handle Tubes | Tube bender | Bend radius | Die selection | - | Min 3x tube OD | Template | First 2 | Each setup | Setup sheet | Select correct die |
| 120 | Weld Frame Assembly | MIG welder | Weld penetration | Wire feed, voltage, travel speed | CC | Full penetration per AWS D1.1 | Visual; Destructive (setup) | 100% visual; 1 destruct/month | Continuous; Monthly | Weld log; WPS | Stop; re-weld; retrain |
| 120 | Weld Frame Assembly | MIG welder | Fillet size | Wire feed, voltage | CC | Min 1/8" fillet | Fillet gauge | 100% | Each weld | Weld inspection log | Re-weld to spec |
| 120 | Weld Frame Assembly | MIG welder | Weld defects | Welder technique, gas coverage | CC | No cracks, porosity, undercut | Visual per AWS D1.1 | 100% | Each weld | Weld inspection log | Grind out; re-weld |
| 130 | Inspect Frame Welds | Fillet gauge, Visual | Weld quality | - | CC | AWS D1.1 Clause 9 | Visual + Gauge | 100% | Each frame | Inspection record | Reject; re-weld |

---

### Section 3: Sheet Metal Fabrication

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 160 | Laser Cut Hopper | Fiber laser | Profile dimensions | Focus, power, speed, gas | SC | Per drawing +/-0.010" | CMM or fixture | First 3 + 1/50 | Each program; per batch | Laser cut log | Adjust parameters |
| 160 | Laser Cut Hopper | Fiber laser | Edge quality | Assist gas, focus | - | Burr <0.015" | Visual, burr gauge | 100% | Continuous | Visual acceptance | Deburr; adjust laser |
| 180 | Laser Cut Motor Mount | Fiber laser | Hole pattern | Program accuracy | CC | Hole location +/-0.005" | CMM, pin gauge | First 3 + 1/25 | Each setup; per batch | Dimensional record | Adjust program |
| 210 | Form Hopper Body | Press brake | Bend angle | Tonnage, die selection | SC | Per drawing +/-1 deg | Protractor, template | First 2 + 1/20 | Each setup; per batch | Brake log | Adjust tonnage |
| 210 | Form Hopper Body | Press brake | Bend location | Back gauge setting | SC | Per drawing +/-0.030" | Template, tape | First 2 + 1/20 | Each setup; per batch | Setup sheet | Adjust back gauge |
| 220 | Form Chute Tube | Plate roll | Inside diameter | Roll pressure, passes | SC | 6" ID +/-0.060" | Inside calipers | First 2 + 1/20 | Each setup; per batch | Roll log | Adjust roll pressure |

---

### Section 4: Auger Manufacturing (CRITICAL)

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 270 | Form Helical Flight Sec 1 | Flight forming press | Pitch | Die setting, material feed | CC | P/D ratio 0.6; Pitch 3.3" +/-0.1" | Pitch gauge, tape | 100% | Each flight | Flight forming log | Adjust die; scrap if OOT |
| 270 | Form Helical Flight Sec 1 | Flight forming press | OD | Die selection | CC | 5.5" +/-0.030" | OD ring gauge | 100% | Each flight | Dimensional record | Adjust; scrap if OOT |
| 270 | Form Helical Flight Sec 1 | Flight forming press | ID | Die selection | CC | 2.5" +/-0.030" | ID plug gauge | 100% | Each flight | Dimensional record | Adjust; scrap if OOT |
| 280 | Form Helical Flight Sec 2 | Flight forming press | Pitch | Die setting, material feed | CC | P/D ratio 0.85; Pitch 4.7" +/-0.1" | Pitch gauge, tape | 100% | Each flight | Flight forming log | Adjust die; scrap if OOT |
| 290 | Weld Flight Sections | MIG welder | Weld integrity | Wire feed, voltage | CC | Full penetration; Smooth transition | Visual, bend test (setup) | 100% visual | Each auger | Weld log | Re-weld; scrap if cracked |
| 310 | Weld Fingers to Flight | MIG welder | Finger position | Fixture accuracy | SC | Inward extending; Spacing per dwg | Template, visual | 100% | Each auger | Assembly record | Re-position; re-weld |
| 310 | Weld Fingers to Flight | MIG welder | Finger angle | Welding technique | SC | Perpendicular +/-5 deg | Protractor | 100% | Each auger | Inspection record | Re-weld |
| 320 | Machine Drive Coupling | Lathe | Thread form | Tool selection, feed | CC | Left-hand Acme per spec | Thread gauge, go/no-go | 100% | Each auger | Thread inspection log | Re-machine; scrap |
| 330 | Inspect Auger Assembly | CMM, Gauges | Overall length | - | SC | 24" total +/-0.25" | Tape measure | 100% | Each auger | Final inspection record | Rework or scrap |
| 330 | Inspect Auger Assembly | Go/No-go gauges | All critical dimensions | - | CC | Per drawing | CMM or gauge set | 100% | Each auger | Dimensional report | Quarantine; disposition |

---

### Section 5: Motor Subassembly (CRITICAL)

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 360 | Install Drive Coupling | Torque wrench | Bolt torque | Torque wrench calibration | CC | 5/16"-18 Grade 8: 25 ft-lb +/-2 | Torque wrench | 100% | Each assembly | Torque record | Re-torque; verify calibration |
| 360 | Install Drive Coupling | Visual | Coupling alignment | Assembly technique | CC | Concentric within 0.010" | Dial indicator | 100% | Each assembly | Alignment record | Re-align; re-assemble |
| 370 | Connect Wiring Harness | Crimping tool | Crimp quality | Tool die selection | SC | Per wire gauge; Pull test pass | Pull test (5 lbs) | 3 per harness | Each assembly | Crimp record | Re-crimp |
| 390 | Install Fwd/Rev Switch | Multimeter | Switch function | Wiring accuracy | CC | Correct polarity; No shorts | Continuity test | 100% | Each assembly | Electrical test log | Re-wire; replace switch |
| 400 | Test Motor Subassembly | Motor test stand | Forward operation | - | CC | Smooth rotation; No stall | Run test 30 sec | 100% | Each assembly | Motor test record | Troubleshoot; replace motor |
| 400 | Test Motor Subassembly | Motor test stand | Reverse operation | - | CC | Smooth rotation; No stall | Run test 30 sec | 100% | Each assembly | Motor test record | Troubleshoot; replace motor |
| 400 | Test Motor Subassembly | Clamp ammeter | Running current | Motor condition | CC | 1.6A +/-0.2A | Ammeter reading | 100% | Each assembly | Motor test record | Reject motor; investigate |
| 400 | Test Motor Subassembly | GFCI test button | GFCI function | Cord integrity | CC | Trips within 25ms | GFCI trip test | 100% | Each assembly | Safety test record | Replace cord; re-test |

---

### Section 6: Water System Assembly (CRITICAL)

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 420 | Assemble Inlet Fitting | Hand tools | Thread engagement | Thread sealant application | SC | Min 3 full threads; Sealant coverage | Visual | 100% | Each assembly | Assembly checklist | Re-assemble with sealant |
| 430 | Install Flow Control | Hand tools | Valve operation | Mounting torque | SC | Smooth 0-100 dial rotation | Functional check | 100% | Each assembly | Assembly checklist | Replace valve |
| 440 | Install Solenoid Valve | Hand tools | Flow direction | Installation orientation | CC | Arrow matches flow direction | Visual verification | 100% | Each assembly | Assembly checklist | Re-install correctly |
| 450 | Cut Supply Tubing | Tube cutter | Tube lengths | Cutter blade condition | - | 34.25", 7.28", 5.9" +/-0.25" | Tape measure | First 3 | Each batch | Cut record | Re-cut |
| 460 | Install Spray Nozzles | Hand tools | Nozzle position | Orientation | SC | Spray into chute; 65 deg fan | Visual, flow test | 100% | Each assembly | Assembly checklist | Re-position |
| 470 | Pressure Test Water System | Pressure test fixture | Leak-free | System integrity | CC | No leaks at 30 PSI for 60 sec | Pressure gauge, visual | 100% | Each assembly | Pressure test record | Find leak; repair; re-test |
| 470 | Pressure Test Water System | Pressure test fixture | Max pressure | Fitting integrity | CC | Holds 145 PSI for 30 sec | Pressure gauge | 1 per lot | Per lot (min 1/day) | Burst test record | Quarantine lot; investigate |
| 470 | Pressure Test Water System | Flow meter | Flow rate | System restriction | SC | Min 1 GPM at 40 PSI | Flow meter | 100% | Each assembly | Flow test record | Clear restriction; re-test |

---

### Section 7: Welded Assembly

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 500 | Weld Hopper to Chute | MIG welder, Fixture | Aperture alignment | Fixture accuracy | CC | Concentric within 0.060" | Fixture verification | 100% | Each assembly | Fixture check log | Adjust fixture; re-weld |
| 500 | Weld Hopper to Chute | MIG welder | Weld penetration | Weld parameters | CC | Full penetration at aperture | Visual, Cut test (setup) | 100% visual; 1 cut/month | Continuous; Monthly | Weld log | Re-weld; adjust parameters |
| 520 | Weld Motor Mount | MIG welder | Mount flatness | Welding sequence | CC | Flat within 0.030" | Straight edge | 100% | Each assembly | Weld inspection | Grind/re-weld; scrap if severe |
| 520 | Weld Motor Mount | MIG welder | Hole alignment | Fixture accuracy | CC | Holes align with motor +/-0.010" | Pin gauge | 100% | Each assembly | Dimensional record | Re-weld mount plate |
| 540 | Inspect All Welds | Visual, Gauges | Overall weld quality | - | CC | AWS D1.3 (sheet); D1.1 (tube) | Visual per AWS | 100% | Each assembly | Weld inspection report | Mark defects; re-weld |

---

### Section 8: Final Assembly (CRITICAL)

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 640 | Install Auger | Assembly fixture | Auger engagement | Installation technique | CC | Full engagement in housing; Free rotation | Manual rotation check | 100% | Each assembly | Assembly checklist | Re-install; check clearance |
| 650 | Mount Motor Assembly | Torque wrench | Bolt torque | Torque wrench calibration | CC | 5/16"-18: 17 ft-lb +/-2 | Torque wrench | 100% | Each assembly | Torque record | Re-torque |
| 650 | Mount Motor Assembly | Dial indicator | Coupling alignment | Motor positioning | CC | Runout <0.015" | Dial indicator | 100% | Each assembly | Alignment record | Re-align motor |
| 660 | Install Wheels/Axle | Torque wrench | Axle nut torque | Torque wrench calibration | SC | 5/8"-11 nylock: 135 ft-lb +/-10 | Torque wrench | 100% | Each assembly | Torque record | Re-torque |
| 690 | Connect Electrical | Multimeter | Ground continuity | Connection integrity | CC | <0.1 ohm ground to plug | Ohmmeter | 100% | Each assembly | Electrical test log | Re-wire; repair |
| 720 | Apply Labels | Visual | Label presence | Correct labels | SC | All required labels present | Visual checklist | 100% | Each assembly | Assembly checklist | Apply missing labels |

---

### Section 9: Final Testing (CRITICAL)

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 730 | Electrical Safety Test | Hipot tester | Dielectric strength | Insulation integrity | CC | Per UL requirements | Hipot test | 100% | Each unit | Electrical safety record | Fail unit; investigate |
| 730 | Electrical Safety Test | Ohmmeter | Ground continuity | Ground path | CC | <0.1 ohm | Ohmmeter | 100% | Each unit | Electrical safety record | Repair; re-test |
| 740 | Functional Test - Dry Run | Test stand | Motor forward | Motor function | CC | Smooth rotation; No noise | Run test 60 sec | 100% | Each unit | Functional test record | Troubleshoot; repair |
| 740 | Functional Test - Dry Run | Test stand | Motor reverse | Motor function | CC | Smooth rotation; No stall | Run test 60 sec | 100% | Each unit | Functional test record | Troubleshoot; repair |
| 740 | Functional Test - Dry Run | Tachometer | Auger speed | Motor/auger system | CC | 118 RPM +/-10% (106-130 RPM) | Tachometer | 100% | Each unit | Speed test record | Investigate; adjust/repair |
| 750 | Water System Test | Pressure gauge | System pressure | Supply pressure | CC | Functions at 30 PSI min | Pressure test | 100% | Each unit | Water test record | Repair leaks; re-test |
| 750 | Water System Test | Electrical | Solenoid actuation | Electrical connection | CC | Opens/closes on command | Switch test | 100% | Each unit | Water test record | Repair wiring; replace valve |
| 750 | Water System Test | Flow meter | Flow control range | Valve function | SC | Dial 0-100 varies flow | Flow observation | 100% | Each unit | Water test record | Replace flow control valve |
| 760 | Swivel and Tilt Test | Manual | Swivel range | Pivot assembly | SC | 330 deg minimum | Rotation test | 100% | Each unit | Function test record | Adjust pivot; lubricate |
| 760 | Swivel and Tilt Test | Manual | Tilt positions | Locking mechanism | SC | 3 positions lock securely | Manual test | 100% | Each unit | Function test record | Adjust lock mechanism |
| 770 | Wet Mix Test | Concrete bags | Mix quality | Overall system | CC | Consistent mix; No jams; No leaks | Mix 1 bag concrete | 1 per shift minimum | Per shift | Wet test record | Quarantine; full investigation |
| 780 | Final Visual | Visual | Cosmetic defects | Surface finish | - | No visible defects | Visual inspection | 100% | Each unit | Final inspection record | Touch-up; rework |

---

### Section 10: Packaging

| Op # | Process Name | Machine/Device/Tooling | Product Characteristics | Process Characteristics | Spec. Char. | Specification/Tolerance | Evaluation Method | Sample Size | Sample Freq | Control Method | Reaction Plan |
|------|--------------|----------------------|------------------------|------------------------|-------------|------------------------|-------------------|-------------|-------------|----------------|---------------|
| 830 | Pack Unit - Box 1 | Packaging materials | Protection | Packing technique | - | No movement in box; Corners protected | Visual, shake test | 100% | Each unit | Packing checklist | Re-pack |
| 840 | Pack Accessories | Packaging materials | Completeness | Kit contents | SC | All items per packing list | Count verification | 100% | Each unit | Packing checklist | Add missing items |
| 850 | Label Boxes | Labels | Correct labeling | Label accuracy | - | Correct address, handling marks | Visual | 100% | Each unit | Shipping checklist | Re-label |

---

## Summary of Special Characteristics

### Critical Characteristics (CC)

| Op # | Characteristic | Specification | Why Critical |
|------|---------------|---------------|--------------|
| 40 | Motor IP55/GFCI | GFCI trips per spec | Electrical safety |
| 120 | Weld penetration | Full per AWS D1.1 | Structural integrity |
| 270/280 | Auger pitch | P/D 0.6 and 0.85 +/-0.1 | Mixing performance |
| 320 | Drive coupling thread | Left-hand Acme | Motor engagement |
| 360 | Coupling bolt torque | 25 ft-lb | Prevents loosening |
| 400 | GFCI function | Trips within 25ms | User safety |
| 470 | Water system leak-free | No leaks at 30 PSI | Electrical hazard prevention |
| 520 | Motor mount alignment | +/-0.010" | Auger coupling |
| 650 | Motor mounting torque | 17 ft-lb | Prevents loosening |
| 730 | Dielectric/Ground | Per UL | Electrical safety |
| 740 | Auger speed | 118 RPM +/-10% | Product performance |
| 770 | Wet mix function | No jams, consistent mix | Customer satisfaction |

### Significant Characteristics (SC)

| Op # | Characteristic | Specification | Why Significant |
|------|---------------|---------------|-----------------|
| 20 | Steel thickness | 0.0747" +/-0.005" | Material strength |
| 90 | Handle bend angle | Per dwg +/-2 deg | Fit and ergonomics |
| 160 | Hopper profile | +/-0.010" | Assembly fit |
| 310 | Finger position | Per drawing | Mixing efficiency |
| 660 | Axle nut torque | 135 ft-lb | Wheel retention |

---

## Gauge and Equipment Requirements

| Equipment | Calibration Frequency | Accuracy Required |
|-----------|----------------------|-------------------|
| Torque wrenches | 6 months or 5000 cycles | +/-4% |
| Micrometers | 12 months | +/-0.0001" |
| Calipers | 12 months | +/-0.001" |
| Pressure gauges | 12 months | +/-2% FS |
| Multimeters | 12 months | +/-1% |
| Hipot tester | 12 months | Per UL |
| Tachometer | 12 months | +/-1% |
| CMM | 12 months | Per ISO 10360 |

---

## Reaction Plan Summary

| Severity | Action Required |
|----------|-----------------|
| Minor (non-critical OOT) | Adjust process; rework part; continue |
| Major (SC OOT) | Stop; adjust; re-inspect last 10 units |
| Critical (CC OOT) | Stop line; quarantine; notify Quality; root cause |
| Safety (electrical, structural) | Stop line; quarantine all; full investigation; notify management |

---

## Document Control

| Rev | Date | Description | Author | Approved |
|-----|------|-------------|--------|----------|
| A | 2026-05-17 | Initial Pre-Launch Release | Quality Eng | ________ |

---

## Approval Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Manager | | | |
| Manufacturing Manager | | | |
| Engineering Manager | | | |
| Plant Manager | | | |

---

*This Control Plan is prepared in accordance with AIAG APQP and PPAP requirements. It will be updated to Production Control Plan status after successful PPAP approval and initial production validation.*
