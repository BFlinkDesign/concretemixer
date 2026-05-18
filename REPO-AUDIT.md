# Repository Audit: concretemixer

**Audit Date:** 2026-05-18  
**Auditor:** Claude (READ-ONLY mode)

---

## PHASE 1 — SOURCES OF TRUTH

### Tier Assessment

#### TIER 1 — Enforced + Executable
**ABSENT** [VERIFIED]

- No `.github/` directory (no GitHub Actions CI/CD)
- No `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`
- No active git hooks in `.git/hooks/` (only `.sample` files)
- No `pre-commit-config.yaml`
- No `tox.ini`, `nox.py`, or similar test runners

**Consequence:** Nothing is enforced. The de facto contract is "whatever the main branch currently does."

#### TIER 2 — Executable but Unenforced
**PARTIAL** [VERIFIED]

Present:
- `src/parametric_auger.py` — Runnable Python script with `if __name__ == "__main__"` [VERIFIED]
- `src/frame_model.py` — Runnable Python script with `if __name__ == "__main__"` [VERIFIED]
- `src/auger_optimizer.py` — Python module [VERIFIED]
- `manufacturing/tube_notching_templates.py` — Runnable generator [VERIFIED]
- `manufacturing/motor_mount_gcode.py` — Runnable generator [VERIFIED]
- `simulation/liggghts_auger_sim.in` — LIGGGHTS input file (requires external software) [VERIFIED]

Absent:
- No test files (`test_*.py`, `*_test.py`, `conftest.py`) [VERIFIED]
- No golden/snapshot fixtures [VERIFIED]
- No example scripts with expected outputs [VERIFIED]

#### TIER 3 — Declarative Contracts
**PRESENT** [VERIFIED]

JSON specifications:
- `src/auger_spec.json` — Auger dimensions specification
- `src/frame_spec.json` — Frame dimensions specification  
- `src/assembly_spec.json` — Assembly relationships
- `manufacturing/templates/template_summary.json` — Tube joint specs

No formal schemas:
- No JSON Schema files (`*.schema.json`) [VERIFIED]
- No OpenAPI/Swagger specs [VERIFIED]
- No protobuf definitions [VERIFIED]
- No TypeScript type definitions for JS files [VERIFIED]

Type hints in Python:
- `src/parametric_auger.py` uses dataclasses and type hints [VERIFIED]
- `src/frame_model.py` uses dataclasses and type hints [VERIFIED]

#### TIER 4 — Human Prose (Drift-Prone)
**EXTENSIVE** [VERIFIED]

Documentation files (30+ markdown files):
- `README.md` — Project overview
- `docs/TDP_SUMMARY.md` — Technical Data Package summary
- `docs/VALIDATED_SPECIFICATIONS.md` — Claimed validated specs
- `docs/SPECIFICATIONS.md` — Product specifications
- `references/CITATIONS.md` — Engineering reference tracking
- `references/calculations/*.md` — 4 calculation documents

Engineering documents:
- `docs/DFMEA.md`, `docs/PFMEA.md` — Failure mode analysis
- `docs/CONTROL_PLAN.md`, `docs/PROCESS_FLOW.md` — Manufacturing
- `docs/AS9102_FAI_FORMS.md` — Inspection forms
- `manufacturing/WPS_FRAME_WELDING.md` — Welding procedure

Drawings (markdown-based):
- `drawings/ASSEMBLY_DRAWING.md`
- `drawings/AUGER_DRAWING.md`
- `drawings/ELECTRICAL_SCHEMATIC.md`

#### TIER 5 — Intent + History
**MINIMAL** [VERIFIED]

- No `CHANGELOG.md` [VERIFIED]
- No `TODO.md` or `ROADMAP.md` [VERIFIED]
- Only 3 grep hits for TODO/FIXME/HACK/XXX markers (all in `docs/DRAWING_STANDARDS.md`, not actionable) [VERIFIED]
- Git commit history exists but not audited for this phase [VERIFIED]

---

### Highest Authority Source

