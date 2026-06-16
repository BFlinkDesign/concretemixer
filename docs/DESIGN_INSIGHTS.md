# Design Insights — Unique Discoveries & Enhancement Roadmap

Findings produced by the computational framework (`src/`), each derived
from physics applied across the published specifications and patents —
not from any single source. Every number below is reproducible:

```bash
python src/mixer_analysis.py        # cross-specification analysis
python src/mixer_cad.py --report    # full-machine CAD validation
python -m pytest src/               # 108-test verification suite
```

---

## Part 1 — Unique Discoveries

### D1. The throughput claim reveals the true housing bore (~6.5", not 6.0")

The repo's #1 unknown ([DATA_REQUIREMENTS.md](./DATA_REQUIREMENTS.md)) is
the housing internal diameter, assumed 6.0". Inverting the screw-conveyor
flow equation `Q = (π/4)·D³·(P/D)·N·η` against the manufacturer's claimed
45 bags/hr at η = 0.35 (CEMA inclined-screw mid-range) gives:

| Quantity | Value |
|---|---|
| Implied auger OD | **≈ 5.0"** |
| Implied housing ID | **≈ 6.5"** |
| At the assumed 6.0" bore, claim requires | η = 0.47 (above the 0.30–0.45 CEMA range) |

**Prediction:** a bore-gauge measurement will find ~6.4–6.6", not 6.0".
This is a falsifiable, measurable refinement of the reverse-engineering
baseline. (`mixer_analysis.implied_auger_size`)

### D2. The published electrical specs violate conservation of energy

The spec sheet states **0.5 HP (373 W mechanical output)** *and*
**2.6 A @ 120 V (312 W electrical input)** — an implied efficiency of
120%. Both cannot describe continuous full-load operation. At a realistic
75% drive efficiency, full 0.5 HP requires **~4.1 A**; conversely 2.6 A
continuous supports at most **~0.31 HP**. The "0.5 HP" rating is most
plausibly a peak/stall figure. This matters for the 12-hour duty-cycle
design: generator and circuit sizing should assume ≥ 4–5 A.
(`mixer_analysis.power_audit`)

### D3. "Direct drive" conceals a ~67:1 reduction

A 0.5 HP DC motor natively runs 1750–3600 RPM; the auger turns ~27 RPM.
The "direct drive" is necessarily an integrated gearmotor with a
**~67:1** reduction (at an 1800 RPM base), delivering **~83 ft-lb** at
the auger after gearbox losses. This also explains the **left-hand Acme**
coupling in patent 10,259,140: with the auger's forward rotation, a LH
thread self-tightens under load where a RH thread would unscrew.
(`mixer_analysis.drivetrain_analysis`)

### D4. Single-finger jam is the governing structural case — UHMW fingers fail it

The original shear analysis divided motor torque across all 8 fingers
(~370 psi on UHMW — passes). But the governing case is a stone wedged
against **one** finger reacting the full ~97 ft-lb alone: **~3,000 psi**.
UHMW (allowable 800 psi at SF 2.5) **fails**; 1045 steel (allowable
4,800 psi) passes with margin. This independently confirms the steel-
finger requirement reached earlier via thermal arguments.
(`AugerOptimizer.calculate_finger_shear`)

### D5. The default finger length cannot physically fit

A 2.0" finger projecting inward from the flight inner edge (inner radius
≈ 1.85" at the 6" bore) would cross the auger centerline — opposing
fingers would collide and the open center (the shaftless design's
defining feature) would be blocked. Maximum workable finger projection at
this geometry is **≈ 1.5"**. The CAD module clamps finger length to
preserve a minimum open-center radius. (`auger_cad.build_finger_mesh`)

### D6. Skeleton sizing was 36% oversized by a double-counted safety factor

The torsion sizing applied SF = 2.5 both in the allowable stress *and* on
the torque, inflating the minimum skeleton diameter from 0.78" to 1.06".
Corrected: **0.78" minimum → 0.875" standard stock**.
(`AugerOptimizer.calculate_skeleton_diameter`)

### D7. Water system operating point: 0.66 GPM through ~0.047" orifices

Mass balance at 45 bags/hr with 3.5 qt/bag: **0.66 GPM total**
(0.33 GPM/nozzle), making water **8.4%** of wet-mix mass flow. At the
specified 30 PSI minimum supply, each nozzle orifice computes to
**~3/64" (0.047")** — small enough that *water filtration matters*:
a clogged nozzle halves hydration and the mix stiffens at the discharge.
A garden hose (4–6 GPM available) has > 6× headroom.
(`mixer_analysis.water_demand`)

