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
import struct
import sys
from collections import Counter
from typing import Dict, List, Sequence, Tuple

Vec3 = Tuple[float, float, float]
Triangle = Tuple[Vec3, Vec3, Vec3]

MIN_FACET_AREA_IN2 = 1e-9


def read_binary_stl(path: str) -> List[Triangle]:
    """Parse a binary STL file, validating its declared structure."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.read(80)
        (count,) = struct.unpack("<I", f.read(4))
        expected_size = 84 + 50 * count
        if size != expected_size:
            raise ValueError(
                f"{path}: file is {size} bytes, header declares {count} "
                f"triangles ({expected_size} bytes)"
            )
        triangles = []
        for _ in range(count):
            values = struct.unpack("<12fH", f.read(50))
            triangles.append((
                (values[3], values[4], values[5]),
                (values[6], values[7], values[8]),
                (values[9], values[10], values[11]),
            ))
    return triangles


def _facet_area(tri: Triangle) -> float:
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    return 0.5 * math.sqrt(nx * nx + ny * ny + nz * nz)


def split_shells(triangles: Sequence[Triangle]) -> List[List[Triangle]]:
    """Group triangles into vertex-connected shells (union-find)."""
    parent = list(range(len(triangles)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    seen: Dict[Vec3, int] = {}
    for index, tri in enumerate(triangles):
        for vertex in tri:
            if vertex in seen:
                union(seen[vertex], index)
            else:
                seen[vertex] = index

    shells: Dict[int, List[Triangle]] = {}
    for index, tri in enumerate(triangles):
        shells.setdefault(find(index), []).append(tri)
    return list(shells.values())


def _is_watertight(triangles: Sequence[Triangle]) -> bool:
    edges = Counter()
    for v0, v1, v2 in triangles:
        edges[(v0, v1)] += 1
        edges[(v1, v2)] += 1
        edges[(v2, v0)] += 1
    return all(
        count == 1 and edges[(b, a)] == 1 for (a, b), count in edges.items()
    )


def _signed_volume(triangles: Sequence[Triangle]) -> float:
    total = 0.0
    for v0, v1, v2 in triangles:
        cx = v1[1] * v2[2] - v1[2] * v2[1]
        cy = v1[2] * v2[0] - v1[0] * v2[2]
        cz = v1[0] * v2[1] - v1[1] * v2[0]
        total += (v0[0] * cx + v0[1] * cy + v0[2] * cz) / 6.0
    return total


def audit_triangles(triangles: Sequence[Triangle], name: str) -> Dict[str, object]:
    """Run all manufacturability checks on a parsed mesh."""
    failures: List[str] = []

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

    degenerate = sum(1 for t in triangles if _facet_area(t) < MIN_FACET_AREA_IN2)
    if degenerate:
        failures.append(f"{degenerate} degenerate facets")

    shells = split_shells(triangles)
    open_shells = 0
    inverted_shells = 0
    total_volume = 0.0
    for shell in shells:
        if not _is_watertight(shell):
            open_shells += 1
        volume = _signed_volume(shell)
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


def audit_file(path: str) -> Dict[str, object]:
    """Parse an STL from disk and audit it."""
    return audit_triangles(read_binary_stl(path), os.path.basename(path))


def audit_paths(paths: Sequence[str]) -> List[Dict[str, object]]:
    """Audit STL files and/or directories of STL files."""
    files: List[str] = []
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