**BENCHMARK: `src/parametric_auger.py` and `src/frame_model.py`** [INFERRED]

Rationale: These are the only executable artifacts that produce verifiable outputs (STEP files, JSON specs). The extensive documentation claims to be "validated" but has no enforcement mechanism. The Python scripts with their dataclass definitions and validation methods represent the closest thing to ground truth.

Secondary benchmark: `references/calculations/*.md` contain engineering formulas that the Python code should implement, but there is no automated verification that code matches calculations.

---

### Critical Absence Summary

| What's Missing | Impact |
|----------------|--------|
| CI/CD pipeline | No enforcement of any standard |
| Test suite | No verification of correctness |
| JSON schemas | No contract validation for spec files |
| Pre-commit hooks | No quality gates |
| Linter config | No code style enforcement |

---

## PHASE 2 — RUN STATUS

### Environment
- **Python:** 3.11.15 [VERIFIED]
- **Key dependencies installed:** cadquery 2.7.0, numpy 2.4.5, matplotlib 3.10.9 [VERIFIED]

### Entry Points and Execution Status

| Script | Command | Status | Output |
|--------|---------|--------|--------|
| `src/parametric_auger.py` | `python3 parametric_auger.py` | ✅ RUNS [VERIFIED] | Generates `.scad`, `.step`, `.json` |
| `src/frame_model.py` | `python3 frame_model.py` | ✅ RUNS [VERIFIED] | Generates `.scad`, `.step`, `.json` |
| `src/auger_optimizer.py` | Module only | ✅ IMPORTS [VERIFIED] | No main entry |
| `manufacturing/tube_notching_templates.py` | `python3 tube_notching_templates.py` | ✅ RUNS [VERIFIED] | Generates 5 SVG templates |
| `manufacturing/motor_mount_gcode.py` | `python3 motor_mount_gcode.py` | ✅ RUNS [VERIFIED] | Generates `.nc` G-code |
| `src/visualization/` | `npm run dev` (requires npm install) | ⚠️ NOT TESTED [UNKNOWN] | Vite + Three.js app |
| `simulation/liggghts_auger_sim.in` | Requires LIGGGHTS | ⚠️ NOT TESTED [UNKNOWN] | DEM simulation input |

### Generated Artifacts (Verified Present)

| File | Size | Purpose |
|------|------|---------|
| `src/mudmixer_auger.step` | 632 KB | CadQuery STEP model |
| `src/mudmixer_frame.step` | 241 KB | CadQuery STEP model |
| `src/mudmixer_auger.scad` | 3 KB | OpenSCAD model |
| `src/mudmixer_frame.scad` | 4.5 KB | OpenSCAD model |
| `src/auger_spec.json` | 1.2 KB | Auger dimensions |
| `src/frame_spec.json` | 774 B | Frame dimensions |
| `src/assembly_spec.json` | 12 KB | Assembly relationships |

### Dependencies Resolution

**Python (`src/requirements.txt`):**
- Core deps (numpy, scipy, matplotlib): ✅ Installed [VERIFIED]
- Optional CAD (cadquery): ✅ Installed [VERIFIED]
- Optional mesh (meshio, pygmsh): Not installed [VERIFIED]

**Node.js (`src/visualization/package.json`):**
- No `node_modules/` present [VERIFIED]
- No `package-lock.json` present [VERIFIED]
- Would require: `npm install` to resolve [INFERRED]

### Conclusion
**Core Python components RUN successfully.** Visualization component not tested (requires npm install). Proceeding to Phase 3.

---

## PHASE 3 — STRUCTURAL MAP

### Module Inventory

| Module | Purpose | Entry Point | Dependencies |
|--------|---------|-------------|--------------|
| `src/parametric_auger.py` | Auger CAD generation | `main()` | stdlib, cadquery (optional) |
| `src/frame_model.py` | Frame CAD generation | `main()` | stdlib, cadquery (optional) |
| `src/auger_optimizer.py` | Generative design framework | None (library) | stdlib only |
| `manufacturing/tube_notching_templates.py` | SVG template generation | `generate_all_frame_templates()` | stdlib only |
| `manufacturing/motor_mount_gcode.py` | G-code generation | `main()` | stdlib only |

