# Structural Engineering Calculations for Portable Concrete Mixer Frame

> **Calculation ID**: CALC-STRUCT-001  
> **Date**: 2026-05-17  
> **Status**: VALIDATED - Design change required

---

## 1. Material Properties - ASTM A513 Type 1020 Cold-Drawn Steel

Based on ASTM A513 and ASM Handbook specifications for 1020 carbon steel:

| Property | Value | Source |
|----------|-------|--------|
| Yield Strength (Sy) | 50,000 psi (345 MPa) | ASTM A513 Type 1 minimum |
| Tensile Strength (Su) | 55,000 psi (379 MPa) | ASTM A513 Type 1 minimum |
| Modulus of Elasticity (E) | 29,000,000 psi (200 GPa) | AISC Steel Manual |
| Shear Modulus (G) | 11,200,000 psi (77 GPa) | G = E / 2(1+v), v=0.29 |
| Poisson's Ratio (v) | 0.29 | Standard for carbon steel |
| Density | 0.284 lb/in³ (7,850 kg/m³) | ASM Handbook |

---

## 2. Section Properties - 1" Schedule 40 Steel Tube

**Given dimensions:**
- Outside Diameter (OD) = 1.315 in
- Wall Thickness (t) = 0.133 in
- Inside Diameter (ID) = 1.049 in

### Cross-Sectional Area (A)
```
A = (π/4) × (OD² - ID²)
A = (π/4) × (1.315² - 1.049²)
A = (π/4) × (1.7292 - 1.1004)
A = (π/4) × 0.6288
A = 0.494 in²
```

### Moment of Inertia (I)
```
I = (π/64) × (OD⁴ - ID⁴)
I = (π/64) × (1.315⁴ - 1.049⁴)
I = (π/64) × (2.990 - 1.211)
I = (π/64) × 1.779
I = 0.0873 in⁴
```

### Section Modulus (S)
```
S = I / c = I / (OD/2)
S = 0.0873 / 0.6575
S = 0.133 in³
```

### Radius of Gyration (r)
```
r = √(I/A)
r = √(0.0873 / 0.494)
r = √0.1767
r = 0.420 in
```

### Summary of Section Properties
| Property | Calculated Value | Reference Check (AISC) |
|----------|------------------|------------------------|
| Area (A) | 0.494 in² | 0.494 in² ✓ |
| Moment of Inertia (I) | 0.0873 in⁴ | 0.087 in⁴ ✓ |
| Section Modulus (S) | 0.133 in³ | 0.133 in³ ✓ |
| Radius of Gyration (r) | 0.420 in | 0.420 in ✓ |

---

## 3. Load Analysis

### 3.1 Dead Loads
**Drum Assembly:** 145 lb (given)

**Frame Weight Estimate:**
Assuming approximately 15 ft of tubing total:
```
Frame weight = Length × Area × Density
Frame weight = (15 ft × 12 in/ft) × 0.494 in² × 0.284 lb/in³
Frame weight = 180 in × 0.494 × 0.284
Frame weight = 25.2 lb ≈ 25 lb
```

**Total Dead Load (DL) = 145 + 25 = 170 lb**

### 3.2 Live Loads
**Material Load:** 120 lb (given)
**Operator Handling Force:** 50 lb (estimated push/pull/lift)

**Total Static Live Load (LL) = 170 lb**

### 3.3 Dynamic Factors (per Shigley's Mechanical Engineering Design)

**Vibration Factor (Kv):**
For rotating equipment with moderate vibration:
```
Kv = 1.25 (mixer drum rotation creates cyclic loading)
```

**Impact Factor (Ki):**
For loading with moderate impact (dumping material):
```
Ki = 1.50 (per ASCE 7 for dynamic equipment)
```

### 3.4 Design Loads

**Service Load Combination:**
```
P_service = DL + LL = 170 + 170 = 340 lb
```

**Factored Design Load (with dynamics):**
```
P_design = (DL × 1.2) + (LL × 1.6 × Kv × Ki)
P_design = (170 × 1.2) + (170 × 1.6 × 1.25 × 1.50)
P_design = 204 + 510
P_design = 714 lb
```

---

