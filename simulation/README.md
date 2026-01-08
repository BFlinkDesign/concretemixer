# Physics Simulation

Ultra-realistic physics simulation for the 4" OD shaftless helical auger concrete mixer.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run full simulation
python auger_physics.py
```

## Simulation Components

### 1. Flow Dynamics (Bingham Plastic Model)

The simulation models wet concrete as a **Bingham plastic fluid**:

```
τ = τ₀ + μ × γ̇

Where:
  τ  = Shear stress
  τ₀ = Yield stress (material won't flow below this)
  μ  = Plastic viscosity
  γ̇  = Shear rate
```

| Concrete Type | Yield Stress (Pa) | Viscosity (Pa·s) |
|---------------|-------------------|------------------|
| Standard Mix | 200 | 30 |
| High-Strength | 250 | 35 |
| Fast-Setting | 300 | 40 |
| Mortar | 150 | 20 |
| Sand Mix | 180 | 25 |
| Grout | 100 | 15 |

### 2. Volumetric Flow Calculation

For shaftless augers:

```
Q = (π × D² × P × N × η) / 4

Where:
  D = Flow diameter (4.0")
  P = Pitch (2.0" - 3.5" variable)
  N = RPM (27)
  η = Fill efficiency (0.30 - 0.45)
```

**Expected throughput: 45+ bags/hr (80 lb bags)**

### 3. Torque & Power Analysis

The simulation calculates required torque from:
- Material conveying (gravity component)
- Viscous shear (Bingham fluid resistance)
- Mechanical friction (bearings, seals)

```
T_total = T_gravity + T_shear + T_friction
P_required = T_total × ω
```

### 4. Thermal Model

Heat generation during continuous operation:
- Motor inefficiency losses (~20%)
- Viscous dissipation in concrete
- Mechanical friction

Lumped-capacitance model estimates temperature rise for duty cycle planning.

### 5. Particle Simulation (DEM-style)

Discrete particle simulation for aggregate behavior:
- Gravity
- Auger drag/conveying
- Wall collisions with restitution
- Particle size distribution (0.125" - 0.5")

## Output Files

After running `auger_physics.py`:

| File | Description |
|------|-------------|
| `simulation_results.png` | 4-panel analysis plot |
| `particle_simulation.png` | Particle trajectory visualization |

## 3D Model (OpenSCAD)

The parametric 3D model is in `/models/auger_assembly.scad`.

### Opening the Model

1. Install [OpenSCAD](https://openscad.org/downloads.html)
2. Open `auger_assembly.scad`
3. Press F5 for preview or F6 for full render

### Customization

Edit parameters at the top of the file:

```openscad
auger_od = 4.0;           // Auger outer diameter
pitch_hopper = 2.0;       // Hopper section pitch
pitch_chute = 3.5;        // Chute section pitch
```

### Animation

1. View → Animate
2. Set FPS: 30, Steps: 360
3. Watch the auger rotate!

### STL Export

For 3D printing or FEA import:

```openscad
// Uncomment at bottom of file:
scale([25.4, 25.4, 25.4]) complete_assembly();
```

Then: Design → Export as STL

## Key Results (Standard Concrete Mix)

| Parameter | Value |
|-----------|-------|
| Throughput | ~47 bags/hr |
| Torque Margin | +65% |
| Shear Rate | ~85 1/s |
| Temp Rise | ~8°C above ambient |
| Motor Adequate | YES ✓ |

## API Usage

```python
from auger_physics import (
    AugerSpecs, HousingSpecs, MotorSpecs,
    AugerFlowSimulation, ConcreteType
)

# Initialize
auger = AugerSpecs()
housing = HousingSpecs()
motor = MotorSpecs()

# Run simulation
sim = AugerFlowSimulation(auger, housing, motor, ConcreteType.STANDARD_MIX)

# Get results
throughput = sim.calculate_throughput_bags_per_hour()
motor_ok = sim.check_motor_adequacy()

print(f"Throughput: {throughput:.1f} bags/hr")
print(f"Motor adequate: {motor_ok['adequate']}")
```

## Physical Assumptions

1. **Auger OD**: 4.0" (confirmed)
2. **Housing ID**: 5.047" (5" Sch 40 pipe)
3. **Clearance**: 0.52" per side
4. **Motor**: 0.5 HP @ 27 RPM
5. **Fill Efficiency**: 35% (typical for inclined operation)
6. **Inclination**: 15° discharge angle
