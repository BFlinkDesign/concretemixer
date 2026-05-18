# Process FMEA (PFMEA) - MudMixer Concrete Mixer

## FMEA Header Information

| Field | Value |
|-------|-------|
| **FMEA Number** | PFMEA-MM-001 |
| **Subject** | MudMixer MMXR-3225 Continuous Concrete Mixer Manufacturing Process |
| **Manufacturing Responsibility** | Manufacturing Engineering |
| **Model Year/Platform** | 2026 |
| **Key Date** | 2026-05-17 |
| **FMEA Revision** | Rev A |
| **Prepared By** | Manufacturing Engineering / Quality Engineering |
| **Core Team** | Manufacturing Engineering, Quality, Production, Welding Engineering |
| **FMEA Type** | Process FMEA (AIAG-VDA Format) |
| **Control Plan Reference** | CP-MM-001 Rev A |
| **Process Flow Reference** | PFD-MM-001 Rev A |

---

## Process FMEA Scope

This PFMEA covers the manufacturing processes for the MudMixer MMXR-3225 Continuous Concrete Mixer, focusing on:

1. **Frame Fabrication** - Tube cutting, bending, welding (Op 60-140)
2. **Sheet Metal Fabrication** - Laser cutting, forming, rolling (Op 150-240)
3. **Auger Manufacturing** - Flight forming, welding, machining (Op 250-340)
4. **Motor Subassembly** - Coupling installation, wiring, testing (Op 350-400)
5. **Water System Assembly** - Fitting, valve, tubing assembly (Op 410-470)
6. **Welded Assembly** - Major structural welding (Op 480-550)
7. **Final Assembly** - Component integration (Op 630-720)
8. **Testing and Inspection** - Functional and safety testing (Op 730-780)

---

## Rating Scales (AIAG-VDA)

### Severity Rating Scale

| Rating | Effect | Criteria for Manufacturing Process |
|--------|--------|-----------------------------------|
| 10 | Hazardous without warning | May endanger operator without warning |
| 9 | Hazardous with warning | May endanger operator with warning |
| 8 | Loss of primary function | 100% of product scrapped or requires repair >1 hour |
| 7 | Degradation of primary function | Product sorted and portion scrapped; repair <1 hour |
| 6 | Loss of secondary function | 100% of product may have to be reworked offline |
| 5 | Degradation of secondary function | Portion of product reworked offline |
| 4 | Annoying defect noticed by most | 100% reworked at station before shipment |
| 3 | Annoying defect noticed by some | Portion reworked at station before shipment |
| 2 | Annoying defect noticed by few | Slight inconvenience to process or operator |
| 1 | No effect | No discernible effect |

### Occurrence Rating Scale

| Rating | Probability | Process Capability (Cpk) |
|--------|-------------|--------------------------|
| 10 | Very high | <0.33; Inherent failure rate |
| 9 | High | >=0.33; Defects expected daily |
| 8 | High | >=0.51; Defects expected weekly |
| 7 | Moderate | >=0.67; Defects expected monthly |
| 6 | Moderate | >=0.83; Defects expected quarterly |
| 5 | Moderate | >=1.00; Process in statistical control |
| 4 | Low | >=1.17; Process capable |
| 3 | Low | >=1.33; Process highly capable |
| 2 | Very low | >=1.50; Process very highly capable |
| 1 | Remote | >=1.67; Defects almost impossible |

### Detection Rating Scale

| Rating | Detection Ability | Description |
|--------|-------------------|-------------|
| 10 | Almost impossible | No process control; defect passes to customer |
| 9 | Very remote | Defect detected at final inspection after packaging |
| 8 | Remote | Defect detected at final inspection before packaging |
| 7 | Very low | Defect detected at subsequent operation by operator |
| 6 | Low | Defect detected at subsequent operation by automated system |
| 5 | Moderate | Defect detected at the station by operator |
| 4 | Moderately high | Defect detected at the station by automated controls |
| 3 | High | Error-proofing at subsequent station (poka-yoke) |
| 2 | Very high | Error-proofing at station detects discrepant part |
| 1 | Almost certain | Error-proofing prevents defect from being made |

### Action Priority (AP) Logic Table

| Severity | Occurrence | Detection | Action Priority |
|----------|------------|-----------|-----------------|
| 9-10 | Any | Any | **H (High)** |
| 7-8 | 7-10 | Any | **H (High)** |
| 7-8 | 4-6 | 7-10 | **H (High)** |
| 7-8 | 4-6 | 1-6 | **M (Medium)** |
| 7-8 | 1-3 | Any | **M (Medium)** |
| 5-6 | 7-10 | Any | **M (Medium)** |
| 5-6 | 4-6 | 7-10 | **M (Medium)** |
| 5-6 | 4-6 | 1-6 | **L (Low)** |
| 5-6 | 1-3 | Any | **L (Low)** |
| 1-4 | Any | Any | **L (Low)** |

---

## Process FMEA Worksheet

