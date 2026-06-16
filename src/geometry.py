#!/usr/bin/env python3
"""
Shared mesh geometry library for the MudMixer computational framework.

Single source of truth for the triangle-mesh math used by auger_cad,
mixer_cad, and manufacturing_audit:

    vectors      sub, cross, normalize
    mesh math    volume, centroid, bounding box, watertightness,
                 facet area, shell splitting, orientation flip
    transforms   rotation matrices, rigid transform, Rodrigues rotation
    primitives   box, cylinder, tube, rectangular funnel, pipe between
                 two points — all watertight, outward-wound solids
    STL I/O      binary write and validated binary read

Everything is standard library only and unit-consistent (inches).
"""

import math
import struct
from collections import Counter
from collections.abc import Sequence

Vec3 = tuple[float, float, float]
Triangle = tuple[Vec3, Vec3, Vec3]
Matrix3 = tuple[Vec3, Vec3, Vec3]

# ---------------------------------------------------------------------------
# Vector operations
# ---------------------------------------------------------------------------


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def normalize(v: Vec3) -> Vec3:
    mag = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if mag == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / mag, v[1] / mag, v[2] / mag)


# ---------------------------------------------------------------------------
# Mesh measurements
# ---------------------------------------------------------------------------


def mesh_volume(triangles: Sequence[Triangle]) -> float:
    """Signed enclosed volume via the divergence theorem (in³).

    Positive for consistently outward-wound watertight meshes.
    """
    volume = 0.0
    for v0, v1, v2 in triangles:
        c = cross(v1, v2)
        volume += (v0[0] * c[0] + v0[1] * c[1] + v0[2] * c[2]) / 6.0
    return volume


def mesh_centroid(triangles: Sequence[Triangle]) -> Vec3:
    """Volume centroid via signed tetrahedron decomposition."""
    volume = 0.0
    cx = cy = cz = 0.0
    for v0, v1, v2 in triangles:
        c = cross(v1, v2)
        tet = (v0[0] * c[0] + v0[1] * c[1] + v0[2] * c[2]) / 6.0
        volume += tet
        cx += tet * (v0[0] + v1[0] + v2[0]) / 4.0
        cy += tet * (v0[1] + v1[1] + v2[1]) / 4.0
        cz += tet * (v0[2] + v1[2] + v2[2]) / 4.0
    if volume == 0:
        return (0.0, 0.0, 0.0)
    return (cx / volume, cy / volume, cz / volume)


def bounding_box(triangles: Sequence[Triangle]) -> tuple[Vec3, Vec3]:
    xs = [v[0] for tri in triangles for v in tri]
    ys = [v[1] for tri in triangles for v in tri]
    zs = [v[2] for tri in triangles for v in tri]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def is_watertight(triangles: Sequence[Triangle]) -> bool:
    """True if every directed edge is paired with exactly one reverse edge.

    This is the closed + manifold + consistently-oriented condition a
    printable/CAM-ready mesh must satisfy.
    """
    edges: Counter[tuple[Vec3, Vec3]] = Counter()
    for v0, v1, v2 in triangles:
        edges[(v0, v1)] += 1
        edges[(v1, v2)] += 1
        edges[(v2, v0)] += 1
    return all(count == 1 and edges[(b, a)] == 1 for (a, b), count in edges.items())


def facet_area(tri: Triangle) -> float:
    n = cross(sub(tri[1], tri[0]), sub(tri[2], tri[0]))
    return 0.5 * math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)


def flip(triangles: Sequence[Triangle]) -> list[Triangle]:
    """Reverse the orientation of every triangle."""
    return [(a, c, b) for a, b, c in triangles]


