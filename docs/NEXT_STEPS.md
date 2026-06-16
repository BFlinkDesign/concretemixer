# Next Steps / TODO

Status as of the PR #2 merge. The computational framework, CAD model,
simulation, BOM/procurement, and CI are **done and merged**. What remains
is real-world validation and the enhancement roadmap — none of it blocks
using the existing artifacts, but the first item gates fabrication.

## 1. Physical measurements (blocks fabrication)

The framework's predictions are falsifiable. Confirm them on real hardware
before cutting metal. Priority order from `docs/DATA_REQUIREMENTS.md`:

- [ ] **Chute bore ID** — bore gauge. Model predicts **6.48"** (D1/D11).
      This is the single highest-leverage measurement: it picks which of
      the two already-audited STL sets (6.0" vs 6.5") to fabricate.
- [ ] **Auger OD** — caliper. Predicted ~5.0".
- [ ] **Acme thread size** — thread gauge (LH confirmed by patent).
- [ ] **Bearing specifications** — disassembly.
- [ ] **Measured full-load current** — clamp meter. Model says ~4.1 A;
      published 2.6 A is inconsistent (D2). Confirms generator/circuit sizing.
- [ ] **Gear reduction ratio** — confirms the ~67:1 inferred in D3.

When the bore is measured: set `--housing-id <measured>` and rerun
`python src/build_all.py`; the matching STL set regenerates and re-audits
automatically. If it lands outside [6.0, 6.5], widen the build matrix in
`build_all.py`.

## 2. Analysis gaps (framework extensions)

- [ ] **CFD run.** `CFDParameters` in `auger_optimizer.py` emits Bingham-
      plastic boundary conditions but nothing consumes them. Export a mesh
      from `mixer_cad.py` and run an actual solve to validate the fill-
      efficiency assumption (η≈0.35) the throughput claim rests on (D1).
- [ ] **Validate η empirically.** The 6.5" convergence assumes CEMA mid-
      range fill efficiency. A bench test (bags/hr at known RPM) would
      pin it directly and tighten the bore prediction.
- [ ] **Bearing/load-path FEA.** ENGINEERING.md §3 is now self-consistent
      (D13) but still closed-form; a frame FEA would confirm the SF≥3.3.

## 3. Enhancement roadmap (from DESIGN_INSIGHTS.md Part 2)

Ranked by value-to-effort for the 12-hour jobsite variant. Not started.

- [ ] **E1. Motor-current slump sensing** (highest value) — closed-loop
      water control off the existing motor lead. Eliminates the operator's
      full-time dial-watching task.
- [ ] **E2. Jam detection + auto-reverse** — same sensor; protects fingers
      from the 3,000 psi single-finger jam case (D4).
- [ ] **E3. BLDC motor upgrade** — brush wear is the #1 service item over
      12-hour duty; adds free torque telemetry for E1/E2.
- [ ] **E4. Hopper anti-bridging vibrator** — pulsed on E1's starvation signal.
- [ ] **E5. Quick-release auger cartridge** — end-of-day cleanout; cured
      concrete in the housing is the continuous mixer's failure mode.
- [ ] **E6. Replaceable UHMW chute wear liner** — abrasion consumable.
- [ ] **E7. Batch telemetry** — bags/runtime/water/jams to app; produces
      the dataset to confirm D1 across production units.

## 4. Repo housekeeping (optional)

- [ ] Tag a release once the bore is measured and one STL set is "blessed".
- [ ] `dist/` is git-ignored and rebuilt by CI; consider publishing the
      `mudmixer-cad-package` artifact to a release for shop access.
- [ ] If the framework grows, split `src/` into a package with `__init__`
      and absolute imports (currently flat modules, sys.path-relative).

## Done (for reference)

Framework, watertight CAD (auger + 17-component machine), discoveries
D1-D14 with corrected docs, 12-hour digital twin, CAD-reconciled BOM +
procurement audit, file-level manufacturing audit, automated build, and
CI gating lint/type-check/108 tests. See `docs/DESIGN_INSIGHTS.md` for the
discovery-to-test verification matrix.