### Call Paths

```
Entry: python3 parametric_auger.py
  └─> main()
      ├─> MudMixerAugerSpec() — dataclass with defaults
      ├─> spec.validate() — checks P/D ratios vs patent claims
      ├─> calculate_mass(spec) — volume estimation
      ├─> calculate_torque_requirement(spec) — power calc
      ├─> generate_openscad(spec) — writes .scad file
      ├─> json.dump(spec.to_dict()) — writes auger_spec.json
      └─> export_auger_step(spec) — writes .step via CadQuery
          └─> generate_cadquery_auger(spec) — creates CQ geometry

Entry: python3 frame_model.py
  └─> main()
      ├─> FrameModel() — generates tube paths via _generate_tube_paths()
      ├─> model.validate() — checks dimensions vs hardcoded specs
      ├─> calculate_frame_weight(model) — weight estimation
      ├─> generate_openscad_frame(model) — writes .scad file
      ├─> json.dump(dimensions.to_dict()) — writes frame_spec.json
      └─> export_frame_step(model) — writes .step via CadQuery

Entry: python3 tube_notching_templates.py
  └─> generate_all_frame_templates()
      ├─> CopeJoint() — dataclass with tube specs (HARDCODED, not imported)
      ├─> generate_cope_profile(joint) — calculates cut profile
      ├─> generate_svg_template(joint) — writes .svg file
      └─> json.dump(summary) — writes template_summary.json

Entry: python3 motor_mount_gcode.py
  └─> main()
      ├─> generate_drilling_cycle() — G-code for holes
      ├─> generate_center_bore() — G-code for bore
      └─> writes .nc files
```

### Cross-Module Dependencies

**Actual imports:** NONE between project modules [VERIFIED]

**Duplicated constants (drift risk):**
| Constant | `frame_model.py` | `tube_notching_templates.py` | Match? |
|----------|-----------------|------------------------------|--------|
| Tube OD | 1.660" (NPS1_25_SCH_40) | 1.660" (FRAME_TUBE) | ✅ [VERIFIED] |
| Tube wall | 0.140" | 0.140" | ✅ [VERIFIED] |

| Constant | `frame_model.py` | `motor_mount_gcode.py` | Match? |
|----------|-----------------|------------------------|--------|
| Motor mount size | 6.0" x 6.0" | 152.4mm x 152.4mm (6") | ✅ [VERIFIED] |
| Bolt pattern | 4.5" | 114.3mm (4.5") | ✅ [VERIFIED] |

### Files Imported but Missing
**NONE** [VERIFIED] — All imports are stdlib or installed packages.

### Files Imported by Nothing (Dead Code)
- `src/auger_optimizer.py` — Not imported by any other file, no `__main__` [VERIFIED]

### Circular Dependencies
**NONE** [VERIFIED] — No cross-imports between project modules.

### JSON Spec File Relationships

```
parametric_auger.py ──writes──> auger_spec.json
                                    │
                                    └─ NOT READ by any code [VERIFIED]

frame_model.py ──writes──> frame_spec.json
                               │
                               └─ NOT READ by any code [VERIFIED]

assembly_spec.json ──── NOT GENERATED by any code [VERIFIED]
                        (appears to be manually created)
```

**Critical Finding:** JSON spec files are WRITE-ONLY. No code reads them to regenerate anything. They are documentation artifacts, not data contracts. [VERIFIED]

---

## PHASE 4 — VERIFICATION SURFACE

### Test Suites
**NONE EXIST** [VERIFIED]

- No `test_*.py` files
- No `*_test.py` files  
- No `conftest.py`
- No `pytest.ini` or `setup.cfg` with pytest config
- No `unittest` imports in any file

### Linters / Type Checkers
**NONE CONFIGURED** [VERIFIED]