### Section 1: Frame Fabrication - Welding (Op 120-140)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 1.1 | 120 | Weld frame assembly per AWS D1.1 | **Weld porosity** (gas pockets in weld) | Local: Reduced weld strength; Next: Frame joint weakness; Customer: Potential frame failure under load, safety hazard | 8 | Contaminated base metal (oil, rust, moisture) | 5 | Operator training on surface prep; WPS requires clean surface; Pre-weld visual check | Visual inspection 100% per AWS D1.1 (Op 130); Fillet gauge check | 5 | **M** | Add pre-weld surface cleanliness specification; Implement solvent wipe procedure |
| 1.2 | 120 | Weld frame assembly per AWS D1.1 | **Weld porosity** (gas pockets in weld) | Local: Reduced weld strength; Next: Frame joint weakness; Customer: Potential frame failure under load, safety hazard | 8 | Insufficient shielding gas coverage | 5 | Gas flow meter on welder; WPS specifies 75/25 Ar/CO2 at 25-30 CFH | Visual inspection 100% per AWS D1.1 (Op 130) | 5 | **M** | Add gas flow verification to setup checklist; Replace gas delivery hoses annually |
| 1.3 | 120 | Weld frame assembly per AWS D1.1 | **Incomplete fusion** (lack of bond between weld and base metal) | Local: Weak joint; Next: Structural failure; Customer: Frame collapse potential, injury hazard | 9 | Insufficient heat input (low voltage/amperage) | 4 | WPS with specified parameters; Welder qualification per AWS D1.1 | Visual inspection (Op 130); Monthly destructive testing | 6 | **H** | Add weld parameter monitoring system; Implement pre-production weld coupons |
| 1.4 | 120 | Weld frame assembly per AWS D1.1 | **Incomplete fusion** (lack of bond between weld and base metal) | Local: Weak joint; Next: Structural failure; Customer: Frame collapse potential, injury hazard | 9 | Improper joint fit-up (excessive gap) | 4 | Weld fixture ensures alignment; Notch tube ends per mating profile (Op 100) | Visual check of fit-up before welding; Inspection record | 5 | **H** | Add go/no-go gap gauge to fixture; Maximum gap 1/16" specification |
| 1.5 | 120 | Weld frame assembly per AWS D1.1 | **Weld undercut** (groove melted into base metal) | Local: Stress concentration; Next: Reduced fatigue life; Customer: Premature frame cracking | 7 | Excessive travel speed | 5 | WPS specifies travel speed range; Operator training | Visual inspection 100% (Op 130); AWS D1.1 acceptance criteria | 5 | **M** | Add travel speed reference on fixture; Mark weld start/stop points |
| 1.6 | 120 | Weld frame assembly per AWS D1.1 | **Weld cracks** (hot cracking or cold cracking) | Local: Weld failure initiation; Next: Progressive crack growth; Customer: Catastrophic frame failure | 9 | Improper welding sequence causing stress concentration | 3 | WPS defines weld sequence; Balanced welding technique training | Visual inspection 100% (Op 130); Crack detection at weld areas | 5 | **M** | Document weld sequence on work instruction; Add balanced welding diagram |
| 1.7 | 120 | Weld frame assembly per AWS D1.1 | **Excessive spatter** | Local: Poor appearance; Next: Requires additional grinding; Customer: Cosmetic defect, potential injury from sharp edges | 4 | Incorrect wire feed speed or voltage | 6 | WPS parameter ranges; Setup verification | Visual inspection (Op 130); Grinding required if excessive (Op 140) | 4 | **L** | Add anti-spatter spray to standard procedure |
| 1.8 | 120 | Weld frame assembly per AWS D1.1 | **Weld distortion** (frame out of square/flat) | Local: Frame misalignment; Next: Assembly interference; Customer: Uneven operation, wheel alignment issues | 7 | Excessive heat input; Improper clamping | 5 | Weld fixture with clamping; WPS heat input limits | Dimensional check after welding; Square check +/-1 degree | 5 | **M** | Add distortion allowance to fixture design; Implement intermittent welding sequence |
| 1.9 | 120 | Weld frame assembly per AWS D1.1 | **Undersized fillet weld** | Local: Insufficient throat; Next: Reduced load capacity; Customer: Joint failure under normal use | 8 | Insufficient passes; Operator technique | 5 | WPS specifies min 1/8" fillet; Operator qualification | 100% fillet gauge inspection (Op 130) | 3 | **M** | Add fillet gauge to weld station; Operator self-check before moving to inspection |
| 1.10 | 130 | Inspect frame welds per AWS D1.1 | **Missed defect during inspection** | Local: Defective weld passes; Next: Frame shipped with defect; Customer: Field failure, warranty claim, injury potential | 8 | Inspector fatigue; Inadequate lighting | 4 | Certified weld inspector; Inspection checklist | No detection - this IS the detection step | 8 | **H** | Add secondary inspection for critical joints; Improve lighting at inspection station |

---