### D8. The CAD mass budget closes on the 145 lb spec

Building every major component as a watertight solid with real material
densities yields **131 lb modeled** + 8–22 lb of unmodeled hardware
(guard, pivot plates, plumbing, fasteners) = **139–153 lb**, bracketing
the published 145 lb. The spec weight is consistent with 14 ga
construction. (`mixer_cad.validate_assembly`)

### D9. Ergonomics: the loaded machine takes ~72 lb at the handles

From the mesh-derived center of gravity: empty CG sits 0.4" ahead of
mid-frame, 59% of weight on the wheels; wheelbarrow-style handle lift is
**~41 lb empty** and **~72 lb with a full 120 lb hopper** — heavy but
two-person manageable, and the loaded CG stays 18.7" behind the axle
(no forward tip at any hopper level). Practical takeaway: **position the
mixer before loading**. (`mixer_cad.validate_assembly`)

### D10. Hopper rated capacity corresponds to a 76% fill

The modeled hopper cavity (1.5 ft³) holds ~158 lb of dry mix struck
level; the 120 lb rating is a 76% fill — sensible headroom for bag
dumping and the guard. The optional 300 lb extension therefore roughly
*triples* cavity volume, consistent with the published extension photos.
(`mixer_analysis.hopper_capacity_check`)

### D11. The design is self-consistent only at the 6.5" bore

Closing the D1 loop with fixed-point iteration (bore → optimized
geometry → predicted throughput → implied bore) converges in 2
iterations to **bore 6.48", auger OD 4.98", pitches 3.23"/4.23"** — a
design point that reproduces the claimed 45.0 bags/hr exactly at CEMA
mid-range fill efficiency while satisfying every patent P/D constraint.
The published performance and the patent geometry agree with each other
*only* at this size. (`mixer_analysis.converged_design`)

### D12. A simulated 12-hour day independently reproduces the duty-cycle spec

The time-domain simulation (`mixer_simulation.py`) of a full jobsite day
at the converged design point — operator feed loop, lunch break, thermal
lags, honest electrical draw — yields:

| Quantity | Simulated | Cross-reference |
|---|---|---|
| Bags mixed | **524** | `DutyCycle.JOBSITE_12HR` defined 500/session (+4.8%) |
| Concrete placed | 11.6 yd³ | ~1 yd³/hr claim ✓ |
| Water | 458 gal | D7 rate × runtime ✓ |
| Energy | 5.7 kWh | ~$1 of electricity per 12 yd³ day |
| Steel fingers | peak 156°F | 644°F margin |
| UHMW fingers | peak 156°F | **exceeds 116°F heat-deflection within the first hour** |
| Enclosure (no fan) | 147°F | above the 140°F electronics derating threshold |
| Enclosure (with fan) | 112°F | confirms "active cooling required" |

The UHMW result sharpens the material conclusion: UHMW fingers don't
melt in service — they *soften and deform* (deflection limit crossed in
under an hour of continuous mixing), losing mixing effectiveness long
before visible failure. The enclosure numbers convert the README's
"active cooling required" from a judgment into a computed requirement.

### D13. The repo's own structural analysis used wrong load paths (now corrected)

[ENGINEERING.md](./ENGINEERING.md) originally modeled the axle with 100%
of machine weight on a 6" moment arm (61,875 psi — "needs 3/4" hardened
axle") and the frame as a single tube under a 500 lb point load
(44,117 psi > 36,000 psi yield, yet labeled "adequate"). Both load paths
were wrong:

- The CAD mass model shows wheels carry **~59%** of weight when parked,
  and the true bending arm is the **~2"** bracket-to-wheel offset.
  Corrected axle stress: **16,700 psi → SF 2.2–3.2** — the production
  machine's 5/8" axle is fine, which is presumably why MudMixer ships one.
- The frame load is shared by two rails and distributed: **10,900 psi →
  SF 3.3** (or 5,600 psi with true schedule-40 pipe).

The CAD-derived load fractions turned a self-contradictory hand
calculation into a consistent one. (`mixer_cad.validate_assembly`,
corrected derivations in ENGINEERING.md §3)

### D14. The original BOM specifies a machine that jams, blows its fuse, and over-waters

Running the procurement audit (`bom_generator.procurement_audit`) against
the hand-written [BOM.md](./BOM.md) found three buy-list errors:

