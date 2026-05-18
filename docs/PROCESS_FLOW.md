# Process Flow Diagram - MudMixer Concrete Mixer

**Document Number:** PFD-MM-001  
**Revision:** A  
**Date:** 2026-05-17  
**Product:** MudMixer MMXR-3225 Continuous Concrete Mixer  
**Prepared By:** Manufacturing Engineering  
**AIAG Reference:** APQP Manual, Section 3.3

---

## Process Flow Legend

| Symbol | Process Type | Description |
|--------|--------------|-------------|
| O | Operation | Value-added processing step |
| => | Transport | Movement of material between stations |
| [] | Inspection | Quality verification point |
| D | Delay | Waiting/staging period |
| V | Storage | Inventory holding point |

---

## Process Flow Diagram

| Op # | Process Type | Operation Description | Equipment/Workstation | Key Process Parameters |
|------|--------------|----------------------|----------------------|------------------------|
| **RECEIVING & INSPECTION** |||||
| 10 | V | Raw Material Receiving - Steel | Receiving Dock | Verify material certs, heat numbers |
| 20 | [] | Incoming Inspection - Steel Sheet & Tube | QC Lab | 14 ga sheet: 0.0747" +/-0.005"; 1" pipe: Schedule 40 |
| 30 | V | Raw Material Receiving - Purchased Components | Receiving Dock | Verify P.O., packing slip, quantities |
| 40 | [] | Incoming Inspection - Motors, Valves, Wheels | QC Lab | Motor: 250W IP55; Solenoid: 3/8" brass 120V |
| 50 | V | Raw Material Storage | Warehouse | FIFO inventory management |
| **FRAME FABRICATION** |||||
| 60 | => | Transport Steel Tube to Cutting | Forklift/Cart | Material handling per traveler |
| 70 | O | Cut Frame Tubes to Length | Tube Saw / Cold Cut Saw | Main frame: 66.5" total; Cross members: 27.5"; Handles: 36" ea |
| 80 | [] | Inspect Cut Lengths | Measuring Station | Length +/-0.125"; Square cut +/-1 degree |
| 90 | O | Bend Handle Tubes | Tube Bender | Bend angle per drawing; Min bend radius 3x OD |
| 100 | O | Notch Tube Ends (Cope) | Notcher / Hole Saw | Notch profile per mating tube |
| 110 | O | Drill Axle Bracket Holes | Drill Press | 5/8" dia for axle; Location per drawing |
| 120 | O | Weld Frame Assembly | MIG Welder | AWS D1.1 Clause 9; ER70S-6 wire; 75/25 Ar/CO2 |
| 130 | [] | Inspect Frame Welds | Weld Station | Visual per AWS D1.1; Min fillet 1/8" |
| 140 | O | Grind Welds (as required) | Angle Grinder | Smooth transition; No undercut |
| **SHEET METAL FABRICATION** |||||
| 150 | => | Transport Steel Sheet to Laser | Forklift | 14 ga sheet steel |
| 160 | O | Laser Cut Hopper Blank | Fiber Laser | Cutting speed per material; Edge quality <Ra 6.3 |
| 170 | O | Laser Cut Chute Blank | Fiber Laser | 6" developed width; 20" length |
| 180 | O | Laser Cut Motor Mount Plate | Fiber Laser | 1/4" plate; Hole pattern per motor spec |
| 190 | O | Laser Cut Pivot Plates | Fiber Laser | 1/4" x 6" x 6"; Center hole 1/2" |
| 200 | [] | Inspect Laser Cut Parts | QC Station | Dimensions +/-0.010"; Edge burr <0.015" |
| 210 | O | Form Hopper Body | Press Brake | Bend sequence per setup sheet; Spring-back compensated |
| 220 | O | Form Chute Tube | Plate Roll | 6" ID; Seam alignment for welding |
| 230 | O | Roll Hopper Rim Edge | Bead Roller | 3/8" rod welded to rolled edge |
| 240 | [] | Inspect Formed Parts | QC Station | Profile per template; Dimensions +/-0.030" |
| **AUGER MANUFACTURING** |||||
| 250 | => | Transport Auger Material | Cart | Steel strip for flight fabrication |
| 260 | O | Cut Auger Flight Blanks | Plasma / Laser | ID 2.5"; OD 5.5"; Section lengths per design |
| 270 | O | Form Helical Flight - Section 1 | Flight Forming Press | P/D ratio 0.6; Pitch 3.3"; Hopper section ~10" |
| 280 | O | Form Helical Flight - Section 2 | Flight Forming Press | P/D ratio 0.85; Pitch 4.7"; Chute section ~14" |
| 290 | O | Weld Flight Sections Together | MIG Welder | Continuous flight; Smooth transition zone |
| 300 | O | Cut/Form Auger Fingers | Press / Shear | 3/8" x 2" steel rod; 8-12 fingers |
| 310 | O | Weld Fingers to Flight | MIG Welder | Inward extending; Spacing per patent design |
| 320 | O | Machine Drive Coupling End | Lathe / Mill | Left-hand Acme thread per motor interface |
| 330 | [] | **CRITICAL: Inspect Auger Assembly** | QC Station | Pitch: +/-0.1"; OD: 5.5" +/-0.030"; Finger angle +/-5 deg |
| 340 | O | Balance Check (if required) | Balancing Stand | Runout <0.030" at 118 RPM |
| **MOTOR SUBASSEMBLY** |||||
| 350 | => | Transport Motor to Assembly | Cart | Motor MMXR-P209B |
| 360 | O | Install Drive Coupling to Motor | Assembly Bench | Torque 5/16"-18 Grade 8 bolts to 25 ft-lb |
| 370 | O | Connect Wiring Harness | Assembly Bench | Wire routing per diagram; Crimp connections |
| 380 | O | Install GFCI Power Cord | Assembly Bench | 14 AWG, 3-conductor SJTW; 3 ft length |
| 390 | O | Install Forward/Reverse Switch | Assembly Bench | DPDT switch; Weatherproof housing |
| 400 | [] | **CRITICAL: Test Motor Subassembly** | Test Stand | Forward/Reverse operation; Current 1.6A; GFCI trip test |
| **WATER SYSTEM ASSEMBLY** |||||
| 410 | => | Transport Water Components | Cart | Valves, tubing, fittings |
| 420 | O | Assemble Inlet Fitting | Assembly Bench | 3/4" GHT brass fitting; Thread sealant |
| 430 | O | Install Flow Control Valve | Assembly Bench | 3/8" needle valve; Dial graduated 0-100 |
| 440 | O | Install Solenoid Valve | Assembly Bench | 3/8" brass, 120V; Orientation per flow arrow |
| 450 | O | Cut and Route Supply Tubing | Assembly Bench | 3/8" OD tubing; Lengths 34.25", 7.28", 5.9" |
| 460 | O | Install Spray Nozzles | Assembly Bench | 2 nozzles; 1/4" NPT; 65 deg fan pattern |
| 470 | [] | **CRITICAL: Pressure Test Water System** | Test Stand | 30 PSI min; 145 PSI max; No leaks |
| **WELDED ASSEMBLY** |||||
| 480 | => | Transport Subassemblies to Weld Cell | Overhead Crane/Cart | Frame, hopper, chute, pivot plates |
| 490 | O | Fixture Hopper to Chute | Weld Fixture | Aperture alignment; Rigid coupling |
| 500 | O | Weld Hopper to Chute | MIG Welder | AWS D1.3 per 14 ga; Full penetration at aperture |
| 510 | O | Install Pivot Assembly | Weld Fixture | Fixed plate to frame; Moving plate to chute |
| 520 | O | Weld Motor Mount to Hopper | MIG Welder | 1/4" plate; 4-corner mount pattern |
| 530 | O | Weld Axle Brackets to Frame | MIG Welder | Position for 27.5" width; 5/8" axle clearance |
| 540 | [] | **CRITICAL: Inspect All Welds** | Weld Station | Visual per AWS D1.3/D1.1; Dimensional check |
| 550 | O | Grind and Finish Welds | Angle Grinder | Smooth surfaces; Prep for paint |
| **SURFACE FINISHING** |||||
| 560 | => | Transport to Paint/Coat Area | Overhead Conveyor | Cleaned weldment |
| 570 | O | Surface Preparation | Blast Cabinet / Chemical | Remove mill scale, oil, contaminants |
| 580 | O | Apply Primer | Spray Booth | Rust-preventive primer; 1.0-1.5 mil DFT |
| 590 | D | Primer Cure | Drying Area | Per primer spec; Typically 30-60 min |
| 600 | O | Apply Topcoat | Spray Booth | Enamel or powder coat; 2.0-3.0 mil DFT |
| 610 | D | Topcoat Cure | Oven / Drying Area | Per coating spec |
| 620 | [] | Inspect Coating | QC Station | Coverage 100%; Adhesion per tape test; DFT per spec |
| **FINAL ASSEMBLY** |||||
| 630 | => | Transport to Final Assembly | Cart | Painted weldment, all subassemblies |
| 640 | O | Install Auger into Housing | Assembly Station | Insert from chute end; Engage drive coupling |
| 650 | O | **CRITICAL: Mount Motor Assembly** | Assembly Station | 5/16"-18 bolts; Torque 17 ft-lb; Coupling engagement verified |
| 660 | O | Install Wheels and Axle | Assembly Station | Marathon flat-free 10"; 5/8"-11 nylock nuts torque 135 ft-lb |
| 670 | O | Install Handle Grips | Assembly Station | Rubber grips on 1" tube handles |
| 680 | O | Install Water System to Hopper | Assembly Station | Nozzle positioning into chute; Tubing routing |
| 690 | O | Connect Electrical System | Assembly Station | Motor to switch to cord; Ground continuity |
| 700 | O | Install Support Rests/Feet | Assembly Station | 4 rubber-padded feet; Level positioning |
| 710 | O | Install Guards and Safety Covers | Assembly Station | Auger guard hinged; Latch functional |
| 720 | O | Apply Labels and Decals | Assembly Station | Warning labels; Safety decals; Serial number plate |
| **TESTING & INSPECTION** |||||
| 730 | [] | **CRITICAL: Electrical Safety Test** | Test Station | Ground continuity <0.1 ohm; Dielectric per UL |
| 740 | [] | **CRITICAL: Functional Test - Dry Run** | Test Station | Motor forward/reverse; Auger rotation smooth; 118 RPM +/-10% |
| 750 | [] | **CRITICAL: Water System Test** | Test Station | Flow at 40 PSI; Solenoid actuation; Dial 0-100 |
| 760 | [] | Swivel and Tilt Test | Test Station | 330 deg rotation; 3 tilt positions lock |
| 770 | [] | **CRITICAL: Wet Mix Test (Sample)** | Test Area | 1 bag concrete; Mix quality; No jams |
| 780 | [] | Final Visual Inspection | QC Station | Appearance; Completeness; No defects |
| 790 | O | Touch-up Paint (if required) | Touch-up Station | Match color; Cover scratches |
| **PACKAGING** |||||
| 800 | => | Transport to Packaging | Cart | Completed, tested unit |
| 810 | O | Install Shipping Protection | Packaging Station | Foam, cardboard protectors |
| 820 | O | Prepare Accessories Kit | Packaging Station | Hardware, manual, warranty card |
| 830 | O | Pack Unit - Box 1 | Packaging Station | Main unit; 50" x 21" x 28" |
| 840 | O | Pack Accessories - Box 2 | Packaging Station | Handles, hardware; 31" x 17" x 6" |
| 850 | O | Label Boxes | Packaging Station | Shipping labels; Handling instructions |
| 860 | [] | Final Packaging Inspection | QC Station | Complete; Secure; Labels correct |
| 870 | V | Finished Goods Storage | Warehouse | FIFO; Climate controlled |
| 880 | => | Ship to Customer | Shipping Dock | LTL/Parcel per order |

