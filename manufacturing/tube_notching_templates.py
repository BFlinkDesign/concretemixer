#!/usr/bin/env python3
"""
Tube Notching/Coping Template Generator for MudMixer Frame

Generates printable SVG templates for cutting tube joints.
Based on validated frame spec: 1-1/4" Schedule 40 (OD=1.660")

Reference: CALC-STRUCT-001 - Frame upgraded to 1-1/4" Sch 40 for SF=2.19
"""

import math
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TubeSpec:
    """Tube specification from ASTM A513 / AISC Manual"""
    name: str
    od_inches: float  # Outer diameter
    wall_inches: float  # Wall thickness

    @property
    def od_mm(self) -> float:
        return self.od_inches * 25.4

    @property
    def circumference_mm(self) -> float:
        return math.pi * self.od_mm

# Validated tube spec per CALC-STRUCT-001
FRAME_TUBE = TubeSpec(
    name="1-1/4\" Schedule 40",
    od_inches=1.660,
    wall_inches=0.140
)

@dataclass
class CopeJoint:
    """Defines a tube coping joint"""
    name: str
    cope_tube: TubeSpec  # Tube being cut
    mating_tube: TubeSpec  # Tube it mates against
    angle_degrees: float  # Joint angle (90° = perpendicular)

def generate_cope_profile(joint: CopeJoint, points: int = 360) -> List[Tuple[float, float]]:
    """
    Generate the cope cut profile for a tube joint.

    Returns list of (x, y) points where:
    - x = position around tube circumference (0 to circumference)
    - y = cut depth from tube end

    Math: For tube A coping into tube B at angle θ:
    y(φ) = (R_B / sin(θ)) * (1 - cos(φ))

    Where φ is angle around cope tube, R_B is mating tube radius
    """
    R_cope = joint.cope_tube.od_mm / 2
    R_mate = joint.mating_tube.od_mm / 2
    theta = math.radians(joint.angle_degrees)

    circumference = joint.cope_tube.circumference_mm
    profile = []

    for i in range(points + 1):
        phi = (i / points) * 2 * math.pi  # Angle around tube
        x = (i / points) * circumference  # Position on flattened template

        # Cope depth formula for cylinder intersection
        y = (R_mate / math.sin(theta)) * (1 - math.cos(phi))

        profile.append((x, y))

    return profile

