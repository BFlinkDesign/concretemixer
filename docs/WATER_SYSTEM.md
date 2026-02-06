# Water Supply System

## Overview

The MudMixer uses a pressurized water injection system with dual spray nozzles to hydrate dry cementitious materials as they enter the auger. This continuous hydration is key to the mixer's ability to produce consistent output.

## System Diagram

```
                                    ┌─────────────────┐
                                    │   HOPPER        │
                                    │                 │
    ┌──────────┐                    │   Dry Mix ↓    │
    │  Garden  │                    │                 │
    │   Hose   │                    └────────┬────────┘
    │  (30+PSI)│                             │
    └────┬─────┘                             │ Aperture
         │                                   ▼
         │                        ┌──────────────────────┐
    ┌────▼─────┐                  │ ←─ Nozzle 1 (spray)  │
    │  Water   │                  │                      │
    │  Inlet   │                  │    AUGER ENTRY       │
    └────┬─────┘                  │                      │
         │                        │ ←─ Nozzle 2 (spray)  │
    ┌────▼─────┐                  └──────────┬───────────┘
    │   Flow   │                             │
    │ Control  │◄─── Adjustable              ▼
    │   Dial   │     by operator      ┌──────────────────┐
    └────┬─────┘                      │      CHUTE       │
         │                            │                  │
    ┌────▼─────┐                      │  Mixed material  │
    │ Internal │                      │       ↓          │
    │  Supply  │──────────────────────►                  │
    │   Line   │                      └──────────────────┘
    └──────────┘
```

## Components

### Water Inlet

| Specification | Value |
|---------------|-------|
| Connection | Standard garden hose thread (GHT) |
| Size | 3/4" hose fitting |
| Location | Near hopper on frame |
| Type | Quick-connect or threaded |

### Solenoid Valve (MMXR-P114)

| Specification | Value |
|---------------|-------|
| Part Number | MMXR-P114 |
| Size | 3/8-inch brass |
| Type | Electrically actuated |
| Evolution Upgrade | Waterproof solenoid |
| Pressure Rating | Up to 145 PSI (10 bar) |
| Temperature Range | 15°F to 250°F |
| Response Time | <1 second |
| Seal Material | FKM (Viton) |

### Flow Control Dial

| Specification | Value |
|---------------|-------|
| Type | Needle valve (metering device) |
| Adjustment | Fully adjustable (0-100 scale) |
| Range | Off to full flow |
| Starting Position | 35-50 for concrete |
| Marking | Graduated dial |
| Location | Accessible during operation |

### Internal Supply Line

| Specification | Value |
|---------------|-------|
| Material | Flexible tubing (reinforced) |
| Size | 3/8" to 1/2" ID |
| Routing | From inlet to nozzles |
| Fittings | Barbed or compression |

### Spray Nozzles

| Specification | Value |
|---------------|-------|
| Part Number | MMXR-P122 (nozzle adapter) |
| Thread | 1/4" NPT Male |
| Quantity | 2 (dual configuration) |
| Location | At aperture/auger entry point |
| Pattern | Fan or cone spray |
| Material | Brass or stainless steel |
| Orientation | Angled into material flow |

### Confirmed Water System Part Numbers

| Part Number | Description | Price |
|-------------|-------------|-------|
| MMXR-P114 | 3/8" Brass Solenoid Valve | $144.00 |
| MMXR-P122 | 1/4" NPT Male Nozzle Adapter Spray Head | $24.54 |
| MMXR-P121 | 3/8" OD × 1/4" NPT Female Straight Adapter | $30.54 |
| MMXR-P108 | 3/8" OD Tubing × 34.25" | $7.83 |
| — | Two Way Divider 3/8" OD × 2-3/8" OD | $12.14 |

