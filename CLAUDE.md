# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## What this is

Reverse-engineering documentation **and a working computational framework**
for the MudMixer continuous concrete/mortar mixer (US 10,259,140 /
US 11,285,639). The repo started as Markdown specs; it now also contains a
parametric CAD + analysis + simulation toolchain in `src/` that generates
manufacturable geometry and validates it against the published specs.

This is reverse-engineered, educational work. **Every critical dimension is
a computed estimate until measured on real hardware** — see "Known vs
unknown" below and `docs/DATA_REQUIREMENTS.md`.

## Repository layout

```
docs/        Reverse-engineered specifications (Markdown)
  SPECIFICATIONS.md     dimensions, power, capacity, performance
  ASSEMBLIES.md         six main assemblies + component refs
  AUGER_DESIGN.md       shaftless variable-pitch auger geometry
  WATER_SYSTEM.md       dual spray nozzles, flow control
  POWER_SYSTEM.md       dual power (120V AC + DeWalt FlexVolt)
  ENGINEERING.md        design calculations (structural §3 corrected, D13)
  BOM.md                ORIGINAL hand BOM — superseded for procurement (D14)
  DATA_REQUIREMENTS.md  known vs unknown specs; predictions now annotated
  DESIGN_INSIGHTS.md    computed discoveries D1-D14 + enhancement roadmap E1-E7

drawings/    ASCII drawings (*.md) + generated PNGs (render/drawing/sim)

src/         Python framework (core is standard-library-only)
  geometry.py            shared mesh library (vectors, primitives, STL I/O)
  auger_optimizer.py     generative design + CLI (geometry, finger, thermal,
                         power, CFD params)
  auger_cad.py           auger mesh build, STL export, render
  mixer_cad.py           full 17-component machine, validation, drawing sheet
  mixer_analysis.py      cross-spec physics + converged design point
  mixer_simulation.py    12-hour duty-cycle digital twin
  bom_generator.py       CAD-reconciled BOM + procurement audit
  manufacturing_audit.py file-level STL verification gate
  build_all.py           one-command regeneration of every artifact
  test_*.py              108 tests
  requirements.txt       deps (matplotlib for renders; pytest/ruff/mypy dev)

pyproject.toml           ruff + mypy + pytest config
.github/workflows/tests.yml   CI: lint -> typecheck -> tests -> validate -> build -> audit
```

## Working in this repo

Quality gates (all enforced in CI, run them before pushing):

```bash
pip install pytest matplotlib ruff mypy
ruff check src/        # lint  (config in pyproject.toml)
mypy                   # type check (15 source files, clean)
python -m pytest src/  # 108 tests
```

Regenerate every artifact (STLs at both bores, renders, drawing sheet,
simulation, BOM/procurement, manifest) — self-gated by CAD validation and
the manufacturing audit:

```bash
python src/build_all.py --out dist
```

Common entry points:

```bash
python src/mixer_cad.py --report                    # validate baseline 6.0" bore
python src/mixer_cad.py --housing-id 6.5 --report   # validate converged 6.5" bore
python src/mixer_analysis.py                         # discoveries D1-D11
python src/mixer_simulation.py --plot sim.png        # 12-hour digital twin
python src/bom_generator.py --housing-id 6.5 --md bom.md
python src/manufacturing_audit.py dist/stl           # STL gate (CI uses this)
```

## Conventions

- **Core stays standard-library-only.** `matplotlib` is an optional
  rendering dependency; `numpy`/`scipy` are listed but unused by the core.
  Do not add runtime dependencies to the calculation/geometry/STL paths.
- **Units are inches and pounds** throughout the geometry and CAD code.
- **Mesh math lives in `geometry.py`.** Do not re-implement watertightness,
  volume, transforms, or STL I/O elsewhere — import them. (The pre-refactor
  triplication is exactly the bug class the shared library prevents.)
- **Every discovery is falsifiable and tested.** New claims in
  `DESIGN_INSIGHTS.md` must trace to a function and a test (see the
  Verification Matrix at the bottom of that file).
- **Two design points are first-class:** 6.0" baseline (repo's original
  assumption) and 6.5" converged (D1/D11). New CAD/validation code should
  accept `housing_id` and pass at both.

## Known vs unknown (read before trusting any number)

CONFIRMED from manufacturer/patents: max aggregate 0.5", LH Acme coupling,
P/D ratios (hopper 0.2-0.9, chute 0.6-1.0), chute 16-30", 145 lb dry,
120 lb hopper, 16" discharge, 66.5×27.5×35 envelope.

COMPUTED PREDICTIONS (not yet measured): housing bore ~6.48", auger OD
~5.0" (D1/D11); full-load current ~4.1 A not the published 2.6 A (D2);
~67:1 gear reduction (D3). The single blocking real-world measurement is
the **chute bore** — a bore gauge confirms or refutes 6.5".

## Status / TODO

Code + docs are merged (PR #2). Outstanding work is tracked in
**`docs/NEXT_STEPS.md`** — physical measurements, CFD, and the E1-E7
enhancement roadmap. Update that file (not this one) as items close.