| BOM item | As written | Problem | Corrected |
|---|---|---|---|
| 3.1 + 4.1 | 5.5" auger in 6" ID chute | 0.25"/side — jams on the confirmed 0.5" aggregate (needs 0.60") | 4.5" @ 6.0" bore / 5.0" @ 6.5" bore |
| 5.11 | 15 A fuse | 24 V DC bus draws ~18 A at 0.5 HP — blows at full load | 25 A fuse, 10 AWG DC wiring |
| 6.6 | 1/8" nozzle orifice | ~7× the required 0.33 GPM/nozzle at 30 PSI | ~3/64" orifice + inline filter |

The $360–650 cost estimate also underbudgets the sealed ~67:1 gearmotor;
the reconciled total is ~$1,050. Procurement now comes from
`src/bom_generator.py`, which derives raw-stock quantities (24 ft² of
14 ga sheet, 23.5 ft of 1" pipe, flight/skeleton/axle bar stock) from
the CAD mesh volumes and audit-gates the parts list in CI.

---

## Part 2 — Rich Enhancement Opportunities

Ranked by value-to-effort for the optimized 12-hour jobsite variant.

### E1. Motor-current slump sensing (closed-loop water control) — highest value
Auger torque rises monotonically with mix stiffness, and DC motor current
is proportional to torque. A $5 current sensor on the existing motor lead
gives a real-time consistency signal; a PID loop driving a proportional
water valve holds slump constant as ambient temperature, bag moisture,
and feed rate drift. Eliminates the operator's main full-time task
(dial-watching) during 12-hour runs. Pairs with D2: the current sensor
also provides honest load data.

### E2. Jam detection + auto-reverse
The same current sensor detects the D4 jam signature (current spike to
stall). Firmware response: cut power within ~100 ms, auto-reverse one
revolution, retry. Protects the fingers from the 3,000 psi jam case and
clears most aggregate wedges without operator intervention. The motor is
already reversible — this is software plus one sensor.

### E3. BLDC upgrade for the 12-hour duty cycle
A 750 W BLDC with FOC replaces the brushed DC motor: no brush wear over
12-hour duty (brushes are the #1 service item), ~10–15% efficiency gain
(extends D2's battery runtimes), soft-start (kinder to the LH Acme
coupling), and free torque telemetry for E1/E2.

### E4. Hopper anti-bridging vibrator
Dry mix with 0.5" aggregate bridges over apertures when the wall half
angle is too shallow for its ~35–40° angle of repose. A 12 V eccentric
vibration motor on the hopper wall, pulsed only when E1's current signal
shows feed starvation (current droop at constant RPM), prevents
rat-holing during continuous runs.

### E5. Quick-release auger cartridge
Cleanup is the continuous mixer's weak point: cured concrete in the
housing is fatal. Replace the welded-in auger with a cartridge: auger +
front bearing + wear sleeve as one assembly retained by the swivel
collar's cam-lock. End-of-day swap in minutes; second cartridge runs
while the first soaks.

### E6. Replaceable chute wear liner
Concrete is highly abrasive; D1's flow numbers imply ~12 yd³/day of
aggregate-laden mix over the housing bottom in 12-hour duty. A UHMW
half-shell liner (UHMW is fine *here* — it sees abrasion, not the finger
jam loads of D4) extends housing life and is a consumable, not a weldment.

### E7. Batch telemetry
Bags mixed (current-signature counting via E1's sensor), runtime, water
totals, and jam counts logged to BLE/app. Turns the 45 bags/hr marketing
number into a measured fleet statistic — and provides the dataset that
would let D1's bore estimate be confirmed across production units.

---

## Verification Matrix

| Insight | Computed by | Tested in |
|---|---|---|
| D1 | `mixer_analysis.implied_auger_size` | `test_mixer.py::TestThroughputAnalysis` |
| D2 | `mixer_analysis.power_audit` | `test_mixer.py::TestWaterAndPower` |
| D3 | `mixer_analysis.drivetrain_analysis` | `test_mixer.py::TestWaterAndPower` |
| D4 | `AugerOptimizer.calculate_finger_shear` | `test_auger_optimizer.py::TestFingerShear` |
| D5 | `auger_cad.build_finger_mesh` | `test_auger_cad.py::TestFullMesh` |
| D6 | `AugerOptimizer.calculate_skeleton_diameter` | `test_auger_optimizer.py::TestSkeletonSizing` |
| D7 | `mixer_analysis.water_demand` | `test_mixer.py::TestWaterAndPower` |
| D8, D9 | `mixer_cad.validate_assembly` | `test_mixer.py::TestAssembly` |
| D10 | `mixer_analysis.hopper_capacity_check` | `test_mixer.py::TestHopperCapacity` |
| D11 | `mixer_analysis.converged_design` | `test_mixer_simulation.py::TestConvergedDesign` |
| D12 | `mixer_simulation.simulate` | `test_mixer_simulation.py` (mass/energy/thermal) |