Source: [Foards MudMixer Parts](https://www.foards.com/pages/mud-mixer-parts-mmxr-3221)

## Operating Parameters

| Parameter | Requirement |
|-----------|-------------|
| Minimum Inlet Pressure | 30 PSI (207 kPa) |
| Recommended Pressure | 40-60 PSI (276-414 kPa) |
| Water Temperature | Ambient (40-90°F recommended) |
| Flow Rate | Variable based on material |

## Water-to-Mix Ratios

Typical water requirements for common mixes:

| Material | Water per 80 lb bag | Notes |
|----------|---------------------|-------|
| Concrete Mix | 3-4 quarts (2.8-3.8 L) | Adjust for slump |
| Mortar Mix | 4-5 quarts (3.8-4.7 L) | More water for workability |
| Sand Topping | 2-3 quarts (1.9-2.8 L) | Less water needed |
| Stucco | 5-6 quarts (4.7-5.7 L) | Varies by type |

## Nozzle Configuration

### Dual Nozzle Arrangement

```
          TOP VIEW AT APERTURE

              ┌─────────────┐
              │   Hopper    │
              │   Opening   │
              └──────┬──────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    │  Nozzle 1 ─► ↓↓↓↓ ◄─ Nozzle 2  │
    │            (spray pattern)      │
    │                │                │
    │          ══════════════         │
    │             Auger               │
    └─────────────────────────────────┘


          SIDE VIEW

         Dry material
              ↓
         ┌────────┐
         │ Hopper │
         └───┬────┘
             │
    ╔════════╪════════╗
    ║  ↗     ↓     ↖  ║  ← Spray nozzles angled into flow
    ║   Nozzle   Nozzle
    ║                 ║
    ║  ═══════════════║  ← Auger
    ╚═════════════════╝
             │
             ▼
          Chute
```

### Spray Pattern Objectives

1. **Even coverage**: Water distributed across material width
2. **Early contact**: Hydration begins immediately at auger entry
3. **No dry pockets**: Overlapping spray patterns prevent dry spots
4. **No flooding**: Controlled flow prevents over-wetting

## Flow Control Operation

### Dial Settings

```
        OFF ───┬─── LOW ───┬─── MED ───┬─── HIGH ───┬─── MAX
               │           │           │            │
               ▼           ▼           ▼            ▼
           Closed     Light flow   Normal      Maximum
                      (grout)      (concrete)  (dry mixes)
```

### Adjustment Guidelines

| Material Type | Dial Setting | Indicator |
|---------------|--------------|-----------|
| Pre-wetted aggregate | Low | Material already moist |
| Standard concrete | Medium | Typical 80 lb bag |
| Dry mortar | Medium-High | Absorbs more water |
| Rapid-set products | High | Quick hydration needed |

## System Maintenance

### Regular Checks

| Component | Frequency | Action |
|-----------|-----------|--------|
| Nozzles | Weekly | Check for clogs, clean |
| Supply line | Monthly | Inspect for kinks, cracks |
| Flow control | Monthly | Verify smooth operation |
| Inlet fitting | Monthly | Check for leaks |

### Winterization

1. Drain all water from system
2. Blow out lines with compressed air
3. Store in above-freezing location
4. Cover inlet fitting

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Low water flow | Clogged nozzle | Remove and clean |
| Uneven mix | Nozzle misaligned | Adjust spray direction |
| No water | Kinked supply line | Straighten tubing |
| Leaking | Loose fitting | Tighten or replace |

## Design Considerations for Replication

### Nozzle Selection

| Type | Pros | Cons |
|------|------|------|
| Flat fan | Even coverage, simple | May clog with debris |
| Full cone | 360° coverage | Uses more water |
| Hollow cone | Atomization | Pressure-sensitive |
| Adjustable | Versatile | More expensive |

### Recommended Specifications

| Component | Specification |
|-----------|---------------|
| Nozzle orifice | 1/8" to 3/16" |
| Spray angle | 65° to 80° |
| Material | Brass (minimum), stainless preferred |
| Flow rate @ 40 PSI | 0.5-1.5 GPM per nozzle |

### Mounting Considerations

- Nozzles should be accessible for cleaning
- Protect from impact damage
- Angle toward material flow (not against)
- Position for maximum mixing time in chute
