#!/usr/bin/env python3
"""
Parametric Shaftless Auger Generator for MudMixer Reverse Engineering

Generates complete parametric auger models with:
- Variable pitch sections (hopper vs chute)
- 4 inward-extending mixing fingers per patent
- Left-hand Acme thread motor coupling
- Configurable OD (2.5" per validated specs)
- Export to STEP format using cadquery or build123d

Patent References:
- US 10,259,140 B1: Auger OD 2.5" (2.25-3.25 range), P/D 0.2-0.9 (hopper), 0.3-1.8 (chute)
- US 11,285,639 B2: P/D 0.6-1.0 for chute section

Validated Specifications:
- Auger OD: 2.5 inches (patent preferred range 2.25-3.25)
- Hopper P/D ratio: 0.4-0.6 (preferred)
- Chute P/D ratio: 0.6-1.0 (preferred)
- Finger count: 4 (patent preferred embodiment)
- Motor coupling: Left-Hand Acme Thread

Author: Reverse Engineering Project
Date: 2026-02-06
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Union
from enum import Enum
from pathlib import Path
import math
import json
import warnings

# Optional CAD library imports - code will work without them installed
CADQUERY_AVAILABLE = False
BUILD123D_AVAILABLE = False

try:
    import cadquery as cq
    from cadquery import exporters
    CADQUERY_AVAILABLE = True
except ImportError:
    pass

try:
    import build123d as bd
    BUILD123D_AVAILABLE = True
except ImportError:
    pass

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


def generate_cadquery_auger(spec: MudMixerAugerSpec, output_path: Optional[str] = None) -> "cq.Workplane":
    """
    Generate a complete parametric auger model using CadQuery.

    Creates a shaftless helical auger with:
    - Variable pitch sections (hopper, transition, chute)
    - 4 inward-extending mixing fingers
    - Left-hand Acme thread motor coupling
    - Proper helix direction (right-handed per patent)

    Args:
        spec: MudMixerAugerSpec with all auger parameters
        output_path: Optional path to export STEP file

    Returns:
        CadQuery Workplane object representing the complete auger

    Raises:
        ImportError: If cadquery is not installed
    """
    if not CADQUERY_AVAILABLE:
        raise ImportError(
            "CadQuery is not installed. Install with: pip install cadquery\n"
            "Or use generate_openscad() for OpenSCAD output instead."
        )

    # Convert inches to mm (CadQuery uses mm by default)
    mm = 25.4

    od = spec.outer_diameter * mm
    id_inner = spec.inner_diameter * mm
    flight_thickness = spec.flight_thickness * mm

    # Flight cross-section: rectangular profile
    flight_width = (od - id_inner) / 2

    def create_helix_section(
        start_z: float,
        length: float,
        pitch: float,
        od: float,
        id_inner: float,
        thickness: float
    ) -> "cq.Workplane":
        """Create a single helix section with specified pitch."""
        # Number of turns
        turns = length / pitch

        # Create the helical path
        # Right-handed helix (per patent) - positive pitch direction
        helix = cq.Wire.makeHelix(
            pitch=pitch,
            height=length,
            radius=(od + id_inner) / 4,  # Mean radius
            lefthand=False,  # Right-handed per patent
        )

        # Create flight cross-section (rectangular)
        flight_profile = (
            cq.Workplane("XZ")
            .center((od + id_inner) / 4, 0)
            .rect(flight_width, thickness)
        )

        # Sweep along helix
        section = flight_profile.sweep(helix, isFrenet=True)

        # Translate to start position
        section = section.translate((0, 0, start_z))

        return section

    # Build auger from sections
    auger = cq.Workplane("XY")
    current_z = 0.0

    for section in spec.sections:
        length_mm = section.length_inches * mm
        pitch_mm = section.pitch_inches * mm

        helix_section = create_helix_section(
            start_z=current_z,
            length=length_mm,
            pitch=pitch_mm,
            od=od,
            id_inner=id_inner,
            thickness=flight_thickness
        )

        auger = auger.union(helix_section)
        current_z += length_mm

    # Add mixing fingers (4 per patent preferred embodiment)
    for finger in spec.fingers:
        finger_pos_z = finger.position_inches * mm
        finger_length = finger.length_inches * mm
        finger_diameter = finger.diameter_inches * mm
        angle_rad = math.radians(finger.angle_degrees)

        # Calculate finger position on the helix
        # Finger extends inward from the inner edge of the flight
        finger_start_radius = id_inner / 2

        # Create finger cylinder
        finger_cyl = (
            cq.Workplane("XY")
            .center(finger_start_radius - finger_length / 2, 0)
            .circle(finger_diameter / 2)
            .extrude(finger_length)
            .rotate((0, 0, 0), (0, 0, 1), finger.angle_degrees)
            .translate((0, 0, finger_pos_z))
        )

        auger = auger.union(finger_cyl)

    # Add motor coupling (Left-Hand Acme Thread)
    coupling_length = spec.coupling_length * mm
    coupling_od = spec.coupling_major_diameter * mm

    # Simplified coupling - cylindrical boss with thread indication
    # Full Acme thread geometry would require additional thread library
    coupling = (
        cq.Workplane("XY")
        .circle(coupling_od / 2)
        .extrude(-coupling_length)  # Extends from motor end (z=0) backward
    )

    # Add thread grooves (simplified representation)
    # Acme thread: 29-degree thread angle, 0.5 pitch typical
    thread_pitch = 0.5 * mm  # Typical Acme pitch
    thread_depth = 0.1 * coupling_od

    # Create helical groove for visual thread representation
    # Note: Left-hand thread (lefthand=True) per patent
    thread_helix = cq.Wire.makeHelix(
        pitch=thread_pitch,
        height=coupling_length * 0.8,
        radius=coupling_od / 2 - thread_depth / 2,
        lefthand=True,  # LEFT-HAND per patent specification
    )

    # Thread profile (V-shape approximation of Acme)
    thread_profile = (
        cq.Workplane("XZ")
        .center(coupling_od / 2 - thread_depth / 2, 0)
        .polygon(3, thread_depth)  # Triangular approximation
    )

    thread_cut = thread_profile.sweep(thread_helix, isFrenet=True)
    thread_cut = thread_cut.translate((0, 0, -coupling_length * 0.9))

    coupling = coupling.cut(thread_cut)
    auger = auger.union(coupling)

    # Export to STEP if path provided
    if output_path:
        output_path = Path(output_path)
        if output_path.suffix.lower() in ['.step', '.stp']:
            exporters.export(auger, str(output_path))
            print(f"Exported STEP file: {output_path}")
        else:
            warnings.warn(f"Unsupported format: {output_path.suffix}. Use .step or .stp")

    return auger


def generate_build123d_auger(spec: MudMixerAugerSpec, output_path: Optional[str] = None):
    """
    Generate a complete parametric auger model using build123d.

    Alternative to CadQuery using the build123d library.

    Args:
        spec: MudMixerAugerSpec with all auger parameters
        output_path: Optional path to export STEP file

    Returns:
        build123d Part object representing the complete auger

    Raises:
        ImportError: If build123d is not installed
    """
    if not BUILD123D_AVAILABLE:
        raise ImportError(
            "build123d is not installed. Install with: pip install build123d\n"
            "Or use generate_cadquery_auger() or generate_openscad() instead."
        )

    # Convert inches to mm
    mm = 25.4

    od = spec.outer_diameter * mm
    id_inner = spec.inner_diameter * mm
    flight_thickness = spec.flight_thickness * mm
    flight_width = (od - id_inner) / 2

    with bd.BuildPart() as auger:
        current_z = 0.0

        # Build each helix section
        for section in spec.sections:
            length_mm = section.length_inches * mm
            pitch_mm = section.pitch_inches * mm
            turns = section.turns

            # Create helix path
            with bd.BuildLine() as helix_path:
                bd.Helix(
                    pitch=pitch_mm,
                    height=length_mm,
                    radius=(od + id_inner) / 4,
                    lefthand=False,  # Right-handed per patent
                )

            # Flight profile
            with bd.BuildSketch(bd.Plane.XZ) as flight:
                with bd.Locations([((od + id_inner) / 4, 0)]):
                    bd.Rectangle(flight_width, flight_thickness)

            # Sweep flight along helix
            bd.sweep(flight.sketch, helix_path.line)

            # Move for next section
            with bd.Locations([(0, 0, length_mm)]):
                current_z += length_mm

        # Add fingers
        for finger in spec.fingers:
            finger_pos_z = finger.position_inches * mm
            finger_length = finger.length_inches * mm
            finger_radius = (finger.diameter_inches * mm) / 2

            # Position and create finger
            with bd.Locations([(0, 0, finger_pos_z)]):
                with bd.BuildSketch(bd.Plane.XY.rotated((0, 0, finger.angle_degrees))) as finger_sketch:
                    with bd.Locations([(id_inner / 2 - finger_length / 2, 0)]):
                        bd.Circle(finger_radius)
                bd.extrude(finger_sketch.sketch, finger_length)

        # Motor coupling with left-hand Acme thread
        coupling_length = spec.coupling_length * mm
        coupling_radius = (spec.coupling_major_diameter * mm) / 2

        with bd.Locations([(0, 0, -coupling_length)]):
            bd.Cylinder(radius=coupling_radius, height=coupling_length)

    result = auger.part

    # Export to STEP if path provided
    if output_path:
        output_path = Path(output_path)
        if output_path.suffix.lower() in ['.step', '.stp']:
            result.export_step(str(output_path))
            print(f"Exported STEP file: {output_path}")

    return result


def export_auger_step(spec: MudMixerAugerSpec, output_path: str) -> bool:
    """
    Export auger to STEP format using available CAD library.

    Tries CadQuery first, then build123d, falls back to error message.

    Args:
        spec: MudMixerAugerSpec with all auger parameters
        output_path: Path for STEP output file

    Returns:
        True if export successful, False otherwise
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if CADQUERY_AVAILABLE:
        try:
            generate_cadquery_auger(spec, str(output_path))
            return True
        except Exception as e:
            warnings.warn(f"CadQuery export failed: {e}")

    if BUILD123D_AVAILABLE:
        try:
            generate_build123d_auger(spec, str(output_path))
            return True
        except Exception as e:
            warnings.warn(f"build123d export failed: {e}")

    print(
        "STEP export requires CadQuery or build123d.\n"
        "Install with: pip install cadquery\n"
        "         or: pip install build123d\n"
        "\n"
        "OpenSCAD output is available without additional dependencies.\n"
        "Use generate_openscad(spec) to create .scad file."
    )
    return False


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


