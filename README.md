# MudMixer Reverse Engineering Project

## Overview

This project contains reverse-engineered documentation of the MudMixer portable continuous concrete/mortar mixer. The MudMixer is a patented continuous-feed mixing system that uses a shaftless helical auger to hydrate and mix bagged cementitious materials.

## Product Summary

| Attribute | Value |
|-----------|-------|
| **Manufacturer** | MudMixer, LLC (formerly Red Dog Mobile Shelters, LLC) |
| **Model** | MMXR-3221 / MMXR-3225 (Evolution) |
| **Type** | Continuous-feed portable electric mixer |
| **Patents** | US 10,259,140 B1, US 11,285,639 B2, D943,639 |

## Key Features

- **Continuous Mixing**: Unlike batch mixers, material flows through continuously
- **Shaftless Helical Auger**: Variable-pitch design for optimal mixing and conveyance
- **Dual Spray Nozzles**: Water injection system with adjustable flow control
- **330° Swivel**: Precision placement capability
- **Portable Design**: Flat-free tires, lightweight frame (145 lbs)

## Documentation Structure

- [Technical Specifications](./docs/SPECIFICATIONS.md) - Dimensions, power, capacity
- [Main Assemblies](./docs/ASSEMBLIES.md) - Frame, hopper, chute, drive system
- [Auger Design](./docs/AUGER_DESIGN.md) - Shaftless auger geometry and principles
- [Water System](./docs/WATER_SYSTEM.md) - Spray nozzle and flow control
- [Bill of Materials](./docs/BOM.md) - Component list for replication
- [Engineering Calculations](./docs/ENGINEERING.md) - Design calculations and principles

## Operation Principle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DRY MIX ──▶ HOPPER ──▶ AUGER + WATER ──▶ CHUTE ──▶ OUTPUT │
│              (120 lbs)    (dual spray)     (16")            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

1. Dry bagged mix (concrete, mortar, stucco) is loaded into the hopper
2. Material flows by gravity into the shaftless auger
3. Water is injected via dual spray nozzles at adjustable rate
4. Auger rotates, mixing and conveying material through chute
5. Mixed material exits through 330° swivel chute for placement

## Performance

- **Throughput**: 45+ bags (80 lb) per hour
- **Output Rate**: ~1 cubic yard per hour
- **Mix Rate**: ~1 bag (60 lb) per minute

## Patents Referenced

| Patent | Title | Filed | Issued |
|--------|-------|-------|--------|
| US 10,259,140 B1 | Portable concrete mixer for hydrating and mixing concrete mix containing gravel aggregate in a continuous process | Oct 19, 2018 | Apr 16, 2019 |
| US 11,285,639 B2 | Portable mixer for hydrating and mixing cementitious mix in a continuous process | Mar 13, 2019 | Mar 29, 2022 |
| D943,639 | Design Patent (Mixer appearance) | - | Feb 15, 2022 |

## Sources

- [MudMixer Official Website](https://mudmixer.com/)
- [MudMixer Specifications](https://mudmixer.com/pages/specs)
- [US Patent 10,259,140](https://patents.justia.com/patent/10259140)
- [Freepatentsonline US 11,285,639](https://www.freepatentsonline.com/11285639.html)

## Disclaimer

This reverse engineering documentation is for educational and research purposes only. The MudMixer design is protected by the patents listed above. Any commercial use or manufacture must respect applicable intellectual property rights.
