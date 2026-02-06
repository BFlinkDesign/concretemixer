# Validated Specifications - MudMixer Reverse Engineering

> **Last Updated**: 2026-02-06
> **Data Sources**: Patents, OEM parts listings, manufacturer specs, forum reports, competitor analysis
> **Validation Level**: ★★★★★ = Confirmed from primary source | ★★★☆☆ = Calculated/Inferred | ★☆☆☆☆ = Estimated

---

## 1. PRODUCT LINE SPECIFICATIONS

### Model Comparison

| Spec | MMXR-3221 | MMXR-3225 (Evolution) | MudMixer Pro (2026) |
|------|-----------|----------------------|---------------------|
| Status | Discontinued | Current | NEW (WoC 2026) |
| Motor Power | 0.5 HP (373W) | 250W (IP55) | **1.5 HP** |
| Running Amps | 2.6 A | 1.6 A | TBD |
| Hopper Capacity | 120 lbs | 120 lbs | **250 lbs** |
| Throughput | 40-45 bags/hr | 45+ bags/hr | **3+ yd³/hr** |
| Wheels | 2 flat-free | 2 flat-free | **4 all-terrain** |
| Swivel | 330° | 330° | **360°** |
| Warranty | 1 year | 2 years | TBD |
| Price | ~$2,995 | ~$3,695 | TBD |

---

## 2. VALIDATED DIMENSIONS

### Overall Machine (★★★★★ Confirmed)

| Dimension | Value (in) | Value (mm) | Source |
|-----------|-----------|------------|--------|
| Overall Length | 66.5 | 1689 | MudMixer Specs |
| Overall Width | 27.5 | 699 | MudMixer Specs |
| Overall Height | 35 | 889 | MudMixer Specs |
| Dry Weight | 145 lbs | 66 kg | MudMixer Specs |
| Shipping Box 1 | 50 × 21 × 28 | 1270 × 533 × 711 | Home Depot |
| Shipping Box 2 | 31 × 17 × 6 | 787 × 432 × 152 | Home Depot |

### Auger Dimensions (★★★★☆ From Patent)

| Parameter | Value | Source | Confidence |
|-----------|-------|--------|------------|
| Auger OD | **2.5 inches** (2.25-3.25 range) | Patent 10,259,140 | ★★★★☆ |
| Auger Length | ~36 inches | Parts listing | ★★★☆☆ |
| Helix Direction | Right-handed | Patent 10,259,140 | ★★★★★ |
| Motor Coupling | **Left-Hand Acme Thread** | Patent 10,259,140 | ★★★★★ |
| Finger Count | **4 (preferred)** | Patent Claim | ★★★★☆ |
| Flight Thickness | ~3/16 inch | Industry standard | ★★★☆☆ |

### Pitch-to-Diameter Ratios (★★★★★ From Patents)

| Section | P/D Ratio Range | Preferred | Patent |
|---------|-----------------|-----------|--------|
| Hopper (1st body) | 0.2 - 0.9 | **0.4 - 0.6** | US 10,259,140 |
| Chute (2nd body) | 0.3 - 1.8 | **0.6 - 1.0** | US 11,285,639 |

### Chute Specifications (★★★★★ Confirmed)

