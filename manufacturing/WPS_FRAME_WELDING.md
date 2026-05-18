# Welding Procedure Specification (WPS)
## MudMixer Frame Assembly

> **Standard**: AWS D1.1 Structural Welding Code - Steel  
> **Reference**: CALC-STRUCT-001 (Weld sizing per Section 6.2)  
> **Document**: WPS-MM-001  
> **Date**: 2026-05-17

---

## 1. SCOPE

This WPS covers all structural welds on the MudMixer portable concrete mixer frame assembly, including:
- Frame tube-to-tube joints
- Motor mount attachment
- Axle supports
- Handle attachments
- Hopper support structure

---

## 2. BASE METAL SPECIFICATION

| Property | Value | Reference |
|----------|-------|-----------|
| Material | ASTM A513 Type 1020 | Frame tubes |
| Form | ERW mechanical tubing | 1-1/4" Sch 40 |
| OD | 1.660" (42.2 mm) | AISC Manual |
| Wall | 0.140" (3.56 mm) | Schedule 40 |
| Yield Strength | 50,000 psi min | ASTM A513 |
| Tensile Strength | 55,000 psi min | ASTM A513 |
| Carbon Equivalent | 0.35 max (typical) | No preheat required |

---

## 3. FILLER METAL SPECIFICATION

| Parameter | Value |
|-----------|-------|
| AWS Classification | ER70S-6 |
| Diameter | 0.030" (0.8 mm) or 0.035" (0.9 mm) |
| Supplier | Lincoln Electric, Hobart, or equivalent |
| Storage | Per AWS A5.18 |

**ER70S-6 Properties:**
- Tensile: 70,000 psi min
- Yield: 58,000 psi min
- Elongation: 22% min
- CVN: 20 ft-lb @ 0°F

---

## 4. SHIELDING GAS

| Parameter | Value |
|-----------|-------|
| Type | 75% Argon / 25% CO2 (C25) |
| Alternative | 90% Argon / 10% CO2 (C10) |
| Flow Rate | 25-35 CFH (12-17 L/min) |
| Purity | 99.95% min (welding grade) |

---

## 5. WELDING PROCESS

| Parameter | Value |
|-----------|-------|
| Process | GMAW (MIG) |
| Mode | Short-circuit transfer |
| Position | All positions (1G, 2G, 3G, 4G, 5G, 6G) |
| Progression | Uphill for vertical |

---

## 6. JOINT DESIGNS AND WELD SIZES

### 6.1 Frame Tube Joints (Per CALC-STRUCT-001)

| Joint Location | Type | Weld Size | Minimum Leg |
|----------------|------|-----------|-------------|
| Main frame joints | Fillet | 3/16" | 4.8 mm |
| Cross member connections | Fillet | 3/16" | 4.8 mm |
| Handle attachments | Fillet | 3/16" | 4.8 mm |
| Leg/axle supports | Fillet | 3/16" | 4.8 mm |
| Motor mount plate | Fillet | 1/4" | 6.4 mm |

### 6.2 Fillet Weld Details

```
          Tube A
            ↓
         ╱─────╲
        │       │
  ======│═══════│======  ← Tube B
        │   ↑   │
         ╲─┼───╱
           │
           │
    ┌──────┴──────┐
    │  Fillet     │
    │  Weld       │
    │  3/16"      │
    │  (4.8mm)    │
    └─────────────┘

Weld around full circumference
where tubes intersect (cope joint)
```

### 6.3 Minimum Weld Sizes per AWS D1.1 Table 5.8

| Base Metal Thickness | Min Fillet Size |
|---------------------|-----------------|
| ≤ 1/4" (6.4 mm) | 1/8" (3.2 mm) |
| > 1/4" to 1/2" | 3/16" (4.8 mm) |
| > 1/2" to 3/4" | 1/4" (6.4 mm) |

**Note:** 0.140" wall requires minimum 1/8" fillet; 3/16" specified provides SF margin.

---

## 7. WELDING PARAMETERS

### 7.1 Short-Circuit GMAW (0.035" wire)

| Position | Voltage | WFS | Amperage | CTWD |
|----------|---------|-----|----------|------|
| Flat (1G) | 18-20V | 200-250 IPM | 120-150A | 1/2"-5/8" |
| Horizontal (2G) | 17-19V | 180-230 IPM | 110-140A | 1/2"-5/8" |
| Vertical Up (3G) | 17-18V | 150-200 IPM | 100-130A | 3/8"-1/2" |
| Overhead (4G) | 17-18V | 150-200 IPM | 100-130A | 3/8"-1/2" |

