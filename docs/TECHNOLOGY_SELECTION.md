# Technology Selection Matrix - MudMixer Reverse Engineering

> **Purpose**: Systematic evaluation of technologies for closing critical gaps  
> **Methodology**: Pugh Matrix with weighted criteria  
> **Date**: 2026-05-17

---

## 1. CRITICAL GAP: Internal Geometry Capture (G1)

### 1.1 Technology Options Evaluation

**Objective**: Capture housing ID, auger OD, clearance, and internal finger geometry

| Criteria | Weight | CT Scan | Disassembly | Endoscope | Bore Gauge |
|----------|--------|---------|-------------|-----------|------------|
| Accuracy | 0.25 | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★★★★★ |
| Non-destructive | 0.20 | ★★★★★ | ★☆☆☆☆ | ★★★★★ | ★★★★☆ |
| Cost efficiency | 0.20 | ★★☆☆☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| Data completeness | 0.20 | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★☆☆☆ |
| Time efficiency | 0.15 | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| **WEIGHTED SCORE** | | **4.0** | **3.4** | **3.3** | **3.9** |

### 1.2 Recommended Approach

**Primary**: Bore gauge + caliper measurement ($100, 30 min)  
**Secondary**: Industrial CT scan if comprehensive model needed ($1,500+)

---

## 2. CRITICAL GAP: Motor Coupling Specification (G2)

### 2.1 Technology Options Evaluation

**Objective**: Identify exact Acme thread size and pitch

| Criteria | Weight | Thread Gauge | Manufacturer Contact | 3D Scan | Measurement |
|----------|--------|--------------|----------------------|---------|-------------|
| Accuracy | 0.30 | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| Cost | 0.25 | ★★★★☆ | ★★★★★ | ★★☆☆☆ | ★★★★★ |
| Speed | 0.25 | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| Certainty | 0.20 | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| **WEIGHTED SCORE** | | **4.7** | **4.1** | **2.7** | **4.5** |

### 2.2 Recommended Approach

**Primary**: Acme thread gauge set ($50-100)  
**Backup**: Contact MudMixer support (806) 515-4683

### 2.3 Thread Gauge Purchase Specification

| Item | Specification | Source | Price |
|------|---------------|--------|-------|
| Acme Thread Gauge Set | 1/4" - 1" LH | Amazon/McMaster | $75-150 |
| Thread Pitch Gauge | Metric + Imperial | Harbor Freight | $15 |

---

## 3. CRITICAL GAP: Bearing Configuration (G3)

### 3.1 Technology Options Evaluation

**Objective**: Identify bearing type, ID, OD, and load rating

| Criteria | Weight | Disassembly | CT Scan | Manufacturer | Cross-reference |
|----------|--------|-------------|---------|--------------|-----------------|
| Accuracy | 0.30 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Non-destructive | 0.20 | ★☆☆☆☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| Cost | 0.25 | ★★★★☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| Completeness | 0.25 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★☆☆☆ |
| **WEIGHTED SCORE** | | **3.8** | **3.6** | **4.7** | **3.5** |

### 3.2 Recommended Approach

**Primary**: Contact MudMixer support for motor/bearing specs  
**Secondary**: Order motor ($867.51, MMXR-P209) and document during replacement

---

## 4. CAD SOFTWARE SELECTION

### 4.1 Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Parametric modeling | ★★★★★ | Must support design changes |
| Sheet metal features | ★★★★☆ | 14 ga steel body |
| Helical/spiral features | ★★★★★ | Auger geometry |
| FEA integration | ★★★★☆ | Structural validation |
| CFD capability | ★★★☆☆ | Flow simulation |
| BOM generation | ★★★★☆ | Manufacturing output |
| STEP/IGES export | ★★★★★ | Interoperability |
| Cost | ★★★☆☆ | Budget consideration |

### 4.2 Software Comparison

