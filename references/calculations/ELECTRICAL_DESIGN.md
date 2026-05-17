# Concrete Mixer Electrical Design Specification
## 120V AC, 15A Circuit - NEC 2023 Compliant

---

## 1. MOTOR CIRCUIT CALCULATIONS

### 1.1 Motor Selection Basis
- **Motor Power Range:** 250-500W (0.33-0.67 HP)
- **Design Basis:** 500W (worst case for sizing)
- **Voltage:** 120V AC, Single Phase
- **Assumed Power Factor:** 0.85 (typical for small AC motors)

### 1.2 Full Load Amps (FLA) Calculation

```
FLA = P / (V × PF × η)
Where:
  P = 500W
  V = 120V
  PF = 0.85
  η = 0.80 (assumed motor efficiency)

FLA = 500 / (120 × 0.85 × 0.80)
FLA = 500 / 81.6
FLA = 6.13A (use 6.5A for calculations with margin)
```

**Note:** Always verify FLA from motor nameplate. NEC 430.6(A)(1) requires using nameplate FLA for overload protection.

### 1.3 Wire Sizing per NEC Table 310.16

| Circuit | Load (A) | Min AWG (60°C) | Selected AWG | Ampacity |
|---------|----------|----------------|--------------|----------|
| Motor Circuit | 6.5A | 14 AWG (15A) | **12 AWG** | 20A |
| Control Circuit | <1A | 18 AWG | **14 AWG** | 15A |
| Solenoid Circuit | 2.5A inrush | 14 AWG | **14 AWG** | 15A |

**Selection Rationale:**
- 12 AWG selected for motor circuit to minimize voltage drop and provide headroom
- Per NEC 240.4(D), 14 AWG max OCPD = 15A, 12 AWG max OCPD = 20A
- 12 AWG provides 25A ampacity at 90°C (SOOW rating) per Table 310.16

### 1.4 Voltage Drop Calculation (10' Cord Length)

```
VD = (2 × L × I × R) / 1000

Where:
  L = 10 feet (one-way length)
  I = 6.5A (motor FLA)
  R = Resistance per 1000 ft

For 12 AWG Copper:
  R = 1.588 Ω/1000 ft
  VD = (2 × 10 × 6.5 × 1.588) / 1000
  VD = 0.206V

Voltage Drop % = (0.206 / 120) × 100 = 0.17%
```

**Result:** 0.17% voltage drop - ACCEPTABLE (NEC recommends <3% for branch circuits, <5% total)

For 14 AWG Copper (comparison):
```
R = 2.525 Ω/1000 ft
VD = (2 × 10 × 6.5 × 2.525) / 1000 = 0.328V (0.27%)
```

---

## 2. CIRCUIT PROTECTION

### 2.1 Motor Overload Protection (NEC 430.32)

```
Overload Rating = FLA × 125% (for motors with SF ≥ 1.15)
Overload Rating = 6.5A × 1.25 = 8.13A

Select: 8A or 9A thermal overload
```

**Per NEC 430.32(A)(1):**
- Motors marked with Service Factor ≥ 1.15: Use 125% of nameplate FLA
- All other motors: Use 115% of nameplate FLA

### 2.2 Branch Circuit Breaker Sizing

**Per NEC 430.52 - Motor Branch Circuit Short-Circuit Protection:**

For single-phase motors with inverse time breaker:
```
Maximum OCPD = FLA × 250%
Maximum OCPD = 6.5 × 2.50 = 16.25A

Standard sizes: 15A or 20A
Selected: 15A (matches receptacle rating)
```

**Note:** Since this is cord-and-plug connected equipment on a standard 15A receptacle circuit, the 15A branch circuit breaker in the building panel provides short-circuit protection.

### 2.3 GFCI Requirements

**Applicable NEC Sections:**
- **NEC 210.8(B):** GFCI protection required for outdoor outlets other than dwelling units
- **NEC 210.8(F):** Outdoor outlets for dwelling units
- **NEC 590.6:** Temporary installations (construction sites) - ALL 125V, 15/20/30A receptacles

**GFCI Trip Current:** 4-6 mA (Class A)

**Specified GFCI Devices:**