### Section 2: Auger Manufacturing - Flight Forming (Op 260-290)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 2.1 | 270 | Form helical flight Section 1 (P/D 0.6, pitch 3.3") | **Incorrect pitch** (pitch outside +/-0.1" tolerance) | Local: Improper material conveyance; Next: Mixing inefficiency; Customer: Slow throughput, poor mix quality | 7 | Die setting error | 5 | Die setup procedure; First article inspection | 100% pitch gauge measurement (Op 330); Flight forming log | 4 | **M** | Add pitch setting verification tool; Document die change procedure |
| 2.2 | 270 | Form helical flight Section 1 | **Incorrect pitch** | Local: Improper material conveyance; Next: Mixing inefficiency; Customer: Slow throughput, poor mix quality | 7 | Material feed rate variation | 5 | Material feed control on press; Operator training | 100% pitch gauge measurement (Op 330) | 4 | **M** | Add material feed rate indicator; Standardize material strip width |
| 2.3 | 270 | Form helical flight Section 1 (OD 5.5" +/-0.030") | **Oversized OD** (flight too large) | Local: Auger won't fit in chute; Next: Assembly failure; Customer: Production delay | 7 | Die wear; Incorrect die selection | 4 | Die inventory control; Die inspection schedule | 100% OD ring gauge check (Op 330); Go/no-go gauge | 3 | **M** | Add die wear tracking; Replace die at defined usage limit |
| 2.4 | 270 | Form helical flight Section 1 (OD 5.5" +/-0.030") | **Undersized OD** (flight too small) | Local: Excessive clearance in chute; Next: Material bypass/leakage; Customer: Reduced mixing efficiency, material waste | 6 | Die setting; Material springback | 5 | Die setup procedure; Springback compensation | 100% OD ring gauge check (Op 330) | 3 | **L** | Characterize material springback; Adjust die for compensation |
| 2.5 | 270 | Form helical flight Section 1 (ID 2.5" +/-0.030") | **Incorrect ID** (flight won't fit on shaft) | Local: Assembly failure; Next: Cannot complete auger; Customer: Production delay, scrap | 7 | Die setting error; Material variation | 4 | Die setup procedure; Material specification | 100% ID plug gauge check (Op 330) | 3 | **M** | Add ID verification to first article; Control material thickness variation |
| 2.6 | 280 | Form helical flight Section 2 (P/D 0.85, pitch 4.7") | **Incorrect pitch** (wrong transition ratio) | Local: Improper material acceleration; Next: Mixing zone inefficiency; Customer: Inconsistent mix, potential jams | 7 | Die setting error; Confusion with Section 1 dies | 5 | Separate die identification; Setup sheet verification | 100% pitch measurement (Op 330); Different gauge for Section 2 | 4 | **M** | Color-code Section 1 vs Section 2 dies; Add die selection checklist |
| 2.7 | 270/280 | Form helical flights | **Flight thickness variation** (thin spots) | Local: Weak flight sections; Next: Premature wear; Customer: Shortened auger life, replacement cost | 6 | Material thickness variation; Forming stress | 5 | Incoming material inspection (0.0747" +/-0.005"); Controlled forming parameters | Visual inspection; Thickness check at Op 330 | 5 | **L** | Add flight thickness minimum check; Specify forming limits |
| 2.8 | 290 | Weld flight sections together | **Incomplete weld at transition** | Local: Weak joint between sections; Next: Flight separation during operation; Customer: Auger failure, work stoppage, potential safety issue | 8 | Fit-up gap at transition; Insufficient penetration | 4 | Weld fixture for alignment; WPS for full penetration | Visual inspection 100%; Bend test monthly | 5 | **M** | Add transition joint fixture; Specify gap tolerance <1/16" |
| 2.9 | 290 | Weld flight sections together | **Discontinuity at pitch transition** | Local: Irregular flight profile; Next: Material flow disruption; Customer: Mixing inconsistency, potential jam point | 6 | Improper alignment of different pitch sections | 5 | Weld fixture positions sections; Alignment marks on flight | Visual inspection; Profile check with template | 5 | **L** | Add alignment scribe marks; Verify smooth transition |
| 2.10 | 270/280 | Form helical flights | **Flight distortion** (warped or twisted) | Local: Auger runout; Next: Chute contact; Customer: Noise, accelerated wear, binding | 7 | Uneven forming pressure; Material stress | 4 | Press calibration; Uniform material condition | Balance check (Op 340); Runout <0.030" | 4 | **M** | Add in-process straightening; Stress relief procedure if needed |

---

### Section 3: Auger Manufacturing - Finger Welding and Machining (Op 300-340)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 3.1 | 310 | Weld mixing fingers to flight (8-12 fingers, inward extending) | **Incorrect finger spacing** | Local: Uneven material breakup; Next: Mixing quality variation; Customer: Inconsistent mix, potential bridging | 6 | Template/fixture error; Operator judgment | 5 | Spacing template per patent design; Work instruction with dimensions | 100% template verification (Op 330); Visual inspection | 4 | **L** | Add laser marking on flight for finger positions |
| 3.2 | 310 | Weld mixing fingers to flight | **Incorrect finger angle** (perpendicular +/-5 deg) | Local: Improper material engagement; Next: Reduced mixing action; Customer: Poor mix quality | 5 | Welding technique; Finger positioning | 5 | Operator training; Angle specification in work instruction | 100% protractor check (Op 330) | 4 | **L** | Add angle fixture for finger welding; Go/no-go angle gauge |
| 3.3 | 310 | Weld mixing fingers to flight | **Cold weld on finger** (poor fusion) | Local: Finger detachment during operation; Next: Loose metal in mix; Customer: Concrete contamination, equipment damage | 8 | Insufficient heat input; Contaminated finger rod | 4 | WPS for finger welding; Clean finger stock | Visual inspection; Pull test (5 lbs) per sample | 5 | **M** | Add finger pull test to first article; 100% visual of finger weld roots |
| 3.4 | 310 | Weld mixing fingers to flight | **Missing finger(s)** | Local: Reduced mixing elements; Next: Lower mixing effectiveness; Customer: Inconsistent mix, customer complaint | 5 | Operator error; Count mistake | 4 | Work instruction specifies count (8-12); Visual reference photo | 100% count verification (Op 330) | 3 | **L** | Add count checklist; Photo of completed auger for reference |
| 3.5 | 320 | Machine drive coupling end (left-hand Acme thread) | **Thread form error** (incorrect profile) | Local: Coupling won't engage; Next: Motor cannot drive auger; Customer: Inoperable machine | 8 | Wrong threading tool; Incorrect lathe setup | 3 | Thread tool identification; Setup sheet for LH Acme | 100% thread gauge check (Op 330); Go/no-go gauge | 2 | **M** | Add thread form master for setup verification |
| 3.6 | 320 | Machine drive coupling end | **Thread pitch error** | Local: Cross-threading during assembly; Next: Damaged coupling or motor shaft; Customer: Assembly failure, warranty claim | 8 | Feed rate error; Tool wear | 3 | CNC program verified; Thread tool inspection | 100% thread gauge check (Op 330); Lead checking gauge | 3 | **M** | Add pitch verification to setup; Thread master check at shift start |
| 3.7 | 320 | Machine drive coupling end | **Wrong hand thread** (right-hand instead of left-hand) | Local: Thread loosens during operation; Next: Auger disengages from motor; Customer: Complete loss of function, safety hazard | 9 | Operator error; Wrong program | 2 | Program selection verification; Visual thread direction check | 100% thread engagement test (Op 330); Direction verification | 3 | **M** | Add left-hand thread verification sign at station; Color-code LH programs |
| 3.8 | 330 | Inspect auger assembly (critical inspection) | **Missed dimension during inspection** | Local: Out-of-spec auger shipped; Next: Assembly or performance failure; Customer: Field failure, warranty, safety | 8 | Inspector error; Incomplete checklist | 3 | Inspection checklist; Certified inspector | CMM verification on sample basis | 6 | **M** | Add CMM backup inspection 1/shift; Rotate inspectors to reduce fatigue |
| 3.9 | 340 | Balance check (runout <0.030" at 118 RPM) | **Excessive runout** not detected | Local: Unbalanced auger installed; Next: Vibration during operation; Customer: Noise, accelerated bearing wear, potential chute damage | 6 | Balance stand calibration; Incorrect measurement technique | 4 | Balance stand calibration schedule; Operator training | Runout measurement at Op 340; Functional test at Op 740 | 4 | **L** | Add runout acceptance mark on auger; Tighter tolerance for premium models |

---

### Section 4: Assembly Operations (Op 350-720)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 4.1 | 360 | Install drive coupling to motor (5/16"-18 Grade 8, 25 ft-lb) | **Under-torque** (bolts loose) | Local: Coupling loosens during operation; Next: Auger disconnect; Customer: Complete loss of function, potential safety issue | 8 | Torque wrench out of calibration; Operator error | 4 | Calibrated torque wrench (6-month cycle); Torque specification on work instruction | 100% torque verification; Torque record | 4 | **M** | Add torque audit program; Click-type wrench with lockout |
| 4.2 | 360 | Install drive coupling to motor | **Over-torque** (thread damage) | Local: Stripped threads; Next: Cannot secure coupling; Customer: Motor replacement required | 7 | Operator error; Wrong torque setting | 3 | Torque wrench with range marking; Training | Torque record review; Visual thread inspection | 5 | **M** | Use torque-limiting wrench; Add maximum torque warning |
| 4.3 | 360 | Install drive coupling to motor | **Coupling misalignment** (>0.010" TIR) | Local: Eccentric rotation; Next: Vibration, bearing wear; Customer: Noise, premature motor failure | 7 | Motor positioning error; Coupling runout | 4 | Dial indicator check specified; Alignment record | 100% alignment verification | 4 | **M** | Add self-centering coupling design; Alignment fixture |
| 4.4 | 440 | Install solenoid valve (flow direction orientation) | **Reversed solenoid installation** | Local: Valve won't open properly; Next: No water flow or backflow; Customer: Inoperable water system | 6 | Operator error; Arrow not visible | 4 | Flow arrow marked on valve; Work instruction with photo | 100% visual verification; Checklist | 4 | **L** | Add arrow direction verification to checklist; Asymmetric fitting design |
| 4.5 | 470 | Pressure test water system (30 PSI, 60 sec, no leaks) | **Leak at fitting** (undetected) | Local: Water loss; Next: Electrical hazard potential; Customer: Water on motor, safety concern | 7 | Improper assembly; Damaged fitting | 5 | Thread sealant procedure; Torque specification | 100% pressure test 60 seconds; Visual leak check | 3 | **M** | Add dye in test water for visibility; Extended pressure hold |
| 4.6 | 470 | Pressure test water system (max 145 PSI) | **Fitting failure at burst test** | Local: System damage; Next: Scrapped water assembly; Customer: (Not shipped - caught in test) | 6 | Defective fitting; Improper assembly | 3 | Incoming inspection of fittings; Assembly torque control | Burst test 1/lot at 145 PSI | 3 | **L** | Maintain burst test records; Supplier quality monitoring |
| 4.7 | 640 | Install auger into housing | **Auger installed backwards** | Local: Reverse conveyance direction; Next: Material feeds wrong way; Customer: Inoperable, material backup | 7 | Operator error; No keying feature | 3 | Coupling thread direction (LH) prevents backward install | Rotation check during motor test (Op 740) | 4 | **M** | Add orientation arrow on auger; Verify during assembly |
| 4.8 | 650 | Mount motor assembly (5/16"-18, 17 ft-lb) | **Under-torque motor bolts** | Local: Motor loosens; Next: Misalignment, vibration; Customer: Motor damage, auger binding, safety hazard | 8 | Torque wrench error; Operator skip | 4 | Calibrated torque wrench; Torque specification | 100% torque record; Torque audit | 4 | **M** | Add torque verification mark (paint dot); Include in final inspection |
| 4.9 | 650 | Mount motor assembly | **Missing motor bolt** | Local: Incomplete fastening; Next: Motor shift during operation; Customer: Catastrophic failure potential | 8 | Operator error; Hardware shortage | 3 | Hardware kit with correct count; Assembly checklist | 100% visual verification; Count verification | 4 | **M** | Add hardware count station; Pre-counted hardware kits |
| 4.10 | 650 | Mount motor assembly | **Wrong bolt grade used** | Local: Inadequate strength; Next: Bolt failure; Customer: Motor detachment, injury hazard | 9 | Mixed hardware inventory; Operator selection error | 2 | Grade 8 bolts specified; Hardware segregation | Head marking verification at assembly | 5 | **M** | Pre-kit hardware; Grade 8 only in assembly area |
| 4.11 | 660 | Install wheels/axle (5/8"-11 nylock, 135 ft-lb) | **Under-torque axle nut** | Local: Wheel loosens; Next: Wheel separation; Customer: Equipment tips, injury hazard | 8 | Torque wrench capability; Operator error | 4 | High-torque wrench (verified calibration); Specification on work instruction | 100% torque record; Torque verification | 4 | **M** | Add cotter pin or castle nut backup; Torque verification audit |
| 4.12 | 690 | Connect electrical system | **Incorrect wiring polarity** | Local: Motor runs wrong direction; Next: Reversed conveyance; Customer: Functional failure (detected at test) | 6 | Wire color coding error; Operator mistake | 3 | Wire color coding; Wiring diagram at station | 100% motor direction test (Op 740) | 3 | **L** | Add polarity test before motor mounting; Keyed connectors |
| 4.13 | 720 | Apply labels and decals | **Missing safety label** | Local: Warning not displayed; Next: Liability exposure; Customer: Potential injury, regulatory issue | 7 | Label shortage; Operator skip | 4 | Label kit per unit; Assembly checklist | 100% visual inspection; Checklist verification | 4 | **M** | Add label presence verification to final inspection; Photo reference |

---

### Section 5: Welded Assembly (Op 480-550)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 5.1 | 500 | Weld hopper to chute (aperture alignment, full penetration) | **Aperture misalignment** (>0.060" offset) | Local: Restricted material flow; Next: Bridging at transition; Customer: Jams, reduced throughput | 7 | Fixture wear; Improper clamping | 4 | Weld fixture with alignment pins; Fixture verification | 100% fixture check log; Dimensional verification (Op 540) | 4 | **M** | Add fixture wear inspection schedule; Alignment verification gauge |
| 5.2 | 500 | Weld hopper to chute | **Incomplete penetration at aperture** | Local: Weak joint at critical location; Next: Crack initiation; Customer: Structural failure, material leakage | 8 | Insufficient heat; Excessive gap | 4 | WPS for full penetration; Welder qualification | Visual inspection 100% (Op 540); Cut test monthly | 5 | **M** | Add radiographic inspection for qualification; Increase cut test frequency |
| 5.3 | 500 | Weld hopper to chute | **Weld distortion** (hopper/chute misaligned) | Local: Assembly out of specification; Next: Auger clearance issues; Customer: Binding, accelerated wear | 7 | Excessive heat; Improper sequence | 5 | Weld sequence defined; Fixture clamping | Dimensional check (Op 540); Assembly fit check | 5 | **M** | Add distortion monitoring; Anti-distortion clamps |
| 5.4 | 520 | Weld motor mount to hopper | **Motor mount not flat** (>0.030" warp) | Local: Motor misalignment; Next: Coupling stress; Customer: Vibration, premature wear, noise | 7 | Weld-induced distortion | 5 | Weld sequence specified; Backing plate | Straightedge check 100% (Op 540); Motor fit verification | 4 | **M** | Add back-welding sequence; Post-weld straightening allowance |
| 5.5 | 520 | Weld motor mount to hopper | **Hole pattern misalignment** (>0.010" error) | Local: Motor bolts don't fit; Next: Motor cannot be installed; Customer: Assembly failure | 7 | Fixture positioning; Weld shrinkage | 4 | Fixture with locating pins; Pre-weld verification | Pin gauge verification 100% (Op 540) | 3 | **M** | Add anti-shrinkage welding technique; Verify fixture monthly |
| 5.6 | 530 | Weld axle brackets to frame | **Incorrect bracket spacing** (not 27.5") | Local: Wheel alignment error; Next: Rolling resistance; Customer: Difficult transport, tracking issues | 6 | Measurement error; Fixture shift | 4 | Fixture sets spacing; Tape measure verification | Dimensional check (Op 540); Wheel fit verification | 4 | **L** | Add spacing gauge to fixture; Pre-weld measurement verification |
| 5.7 | 540 | Inspect all welds (AWS D1.3/D1.1) | **Defect passed at inspection** | Local: Defective weld accepted; Next: Product shipped with defect; Customer: Field failure, warranty, safety | 8 | Inspector fatigue; Difficult access areas | 4 | Certified inspector; AWS D1.3/D1.1 criteria | This IS detection - no further control | 7 | **H** | Add secondary inspection program; Improve inspection access/lighting |

---

### Section 6: Testing Operations (Op 730-780)

| Item | Op # | Process Step/Function | Potential Failure Mode | Potential Effect of Failure | S | Potential Cause/Mechanism | O | Current Process Controls - Prevention | Current Process Controls - Detection | D | AP | Recommended Actions |
|------|------|----------------------|------------------------|----------------------------|---|--------------------------|---|--------------------------------------|-------------------------------------|---|----|--------------------|
| 6.1 | 730 | Electrical safety test (ground continuity <0.1 ohm) | **Ground continuity failure not detected** | Local: Product with ground fault shipped; Next: Electrical shock hazard; Customer: Potential electrocution, death | 10 | Test equipment failure; Operator bypass | 2 | Hipot tester calibration (12-month); Mandatory test hold point | 100% test; Test log review; Equipment self-test | 2 | **H** | Add redundant ground test; Equipment verification at shift start |
| 6.2 | 730 | Electrical safety test (dielectric per UL) | **Hipot test false pass** | Local: Insulation defect not caught; Next: Product shipped with defect; Customer: Electrical shock, fire hazard | 10 | Test equipment malfunction; Improper test lead connection | 2 | Equipment calibration; Test procedure verification | 100% test; Equipment self-check; Calibration certificate | 3 | **H** | Add equipment function verification each shift; Secondary test sample |
| 6.3 | 730 | Electrical safety test | **Test bypassed or skipped** | Local: Untested product; Next: Unknown safety status; Customer: Potential shock hazard | 10 | Production pressure; Test station backup | 2 | Mandatory hold point; Traveler sign-off required | Traveler audit; Test log reconciliation | 4 | **H** | Add test station interlock - no packaging without test completion |
| 6.4 | 740 | Functional test - dry run (motor forward/reverse, 118 RPM +/-10%) | **Motor defect not detected** | Local: Defective motor installed; Next: Field failure; Customer: Inoperable product, warranty claim | 7 | Short test duration; Marginal defects | 4 | 60-second run test; Forward and reverse operation | 100% test; RPM measurement; Current monitoring | 4 | **M** | Extend test duration to 120 seconds; Add vibration monitoring |
| 6.5 | 740 | Functional test - dry run | **Speed out of specification not caught** | Local: Incorrect auger RPM; Next: Throughput variation; Customer: Reduced performance, customer complaint | 6 | Tachometer error; Recording mistake | 4 | Calibrated tachometer; Specified acceptance range (106-130 RPM) | 100% measurement; Test record | 4 | **L** | Add audible alarm on tachometer for out-of-range; Automated recording |
| 6.6 | 750 | Water system test (30 PSI, solenoid actuation) | **Water leak not detected** | Local: Leaking system shipped; Next: Water damage to motor; Customer: Electrical hazard, equipment damage | 7 | Test pressure too low; Short hold time | 4 | Specified test pressure and duration; Visual inspection | 100% pressure test; Visual leak check | 4 | **M** | Add leak indicator dye; Extend hold time to 90 seconds |
| 6.7 | 750 | Water system test | **Solenoid malfunction not detected** | Local: Faulty solenoid installed; Next: Water control failure; Customer: Cannot control water, mix quality issues | 6 | Intermittent defect; Short cycle test | 4 | On/off cycle test; Switch verification | 100% actuation test | 5 | **L** | Add multiple cycle test (10 on/off); Measure actuation time |
| 6.8 | 770 | Wet mix test (1 bag concrete, no jams) | **Inadequate wet test** (doesn't simulate actual use) | Local: Performance issues not found; Next: Field failures; Customer: Jams, poor mix quality | 7 | Test material not representative; Abbreviated test | 4 | Standard test material (1 bag); Test procedure defined | Test observation; Mix quality evaluation | 5 | **M** | Standardize test mix; Add throughput measurement; Rotate test materials |
| 6.9 | 770 | Wet mix test | **Wet test bypassed** | Local: Untested mixing function; Next: Performance unknown; Customer: Potential for field issues | 7 | Sample basis only (1/shift); Time pressure | 4 | 1/shift minimum; Traveler sign-off for tested units | Test log reconciliation; Supervisor verification | 5 | **M** | Increase wet test frequency to 1/10 units; Add wet test tracking |
| 6.10 | 780 | Final visual inspection | **Cosmetic defect missed** | Local: Defective appearance shipped; Next: Customer receives damaged-looking product; Customer: Return, complaint, brand damage | 5 | Inspector fatigue; Lighting; Rush | 5 | Inspection checklist; Acceptance criteria | 100% visual inspection | 5 | **L** | Add inspection lighting standard; Rotate inspectors; Photo standards |

---

## High Priority Action Summary

The following items have **Action Priority = HIGH (H)** and require immediate action:

### 1. Incomplete Fusion in Frame Welding (Items 1.3, 1.4) - Op 120

| Factor | Current | Target |
|--------|---------|--------|
| Severity | 9 | Cannot reduce (safety-critical) |
| Occurrence | 4 | Reduce to 2 |
| Detection | 5-6 | Improve to 3 |

**Recommended Actions:**
1. Implement weld parameter monitoring system (voltage, amperage, wire feed) with real-time display
2. Add pre-production weld coupons at shift start - destructive test verification
3. Add go/no-go gap gauge to fixture (max gap 1/16")
4. Increase monthly destructive testing to weekly during ramp-up
5. Add ultrasonic testing for critical frame joints (sample basis)

**Responsible:** Welding Engineering / Quality Engineering  
**Target Completion:** Within 90 days of production start

---

### 2. Missed Defect at Frame Weld Inspection (Item 1.10) - Op 130

| Factor | Current | Target |
|--------|---------|--------|
| Severity | 8 | Cannot reduce (quality escape) |
| Occurrence | 4 | Reduce to 3 |
| Detection | 8 | Improve to 4 |

**Recommended Actions:**
1. Implement secondary inspection for critical frame joints (100% by second inspector)
2. Improve lighting at inspection station to minimum 100 foot-candles
3. Add magnification option for weld inspection (3x loupe)
4. Rotate inspectors every 2 hours to reduce fatigue
5. Add weld inspection photos to inspection record for critical joints

**Responsible:** Quality Engineering  
**Target Completion:** Before production launch

---

### 3. Missed Defect at Welded Assembly Inspection (Item 5.7) - Op 540

| Factor | Current | Target |
|--------|---------|--------|
| Severity | 8 | Cannot reduce (quality escape) |
| Occurrence | 4 | Reduce to 3 |
| Detection | 7 | Improve to 4 |

**Recommended Actions:**
1. Add access openings/mirrors for difficult-to-inspect welds
2. Implement dual inspection sign-off for hopper-to-chute weld
3. Add weld bead template for critical weld profiles
4. Implement enhanced inspector training with defect samples
5. Add random re-inspection by quality engineer (10% of units)

**Responsible:** Quality Engineering / Manufacturing Engineering  
**Target Completion:** Before production launch

---

### 4. Electrical Safety Test Failures (Items 6.1, 6.2, 6.3) - Op 730

| Factor | Current | Target |
|--------|---------|--------|
| Severity | 10 | Cannot reduce (life safety) |
| Occurrence | 2 | Maintain |
| Detection | 2-4 | Maintain or improve |

**Recommended Actions:**
1. Add test station interlock - unit cannot proceed to packaging without electronic test completion record
2. Implement redundant ground continuity test (two separate measurements)
3. Add equipment function verification with known-good and known-bad reference samples at shift start
4. Add barcode/RFID tracking to link test records to serial numbers
5. Implement test data logging to networked system (prevents manual data entry errors)
6. Add secondary hipot test on 5% sample basis

**Responsible:** Quality Engineering / Test Engineering  
**Target Completion:** Before production launch (mandatory for safe launch)

---

## Medium Priority Action Summary

| Item | Process Step | Failure Mode | Primary Action | Responsible |
|------|--------------|--------------|----------------|-------------|
| 1.1/1.2 | Frame welding | Porosity | Add pre-weld surface cleanliness spec; gas flow verification | Welding Eng |
| 1.5/1.6/1.8 | Frame welding | Undercut/Cracks/Distortion | Document weld sequence; add travel speed reference | Welding Eng |
| 1.9 | Frame welding | Undersized fillet | Add fillet gauge to weld station; operator self-check | Manufacturing |
| 2.1/2.2 | Flight forming Sec 1 | Incorrect pitch | Add pitch setting verification tool | Manufacturing |
| 2.3/2.5 | Flight forming | Incorrect OD/ID | Add die wear tracking; replace at defined limit | Manufacturing |
| 2.6 | Flight forming Sec 2 | Incorrect pitch | Color-code Section 1 vs Section 2 dies | Manufacturing |
| 2.8/2.10 | Flight welding | Incomplete weld/distortion | Add transition joint fixture; alignment verification | Welding Eng |
| 3.3 | Finger welding | Cold weld | Add finger pull test to first article | Quality |
| 3.5/3.6/3.7 | Thread machining | Thread errors | Add thread form master; color-code LH programs | Manufacturing |
| 3.8 | Auger inspection | Missed dimension | Add CMM backup inspection 1/shift | Quality |
| 4.1/4.2/4.3 | Coupling install | Torque/alignment errors | Add torque audit program; alignment fixture | Quality |
| 4.5 | Pressure test | Leak undetected | Add dye in test water; extended pressure hold | Quality |
| 4.7 | Auger install | Backwards installation | Add orientation arrow on auger | Manufacturing |
| 4.8/4.9/4.10 | Motor mounting | Missing/wrong hardware | Pre-kit hardware; Grade 8 only in assembly area | Manufacturing |
| 4.11 | Wheel install | Under-torque | Add cotter pin backup; torque audit | Quality |
| 4.13 | Label application | Missing safety label | Add photo reference verification | Quality |
| 5.1-5.5 | Welded assembly | Alignment/penetration | Add fixture inspection schedule; cut test frequency | Welding Eng |
| 6.4 | Motor test | Defect not detected | Extend test to 120 seconds; add vibration monitoring | Test Eng |
| 6.6/6.8/6.9 | Water/wet test | Issues not detected | Add leak indicator dye; increase wet test frequency | Quality |

---

## Process Control Summary by Critical Characteristic

| Critical Characteristic | Control Plan Op # | PFMEA Coverage | Current Control Adequacy |
|------------------------|-------------------|----------------|-------------------------|
| Weld penetration (CC) | Op 120, 130 | Items 1.3, 1.4, 5.2 | Needs improvement - add monitoring |
| Weld defects - no cracks (CC) | Op 120, 130 | Items 1.6, 5.7 | Needs improvement - secondary inspection |
| Auger pitch P/D 0.6/0.85 (CC) | Op 270, 280 | Items 2.1, 2.2, 2.6 | Adequate with enhancements |
| Auger OD/ID (CC) | Op 270, 280 | Items 2.3, 2.4, 2.5 | Adequate |
| Drive coupling thread (CC) | Op 320 | Items 3.5, 3.6, 3.7 | Adequate with enhancements |
| Coupling bolt torque (CC) | Op 360 | Items 4.1, 4.2 | Adequate |
| Motor mounting torque (CC) | Op 650 | Items 4.8, 4.9 | Adequate |
| Water system leak-free (CC) | Op 470 | Items 4.5, 6.6 | Needs improvement - add dye |
| Dielectric/Ground (CC) | Op 730 | Items 6.1, 6.2, 6.3 | Needs improvement - add interlocks |
| Auger speed 118 RPM (CC) | Op 740 | Items 6.4, 6.5 | Adequate |
| Wet mix function (CC) | Op 770 | Items 6.8, 6.9 | Needs improvement - increase frequency |

---

## Document Control

| Rev | Date | Description | Author | Approved |
|-----|------|-------------|--------|----------|
| A | 2026-05-17 | Initial PFMEA Release | Manufacturing Engineering / Quality Engineering | ________ |

---

## Cross-References

- **Process Flow Diagram:** PFD-MM-001 Rev A
- **Control Plan:** CP-MM-001 Rev A (Pre-Launch)
- **Design FMEA:** DFMEA-MM-001 Rev A
- **AWS Standards:** D1.1 (Structural Steel), D1.3 (Sheet Steel)
- **AIAG-VDA FMEA Handbook:** 2019 Edition

---

## Approval Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Manufacturing Engineering Manager | | | |
| Quality Manager | | | |
| Welding Engineering | | | |
| Production Manager | | | |
| Plant Manager | | | |

---

*This Process FMEA is prepared in accordance with AIAG-VDA FMEA methodology and is a living document. It shall be reviewed and updated during pre-production, production launch, and whenever process changes occur.*
