#!/usr/bin/env python3
"""
MudMixer Automated Build

One command regenerates EVERY artifact the project produces, then gates
the output through the manufacturing audit. This is the repo's automated
backend: CI runs it on every push and uploads the result, so artifacts
can never go stale relative to the code.

Outputs (in --out, default dist/):
    stl/            per-component + assembly STLs at 6.0" and 6.5" bores
    renders/        auger render, assembly four-view, exploded view,
                    drawing sheet, 12-hour simulation timeline
    reports/        CAD validation reports (both bores), cross-spec
                    analysis, simulation summary
    MANIFEST.txt    sha256 + size of every artifact

Exit code is non-zero if validation or the manufacturing audit fails.

Usage:
    python build_all.py --out dist

Dependencies: matplotlib (renders); everything else standard library
"""

import argparse
import contextlib
import hashlib
import io
import os

import manufacturing_audit
import mixer_analysis
import mixer_simulation
from auger_cad import build_auger_mesh, render_mesh, write_binary_stl
from auger_optimizer import AugerOptimizer
from mixer_cad import (
    build_mixer,
    export_stls,
    print_report,
    render_assembly,
    render_drawing_sheet,
    validate_assembly,
)


def _capture(func, *args, **kwargs) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue()


def build(out_dir: str) -> list[str]:
    """Generate all artifacts. Returns paths. Raises on validation failure."""
    stl_dir = os.path.join(out_dir, "stl")
    render_dir = os.path.join(out_dir, "renders")
    report_dir = os.path.join(out_dir, "reports")
    for directory in (stl_dir, render_dir, report_dir):
        os.makedirs(directory, exist_ok=True)

    artifacts: list[str] = []

    def save_report(name: str, content: str) -> str:
        path = os.path.join(report_dir, name)
        with open(path, "w") as f:
            f.write(content)
        return path

    # --- Auger (component-level) ------------------------------------------
    design = AugerOptimizer(6.0).generate_optimized_design()
    auger_mesh = build_auger_mesh(
        design["objects"]["geometry"], design["objects"]["fingers"]
    )
    auger_stl = os.path.join(stl_dir, "auger_6.0in_bore.stl")
    write_binary_stl(auger_mesh, auger_stl)
    artifacts.append(auger_stl)
    auger_png = os.path.join(render_dir, "auger.png")
    render_mesh(auger_mesh, auger_png)
    artifacts.append(auger_png)

    # --- Full machine at both design points --------------------------------
    for bore, tag in ((6.0, "baseline_6.0in"), (6.5, "converged_6.5in")):
        components = build_mixer(housing_id=bore)
        report = validate_assembly(components, housing_id=bore)
        artifacts.append(save_report(
            f"cad_validation_{tag}.txt", _capture(print_report, report)
        ))
        if not report["all_ok"]:
            raise RuntimeError(f"CAD validation failed at {bore}\" bore")

        bore_dir = os.path.join(stl_dir, tag)
        artifacts += export_stls(components, bore_dir)

        if bore == 6.0:
            assembly_png = os.path.join(render_dir, "mixer_assembly.png")
            render_assembly(components, assembly_png)
            artifacts.append(assembly_png)
            exploded_png = os.path.join(render_dir, "mixer_exploded.png")
            render_assembly(components, exploded_png, explode=9.0,
                            views=[("Exploded isometric", 20.0, -50.0)])
            artifacts.append(exploded_png)
            drawing_png = os.path.join(render_dir, "drawing_sheet.png")
            render_drawing_sheet(components, drawing_png)
            artifacts.append(drawing_png)

    # --- Analysis and simulation reports ------------------------------------
    artifacts.append(save_report(
        "cross_spec_analysis.txt", _capture(mixer_analysis.main)
    ))

    # --- Procurement package (both design points, audit-gated) --------------
    import bom_generator
    for bore, tag in ((6.0, "baseline_6.0in"), (6.5, "converged_6.5in")):
        csv_path = os.path.join(report_dir, f"bom_{tag}.csv")
        md_path = os.path.join(report_dir, f"procurement_{tag}.md")
        bom_generator.write_csv(bom_generator.full_bom(bore), csv_path)
        bom_generator.write_markdown(bore, md_path)
        artifacts += [csv_path, md_path]
        failures = [c for c in bom_generator.procurement_audit(bore)
                    if c["status"] != "OK"]
        if failures:
            raise RuntimeError(f"Procurement audit failed at {bore}\": {failures}")

    artifacts.append(save_report(
        "simulation_12hr.txt", _capture(mixer_simulation.main, [])
    ))
    sim_png = os.path.join(render_dir, "simulation_12hr.png")
    mixer_simulation.plot(
        mixer_simulation.simulate(
            mixer_simulation.SimulationConfig(dt_s=2.0)
        ),
        sim_png,
    )
    artifacts.append(sim_png)

    # --- Manufacturing audit gate -------------------------------------------
    results = manufacturing_audit.audit_paths(
        [stl_dir] + [os.path.join(stl_dir, d) for d in os.listdir(stl_dir)
                     if os.path.isdir(os.path.join(stl_dir, d))]
    )
    audit_text = "\n".join(
        f"{r['name']}: {'PASS' if r['ok'] else 'FAIL ' + '; '.join(r['failures'])}"
        f" ({r['triangles']} tris, {r['shells']} shells, "
        f"{r['volume_in3']:.1f} in³)"
        for r in results
    )
    artifacts.append(save_report("manufacturing_audit.txt", audit_text + "\n"))
    failed = [r for r in results if not r["ok"]]
    if failed:
        raise RuntimeError(
            f"Manufacturing audit failed: {[r['name'] for r in failed]}"
        )

    # --- Manifest ------------------------------------------------------------
    manifest_lines = []
    for path in sorted(artifacts):
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
        size = os.path.getsize(path)
        manifest_lines.append(
            f"{digest}  {size:>9}  {os.path.relpath(path, out_dir)}"
        )
    manifest = os.path.join(out_dir, "MANIFEST.txt")
    with open(manifest, "w") as f:
        f.write("\n".join(manifest_lines) + "\n")
    artifacts.append(manifest)

    return artifacts


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Regenerate every MudMixer artifact and audit it"
    )
    parser.add_argument("--out", default="dist", help="Output directory")
    args = parser.parse_args(argv)

    artifacts = build(args.out)
    print(f"BUILD OK: {len(artifacts)} artifacts in {args.out}/ "
          f"(STL files manufacturing-audited, validation gates passed)")
    for line in open(os.path.join(args.out, "MANIFEST.txt")):
        print(" ", line.rstrip())


if __name__ == "__main__":
    main()