| Parameter | Value | Source |
|-----------|-------|--------|
| Chute Length | 16-30 inches (16" standard) | Patent + Specs |
| Chute Angle | -5° to +30° declination | Patent |
| Pivot Positions | 3 (15°, 25°, 35°) | Product specs |
| Swivel Range | 330° (Evolution) | Product specs |
| Extension | +18 inches (MMAC-0133) | Accessory listing |

### Housing (★★☆☆☆ Estimated - CRITICAL GAP)

| Parameter | Estimated | Notes |
|-----------|-----------|-------|
| Housing ID | ~2.6-2.7 inches | Based on 2.5" auger + clearance |
| Clearance | 0.05-0.1 inch per side | CEMA standard = 0.5" total |
| Wall Thickness | 14 gauge (0.075") | Confirmed material |

---

## 3. MOTOR SPECIFICATIONS

### Confirmed Motor Data (★★★★★)

| Parameter | MMXR-3221 | MMXR-3225 | Source |
|-----------|-----------|-----------|--------|
| Part Number | MMXR-P209 | MMXR-P209B | Foards |
| Price | $867.51 | $867.51 | Foards |
| Power Rating | 0.5 HP (373W) | 250W | Specs |
| Input Voltage | 120V AC | 120V AC | Specs |
| Running Amps | 2.6 A | 1.6 A | Specs |
| Protection | Standard | IP55 (GFCI) | Specs |
| Operation | Forward/Reverse | Forward/Reverse | Specs |

### Calculated Motor Performance (★★★☆☆)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Auger Speed | ~118 RPM | Throughput / volume analysis |
| Output Torque | 95-129 N·m (70-95 ft-lb) | T = P / (2π × RPM / 60) |
| Gear Ratio | ~12:1 | 1400 RPM motor / 118 RPM output |

### Probable OEM Motor (★★★☆☆ Inferred)

| Parameter | Value |
|-----------|-------|
| Likely Manufacturer | Taibang Motor (VTV/GPG brand) |
| Probable Model | YN100-200 or 6IK250GN-SFT |
| Frame Size | 104mm × 104mm |
| Gearbox | 65mm spur/helical, 12:1 ratio |
| Output Shaft | 15mm diameter |

---

## 4. WATER SYSTEM SPECIFICATIONS

### Confirmed Parts (★★★★★)

| Part Number | Description | Specification | Price |
|-------------|-------------|---------------|-------|
| MMXR-P114 | Solenoid Valve | 3/8" Brass, 120V | $144.00 |
| MMXR-P118 | Flow Control | 3/8" Needle Valve | $64.46 |
| MMXR-P122 | Nozzle Adapter | 1/4" NPT Male | $24.54 |
| MMXR-P121 | Straight Adapter | 3/8" OD × 1/4" NPT | $30.54 |
| MMXR-P108 | Tubing | 3/8" OD × 34.25" | $7.83 |
| MMXR-P109 | Tubing | 3/8" OD × 7.28" | $10.64 |
| MMXR-P110 | Tubing | 3/8" OD × 5.9" | $8.63 |
| MMXR-P106 | 90° Elbow | 1/2" NPT Female Brass | $9.88 |
| MMXR-P113 | 90° Elbow | 3/8" NPT Quick Connect | $36.52 |

### Water System Specs (★★★★★)

| Parameter | Value | Source |
|-----------|-------|--------|
| Inlet Connection | 3/4" GHT (Garden Hose Thread) | Specs |
| Minimum Pressure | 30 PSI | Specs |
| Recommended Pressure | 40 PSI | Owner's Manual |
| Nozzle Count | 2 (dual spray) | Specs |
| Flow Control Range | 0-100 (dial scale) | Specs |
| Dial Setting (Concrete) | 35-50 | User Guide |

### Solenoid Valve Specs (★★★★☆)

| Parameter | Value |
|-----------|-------|
| Size | 3/8 inch |
| Material | Brass body |
| Type | Normally Closed, 2-way |
| Pressure Rating | Up to 145 PSI (10 bar) |
| Temperature Range | 15°F to 250°F |
| Seal Material | FKM (Viton) |
| Response Time | <1 second |

---

## 5. FRAME SPECIFICATIONS

### Materials (★★★★★ Confirmed)

| Component | Material | Specification |
|-----------|----------|---------------|
| Body/Hopper/Chute | 14-gauge steel | 0.0747" (1.9mm) |
| Frame Tubing | 1" steel pipe | Schedule 40 (1.315" OD, 0.133" wall) |
| Finish | Paint (not powder coat) | User reports |

### Frame Geometry (★★★★☆)

| Component | Specification |
|-----------|---------------|
| Frame Style | Wheelbarrow single-axle |
| Wheel Count | 2 (standard), 4 (Pro) |
| Handle | 1" steel tube, rubber grips |
| Stand-over Height | 35 inches |

### Welding Standards (★★★★☆)

| Standard | Application |
|----------|-------------|
| AWS D1.3 | Sheet steel (≤3/16") - applies to 14 gauge |
| AWS D1.1 Clause 9 | Tubular structures (pipe frame) |
| Minimum Fillet | 1/8" (for T ≤ 1/4") |
| Wire | ER70S-6, 0.023-0.030" |
| Gas | 75% Ar / 25% CO₂ |

---

## 6. WHEEL/TIRE SPECIFICATIONS

### Marathon Flat-Free Tire (★★★★★)

| Parameter | Value |
|-----------|-------|
| Model | Marathon 00210 |
| Tire Size | 4.10/3.50-4 |
| Diameter | 10-10.5 inches |
| Width | 3.3 inches |
| Material | Solid polyurethane foam |
| Tread | Sawtooth |
| Load Rating | 300 lbs per tire |

### Axle/Bearing (★★★★☆)

| Parameter | Value |
|-----------|-------|
| Axle Diameter | 5/8" (standard) |
| Bearing ID | 5/8" (3/4" adapter available) |
| Bearing OD | 1-3/8" |
| Bearing Type | Shielded ball bearing |
| Hub Offset | 2.25" (adjustable 3-7") |