| Location | Device | Part Number | Specifications |
|----------|--------|-------------|----------------|
| Receptacle (Weather-Resistant) | Leviton SmartlockPro | **GFWT1-W** | 15A, 125V, Weather & Tamper Resistant, Self-Test |
| Portable (In-Line) | Hubbell Circuit Guard | **GFPST6C15M** | 15A, 120V, 6' cord, Extra Heavy Duty, Manual Set |
| Portable (25' Cord) | Hubbell Circuit Guard | **GFP25CM** | 15A, 120V, 25', 12/3 SJEOW, Manual Set |

**Per NEC 590.6(A)(1):** All 125V, single-phase, 15-, 20-, and 30-ampere receptacle outlets not part of permanent wiring require GFCI protection.

---

## 3. FORWARD/OFF/REVERSE SWITCH SPECIFICATION

### 3.1 Switch Requirements

- **Configuration:** DPDT (Double Pole Double Throw)
- **Positions:** On-Off-On (Center Off)
- **Current Rating:** Minimum 15A at 125V AC
- **HP Rating:** 3/4 HP minimum at 125V AC
- **Listing:** UL Listed for motor control

### 3.2 Specified Switch

**Primary Selection:**
| Parameter | Specification |
|-----------|---------------|
| Manufacturer | Carling Technologies |
| Part Number | **2GO53-73/TABS** |
| Configuration | DPDT, On-Off-On |
| Current Rating | 15A @ 125V AC, 10A @ 250V AC |
| HP Rating | 3/4 HP @ 125V AC |
| Terminal Type | 0.250" Quick Connect (TABS) |
| Mounting | 15/32" panel hole, threaded bushing |
| Listing | UL, CSA |

**Alternative Selection:**
| Parameter | Specification |
|-----------|---------------|
| Manufacturer | Carling Technologies |
| Part Number | **6GO53-73/TABS** |
| Configuration | DPDT, Momentary On-Off-Momentary On |
| Current Rating | 15A @ 125V AC |
| Notes | For momentary/jog control |

### 3.3 Motor Reversing Circuit Notes

**IMPORTANT:** Single-phase induction motors require specific winding connections for reversing. The switch reverses connections to the START winding only. Verify motor is designed for reversing operation.

For split-phase or capacitor-start motors:
- T1 and T2 are RUN winding terminals
- T5 and T8 are START winding terminals
- Reverse T5 and T8 connections to reverse direction

---

## 4. SOLENOID VALVE ELECTRICAL SPECIFICATIONS

### 4.1 Valve Selection

**Specified Valve:**
| Parameter | Specification |
|-----------|---------------|
| Type | 2-Way, Normally Closed |
| Body | Brass, 3/4" NPT |
| Voltage | 120V AC (110-120V range) |
| Power | 17-24W holding |
| Seal Material | EPDM or NBR (for water service) |

### 4.2 Current Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| Inrush Current | 2.0-2.5A | 50-150ms duration |
| Holding Current | 0.15-0.25A | Steady state |
| Inrush VA | 85-95 VA | Peak apparent power |
| Holding Power | 17-24W | Continuous |

**Inrush/Hold Ratio:** Typically 5:1 to 10:1 for AC solenoids

### 4.3 Back-EMF Protection (Snubber Circuit)

**Required:** Yes - AC solenoids generate significant back-EMF at turn-off

**Recommended Snubber Circuit:**

```
        ┌────[R]────[C]────┐
        │                  │
    ────┤                  ├────  (Across solenoid coil)
        │                  │
        └────────┬─────────┘
                 │
               [MOV]
                 │
        ─────────┴─────────
```

**Component Values:**
| Component | Value | Specification |
|-----------|-------|---------------|
| R (Resistor) | 100Ω | 1/2W minimum, carbon film or metal film |
| C (Capacitor) | 100nF (0.1µF) | X2-rated, 275V AC minimum |
| MOV (Optional) | 150V AC | Littelfuse V150LA10A or equivalent |

**Specified Parts:**
| Component | Manufacturer | Part Number | Source |
|-----------|--------------|-------------|--------|
| X2 Capacitor | KEMET | **R46KN3100JCK1M** | Digi-Key |
| Resistor 100Ω 1/2W | Yageo | **CFR-25JB-52-100R** | Digi-Key |
| MOV 150V | Littelfuse | **V150LA10AP** | Mouser |

---

## 5. POWER CORD SPECIFICATION

### 5.1 Cord Type Selection

| Type | Rating | Jacket | Temperature | Application |
|------|--------|--------|-------------|-------------|
| SJTW | 300V | Thermoplastic | -40°C to +60°C | Light-duty, indoor/outdoor |
| SJOW | 300V | Oil-Resistant | -40°C to +90°C | Medium-duty, outdoor |
| **SOOW** | **600V** | **Oil-Resistant** | **-40°C to +90°C** | **Heavy-duty, outdoor - SELECTED** |

**SOOW Selection Rationale:**
- 600V rating provides safety margin
- Oil and water resistant (CPE jacket)
- Temperature range suitable for outdoor use
- Excellent flexibility and abrasion resistance
- UL Listed and CSA Certified for hard usage

### 5.2 Cord Specifications

| Parameter | Specification |
|-----------|---------------|
| Type | SOOW (Portable Cord, Oil-Resistant) |
| Conductors | 3 (Hot, Neutral, Ground) |
| AWG | 12 AWG |
| Voltage Rating | 600V |
| Temperature | -40°C to +90°C |
| Ampacity | 25A @ 30°C ambient |
| Jacket | CPE (Chlorinated Polyethylene) |
| Insulation | EPDM |
| Color Code | Black (Hot), White (Neutral), Green (Ground) |

**Specified Cord:**
| Source | Part Description |
|--------|------------------|
| EWCS Wire | 12/3 SOOW Portable Cord 600V UL/CSA |
| Nassau National Cable | 12/3 SOOW Black Portable Power Cable |

### 5.3 NEMA Plug Specification

| Parameter | Specification |
|-----------|---------------|
| Type | NEMA 5-15P |
| Rating | 15A, 125V |
| Grounding | 3-wire grounding type |
| Blade Configuration | 2 parallel blades + ground pin |
| Listing | UL 498, CSA C22.2 No. 42 |

**Specified Plug:**
| Manufacturer | Part Number | Description |
|--------------|-------------|-------------|
| Hubbell | **HBL5266C** | 15A, 125V, NEMA 5-15P, Industrial Grade |
| Leviton | **515PV** | 15A, 125V, NEMA 5-15P, Industrial Grade |
| Pass & Seymour | **PS5266X** | 15A, 125V, NEMA 5-15P, Extra Hard Use |

---

## 6. GROUNDING REQUIREMENTS

### 6.1 Equipment Grounding Conductor (EGC) per NEC 250.122

**Per Table 250.122:**
| OCPD Rating | Copper EGC Size |
|-------------|-----------------|
| 15A | 14 AWG |
| 20A | 12 AWG |

**Selected:** 12 AWG (Green) - Part of 12/3 SOOW cord

### 6.2 Ground Continuity Requirements

Per NEC 250.4(A)(5) - Effective Ground-Fault Current Path:
- Ground path must be permanent and continuous
- Capable of carrying maximum fault current likely to occur
- Low enough impedance to facilitate OCPD operation

**Ground Continuity Test:**
- Resistance from equipment frame to supply ground: <0.1Ω
- Test per UL 60335-1 or OSHA requirements

### 6.3 Metal Frame Bonding (NEC 250.4)

All metal parts that may become energized must be bonded to the equipment grounding conductor:

| Component | Bonding Method |
|-----------|----------------|
| Motor Frame | Green wire to motor ground terminal |
| Switch Enclosure | Internal ground lug to EGC |
| Drum/Mixing Vessel | Bonding conductor to frame |
| Control Enclosure | Internal ground bus |

**Bonding Jumper Sizing:** Same as EGC - 12 AWG minimum

**Grounding Hardware:**
- Use listed grounding connectors
- Green hex head screws for ground terminals
- Star washers or serrated lockwashers on painted surfaces

---

## 7. WIRING DIAGRAM

### 7.1 Schematic Diagram

```
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                    CONCRETE MIXER                           │
                                    │                  ELECTRICAL SCHEMATIC                       │
                                    └─────────────────────────────────────────────────────────────┘

    SUPPLY                          GFCI                    SWITCH                      MOTOR
    ══════                          ════                    ══════                      ═════

    ┌──────┐                     ┌────────┐             ┌─────────────┐            ┌──────────────┐
    │ L1   │───BLK──────────────►│ LINE   │             │  DPDT SW    │            │              │
    │(HOT) │         120V AC     │  (BK)  │             │  S1         │            │   MOTOR      │
    │      │                     │        │   BLK       │             │            │    M1        │
    └──┬───┘                     │        ├────────────►│ 1  ●────────┼──●  2      │              │
       │                         │ GFCI   │             │    │   OFF  │  │         │  ┌────────┐  │
       │                         │        │             │    │   ↓    │  │    BLK  │  │ T1     │  │
       │                         │ LOAD   │             │ 3  ●───┼────┼──●  4 ────────►│ (RUN)  │  │
       │                         │  (BK)  │             │    FWD │    │ REV        │  │        │  │
       │                         └───┬────┘             │        │    │            │  │ T2     │  │
       │                             │                  │ 5  ●───┼────┼──●  6 ────────►│ (RUN)  │  │
       │                             │                  │        │    │       WHT  │  │        │  │
       │                             │                  │        │    │            │  │ T5     │  │
       │                             │                  │        └────┼────────────────►(START) │  │
       │                             │                  │             │       BLU  │  │        │  │
       │                             │                  │             └────────────────►T8     │  │
       │                             │                  │                     RED  │  │(START) │  │
       │                             │                  └─────────────┘            │  └────────┘  │
       │                             │                                             │              │
       │     ┌───────────────────────┘                                             │              │
       │     │                                                                     │              │
       │     │                   SOLENOID CIRCUIT                                  │              │
       │     │                   ════════════════                                  │              │
       │     │                                                                     │              │
       │     │   WHT       ┌────────────┐    ┌──────────┐                          │              │
       │     └────────────►│  SWITCH    │    │ SOLENOID │                          │              │
       │                   │    S2      ├───►│   SOL1   │                          │              │
       │                   │  (ON/OFF)  │    │ 120V AC  │                          │              │
       │                   └────────────┘    │          │                          │              │
       │                                     │ ┌──┬──┐  │                          │              │
       │                                     │ │R │C │  │ Snubber                  │              │
       │                                     │ └──┴──┘  │ (100Ω+0.1µF)             │              │
       │                                     └────┬─────┘                          │              │
       │                                          │ BLK                            │              │
       │                                          │                                │              │
    ┌──┴───┐                                      │                                │              │
    │ N    │───WHT────────────────────────────────┴────────────────────────────────┤              │
    │(NEU) │                                                                       │              │
    └──┬───┘                                                                       │              │
       │                                                                           │              │
    ┌──┴───┐                                    FRAME                              │              │
    │ G    │───GRN─────────────────────────────►GROUND◄────────────────────────────┤              │
    │(GND) │                                      ⏚                                │              │
    └──────┘                                                                       └──────────────┘


    NOTES:
    ══════
    1. All wiring 12 AWG SOOW unless noted
    2. Wire colors: BLK=Hot, WHT=Neutral, GRN=Ground, BLU/RED=Motor Start Winding
    3. GFCI: Hubbell GFPST6C15M or equivalent
    4. S1: Carling 2GO53-73/TABS DPDT On-Off-On
    5. S2: SPST 10A toggle for solenoid control
    6. Snubber required on solenoid coil
```

### 7.2 Terminal Designations

**Motor Terminals (Typical Split-Phase/Capacitor-Start):**
| Terminal | Function | Wire Color |
|----------|----------|------------|
| T1 | Run Winding Lead 1 | Black |
| T2 | Run Winding Lead 2 | White |
| T5 | Start Winding Lead 1 | Blue |
| T8 | Start Winding Lead 2 | Red |

**DPDT Switch Terminals:**
| Terminal | Function (FWD) | Function (REV) |
|----------|----------------|----------------|
| 1 | Line Input | Line Input |
| 2 | Line Input | Line Input |
| 3 | To T1 | To T1 |
| 4 | To T5 | To T8 |
| 5 | To T2 | To T2 |
| 6 | To T8 | To T5 |

### 7.3 Wire Color Code

| Color | Function | AWG |
|-------|----------|-----|
| Black | Hot (L1/Line) | 12 |
| White | Neutral | 12 |
| Green | Equipment Ground | 12 |
| Blue | Motor Start Winding | 14 |
| Red | Motor Start Winding (Reversed) | 14 |
| Yellow | Control Circuit (Optional) | 14 |

---

## 8. BILL OF MATERIALS

### 8.1 Major Components

| Item | Description | Manufacturer | Part Number | Qty | Source |
|------|-------------|--------------|-------------|-----|--------|
| 1 | GFCI Portable Cord Set, 15A, 6' | Hubbell | GFPST6C15M | 1 | Grainger |
| 2 | DPDT Toggle Switch, 15A 125VAC | Carling | 2GO53-73/TABS | 1 | Mouser |
| 3 | SOOW Cord, 12/3, 10' | Nassau Cable | 12/3 SOOW | 10 ft | Direct |
| 4 | NEMA 5-15P Plug | Hubbell | HBL5266C | 1 | Grainger |
| 5 | Solenoid Valve, 3/4" NPT, 120VAC | - | - | 1 | - |
| 6 | SPST Toggle Switch, 10A | - | - | 1 | - |

### 8.2 Snubber Components

| Item | Description | Manufacturer | Part Number | Qty | Source |
|------|-------------|--------------|-------------|-----|--------|
| 7 | X2 Capacitor, 100nF 275VAC | KEMET | R46KN3100JCK1M | 1 | Digi-Key |
| 8 | Resistor, 100Ω 1/2W | Yageo | CFR-25JB-52-100R | 1 | Digi-Key |
| 9 | MOV, 150VAC | Littelfuse | V150LA10AP | 1 | Mouser |

### 8.3 Hardware and Accessories

| Item | Description | Qty |
|------|-------------|-----|
| 10 | Ring terminals, 12 AWG, #10 stud | 10 |
| 11 | Quick-disconnect terminals, 0.250" | 12 |
| 12 | Wire nuts, yellow (12-14 AWG) | 10 |
| 13 | Ground screws, green hex, 10-32 | 4 |
| 14 | Cable strain relief, 1/2" NPT | 2 |
| 15 | NEMA 4X enclosure (control box) | 1 |

---

## 9. COMPLIANCE SUMMARY

### 9.1 Applicable Codes and Standards

| Standard | Section | Requirement | Status |
|----------|---------|-------------|--------|
| NEC 2023 | 310.16 | Conductor ampacity | ✓ Compliant |
| NEC 2023 | 430.32 | Motor overload protection | ✓ Compliant |
| NEC 2023 | 430.52 | Motor branch circuit OCPD | ✓ Compliant |
| NEC 2023 | 210.8 | GFCI protection | ✓ Compliant |
| NEC 2023 | 590.6 | Temporary installation GFCI | ✓ Compliant |
| NEC 2023 | 250.122 | EGC sizing | ✓ Compliant |
| NEC 2023 | 250.4 | Grounding and bonding | ✓ Compliant |
| UL 62 | - | Flexible cords and cables | SOOW Listed |
| UL 498 | - | Attachment plugs | Listed |
| UL 943 | - | GFCI devices | Listed |

### 9.2 Key Design Parameters Summary

| Parameter | Value | Code Reference |
|-----------|-------|----------------|
| Motor FLA | 6.5A (calculated) | NEC 430.6 |
| Wire Size (Motor) | 12 AWG | NEC Table 310.16 |
| Voltage Drop | 0.17% @ 10' | NEC 210.19(A) Info Note |
| OCPD Rating | 15A | NEC 430.52 |
| Overload Rating | 8-9A | NEC 430.32 |
| GFCI Trip Level | 4-6 mA | UL 943 Class A |
| EGC Size | 12 AWG | NEC Table 250.122 |

---

## 10. INSTALLATION NOTES

1. **GFCI Test:** Test GFCI device before each use per NEC 590.6(B)

2. **Motor Rotation:** Verify motor rotation direction before connecting to load. Reverse switch operation reverses START winding connections.

3. **Enclosure Rating:** Use NEMA 4X enclosure for outdoor/wet locations per NEC 312.2

4. **Cord Storage:** Inspect cord before each use. Replace if jacket is damaged, exposing conductors.

5. **Grounding:** Verify ground continuity from frame to plug ground pin (<0.1Ω)

6. **Solenoid Snubber:** Install snubber directly at solenoid terminals. Failure to install snubber may cause switch contact damage and EMI.

---

**Document Revision:** 1.0  
**Design Basis:** NEC 2023, UL Standards  
**Prepared For:** Concrete Mixer Electrical System  