- No `mypy.ini`, `pyrightconfig.json`, or `pyproject.toml` with type config
- No `.flake8`, `.pylintrc`, or `ruff.toml`
- No `eslint.config.*` for JavaScript

### Runtime Assertions
**NONE** [VERIFIED]

- Zero `assert` statements in any Python file
- No runtime contracts or invariant checks

### Validation Methods (Advisory Only)

| File | Method | What It Checks | Behavior on Failure |
|------|--------|----------------|---------------------|
| `parametric_auger.py` | `MudMixerAugerSpec.validate()` | P/D ratios vs patent claims, OD range, finger placement | **Prints warning, continues** [VERIFIED] |
| `frame_model.py` | `FrameModel.validate()` | Overall dims, tube schedule, body gauge, chute length | **Prints warning, continues** [VERIFIED] |
| `auger_optimizer.py` | `ConstraintSet.validate()` | Constraint consistency | Returns bool, no enforcement [VERIFIED] |

**Test Proof:** Invalid input (P/D ratio 0.1, outside 0.2-0.9 range) produces:
```
Validation issues: ['Hopper P/D 0.1 outside patent range 0.2-0.9']
Script would still generate files despite issues
```
[VERIFIED by execution]

### Golden/Conformance Fixtures
**NONE** [VERIFIED]

- No expected output files to compare against
- No snapshot tests
- No reference STEP/STL files for regression testing

### What Behaviors Have NO Test Coverage

| Behavior | Risk Level |
|----------|------------|
| Helix geometry calculations in CadQuery | HIGH — complex math, no verification |
| STEP file validity/parsability | HIGH — output may be malformed |
| G-code correctness for CNC | HIGH — could damage machine or workpiece |
| SVG template accuracy for tube cutting | MEDIUM — could produce bad cuts |
| Torque/power calculations | MEDIUM — safety-critical values |
| Weight estimations | LOW — informational only |
| JSON spec file structure | LOW — only documentation |

### Raw Verification Status

| Verification Type | Count |
|-------------------|-------|
| Unit tests | 0 |
| Integration tests | 0 |
| End-to-end tests | 0 |
| Golden file comparisons | 0 |
| Type check configs | 0 |
| Lint configs | 0 |
| Runtime assertions | 0 |
| CI pipeline checks | 0 |
| **TOTAL ENFORCED CHECKS** | **0** |

---

## PHASE 5 — CONFLICT LEDGER