def split_shells(triangles: Sequence[Triangle]) -> list[list[Triangle]]:
    """Group triangles into vertex-connected shells (union-find)."""
    parent = list(range(len(triangles)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    seen: dict[Vec3, int] = {}
    for index, tri in enumerate(triangles):
        for vertex in tri:
            if vertex in seen:
                union(seen[vertex], index)
            else:
                seen[vertex] = index

    shells: dict[int, list[Triangle]] = {}
    for index, tri in enumerate(triangles):
        shells.setdefault(find(index), []).append(tri)
    return list(shells.values())


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------


def rot_x(angle_deg: float) -> Matrix3:
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return ((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c))


def rot_y(angle_deg: float) -> Matrix3:
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return ((c, 0.0, s), (0.0, 1.0, 0.0), (-s, 0.0, c))


def rotation_to(direction: Vec3) -> Matrix3 | None:
    """Rotation taking +z onto `direction` (Rodrigues). None = identity."""
    dn = normalize(direction)
    axis = cross((0.0, 0.0, 1.0), dn)
    s = math.sqrt(axis[0] ** 2 + axis[1] ** 2 + axis[2] ** 2)
    c = dn[2]
    if s < 1e-9:
        return None if c > 0 else rot_x(180.0)
    ax = normalize(axis)
    k = 1 - c
    return (
        (c + ax[0] * ax[0] * k, ax[0] * ax[1] * k - ax[2] * s, ax[0] * ax[2] * k + ax[1] * s),
        (ax[1] * ax[0] * k + ax[2] * s, c + ax[1] * ax[1] * k, ax[1] * ax[2] * k - ax[0] * s),
        (ax[2] * ax[0] * k - ax[1] * s, ax[2] * ax[1] * k + ax[0] * s, c + ax[2] * ax[2] * k),
    )


def transform(
    triangles: Sequence[Triangle],
    rotation: Matrix3 | None = None,
    translation: Vec3 = (0.0, 0.0, 0.0),
) -> list[Triangle]:
    """Apply rotation then translation to every vertex."""

    def apply(v: Vec3) -> Vec3:
        if rotation is not None:
            v = (
                rotation[0][0] * v[0] + rotation[0][1] * v[1] + rotation[0][2] * v[2],
                rotation[1][0] * v[0] + rotation[1][1] * v[1] + rotation[1][2] * v[2],
                rotation[2][0] * v[0] + rotation[2][1] * v[1] + rotation[2][2] * v[2],
            )
        return (v[0] + translation[0], v[1] + translation[1], v[2] + translation[2])

    return [(apply(a), apply(b), apply(c)) for a, b, c in triangles]


# ---------------------------------------------------------------------------
# Watertight solid primitives
# ---------------------------------------------------------------------------


def box(lx: float, ly: float, lz: float) -> list[Triangle]:
    """Axis-aligned box centered at the origin."""
    x, y, z = lx / 2, ly / 2, lz / 2
    p: list[Vec3] = [
        (-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
        (-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z),
    ]
    quads = [
        (0, 3, 2, 1),  # bottom (-z)
        (4, 5, 6, 7),  # top (+z)
        (0, 1, 5, 4),  # front (-y)
        (2, 3, 7, 6),  # back (+y)
        (1, 2, 6, 5),  # right (+x)
        (3, 0, 4, 7),  # left (-x)
    ]
    triangles: list[Triangle] = []
    for a, b, c, d in quads:
        triangles.append((p[a], p[b], p[c]))
        triangles.append((p[a], p[c], p[d]))
    return triangles


def cylinder(radius: float, height: float, segments: int = 32) -> list[Triangle]:
    """Closed cylinder along +z from z=0 to z=height."""
    bottom: list[Vec3] = [
        (radius * math.cos(2 * math.pi * j / segments),
         radius * math.sin(2 * math.pi * j / segments), 0.0)
        for j in range(segments)
    ]
    top: list[Vec3] = [(x, y, height) for x, y, _ in bottom]

    triangles: list[Triangle] = []
    for j in range(segments):
        jn = (j + 1) % segments
        triangles.append((bottom[j], bottom[jn], top[jn]))
        triangles.append((bottom[j], top[jn], top[j]))

    c_bot: Vec3 = (0.0, 0.0, 0.0)
    c_top: Vec3 = (0.0, 0.0, height)
    for j in range(segments):
        jn = (j + 1) % segments
        triangles.append((c_bot, bottom[jn], bottom[j]))
        triangles.append((c_top, top[j], top[jn]))
    return triangles


def tube(
    outer_radius: float, inner_radius: float, height: float, segments: int = 48
) -> list[Triangle]:
    """Closed annular tube (pipe with wall) along +z from z=0 to z=height."""

    def ring(radius: float, z: float) -> list[Vec3]:
        return [
            (radius * math.cos(2 * math.pi * j / segments),
             radius * math.sin(2 * math.pi * j / segments), z)
            for j in range(segments)
        ]

    ob, ot = ring(outer_radius, 0.0), ring(outer_radius, height)
    ib, it = ring(inner_radius, 0.0), ring(inner_radius, height)

    triangles: list[Triangle] = []
    for j in range(segments):
        jn = (j + 1) % segments
        # Outer wall faces outward, inner wall faces the bore.
        triangles.append((ob[j], ob[jn], ot[jn]))
        triangles.append((ob[j], ot[jn], ot[j]))
        triangles.append((ib[jn], ib[j], it[j]))
        triangles.append((ib[jn], it[j], it[jn]))
        # Annular end rings: top faces +z, bottom faces -z.
        triangles.append((ot[j], ot[jn], it[jn]))
        triangles.append((ot[j], it[jn], it[j]))
        triangles.append((ob[jn], ob[j], ib[j]))
        triangles.append((ob[jn], ib[j], ib[jn]))
    return triangles


def rect_funnel(
    top_lx: float, top_ly: float,
    bottom_lx: float, bottom_ly: float,
    height: float, wall: float,
) -> list[Triangle]:
    """Open-top, open-bottom rectangular hopper shell with wall thickness.

    Base aperture is at z=0, rim at z=height. Both openings are framed by
    annular rings so the shell is a closed watertight solid.
    """

    def rect(lx: float, ly: float, z: float) -> list[Vec3]:
        x, y = lx / 2, ly / 2
        # Counterclockwise viewed from +z
        return [(x, y, z), (-x, y, z), (-x, -y, z), (x, -y, z)]

    o_top = rect(top_lx, top_ly, height)
    o_bot = rect(bottom_lx, bottom_ly, 0.0)
    i_top = rect(top_lx - 2 * wall, top_ly - 2 * wall, height)
    i_bot = rect(bottom_lx - 2 * wall, bottom_ly - 2 * wall, 0.0)

    triangles: list[Triangle] = []
    for k in range(4):
        kn = (k + 1) % 4
        # Outer wall (outward) and inner wall (faces the cavity)
        triangles.append((o_bot[k], o_bot[kn], o_top[kn]))
        triangles.append((o_bot[k], o_top[kn], o_top[k]))
        triangles.append((i_bot[kn], i_bot[k], i_top[k]))
        triangles.append((i_bot[kn], i_top[k], i_top[kn]))
        # Rim ring (+z) and aperture ring (-z)
        triangles.append((o_top[k], o_top[kn], i_top[kn]))
        triangles.append((o_top[k], i_top[kn], i_top[k]))
        triangles.append((o_bot[kn], o_bot[k], i_bot[k]))
        triangles.append((o_bot[kn], i_bot[k], i_bot[kn]))
    return triangles


def pipe_between(
    p0: Vec3, p1: Vec3, radius: float = 0.5, segments: int = 20
) -> list[Triangle]:
    """Solid rod from p0 to p1 (e.g. a frame pipe member)."""
    d = sub(p1, p0)
    length = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
    return transform(cylinder(radius, length, segments), rotation_to(d), p0)


# ---------------------------------------------------------------------------
# STL I/O
# ---------------------------------------------------------------------------


def write_binary_stl(
    triangles: Sequence[Triangle],
    path: str,
    solid_name: str = "MudMixer part",
) -> None:
    """Write triangles to a binary STL file with unit facet normals."""
    header = solid_name.encode("ascii", errors="replace")[:80].ljust(80, b"\0")
    with open(path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(triangles)))
        for v0, v1, v2 in triangles:
            normal = normalize(cross(sub(v1, v0), sub(v2, v0)))
            f.write(struct.pack("<12fH", *normal, *v0, *v1, *v2, 0))


def read_binary_stl(path: str) -> list[Triangle]:
    """Parse a binary STL file, validating its declared structure."""
    import os

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
        triangles: list[Triangle] = []
        for _ in range(count):
            values = struct.unpack("<12fH", f.read(50))
            triangles.append((
                (values[3], values[4], values[5]),
                (values[6], values[7], values[8]),
                (values[9], values[10], values[11]),
            ))
    return triangles
