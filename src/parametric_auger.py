#!/usr/bin/env python3
"""
Parametric Shaftless Auger Generator for MudMixer Reverse Engineering

Generates OpenSCAD code for shaftless helical augers with:
- Variable pitch sections (hopper vs chute)
- Inward-extending mixing fingers
- Left-hand Acme thread motor coupling
- Configurable dimensions based on validated patent specifications

Patent References:
- US 10,259,140 B1: Auger OD 2.5" (2.25-3.25 range), P/D 0.2-0.9 (hopper), 0.3-1.8 (chute)
- US 11,285,639 B2: P/D 0.6-1.0 for chute section

Author: Reverse Engineering Project
Date: 2026-02-06
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum
import math
import json

class Material(Enum):
    """Auger material options with mechanical properties"""
    CARBON_STEEL_1045 = ("1045 Steel", 7850, 530, 310, 170)  # kg/m3, UTS MPa, Yield MPa, BHN
    STAINLESS_304 = ("304 SS", 8000, 515, 205, 201)
    AR400 = ("AR400", 7850, 1200, 1000, 400)
    HARDOX_450 = ("Hardox 450", 7850, 1400, 1200, 450)

    def __init__(self, name: str, density: float, uts: float, yield_strength: float, hardness: float):
        self.material_name = name
        self.density = density  # kg/m³
        self.uts = uts  # MPa
        self.yield_strength = yield_strength  # MPa
        self.hardness = hardness  # BHN


@dataclass
class AugerSection:
    """Defines a section of the auger with specific pitch characteristics"""
    name: str
    length_inches: float
    pitch_to_diameter_ratio: float
    start_position: float = 0.0  # inches from motor end

    @property
    def pitch_inches(self) -> float:
        """Calculate actual pitch based on P/D ratio and standard 2.5" OD"""
        return self.pitch_to_diameter_ratio * 2.5

    @property
    def turns(self) -> float:
        """Number of complete helix turns in this section"""
        return self.length_inches / self.pitch_inches


@dataclass
class Finger:
    """Mixing finger extending inward from auger flight"""
    position_inches: float  # Distance from motor end
    length_inches: float = 2.0  # How far it extends into center
    diameter_inches: float = 0.375  # 3/8" rod
    angle_degrees: float = 0.0  # Rotation around helix