| Software | Parametric | Sheet Metal | Helix | FEA | CFD | BOM | Cost/Year |
|----------|------------|-------------|-------|-----|-----|-----|-----------|
| **Fusion 360** | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | $545 |
| **SolidWorks** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | $3,995 |
| **FreeCAD** | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | Free |
| **Onshape** | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | $1,500 |
| **OpenSCAD** | ★★★☆☆ | ★☆☆☆☆ | ★★★★★ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | Free |

### 4.3 Recommended Stack

| Purpose | Primary Tool | Backup |
|---------|--------------|--------|
| **Parametric CAD** | Fusion 360 | FreeCAD |
| **Auger Generation** | OpenSCAD + Python | Fusion 360 coil |
| **FEA** | Fusion 360 Simulation | SimScale (cloud) |
| **CFD** | OpenFOAM | SimScale |
| **Rendering** | Fusion 360 | Blender |
| **3D Printing** | PrusaSlicer | Cura |

---

## 5. SIMULATION TOOLS SELECTION

### 5.1 FEA Tools Comparison (2026 Updated)

| Tool | Auger Stress | Fatigue | Non-linear | Cost | Notes |
|------|--------------|---------|------------|------|-------|
| **Ansys Student** | ★★★★☆ | ★★★★☆ | ★★★★☆ | Free | 512k node limit, 12-mo license |
| **Ansys Mechanical** | ★★★★★ | ★★★★★ | ★★★★★ | $15,000+/yr | Enterprise |
| **SimScale Community** | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Free | Limited core hours |
| **SimScale Pro** | ★★★★★ | ★★★★☆ | ★★★★★ | $3,000+/yr | **RECOMMENDED** |
| **Fusion 360** | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | $545/yr | Good for screening |
| **FreeCAD FEM** | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ | Free | Limited |

**FEA Best Practices for Helical Auger:**
- Use 8-noded elements in stress concentration regions
- Refine mesh at weld toes and shaft-flight connections
- Analyze: torsional stress, bending, combined loading
- Target: Safety factor ≥2.0 vs yield strength
- Fatigue: IIW or ASME Section VIII standards for weld analysis

### 5.2 CFD Tools Comparison (Concrete Flow - 2026 Updated)

Fresh concrete is a **Bingham plastic** - use Herschel-Bulkley model for best accuracy (<10% error).

| Tool | Bingham Support | DEM | Cost | Learning Curve |
|------|-----------------|-----|------|----------------|
| **Ansys Fluent** | ★★★★★ Native | ★★★★★ | $20,000+/yr | High |
| **OpenFOAM** | ★★★★☆ generalisedNewtonian | ★★★☆☆ | Free | Very High |
| **SimScale** | ★★★★☆ Good | ★★☆☆☆ | $3,000+/yr | Medium |
| **EDEM (Altair)** | N/A (DEM only) | ★★★★★ | $10,000+/yr | Medium |
| **Rocky DEM** | N/A | ★★★★★ | Custom | Medium |
| **LIGGGHTS** | N/A | ★★★★☆ | Free | Very High (no GUI) |

**Validation Method:** Simulate ASTM C143 slump test, compare to experimental data

### 5.3 Recommended Simulation Approach

| Phase | Tool | Purpose | Cost |
|-------|------|---------|------|
| Screening | Fusion 360 FEA | Basic stress check | $0 (included) |
| Validation | SimScale | Detailed FEA + CFD | $400/yr |
| Optimization | OpenFOAM | Parametric studies | Free |
| Production | Ansys (consultant) | Certification support | $5,000 (one-time) |

---

## 6. MANUFACTURING TECHNOLOGY SELECTION

### 6.1 Auger Manufacturing Options

| Method | Accuracy | Cost/Unit | Tooling | Min Qty |
|--------|----------|-----------|---------|---------|
| **Cold Forming** | ★★★★★ | $200-500 | $50,000+ | 1,000+ |
| **CNC Machining** | ★★★★★ | $1,000-3,000 | $0 | 1 |
| **3D Printed (Metal)** | ★★★★☆ | $2,000-5,000 | $0 | 1 |
| **Welded Spiral** | ★★★☆☆ | $500-1,000 | $500 | 1 |
| **Cast + Machine** | ★★★★☆ | $800-1,500 | $5,000 | 10+ |