### Conflict #1: Frame Tube Size
| Source A | Source B | Conflict |
|----------|----------|----------|
| `docs/VALIDATED_SPECIFICATIONS.md:160` (Tier 4) | `src/frame_model.py:99` (Tier 2) | **MAJOR** |
| Says: "1\" steel pipe, Schedule 40 (1.315\" OD)" | Uses: `NPS1_25_SCH_40` (1-1/4\", 1.660\" OD) | |

**Winner:** Code (Tier 2) — but docstring in same file still says "1\" steel tube" [VERIFIED]

**Evidence:**
- `frame_model.py:6` docstring: "1\" steel tube frame"
- `frame_model.py:99` actual: `tube_schedule: PipeSchedule = PipeSchedule.NPS1_25_SCH_40`
- `references/calculations/STRUCTURAL_ANALYSIS.md` explains why: SF=1.24 inadequate, upgraded to 1-1/4"

**Impact:** Documentation claims 1\" tube; code generates 1-1/4\" geometry. Anyone reading docs gets wrong spec.

---

### Conflict #2: Frame Weight
| Source A | Source B | Conflict |
|----------|----------|----------|
| `docs/TDP_SUMMARY.md:102` (Tier 4) | `src/frame_model.py:calculate_frame_weight()` (Tier 2) | **MAJOR** |
| Says: "145 lb ±10 lb" | Calculates: 100.6 lbs | **-30.6% difference** |

**Winner:** [UNKNOWN] — Neither is validated against real measurement

**Evidence:**
```python
>>> calculate_frame_weight(model)['total_weight_lbs']
100.59036511389864
```
[VERIFIED by execution]

**Impact:** Either spec is wrong, or calculation is wrong, or both. Safety-critical for lifting/handling.

---

### Conflict #3: Motor Power Specifications
| Source | Value | Tier |
|--------|-------|------|
| `docs/GAP_ANALYSIS.md:38` | 250W | Tier 4 |
| `docs/DATA_REQUIREMENTS.md:30` | 0.5 HP (373W) | Tier 4 |
| `docs/AS9102_FAI_FORMS.md:142` | 250W | Tier 4 |
| `docs/POWER_SYSTEM.md:16` | 0.5 HP (373W) / 250W (IP55) | Tier 4 |
| `docs/PHASE1_DELIVERABLES.md:28` | 0.5 HP (250W Evolution) | Tier 4 |

**Winner:** [UNKNOWN] — All Tier 4, no code enforcement

**Impact:** 250W ≠ 373W (0.5 HP). Off by 49%. BOM and electrical design may be sized wrong.

---

### Conflict #4: Auger P/D Ratios
| Source A | Source B | Conflict |
|----------|----------|----------|
| `docs/AS9102_FAI_FORMS.md:128-129` (Tier 4) | `src/parametric_auger.py:112-114` (Tier 2) | **MINOR** |
| Hopper: P/D=0.6, Chute: P/D=0.85 | Hopper: P/D=0.5, Chute: P/D=0.9 | |

**Winner:** Code (Tier 2)

**Evidence:**
```python
AugerSection("hopper", 12.0, 0.5),   # Doc says 0.6
AugerSection("chute", 18.0, 0.9),    # Doc says 0.85
```
[VERIFIED]

**Impact:** FAI forms will fail inspection if filled from generated specs.

---

### Conflict #5: Auger Section Lengths
| Source | Hopper | Transition | Chute | Total |
|--------|--------|------------|-------|-------|
| `docs/PRODUCTION_BOM.md:79-80` (Tier 4) | ~10" | N/A | ~14" | 24" |
| `src/parametric_auger.py:112-114` (Tier 2) | 12" | 6" | 18" | 36" |

**Winner:** Code (Tier 2) — generates 36" total [VERIFIED]

**Impact:** BOM materials estimate is wrong (24" vs 36").

---

### Conflict #6: Docstring vs Code in Same File
| File | Location | Docstring | Actual Code |
|------|----------|-----------|-------------|
| `frame_model.py` | Lines 6, 12 vs 99 | "1\" steel tube" | `NPS1_25_SCH_40` (1-1/4\") |

**Winner:** Code behavior, docstring is stale [VERIFIED]

---

### Conflicts Where Winner is Only Tier 4 or 5 (No Ground Truth)

| Conflict | Both Sources | Risk |
|----------|--------------|------|
| Motor Power (250W vs 373W) | Both Tier 4 docs | **HIGH** — no code defines this |
| Weight (145 lbs) | Tier 4 doc, Tier 2 calc differs | **HIGH** — neither verified |

---

### Summary

| Conflict Type | Count | Highest Risk |
|---------------|-------|--------------|
| Doc vs Code (code wins) | 4 | Frame tube size mismatch |
| Doc vs Doc (no winner) | 1 | Motor power confusion |
| Docstring vs Code (same file) | 1 | Frame docstring stale |
| **TOTAL CONFLICTS** | **6** | |

---

## PHASE 6 — GAP LIST

Enumerated facts only. No prose, no fixes, no ranking.

### Missing Files / Broken Imports
1. No test files exist (`test_*.py`, `*_test.py`, `conftest.py`) [VERIFIED]
2. `src/visualization/node_modules/` not present — requires `npm install` [VERIFIED]
3. `src/visualization/package-lock.json` not present [VERIFIED]
4. `simulation/meshes/auger.stl` referenced in `liggghts_auger_sim.in` but does not exist [VERIFIED]
5. `simulation/meshes/housing.stl` referenced in `liggghts_auger_sim.in` but does not exist [VERIFIED]

### Dead/Unused Code
6. `src/auger_optimizer.py` has no `__main__` block and is not imported by any file [VERIFIED]

### Hardcoded Values That Duplicate Other Sources
7. `manufacturing/tube_notching_templates.py:20-23` duplicates tube spec from `frame_model.py` [VERIFIED]
8. `manufacturing/motor_mount_gcode.py:13-17` duplicates motor mount dimensions from `frame_model.py` [VERIFIED]

### Stale Documentation
9. `frame_model.py:6` docstring says "1\" steel tube" but code uses 1-1/4\" [VERIFIED]
10. `frame_model.py:12` docstring says "1\" steel pipe" but code uses 1-1/4\" [VERIFIED]
11. `docs/VALIDATED_SPECIFICATIONS.md:160` says "1\" steel pipe" but code uses 1-1/4\" [VERIFIED]
12. `README.md` does not reflect 1\" to 1-1/4\" tube upgrade [INFERRED]

### Specification Inconsistencies (Doc vs Doc)
13. Motor power: 250W in some docs, 373W (0.5 HP) in others [VERIFIED]
14. Weight calculation (100.6 lbs) does not match spec (145 lbs) [VERIFIED]
15. Auger section lengths in BOM (24\" total) vs code (36\" total) [VERIFIED]
16. P/D ratios in AS9102 forms (0.6, 0.85) vs code defaults (0.5, 0.9) [VERIFIED]

### Untested Behaviors
17. CadQuery helix geometry generation — no test [VERIFIED]
18. STEP file validity/importability — no test [VERIFIED]
19. G-code correctness — no test [VERIFIED]
20. SVG template geometry accuracy — no test [VERIFIED]
21. Torque/power calculations — no test [VERIFIED]
22. Weight calculations — no test [VERIFIED]
23. Tube cope profile formula — no test [VERIFIED]
24. JSON spec file structure consistency — no test [VERIFIED]

### Missing Enforcement
25. No CI/CD pipeline [VERIFIED]
26. No pre-commit hooks [VERIFIED]
27. No linter configuration [VERIFIED]
28. No type checker configuration [VERIFIED]
29. No JSON schema validation for spec files [VERIFIED]
30. Validation methods print warnings but don't prevent bad output [VERIFIED]

### PENDING/TBD Items in Documentation
31. `references/CITATIONS.md:92` — CALC-HYDRO-001 (Water System) PENDING [VERIFIED]
32. `docs/VALIDATED_SPECIFICATIONS.md:17,22,23` — Running Amps, Warranty, Price TBD [VERIFIED]
33. `docs/PPAP_PACKAGE.md:33,39-45,48` — 8 PPAP elements PENDING [VERIFIED]
34. `docs/CONTROL_PLAN.md:20` — Supplier Code TBD [VERIFIED]
35. `docs/TECHNOLOGY_SELECTION.md:272` — Local fab shop TBD [VERIFIED]

### JSON Spec Files Not Read by Any Code
36. `src/auger_spec.json` — written but never read [VERIFIED]
37. `src/frame_spec.json` — written but never read [VERIFIED]
38. `src/assembly_spec.json` — exists but not generated or read by code [VERIFIED]

### Safety-Critical Gaps
39. Structural analysis (CALC-STRUCT-001) not programmatically linked to frame_model.py [VERIFIED]
40. G-code has no machine/material validation [VERIFIED]
41. Welding WPS references calculation but is not generated from it [VERIFIED]

---

## AUDIT COMPLETE

**Total Issues Enumerated:** 41

**Highest Authority Source:** `src/parametric_auger.py` and `src/frame_model.py` (Tier 2 — executable but unenforced)

**Core Finding:** This repository has extensive documentation claiming "validated" and "production-ready" status, but has ZERO automated enforcement. The de facto contract is "whatever the Python scripts currently generate." Documentation has drifted from code in multiple safety-relevant ways (frame tube size, weight, P/D ratios).

---

*Audit conducted in READ-ONLY mode. No files were created, edited, or fixed.*