### 7.2 Parameters for 0.030" Wire

| Position | Voltage | WFS | Amperage | CTWD |
|----------|---------|-----|----------|------|
| Flat (1G) | 17-19V | 250-300 IPM | 100-130A | 3/8"-1/2" |
| All other | 16-18V | 200-280 IPM | 90-120A | 3/8"-1/2" |

---

## 8. PREHEAT AND INTERPASS TEMPERATURE

| Condition | Temperature |
|-----------|-------------|
| Preheat | Not required (CE < 0.40) |
| Minimum interpass | 50°F (10°C) |
| Maximum interpass | 400°F (204°C) |

**Note:** If ambient temperature < 32°F (0°C), preheat to 70°F (21°C) minimum.

---

## 9. TECHNIQUE

### 9.1 Joint Preparation
1. Clean joint area to bright metal (wire brush, grinder, or solvent)
2. Remove mill scale, rust, oil, paint within 1" of joint
3. Fit-up gap: 0 to 1/16" (0-1.6 mm) maximum
4. Tack welds: Minimum 1" long, spaced 3-4" apart

### 9.2 Welding Technique
1. Stringer beads preferred (no weave > 3x wire diameter)
2. Maintain 15-20° drag angle (push for flat, drag for vertical)
3. Work angle: 45° for fillet welds
4. Travel speed: 8-15 IPM depending on position
5. Clean between passes if multiple passes required

### 9.3 Multi-Pass Welds
For 1/4" fillet welds on motor mount:
- Pass 1: Root pass, fill gap
- Pass 2: Cap pass to achieve full leg size

---

## 10. VISUAL INSPECTION CRITERIA (AWS D1.1)

### 10.1 Acceptable

| Attribute | Requirement |
|-----------|-------------|
| Cracks | None |
| Fusion | Complete |
| Crater | Filled |
| Profile | Convex or flat |
| Undercut | ≤ 1/32" (0.8 mm) |
| Porosity | ≤ 3/8" diameter, ≤ 1" spacing |
| Leg size | ≥ specified (3/16" or 1/4") |

### 10.2 Unacceptable

- Any cracks
- Incomplete fusion
- Unfilled craters
- Excessive convexity (> 1/8" above flush)
- Undercut > 1/32"
- Overlap
- Insufficient leg size

---

## 11. REPAIR PROCEDURE

1. Mark defect boundaries
2. Remove defect by grinding to sound metal
3. Feather edges (no sharp notches)
4. Re-weld per this WPS
5. Re-inspect per Section 10

---

## 12. WELDER QUALIFICATION

Welders shall be qualified per AWS D1.1 Section 4:
- Test position: 3G (covers all positions for fillet welds)
- Test specimen: 3/8" plate, fillet weld
- Visual and macro etch examination

---

## 13. RECORDS

Maintain records of:
- Welder qualifications (WPQ)
- Filler metal certifications
- Shielding gas certifications
- Inspection reports

---

## 14. APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Prepared By | | | |
| Welding Engineer | | | |
| Quality Manager | | | |

---

## APPENDIX A: WELD SYMBOL REFERENCE

```
Standard AWS Weld Symbols for Drawings:

Fillet Weld (3/16"):
    ─────┬─────
         │╲3/16
         │

Fillet Weld Both Sides (3/16"):
    3/16╱│
    ────┼────
        │╲3/16

All-Around Symbol:
    ─────○─────
         │╲3/16
```

---

## APPENDIX B: QUICK REFERENCE CARD

```
┌───────────────────���────────────────────────┐
│     MUDMIXER FRAME WELDING - QUICK REF     │
├────────��─────────────────────────────��─────┤
│ Process:    GMAW (MIG)                     │
│ Wire:       ER70S-6, 0.035"                │
│ Gas:        75/25 Ar/CO2, 30 CFH           │
│ Volts:      17-20V                         │
│ WFS:        180-250 IPM                    │
│ CTWD:       3/8" - 5/8"                    │
├─────────────────���──────────────────────────┤
│ Weld Sizes:                                │
│   Frame joints:  3/16" fillet              │
│   Motor mount:   1/4" fillet               │
├────────────────────────────────────────────┤
│ Inspect For:                               │
│   ✓ No cracks                              │
│   ✓ Full fusion                            │
│   ✓ Filled craters                         │
│   ✓ Correct leg size                       │
│   ✓ No undercut > 1/32"                    │
└────────���──────────────────────────────────��┘
```