### 6.2 Recommended Path

| Production Volume | Method | Rationale |
|-------------------|--------|-----------|
| 1-5 units | CNC + Welding | Flexibility, no tooling |
| 6-50 units | Cast + Machine | Cost per unit reduction |
| 50-500 units | Cold Forming | Optimal cost/quality |
| 500+ units | Dedicated tooling | Economies of scale |

### 6.3 Frame Manufacturing Options

| Method | Sheet Metal | Tube Frame | Cost/Unit |
|--------|-------------|------------|-----------|
| **Laser Cut + Brake** | ★★★★★ | ★★★☆☆ | $200-400 |
| **Waterjet + Brake** | ★★★★☆ | ★★★☆☆ | $250-450 |
| **Plasma + Brake** | ★★★☆☆ | ★★★☆☆ | $150-300 |
| **Stamping** | ★★★★★ | ★☆☆☆☆ | $50-100 (high vol) |

---

## 7. COST-BENEFIT SUMMARY

### 7.1 Technology Investment Tiers

| Tier | Investment | Capabilities | ROI Break-even |
|------|------------|--------------|----------------|
| **Minimal** | $500 | Measurement + FreeCAD | 1 unit |
| **Standard** | $2,500 | 3D scan + Fusion 360 + SimScale | 3 units |
| **Professional** | $10,000 | CT scan + SolidWorks + Consulting | 10 units |
| **Production** | $50,000 | Full tooling + PLM | 100 units |

### 7.2 Recommended Investment Path

```
Phase 1 ($500): Measurement Tools
├── Thread gauge set: $100
├── Bore gauge: $75
├── Calipers: $50
├── Endoscope: $75
└── Photogrammetry (Meshroom): Free

Phase 2 ($2,000): Digital Tools
├── 3D Scanner (Revopoint): $1,200
├── SimScale subscription: $400
└── Fusion 360: $545 (or free hobby)

Phase 3 ($5,000): Validation
├── CT Scan service: $1,500
├── FEA consulting: $2,000
└── Prototype materials: $1,500

Phase 4 ($10,000): Production Prep
├── First article auger: $3,000
├── Fixture/jig fabrication: $2,000
├── Testing equipment: $3,000
└── Certification: $2,000
```

---

## 8. DECISION LOG

| Date | Decision | Rationale | Approved |
|------|----------|-----------|----------|
| 2026-05-17 | Use Fusion 360 as primary CAD | Cost-effective, adequate features | Pending |
| 2026-05-17 | Pursue bore gauge before CT | Cost savings, sufficient for MVP | Pending |
| 2026-05-17 | Contact MudMixer support | Free data acquisition | Pending |

---

## APPENDIX: Vendor Contacts

### 3D Scanning Services

| Vendor | Service | Location | Contact |
|--------|---------|----------|---------|
| Jesse Garant Metrology | CT Scanning | Windsor, ON | jgarantmc.com |
| Lumafield | CT + Software | Boston, MA | lumafield.com |
| Exact Metrology | 3D Scanning | Cincinnati, OH | exactmetrology.com |
| Direct Dimensions | 3D Scanning | Baltimore, MD | directdimensions.com |

### CAD/Simulation Consulting

| Vendor | Specialty | Rate |
|--------|-----------|------|
| UpWork FEA | Freelance analysis | $50-150/hr |
| SimScale Support | CFD/FEA | Included with Pro |
| Local machine shop | DFM review | $100-200/hr |

### Manufacturing Partners

| Vendor | Capability | Location |
|--------|------------|----------|
| Xometry | CNC, Sheet Metal | Online |
| SendCutSend | Laser cutting | Online |
| Protolabs | Rapid prototyping | Online |
| Local fab shop | Full fabrication | TBD |