def create_custom_auger(
    outer_diameter: float = 2.5,
    total_length: float = 36.0,
    hopper_pd_ratio: float = 0.5,
    chute_pd_ratio: float = 0.9,
    finger_count: int = 4,
    output_format: str = "openscad"
) -> MudMixerAugerSpec:
    """
    Create a custom auger specification with user-defined parameters.

    Args:
        outer_diameter: Auger OD in inches (patent range: 2.25-3.25, preferred: 2.5)
        total_length: Total auger length in inches (default: 36")
        hopper_pd_ratio: P/D ratio for hopper section (patent range: 0.4-0.6)
        chute_pd_ratio: P/D ratio for chute section (patent range: 0.6-1.0)
        finger_count: Number of mixing fingers (patent preferred: 4)
        output_format: "openscad", "cadquery", or "build123d"

    Returns:
        MudMixerAugerSpec with custom parameters
    """
    # Calculate section lengths based on total length
    hopper_length = total_length * 0.33  # ~1/3 for hopper
    transition_length = total_length * 0.17  # ~1/6 for transition
    chute_length = total_length * 0.50  # ~1/2 for chute

    # Create sections with custom P/D ratios
    sections = [
        AugerSection("hopper", hopper_length, hopper_pd_ratio),
        AugerSection("transition", transition_length, (hopper_pd_ratio + chute_pd_ratio) / 2),
        AugerSection("chute", chute_length, chute_pd_ratio),
    ]

    # Distribute fingers evenly with aperture finger at hopper/chute boundary
    aperture_pos = hopper_length
    fingers = []
    if finger_count >= 1:
        # Always include aperture finger per Patent Claim 17
        fingers.append(Finger(aperture_pos, 2.0, 0.375, 90))

    # Distribute remaining fingers
    remaining = finger_count - 1
    if remaining > 0:
        # One in hopper
        fingers.append(Finger(hopper_length / 2, 2.0, 0.375, 0))
        remaining -= 1

    if remaining > 0:
        # Distribute rest in chute
        chute_start = hopper_length + transition_length
        chute_spacing = chute_length / (remaining + 1)
        for i in range(remaining):
            pos = chute_start + chute_spacing * (i + 1)
            angle = (180 + 90 * i) % 360
            fingers.append(Finger(pos, 2.0, 0.375, angle))

    spec = MudMixerAugerSpec(
        outer_diameter=outer_diameter,
        total_length=total_length,
        sections=sections,
        fingers=fingers,
    )

    return spec


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
        print("\nValidation Issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n[OK] Specification validates against patent claims")

    # Print specifications
    print("\nCore Dimensions:")
    print(f"   Auger OD: {spec.outer_diameter}\" ({spec.outer_diameter * 25.4:.1f} mm)")
    print(f"   Auger ID: {spec.inner_diameter:.3f}\" ({spec.inner_diameter * 25.4:.1f} mm)")
    print(f"   Total Length: {spec.total_length}\" ({spec.total_length * 25.4:.0f} mm)")
    print(f"   Housing ID: {spec.housing_id:.3f}\" ({spec.housing_id * 25.4:.1f} mm)")

    print("\nSection Details:")
    position = 0
    for section in spec.sections:
        print(f"   {section.name.upper()}: {section.length_inches}\" length, "
              f"P/D={section.pitch_to_diameter_ratio}, pitch={section.pitch_inches:.2f}\", "
              f"turns={section.turns:.1f}")
        position += section.length_inches

    finger_positions = ', '.join(str(f.position_inches) + '"' for f in spec.fingers)
    print(f"\nFingers: {len(spec.fingers)} (positions: {finger_positions})")

    # Calculate mass
    mass = calculate_mass(spec)
    print(f"\nEstimated Mass: {mass:.2f} kg ({mass * 2.205:.1f} lbs)")

    # Calculate torque
    torque = calculate_torque_requirement(spec)
    print(f"\nTorque Requirements (@ 45 bags/hr):")
    print(f"   Power: {torque['power_watts']:.0f} W ({torque['power_hp']:.2f} HP)")
    print(f"   Torque: {torque['torque_nm']:.1f} N·m ({torque['torque_ft_lb']:.1f} ft-lb)")

    # Generate OpenSCAD
    scad_code = generate_openscad(spec)
    scad_path = "/home/user/concretemixer/src/mudmixer_auger.scad"
    with open(scad_path, "w") as f:
        f.write(scad_code)
    print(f"\nGenerated: {scad_path}")

    # Export JSON spec
    json_path = "/home/user/concretemixer/src/auger_spec.json"
    with open(json_path, "w") as f:
        json.dump(spec.to_dict(), f, indent=2)
    print(f"Generated: {json_path}")

    # Generate export script
    export_script = generate_stl_export_script(spec)
    script_path = "/home/user/concretemixer/src/export_stl.sh"
    with open(script_path, "w") as f:
        f.write(export_script)
    print(f"Generated: {script_path}")

    # Attempt STEP export if CAD library available
    step_path = "/home/user/concretemixer/src/mudmixer_auger.step"
    if CADQUERY_AVAILABLE or BUILD123D_AVAILABLE:
        print(f"\nAttempting STEP export...")
        if export_auger_step(spec, step_path):
            print(f"Generated: {step_path}")
    else:
        print(f"\nNote: STEP export requires cadquery or build123d.")
        print("      Install with: pip install cadquery")
        print("      OpenSCAD output generated as alternative.")

    print("\n" + "=" * 60)
    print("Generation complete. Files ready for CAD import.")
    print("=" * 60)


if __name__ == "__main__":
    main()