def generate_svg_template(joint: CopeJoint, filename: str) -> str:
    """
    Generate printable SVG template for tube coping.

    Template is designed to wrap around the tube.
    Print at 100% scale (no fit-to-page).
    """
    profile = generate_cope_profile(joint)

    # SVG dimensions
    width_mm = joint.cope_tube.circumference_mm + 20  # Add margins
    max_depth = max(p[1] for p in profile)
    height_mm = max_depth + 40  # Add margins

    # Scale for printing (1:1)
    margin = 10

    # Build SVG path
    path_d = f"M {profile[0][0] + margin} {profile[0][1] + margin}"
    for x, y in profile[1:]:
        path_d += f" L {x + margin} {y + margin}"

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width_mm}mm" height="{height_mm}mm"
     viewBox="0 0 {width_mm} {height_mm}">

  <!-- Template for: {joint.name} -->
  <!-- Cope tube: {joint.cope_tube.name} (OD={joint.cope_tube.od_inches}") -->
  <!-- Mating tube: {joint.mating_tube.name} (OD={joint.mating_tube.od_inches}") -->
  <!-- Joint angle: {joint.angle_degrees}° -->
  <!-- Print at 100% scale - DO NOT fit to page -->

  <style>
    .cut-line {{ stroke: black; stroke-width: 0.5; fill: none; }}
    .guide-line {{ stroke: #888; stroke-width: 0.25; stroke-dasharray: 2,2; fill: none; }}
    .text {{ font-family: Arial; font-size: 3mm; }}
  </style>

  <!-- Background -->
  <rect x="0" y="0" width="{width_mm}" height="{height_mm}" fill="white"/>

  <!-- Title -->
  <text x="{width_mm/2}" y="5" class="text" text-anchor="middle" font-weight="bold">
    {joint.name} - Print at 100%
  </text>

  <!-- Circumference guide line (wrap alignment) -->
  <line x1="{margin}" y1="{margin}" x2="{joint.cope_tube.circumference_mm + margin}" y2="{margin}"
        class="guide-line"/>

  <!-- Cut profile -->
  <path d="{path_d}" class="cut-line"/>

  <!-- Alignment marks at 90° intervals -->
  <line x1="{margin}" y1="{margin - 3}" x2="{margin}" y2="{margin + 3}" stroke="red" stroke-width="0.5"/>
  <text x="{margin}" y="{margin - 5}" class="text" text-anchor="middle" font-size="2mm">0°</text>

  <line x1="{joint.cope_tube.circumference_mm/4 + margin}" y1="{margin - 3}"
        x2="{joint.cope_tube.circumference_mm/4 + margin}" y2="{margin + 3}" stroke="red" stroke-width="0.5"/>
  <text x="{joint.cope_tube.circumference_mm/4 + margin}" y="{margin - 5}" class="text" text-anchor="middle" font-size="2mm">90°</text>

  <line x1="{joint.cope_tube.circumference_mm/2 + margin}" y1="{margin - 3}"
        x2="{joint.cope_tube.circumference_mm/2 + margin}" y2="{margin + 3}" stroke="red" stroke-width="0.5"/>
  <text x="{joint.cope_tube.circumference_mm/2 + margin}" y="{margin - 5}" class="text" text-anchor="middle" font-size="2mm">180°</text>

  <line x1="{3*joint.cope_tube.circumference_mm/4 + margin}" y1="{margin - 3}"
        x2="{3*joint.cope_tube.circumference_mm/4 + margin}" y2="{margin + 3}" stroke="red" stroke-width="0.5"/>
  <text x="{3*joint.cope_tube.circumference_mm/4 + margin}" y="{margin - 5}" class="text" text-anchor="middle" font-size="2mm">270°</text>

  <!-- Dimensions -->
  <text x="{margin}" y="{height_mm - 5}" class="text" font-size="2mm">
    Circumference: {joint.cope_tube.circumference_mm:.1f}mm | Max depth: {max_depth:.1f}mm
  </text>

</svg>'''

    # Write file
    with open(filename, 'w') as f:
        f.write(svg)

    return filename

def generate_all_frame_templates():
    """Generate templates for all frame joints."""

    output_dir = Path("/home/user/concretemixer/manufacturing/templates")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define joints from frame_model.py tube paths
    joints = [
        CopeJoint("Cross_to_Main_90deg", FRAME_TUBE, FRAME_TUBE, 90.0),
        CopeJoint("Handle_to_Frame_60deg", FRAME_TUBE, FRAME_TUBE, 60.0),
        CopeJoint("Handle_to_Frame_45deg", FRAME_TUBE, FRAME_TUBE, 45.0),
        CopeJoint("Axle_Support_75deg", FRAME_TUBE, FRAME_TUBE, 75.0),
        CopeJoint("Hopper_Vertical_90deg", FRAME_TUBE, FRAME_TUBE, 90.0),
    ]

    print("=" * 60)
    print("MudMixer Frame - Tube Notching Templates")
    print("=" * 60)
    print(f"\nTube Spec: {FRAME_TUBE.name}")
    print(f"OD: {FRAME_TUBE.od_inches}\" ({FRAME_TUBE.od_mm:.1f}mm)")
    print(f"Circumference: {FRAME_TUBE.circumference_mm:.1f}mm")
    print()

    generated = []
    for joint in joints:
        filename = output_dir / f"cope_{joint.name.lower().replace(' ', '_')}.svg"
        generate_svg_template(joint, str(filename))
        profile = generate_cope_profile(joint)
        max_depth = max(p[1] for p in profile)
        print(f"Generated: {filename.name}")
        print(f"  Joint angle: {joint.angle_degrees}°, Max cut depth: {max_depth:.1f}mm")
        generated.append(str(filename))

    # Generate summary JSON
    summary = {
        "tube_spec": {
            "name": FRAME_TUBE.name,
            "od_inches": FRAME_TUBE.od_inches,
            "wall_inches": FRAME_TUBE.wall_inches,
            "od_mm": FRAME_TUBE.od_mm,
            "circumference_mm": FRAME_TUBE.circumference_mm,
        },
        "joints": [
            {
                "name": j.name,
                "angle_degrees": j.angle_degrees,
                "max_cut_depth_mm": max(p[1] for p in generate_cope_profile(j)),
                "template_file": f"cope_{j.name.lower().replace(' ', '_')}.svg"
            }
            for j in joints
        ],
        "source_calculation": "CALC-STRUCT-001",
        "notes": [
            "Print templates at 100% scale (no fit-to-page)",
            "Wrap template around tube, align 0° mark with weld seam",
            "Mark cut line with scribe or marker",
            "Cut with angle grinder, plasma, or tube notcher"
        ]
    }

    summary_file = output_dir / "template_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nGenerated: {summary_file.name}")
    print(f"\nTotal: {len(generated)} templates in {output_dir}")
    print("\nPrint at 100% scale, wrap around tube, mark and cut.")

    return generated

if __name__ == "__main__":
    generate_all_frame_templates()