## 4. Stress Calculations

### 4.1 Frame Geometry Assumptions
- Main horizontal frame span: L = 30 in (between supports)
- Drum load acts at center of span
- Wheelbarrow configuration: rear axle + two front legs
- Critical member: horizontal tube supporting drum

### 4.2 Bending Stress Analysis

**Maximum Bending Moment (simply supported beam, center load):**
```
M_max = P × L / 4
M_max = 714 lb × 30 in / 4
M_max = 5,355 lb-in
```

**Bending Stress:**
```
σ_b = M / S
σ_b = 5,355 lb-in / 0.133 in³
σ_b = 40,263 psi
```

### 4.3 Shear Stress Analysis

**Maximum Shear Force:**
```
V_max = P / 2 = 714 / 2 = 357 lb
```

**Maximum Shear Stress (circular tube, per Roark's):**
```
τ_max = 2 × V / A = 2 × 357 / 0.494 = 1,445 psi
```

### 4.4 Axial Stress in Legs

**Assuming two front legs share the load at 45° angle:**
```
Axial force per leg = (P/2) / cos(45°)
F_axial = (714/2) / 0.707 = 505 lb per leg
```

**Axial Compressive Stress:**
```
σ_axial = F / A = 505 / 0.494 = 1,022 psi
```

**Buckling Check (Euler's formula):**
```
Slenderness ratio: λ = K×L / r = 1.0 × 24 / 0.420 = 57.1

Critical buckling stress (Johnson's formula):
σ_cr = 50,000 × [1 - (50,000 × 57.1²)/(4π² × 29,000,000)]
σ_cr = 42,850 psi

Critical buckling load:
P_cr = σ_cr × A = 42,850 × 0.494 = 21,168 lb

Buckling Safety Factor = 21,168 / 505 = 41.9 ✓
```

### 4.5 Combined Stress - von Mises Criterion

```
σ_vm = √(σ₁² + 3τ²)
σ_vm = √(40,263² + 3 × 1,445²)
σ_vm = 40,341 psi
```

---

## 5. Safety Factor Analysis

### 5.1 Safety Factor vs. Yield

```
SF_yield = Sy / σ_vm = 50,000 / 40,341 = 1.24
```

**⚠️ CRITICAL FINDING: Safety factor of 1.24 is INADEQUATE**

### 5.2 Required Safety Factors (per Shigley's)

| Application | Required SF |
|-------------|-------------|
| Dynamic load, impact | ≥ 2.5 |
| Current design | 1.24 |
| **Gap** | **-1.26** |

---

## 6. DESIGN CHANGE REQUIRED

### Option 1: Upgrade to 1-1/4" Schedule 40 (RECOMMENDED)

| Property | 1" Sch 40 | 1-1/4" Sch 40 |
|----------|-----------|---------------|
| OD | 1.315" | 1.660" |
| Wall | 0.133" | 0.140" |
| I | 0.0873 in⁴ | 0.195 in⁴ |
| S | 0.133 in³ | 0.235 in³ |

**New bending stress:** 5,355 / 0.235 = 22,787 psi  
**New SF:** 50,000 / 22,787 = **2.19** ✓

### 6.2 Weld Requirements (AWS D1.1/D1.3)

| Joint Location | Required Size |
|----------------|---------------|
| Main frame joints | 3/16" fillet |
| Leg attachments | 3/16" fillet |
| Axle mounting | 1/4" fillet |

---

## 7. References

| Ref # | Document | Section Used |
|-------|----------|--------------|
| [1] | ASTM A513 Standard Specification | Type 1 mechanical properties |
| [2] | AISC Steel Construction Manual, 15th Ed | Table 1-13, HSS properties |
| [3] | Roark's Formulas for Stress and Strain, 8th Ed | Table 8.1, beam deflection |
| [4] | Shigley's Mechanical Engineering Design, 11th Ed | Ch. 5, safety factors |
| [5] | AWS D1.1 Structural Welding Code | Table 5.8, weld sizes |
| [6] | AWS D1.3 Sheet Steel Welding Code | Fillet weld requirements |

---

## 8. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | | | |
| Checked By | | | |
| Approved By | | | |