@dataclass
class MudMixerAugerSpec:
    """
    Complete auger specification based on validated data from patents and measurements.

    All dimensions in inches unless otherwise noted.
    """
    # Core dimensions (from Patent US 10,259,140)
    outer_diameter: float = 2.5  # Range: 2.25-3.25, preferred 2.5-3.0
    flight_thickness: float = 0.1875  # 3/16" (industry standard)
    total_length: float = 36.0  # ~36" from parts listing

    # Housing clearance (CEMA standard: 1/2" total = 1/4" per side)
    housing_clearance: float = 0.125  # Per side, tight for concrete

    # Variable pitch sections (Patent claims)
    sections: List[AugerSection] = field(default_factory=lambda: [
        AugerSection("hopper", 12.0, 0.5),   # P/D 0.4-0.6 preferred
        AugerSection("transition", 6.0, 0.7),
        AugerSection("chute", 18.0, 0.9),    # P/D 0.6-1.0 per US 11,285,639
    ])

    # Fingers (Patent: "plurality of fingers", 4 preferred)
    fingers: List[Finger] = field(default_factory=lambda: [
        Finger(6.0, 2.0, 0.375, 0),      # In hopper section
        Finger(12.0, 2.0, 0.375, 90),    # At aperture (Patent Claim 17)
        Finger(18.0, 2.0, 0.375, 180),   # In chute
        Finger(24.0, 2.0, 0.375, 270),   # In chute
    ])

    # Motor coupling (Patent: Left-Hand Acme Thread)
    coupling_length: float = 2.0
    coupling_thread: str = "left_hand_acme"
    coupling_major_diameter: float = 1.0  # Estimated

    # Material
    material: Material = Material.CARBON_STEEL_1045

    @property
    def inner_diameter(self) -> float:
        """Inner opening of shaftless auger (hollow center)"""
        return self.outer_diameter - (2 * self.flight_thickness) - 1.0  # ~1" open center

    @property
    def housing_id(self) -> float:
        """Required housing internal diameter"""
        return self.outer_diameter + (2 * self.housing_clearance)

    def validate(self) -> List[str]:
        """Validate against patent claims and engineering constraints"""
        issues = []

        # Check P/D ratios against patent claims
        for section in self.sections:
            if section.name == "hopper" and not (0.2 <= section.pitch_to_diameter_ratio <= 0.9):
                issues.append(f"Hopper P/D {section.pitch_to_diameter_ratio} outside patent range 0.2-0.9")
            if section.name == "chute" and not (0.3 <= section.pitch_to_diameter_ratio <= 1.8):
                issues.append(f"Chute P/D {section.pitch_to_diameter_ratio} outside patent range 0.3-1.8")

        # Check OD range
        if not (2.25 <= self.outer_diameter <= 3.25):
            issues.append(f"Auger OD {self.outer_diameter} outside patent range 2.25-3.25")

        # Check for aperture finger (Patent Claim 17)
        aperture_pos = sum(s.length_inches for s in self.sections if s.name == "hopper")
        has_aperture_finger = any(abs(f.position_inches - aperture_pos) < 1.0 for f in self.fingers)
        if not has_aperture_finger:
            issues.append("Missing finger at aperture (hopper-to-chute transition) per Patent Claim 17")

        return issues

    def to_dict(self) -> dict:
        """Export specification as dictionary for JSON/CAD interchange"""
        return {
            "outer_diameter": self.outer_diameter,
            "inner_diameter": self.inner_diameter,
            "flight_thickness": self.flight_thickness,
            "total_length": self.total_length,
            "housing_id": self.housing_id,
            "housing_clearance": self.housing_clearance,
            "sections": [
                {
                    "name": s.name,
                    "length": s.length_inches,
                    "pitch_to_diameter": s.pitch_to_diameter_ratio,
                    "pitch": s.pitch_inches,
                    "turns": s.turns,
                }
                for s in self.sections
            ],
            "fingers": [
                {
                    "position": f.position_inches,
                    "length": f.length_inches,
                    "diameter": f.diameter_inches,
                    "angle": f.angle_degrees,
                }
                for f in self.fingers
            ],
            "coupling": {
                "type": self.coupling_thread,
                "length": self.coupling_length,
                "major_diameter": self.coupling_major_diameter,
            },
            "material": {
                "name": self.material.material_name,
                "density_kg_m3": self.material.density,
                "uts_mpa": self.material.uts,
                "yield_mpa": self.material.yield_strength,
                "hardness_bhn": self.material.hardness,
            },
        }