---

## 7. ELECTRICAL SYSTEM

### Components (★★★★★ Confirmed)

| Part Number | Description | Price |
|-------------|-------------|-------|
| MMXR-P201 | GFCI Power Cord (3') | $52.64 |
| MMXR-P203 | Power Switch (DPDT FWD/OFF/REV) | $34.02 |
| MMXR-P209 | Electric Motor | $867.51 |

### Wiring Specs (★★★★☆)

| Parameter | Value |
|-----------|-------|
| Power Cord | 14 AWG, 3-conductor, SJTW |
| Cord Length | 3 feet |
| Plug Type | 3-prong grounded |
| Internal DC | 12V or 24V (via transformer) |
| Fuse | 15A fast-blow |

---

## 8. FASTENER SPECIFICATIONS

### Auger Pins (★★★★★ Confirmed)

| Part Number | Description | Price |
|-------------|-------------|-------|
| PCSAP001 | M5×60mm Quick-Release Pin | $13.13 |
| PCSAP002 | M2×30mm Clevis Pin | $13.13 |

### Frame Hardware (★★★☆☆ From BOM)

| Size | Grade | Quantity | Application |
|------|-------|----------|-------------|
| 1/4"-20 × 1" | Grade 5 | 20 | General assembly |
| 5/16"-18 × 1" | Grade 5 | 12 | Motor mounting |
| 3/8"-16 × 1.5" | Grade 5 | 8 | Heavy connections |
| 5/16"-18 × 1" | Grade 8 | 4 | Drive coupling |
| 5/8"-11 | Nylock | 4 | Axle nuts |

### Torque Specs (★★★★☆)

| Size | Grade 5 (Dry) | Grade 8 (Dry) |
|------|---------------|---------------|
| 1/4"-20 | 8 ft-lb | 12 ft-lb |
| 5/16"-18 | 17 ft-lb | 25 ft-lb |
| 3/8"-16 | 30 ft-lb | 45 ft-lb |
| 5/8"-11 | 135 ft-lb | 200 ft-lb |

---

## 9. PERFORMANCE DATA

### Throughput (★★★★☆ User Verified)

| Scenario | Bags/Hour | Notes |
|----------|-----------|-------|
| Manufacturer Claim | 45+ | Optimal conditions |
| User Verified | 38-45 | Continuous feeding |
| Typical Real-World | 25-40 | With pauses |
| Solo Operation | 16-25 | One person |
| Two-Person Crew | 35-45 | Optimal |
| Best Verified | 44.6 | 26 bags in 35 min |

### Material Compatibility (★★★★★)

| Material | Status |
|----------|--------|
| Concrete (≤1/2" aggregate) | ✅ YES |
| Mortar | ✅ YES |
| Stucco | ✅ YES |
| Grout | ✅ YES |
| Sand topping mix | ✅ YES |
| Self-leveling | ❌ NO |
| Air crete / Foam | ❌ NO |
| Epoxy products | ❌ NO |
| Straight Portland | ❌ NO |

---

## 10. MANUFACTURING DATA

### Contract Manufacturer (★★★★★)

| Parameter | Value |
|-----------|-------|
| Manufacturer | Prince Manufacturing |
| Location | Ciudad Juarez, Mexico |
| Phone | +52 656-688-0600 |
| Certifications | ISO 9001:2015, ISO 14001, TS 16949 |
| Capabilities | Laser cutting, stamping, welding, powder coating, assembly |

### Company Info (★★★★★)

| Parameter | Value |
|-----------|-------|
| Company | MudMixer, LLC (fka Red Dog Mobile Shelters) |
| Founded | 2018 |
| HQ | Lubbock, TX |
| Phone | (806) 515-4683 |
| Recognition | Inc. 5000 #340 (2025) |

---

## 11. PATENT REFERENCES

### US 10,259,140 B1 (★★★★★)

| Field | Value |
|-------|-------|
| Title | Portable concrete mixer for hydrating and mixing concrete mix containing gravel aggregate in a continuous process |
| Filed | October 19, 2018 |
| Issued | April 16, 2019 |
| Inventors | Dirk Derose, Oscar T. Scott IV |
| Assignee | Red Dog Mobile Shelters, LLC |

**Key Claims:**
- Shaftless helical auger with inward-extending fingers
- Variable pitch (lower in hopper, higher in chute)
- Left-hand Acme thread motor coupling
- Aperture finger at hopper/chute transition

### US 11,285,639 B2 (★★★★★)

| Field | Value |
|-------|-------|
| Title | Portable mixer for hydrating and mixing cementitious mix in a continuous process |
| Filed | January 30, 2020 |
| Issued | March 29, 2022 |
| Inventors | Rick Scott, Tim Gragson, Randy Lacy |

**Key Claims:**
- Pivot range ≥240 degrees
- Hopper lift height <42 inches
- P/D ratio 0.6-1.0 for chute section

---

## 12. CAD/3D MODEL RESOURCES

### Available CAD Downloads

| Component | Source | Format |
|-----------|--------|--------|
| Shaftless Spiral Conveyor | GrabCAD | STEP, SLDPRT |
| 3/8" Brass Solenoid | McMaster-Carr | STEP, SLDPRT |
| 250W DC Gear Motor | GrabCAD | STEP, SLDPRT |
| Clevis Pins (ISO 2341) | TraceParts | STEP, IGES |
| 1" Steel Tube | McMaster-Carr | STEP |
| KWS Screw Conveyor Parts | TraceParts | Multiple |

### Parametric Generators

| Tool | Platform | Use Case |
|------|----------|----------|
| threads-scad | OpenSCAD | Auger thread generation |
| BOSL2 thread_helix() | OpenSCAD | Custom flight profiles |
| MCAD auger() | OpenSCAD | Basic auger geometry |

### AI 3D Reconstruction

| Tool | Best For | Output |
|------|----------|--------|
| Rodin Gen-2 | Product photos | FBX, GLB, OBJ |
| Meta SAM 3D | Single images | Mesh + texture |
| Tripo AI | Fast iteration | Multiple formats |

---

## 13. KNOWN ISSUES & DESIGN FLAWS

### Critical Issues (★★★★★ User Reports)

| Issue | Description | Workaround |
|-------|-------------|------------|
| Water not linked to motor | Water continues during jams | Manual valve shutoff |
| Hopper clogging | Material bridges in hopper | Constant agitation |
| Large aggregate jam | >1/2" aggregate causes jams | Use compliant mixes only |
| Inconsistent water dial | Flow varies without dial change | Ensure 40+ PSI supply |

### Design Limitations

| Limitation | Impact |
|------------|--------|
| Cannot pause mid-pour | Must clean if stopped |
| Two-person optimal | Solo operation slower |
| No speed control | Fixed ~118 RPM |
| Water pressure dependent | Needs 30+ PSI |

---

## Sources

- [MudMixer Specifications](https://mudmixer.com/pages/specs)
- [MudMixer Support](https://mudmixer.com/pages/support)
- [US Patent 10,259,140](https://patents.google.com/patent/US10259140B1)
- [US Patent 11,285,639](https://patents.google.com/patent/US11285639B2)
- [Foards Parts](https://www.foards.com/pages/mud-mixer-parts-mmxr-3221)
- [Home Depot MMXR-3221](https://www.homedepot.com/p/330432979)
- [Home Depot MMXR-3225](https://www.homedepot.com/p/335811481)
- [Prince Manufacturing](https://princemanufacturing.com/)
- [KWS Shaftless Design Standards](https://www.kwsmfg.com/engineering-guides/shaftless-screw-conveyor/)
- [GrabCAD Library](https://grabcad.com/library)
- [TraceParts](https://www.traceparts.com)
