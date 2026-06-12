#!/usr/bin/env python3
"""
MudMixer Manufacturing Audit

Verifies exported STL files exactly as a fabricator's CAM/slicer software
would receive them: parses the binary files back (float32 precision, not
the float64 meshes in memory) and checks every shell for the properties
manufacturing requires:

    structure    declared triangle count matches file size, no NaN/Inf
    geometry     no degenerate (zero-area) facets
    topology     every shell closed and manifold (each directed edge
                 paired with exactly one reverse edge)
    orientation  consistent outward winding (positive enclosed volume)

Exit code is non-zero on any failure, so this is a CI gate.

Usage:
    python manufacturing_audit.py DIR_OR_FILE [...]

Dependencies: none (standard library only)
"""

import math
import os
import sys
from collections.abc import Sequence
from typing import Any

from geometry import (
    Triangle,
    facet_area,
    is_watertight,
    mesh_volume,
    read_binary_stl,
    split_shells,
)

__all__ = [
    "audit_file",
    "audit_paths",
    "audit_triangles",
    "read_binary_stl",
]

MIN_FACET_AREA_IN2 = 1e-9


def audit_triangles(triangles: Sequence[Triangle], name: str) -> dict[str, Any]:
    """Run all manufacturability checks on a parsed mesh."""
    failures: list[str] = []

    if not triangles:
        failures.append("empty mesh")

    for tri in triangles:
        for vertex in tri:
            for coordinate in vertex:
                if math.isnan(coordinate) or math.isinf(coordinate):
                    failures.append("NaN/Inf vertex coordinate")
                    break
            else:
                continue
            break
        else:
            continue
        break

    degenerate = sum(1 for t in triangles if facet_area(t) < MIN_FACET_AREA_IN2)
    if degenerate:
        failures.append(f"{degenerate} degenerate facets")

    shells = split_shells(triangles)
    open_shells = 0
    inverted_shells = 0
    total_volume = 0.0
    for shell in shells:
        if not is_watertight(shell):
            open_shells += 1
        volume = mesh_volume(shell)
        total_volume += volume
        if volume <= 0:
            inverted_shells += 1
    if open_shells:
        failures.append(f"{open_shells}/{len(shells)} shells not watertight")
    if inverted_shells:
        failures.append(f"{inverted_shells}/{len(shells)} shells inverted/non-positive")

    return {
        "name": name,
        "triangles": len(triangles),
        "shells": len(shells),
        "volume_in3": total_volume,
        "failures": failures,
        "ok": not failures,
    }


def audit_file(path: str) -> dict[str, Any]:
    """Parse an STL from disk and audit it."""
    return audit_triangles(read_binary_stl(path), os.path.basename(path))


def audit_paths(paths: Sequence[str]) -> list[dict[str, Any]]:
    """Audit STL files and/or directories of STL files."""
    files: list[str] = []
    for path in paths:
        if os.path.isdir(path):
            files += sorted(
                os.path.join(path, f) for f in os.listdir(path)
                if f.lower().endswith(".stl")
            )
        else:
            files.append(path)
    return [audit_file(f) for f in files]


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: manufacturing_audit.py DIR_OR_FILE [...]")
        return 2

    results = audit_paths(args)
    if not results:
        print("No STL files found")
        return 2

    print("=" * 76)
    print("MANUFACTURING AUDIT — STL files as a fabricator receives them")
    print("=" * 76)
    print(f"{'File':<36}{'Tris':>7}{'Shells':>8}{'Vol in³':>10}  Verdict")
    print("-" * 76)
    for r in results:
        verdict = "PASS" if r["ok"] else "FAIL: " + "; ".join(r["failures"])
        print(f"{r['name']:<36}{r['triangles']:>7}{r['shells']:>8}"
              f"{r['volume_in3']:>10.1f}  {verdict}")
    print("-" * 76)

    failed = [r for r in results if not r["ok"]]
    print(f"RESULT: {len(results) - len(failed)}/{len(results)} files "
          f"manufacturing-clean")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