def generate_openscad(spec: MudMixerAugerSpec) -> str:
    """
    Generate OpenSCAD code for the parametric auger.

    Uses helical sweep with variable pitch sections.
    """

    # Convert inches to mm for OpenSCAD (standard unit)
    mm = 25.4

    code = f'''// MudMixer Shaftless Auger - Parametric Model
// Generated from validated patent specifications
// US 10,259,140 B1 and US 11,285,639 B2

$fn = 100;  // High resolution for smooth helix

// Core dimensions (converted to mm)
auger_od = {spec.outer_diameter * mm};  // {spec.outer_diameter}" outer diameter
auger_id = {spec.inner_diameter * mm};  // {spec.inner_diameter:.3f}" inner diameter (hollow center)
flight_thickness = {spec.flight_thickness * mm};  // {spec.flight_thickness}" flight thickness
total_length = {spec.total_length * mm};  // {spec.total_length}" total length

// Housing
housing_id = {spec.housing_id * mm};  // {spec.housing_id:.3f}" housing ID
housing_wall = 1.9;  // 14-gauge steel

// Section parameters
'''

    # Add section definitions
    position = 0.0
    for i, section in enumerate(spec.sections):
        code += f'''
// Section {i+1}: {section.name}
section_{i}_start = {position * mm};
section_{i}_length = {section.length_inches * mm};
section_{i}_pitch = {section.pitch_inches * mm};  // P/D = {section.pitch_to_diameter_ratio}
section_{i}_turns = {section.turns:.2f};
'''
        position += section.length_inches

    # Add finger positions
    code += '''
// Mixing fingers (4 per patent preferred embodiment)
finger_diameter = ''' + str(spec.fingers[0].diameter_inches * mm) + ''';
finger_length = ''' + str(spec.fingers[0].length_inches * mm) + ''';
finger_positions = [
'''
    for f in spec.fingers:
        code += f'    [{f.position_inches * mm}, {f.angle_degrees}],  // {f.position_inches}" from motor end\n'
    code += '];'

    # Add the helix module
    code += '''

// Helical flight module with variable pitch
module helix_section(length, pitch, od, id, thickness) {
    turns = length / pitch;
    linear_extrude(height = length, twist = turns * 360, convexity = 10)
        translate([id/2, 0, 0])
            square([od/2 - id/2, thickness], center = true);
}

// Single finger module
module finger(pos_z, angle) {
    translate([0, 0, pos_z])
        rotate([0, 0, angle])
            translate([auger_id/2 - finger_length/2, 0, 0])
                rotate([0, 90, 0])
                    cylinder(h = finger_length, d = finger_diameter, center = true);
}

// Complete auger assembly
module auger() {
    color("DarkGray") {
'''

    # Generate each section
    position = 0.0
    for i, section in enumerate(spec.sections):
        code += f'''
        // {section.name.upper()} section
        translate([0, 0, section_{i}_start])
            helix_section(section_{i}_length, section_{i}_pitch, auger_od, auger_id, flight_thickness);
'''
        position += section.length_inches

    code += '''
    }

    // Add fingers
    color("Silver")
    for (fp = finger_positions) {
        finger(fp[0], fp[1]);
    }
}

// Housing (optional, for visualization)
module housing() {
    color("SteelBlue", 0.3)
    difference() {
        cylinder(h = total_length, d = housing_id + housing_wall * 2);
        translate([0, 0, -1])
            cylinder(h = total_length + 2, d = housing_id);
    }
}

// Render
auger();
// %housing();  // Uncomment to show transparent housing
'''

    return code


def generate_stl_export_script(spec: MudMixerAugerSpec) -> str:
    """Generate a script to export the auger as STL using OpenSCAD CLI"""
    return f'''#!/bin/bash
# Export MudMixer auger to STL format
# Requires OpenSCAD installed

SCAD_FILE="mudmixer_auger.scad"
STL_FILE="mudmixer_auger.stl"

# Generate with high quality
openscad -o $STL_FILE -D '$fn=200' $SCAD_FILE

echo "Exported: $STL_FILE"
echo "Dimensions: {spec.outer_diameter}" OD x {spec.total_length}" length"
'''


def calculate_mass(spec: MudMixerAugerSpec) -> float:
    """
    Estimate auger mass based on geometry and material.

    Returns mass in kg.
    """
    # Approximate volume calculation
    # Flight volume = π × mean_radius × flight_width × flight_thickness × total_helix_length

    mean_radius = (spec.outer_diameter + spec.inner_diameter) / 4  # inches
    flight_width = (spec.outer_diameter - spec.inner_diameter) / 2  # inches

    # Calculate total helix length (unrolled)
    total_helix_length = 0
    for section in spec.sections:
        circumference = 2 * math.pi * mean_radius
        helix_length = math.sqrt(circumference**2 + section.pitch_inches**2) * section.turns
        total_helix_length += helix_length

    # Volume in cubic inches
    volume_cu_in = flight_width * spec.flight_thickness * total_helix_length

    # Finger volume
    finger_volume = sum(
        math.pi * (f.diameter_inches/2)**2 * f.length_inches
        for f in spec.fingers
    )

    total_volume_cu_in = volume_cu_in + finger_volume

    # Convert to m³ and calculate mass
    volume_m3 = total_volume_cu_in * (0.0254**3)
    mass_kg = volume_m3 * spec.material.density

    return mass_kg