---

## Process Flow Summary

| Process Category | Operation Count | Inspection Points | Critical Operations |
|-----------------|-----------------|-------------------|---------------------|
| Receiving & Inspection | 5 | 2 | - |
| Frame Fabrication | 9 | 2 | Op 120, 130 (Welding) |
| Sheet Metal Fabrication | 10 | 2 | - |
| Auger Manufacturing | 10 | 1 | Op 330 (Auger Inspection) |
| Motor Subassembly | 6 | 1 | Op 400 (Motor Test) |
| Water System Assembly | 7 | 1 | Op 470 (Pressure Test) |
| Welded Assembly | 8 | 1 | Op 540 (Weld Inspection) |
| Surface Finishing | 7 | 1 | - |
| Final Assembly | 10 | 0 | Op 650 (Motor Mount) |
| Testing & Inspection | 8 | 7 | Op 730, 740, 750, 770 |
| Packaging | 9 | 1 | - |
| **TOTAL** | **89** | **19** | **10** |

---

## Critical Path Operations

The following operations are on the critical path and require special attention:

1. **Op 120/130** - Frame Welding and Inspection (AWS D1.1)
2. **Op 270/280** - Auger Flight Forming (Pitch-to-Diameter ratios)
3. **Op 330** - Auger Assembly Inspection (Critical dimensions)
4. **Op 400** - Motor Subassembly Test (Electrical safety)
5. **Op 470** - Water System Pressure Test (Leak-free operation)
6. **Op 540** - Welded Assembly Inspection (Structural integrity)
7. **Op 650** - Motor Mounting (Drive coupling alignment)
8. **Op 730-770** - Final Testing (Product performance)

---

## Document Control

| Rev | Date | Description | Author | Approved |
|-----|------|-------------|--------|----------|
| A | 2026-05-17 | Initial Release | Mfg Eng | ________ |

---

*This Process Flow Diagram is prepared in accordance with AIAG APQP requirements and serves as the foundation for the Control Plan.*