def calculate_torque_requirement(spec: MudMixerAugerSpec,
                                  throughput_bags_per_hour: float = 45,
                                  bag_weight_lbs: float = 80) -> dict:
    """
    Calculate torque requirements based on throughput.

    Uses screw conveyor power calculation methodology.
    """
    # Convert to SI
    throughput_kg_per_hour = throughput_bags_per_hour * bag_weight_lbs * 0.453592
    throughput_kg_per_sec = throughput_kg_per_hour / 3600

    # Assumed values
    rpm = 118  # From validated specs
    friction_factor = 0.4  # Concrete mix coefficient

    # Power calculation (simplified)
    # P = (Q × L × Ff × g) / (pitch × efficiency)
    Q = throughput_kg_per_sec
    L = spec.total_length * 0.0254  # meters
    g = 9.81
    efficiency = 0.3  # Conservative for concrete
    avg_pitch = sum(s.pitch_inches for s in spec.sections) / len(spec.sections) * 0.0254

    power_watts = (Q * L * friction_factor * g) / (avg_pitch * efficiency)

    # Torque from power and RPM
    torque_nm = (power_watts * 60) / (2 * math.pi * rpm)

    return {
        "throughput_kg_per_hour": throughput_kg_per_hour,
        "rpm": rpm,
        "power_watts": power_watts,
        "power_hp": power_watts / 746,
        "torque_nm": torque_nm,
        "torque_ft_lb": torque_nm * 0.7376,
    }


def main():
    """Generate MudMixer auger specification and export files"""

    print("=" * 60)
    print("MudMixer Shaftless Auger - Parametric Generator")
    print("=" * 60)

    # Create specification from validated data
    spec = MudMixerAugerSpec()

    # Validate against patent claims
    issues = spec.validate()
    if issues:
        print("\n⚠️  Validation Issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ Specification validates against patent claims")

    # Print specifications
    print("\n📐 Core Dimensions:")
    print(f"   Auger OD: {spec.outer_diameter}\" ({spec.outer_diameter * 25.4:.1f} mm)")
    print(f"   Auger ID: {spec.inner_diameter:.3f}\" ({spec.inner_diameter * 25.4:.1f} mm)")
    print(f"   Total Length: {spec.total_length}\" ({spec.total_length * 25.4:.0f} mm)")
    print(f"   Housing ID: {spec.housing_id:.3f}\" ({spec.housing_id * 25.4:.1f} mm)")

    print("\n📊 Section Details:")
    position = 0
    for section in spec.sections:
        print(f"   {section.name.upper()}: {section.length_inches}\" length, "
              f"P/D={section.pitch_to_diameter_ratio}, pitch={section.pitch_inches:.2f}\", "
              f"turns={section.turns:.1f}")
        position += section.length_inches

    finger_positions = ', '.join(str(f.position_inches) + '"' for f in spec.fingers)
    print(f"\n🔩 Fingers: {len(spec.fingers)} (positions: {finger_positions})")

    # Calculate mass
    mass = calculate_mass(spec)
    print(f"\n⚖️  Estimated Mass: {mass:.2f} kg ({mass * 2.205:.1f} lbs)")

    # Calculate torque
    torque = calculate_torque_requirement(spec)
    print(f"\n⚡ Torque Requirements (@ 45 bags/hr):")
    print(f"   Power: {torque['power_watts']:.0f} W ({torque['power_hp']:.2f} HP)")
    print(f"   Torque: {torque['torque_nm']:.1f} N·m ({torque['torque_ft_lb']:.1f} ft-lb)")

    # Generate OpenSCAD
    scad_code = generate_openscad(spec)
    scad_path = "/home/user/concretemixer/src/mudmixer_auger.scad"
    with open(scad_path, "w") as f:
        f.write(scad_code)
    print(f"\n📁 Generated: {scad_path}")

    # Export JSON spec
    json_path = "/home/user/concretemixer/src/auger_spec.json"
    with open(json_path, "w") as f:
        json.dump(spec.to_dict(), f, indent=2)
    print(f"📁 Generated: {json_path}")

    # Generate export script
    export_script = generate_stl_export_script(spec)
    script_path = "/home/user/concretemixer/src/export_stl.sh"
    with open(script_path, "w") as f:
        f.write(export_script)
    print(f"📁 Generated: {script_path}")

    print("\n" + "=" * 60)
    print("Generation complete. Files ready for CAD import.")
    print("=" * 60)


if __name__ == "__main__":
    main()
