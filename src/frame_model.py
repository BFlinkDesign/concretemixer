#!/usr/bin/env python3
"""
Parametric Frame Model for MudMixer Reverse Engineering

Generates complete frame assembly using cadquery or build123d with:
- 1" steel tube frame (Schedule 40: 1.315" OD, 0.133" wall)
- 14 gauge sheet metal body (0.0747" / 1.9mm)
- Overall dimensions: 66.5" L x 27.5" W x 35" H
- Export to STEP format

Validated Specifications (from VALIDATED_SPECIFICATIONS.md):
- Frame Tubing: 1" steel pipe, Schedule 40
- Body/Hopper/Chute: 14-gauge steel (0.0747")
- Overall: 66.5" L x 27.5" W x 35" H
- Weight: 145 lbs dry

Patent References:
- US 10,259,140 B1: Portable concrete mixer structure
- US 11,285,639 B2: Pivot range, lift height specifications

Author: Reverse Engineering Project
Date: 2026-05-17
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from enum import Enum
from pathlib import Path
import math
import json
import warnings

# Optional CAD library imports
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


# Unit conversion constants (inches to mm for CAD)
INCH_TO_MM = 25.4


class SteelGauge(Enum):
    """Standard steel sheet gauges with thickness in inches."""
    GAUGE_10 = (10, 0.1345)
    GAUGE_11 = (11, 0.1196)
    GAUGE_12 = (12, 0.1046)
    GAUGE_14 = (14, 0.0747)
    GAUGE_16 = (16, 0.0598)
    GAUGE_18 = (18, 0.0478)

    def __init__(self, gauge_num: int, thickness_inches: float):
        self.gauge_num = gauge_num
        self.thickness_inches = thickness_inches
        self.thickness_mm = thickness_inches * INCH_TO_MM


class PipeSchedule(Enum):
    """Standard steel pipe schedules for 1" nominal pipe."""
    SCH_40 = ("Schedule 40", 1.315, 0.133)  # OD, wall thickness in inches
    SCH_80 = ("Schedule 80", 1.315, 0.179)
    SCH_10 = ("Schedule 10", 1.315, 0.109)

    def __init__(self, name: str, od_inches: float, wall_inches: float):
        self.schedule_name = name
        self.od_inches = od_inches
        self.wall_inches = wall_inches
        self.id_inches = od_inches - 2 * wall_inches


@dataclass
class FrameDimensions:
    """
    Overall frame dimensions from validated specifications.

    All dimensions in inches unless otherwise noted.
    """
    # Overall machine dimensions (confirmed from MudMixer specs)
    overall_length: float = 66.5  # inches
    overall_width: float = 27.5   # inches
    overall_height: float = 35.0  # inches

    # Frame tube specifications
    tube_schedule: PipeSchedule = PipeSchedule.SCH_40

    # Body material
    body_gauge: SteelGauge = SteelGauge.GAUGE_14

    # Hopper dimensions (calculated from overall and internal geometry)
    hopper_length: float = 24.0   # ~24" hopper section
    hopper_width: float = 20.0    # narrower than overall width
    hopper_height: float = 12.0   # above mixing tube

    # Chute dimensions
    chute_length: float = 16.0    # 16" standard (range 16-30")
    chute_diameter: float = 3.0   # housing ID from auger spec + clearance

    # Handle dimensions
    handle_length: float = 18.0   # extending from frame
    handle_height: float = 30.0   # comfortable grip height
    handle_spread: float = 20.0   # distance between handles

    # Wheel mount dimensions
    wheel_axle_diameter: float = 0.625  # 5/8" axle
    wheel_offset: float = 12.0    # from frame center
    wheel_clearance: float = 2.0  # ground clearance when level

    # Motor mount dimensions
    motor_mount_length: float = 6.0
    motor_mount_width: float = 6.0
    motor_bolt_pattern: float = 4.5  # typical 104mm motor = 4.5" pattern

    @property
    def tube_od(self) -> float:
        """Frame tube outer diameter in inches."""
        return self.tube_schedule.od_inches

    @property
    def tube_wall(self) -> float:
        """Frame tube wall thickness in inches."""
        return self.tube_schedule.wall_inches

    @property
    def body_thickness(self) -> float:
        """Body sheet metal thickness in inches."""
        return self.body_gauge.thickness_inches

    def to_dict(self) -> Dict:
        """Export dimensions as dictionary."""
        return {
            "overall": {
                "length_in": self.overall_length,
                "width_in": self.overall_width,
                "height_in": self.overall_height,
                "length_mm": self.overall_length * INCH_TO_MM,
                "width_mm": self.overall_width * INCH_TO_MM,
                "height_mm": self.overall_height * INCH_TO_MM,
            },
            "frame_tube": {
                "schedule": self.tube_schedule.schedule_name,
                "od_in": self.tube_od,
                "wall_in": self.tube_wall,
                "id_in": self.tube_schedule.id_inches,
            },
            "body": {
                "gauge": self.body_gauge.gauge_num,
                "thickness_in": self.body_thickness,
                "thickness_mm": self.body_thickness * INCH_TO_MM,
            },
            "hopper": {
                "length_in": self.hopper_length,
                "width_in": self.hopper_width,
                "height_in": self.hopper_height,
            },
            "chute": {
                "length_in": self.chute_length,
                "diameter_in": self.chute_diameter,
            },
            "handle": {
                "length_in": self.handle_length,
                "height_in": self.handle_height,
                "spread_in": self.handle_spread,
            },
            "wheels": {
                "axle_diameter_in": self.wheel_axle_diameter,
                "offset_in": self.wheel_offset,
            },
            "motor_mount": {
                "length_in": self.motor_mount_length,
                "width_in": self.motor_mount_width,
                "bolt_pattern_in": self.motor_bolt_pattern,
            },
        }


@dataclass
class FrameTubePath:
    """Defines a path for a frame tube segment."""
    name: str
    start_point: Tuple[float, float, float]  # (x, y, z) in inches
    end_point: Tuple[float, float, float]
    description: str = ""


@dataclass
class FrameModel:
    """
    Complete MudMixer frame model specification.

    Includes all structural elements:
    - Main frame tubes (wheelbarrow style)
    - Handle tubes
    - Motor mounting plate
    - Hopper support structure
    - Chute pivot support
    """
    dimensions: FrameDimensions = field(default_factory=FrameDimensions)

    # Frame tube paths (calculated from dimensions)
    tube_paths: List[FrameTubePath] = field(default_factory=list)

    def __post_init__(self):
        """Generate frame tube paths from dimensions."""
        if not self.tube_paths:
            self.tube_paths = self._generate_tube_paths()

    def _generate_tube_paths(self) -> List[FrameTubePath]:
        """
        Generate all frame tube paths based on validated dimensions.

        Frame geometry follows wheelbarrow-style single-axle design.
        """
        d = self.dimensions
        paths = []

        # Main longitudinal tubes (2 parallel, running length of machine)
        # These form the primary structure
        main_tube_y = d.overall_width / 4  # ~7" from centerline
        main_tube_z = 10.0  # Base height of main tubes

        paths.append(FrameTubePath(
            "main_left",
            start_point=(0, main_tube_y, main_tube_z),
            end_point=(d.overall_length - d.handle_length, main_tube_y, main_tube_z),
            description="Left main longitudinal tube"
        ))

        paths.append(FrameTubePath(
            "main_right",
            start_point=(0, -main_tube_y, main_tube_z),
            end_point=(d.overall_length - d.handle_length, -main_tube_y, main_tube_z),
            description="Right main longitudinal tube"
        ))

        # Cross members (connecting main tubes)
        cross_positions = [6.0, 24.0, 42.0]  # x positions for cross tubes
        for i, x_pos in enumerate(cross_positions):
            paths.append(FrameTubePath(
                f"cross_{i+1}",
                start_point=(x_pos, main_tube_y, main_tube_z),
                end_point=(x_pos, -main_tube_y, main_tube_z),
                description=f"Cross member {i+1}"
            ))

        # Handle tubes (angled upward from main frame)
        handle_start_x = d.overall_length - d.handle_length - 6.0
        handle_spread_y = d.handle_spread / 2

        paths.append(FrameTubePath(
            "handle_left",
            start_point=(handle_start_x, handle_spread_y, main_tube_z),
            end_point=(d.overall_length, handle_spread_y, d.handle_height),
            description="Left handle tube"
        ))

        paths.append(FrameTubePath(
            "handle_right",
            start_point=(handle_start_x, -handle_spread_y, main_tube_z),
            end_point=(d.overall_length, -handle_spread_y, d.handle_height),
            description="Right handle tube"
        ))

        # Handle crossbar (connects handles at top)
        paths.append(FrameTubePath(
            "handle_crossbar",
            start_point=(d.overall_length - 2.0, handle_spread_y, d.handle_height - 2.0),
            end_point=(d.overall_length - 2.0, -handle_spread_y, d.handle_height - 2.0),
            description="Handle crossbar"
        ))

        # Wheel axle support tubes (vertical from main tubes down to axle)
        axle_x = 6.0  # Axle position from front
        axle_z = d.wheel_clearance + 5.0  # Axle height (wheel radius considered)

        paths.append(FrameTubePath(
            "axle_support_left",
            start_point=(axle_x, main_tube_y, main_tube_z),
            end_point=(axle_x, main_tube_y + 2.0, axle_z),
            description="Left axle support"
        ))

        paths.append(FrameTubePath(
            "axle_support_right",
            start_point=(axle_x, -main_tube_y, main_tube_z),
            end_point=(axle_x, -main_tube_y - 2.0, axle_z),
            description="Right axle support"
        ))

        # Hopper support frame (elevated structure)
        hopper_base_x = 18.0
        hopper_top_z = main_tube_z + d.hopper_height

        # Hopper vertical supports
        hopper_y = d.hopper_width / 2 - 2.0
        for side, y_mult in [("left", 1), ("right", -1)]:
            y = hopper_y * y_mult
            paths.append(FrameTubePath(
                f"hopper_vert_{side}_front",
                start_point=(hopper_base_x, y, main_tube_z),
                end_point=(hopper_base_x, y, hopper_top_z),
                description=f"Hopper front vertical {side}"
            ))
            paths.append(FrameTubePath(
                f"hopper_vert_{side}_rear",
                start_point=(hopper_base_x + d.hopper_length - 4.0, y, main_tube_z),
                end_point=(hopper_base_x + d.hopper_length - 4.0, y, hopper_top_z),
                description=f"Hopper rear vertical {side}"
            ))

        # Motor mount support (at rear of hopper section)
        motor_x = hopper_base_x + d.hopper_length
        motor_z = main_tube_z + 4.0

        paths.append(FrameTubePath(
            "motor_support_cross",
            start_point=(motor_x, main_tube_y - 1.0, motor_z),
            end_point=(motor_x, -main_tube_y + 1.0, motor_z),
            description="Motor mount cross support"
        ))

        return paths

    def validate(self) -> List[str]:
        """Validate frame geometry against specifications."""
        issues = []
        d = self.dimensions

        # Check overall dimensions against specs
        if abs(d.overall_length - 66.5) > 1.0:
            issues.append(f"Overall length {d.overall_length}\" deviates from spec 66.5\"")

        if abs(d.overall_width - 27.5) > 1.0:
            issues.append(f"Overall width {d.overall_width}\" deviates from spec 27.5\"")

        if abs(d.overall_height - 35.0) > 2.0:
            issues.append(f"Overall height {d.overall_height}\" deviates from spec 35\"")

        # Check tube schedule
        if d.tube_schedule != PipeSchedule.SCH_40:
            issues.append(f"Tube schedule {d.tube_schedule.schedule_name} differs from spec Schedule 40")

        # Check body gauge
        if d.body_gauge != SteelGauge.GAUGE_14:
            issues.append(f"Body gauge {d.body_gauge.gauge_num} differs from spec 14 gauge")

        # Validate chute range
        if not (16.0 <= d.chute_length <= 30.0):
            issues.append(f"Chute length {d.chute_length}\" outside patent range 16-30\"")

        return issues


def generate_cadquery_frame(model: FrameModel, output_path: Optional[str] = None) -> "cq.Assembly":
    """
    Generate complete frame model using CadQuery.

    Creates:
    - All frame tubes from tube paths
    - Motor mounting plate
    - Wheel axle mounts
    - Hopper shell (simplified)

    Args:
        model: FrameModel with all dimensions and tube paths
        output_path: Optional path to export STEP file

    Returns:
        CadQuery Assembly object

    Raises:
        ImportError: If cadquery is not installed
    """
    if not CADQUERY_AVAILABLE:
        raise ImportError(
            "CadQuery is not installed. Install with: pip install cadquery\n"
            "Or use generate_openscad_frame() for OpenSCAD output."
        )

    mm = INCH_TO_MM
    d = model.dimensions

    # Create assembly
    asm = cq.Assembly()

    # Generate frame tubes
    tube_od = d.tube_od * mm
    tube_id = d.tube_schedule.id_inches * mm

    for path in model.tube_paths:
        # Calculate tube length and direction
        start = tuple(c * mm for c in path.start_point)
        end = tuple(c * mm for c in path.end_point)

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        length = math.sqrt(dx**2 + dy**2 + dz**2)

        if length < 0.1:
            continue  # Skip zero-length tubes

        # Create tube at origin along Z axis
        tube = (
            cq.Workplane("XY")
            .circle(tube_od / 2)
            .circle(tube_id / 2)
            .extrude(length)
        )

        # Calculate rotation angles to align with path
        # Rotate from Z-axis to path direction
        xy_length = math.sqrt(dx**2 + dy**2)
        if xy_length > 0.01:
            angle_z = math.degrees(math.atan2(dy, dx))
            angle_y = math.degrees(math.atan2(xy_length, dz))
        else:
            angle_z = 0
            angle_y = 0 if dz >= 0 else 180

        # Apply rotations
        tube = tube.rotate((0, 0, 0), (0, 1, 0), angle_y)
        tube = tube.rotate((0, 0, 0), (0, 0, 1), angle_z)

        # Translate to start position
        tube = tube.translate(start)

        # Add to assembly
        asm.add(tube, name=path.name, color=cq.Color("gray"))

    # Create motor mounting plate
    motor_plate_x = (18.0 + d.hopper_length) * mm
    motor_plate_y = 0
    motor_plate_z = (10.0 + 4.0) * mm  # main_tube_z + offset

    plate_length = d.motor_mount_length * mm
    plate_width = d.motor_mount_width * mm
    plate_thickness = 0.25 * mm  # 1/4" plate

    motor_plate = (
        cq.Workplane("XY")
        .box(plate_length, plate_width, plate_thickness)
        .faces(">Z")
        .workplane()
        .rect(d.motor_bolt_pattern * mm, d.motor_bolt_pattern * mm, forConstruction=True)
        .vertices()
        .hole(8.0)  # 5/16" bolt holes
        .translate((motor_plate_x, motor_plate_y, motor_plate_z))
    )

    asm.add(motor_plate, name="motor_plate", color=cq.Color("darkgray"))

    # Create simplified hopper shell (14 gauge sheet)
    hopper_thickness = d.body_thickness * mm
    hopper_length = d.hopper_length * mm
    hopper_width = d.hopper_width * mm
    hopper_height = d.hopper_height * mm
    hopper_base_x = 18.0 * mm
    hopper_base_z = 10.0 * mm

    # Hopper as a hollow box (simplified - actual is tapered funnel)
    hopper_outer = (
        cq.Workplane("XY")
        .box(hopper_length, hopper_width, hopper_height)
    )

    hopper_inner = (
        cq.Workplane("XY")
        .box(
            hopper_length - 2 * hopper_thickness,
            hopper_width - 2 * hopper_thickness,
            hopper_height - hopper_thickness
        )
        .translate((0, 0, hopper_thickness))
    )

    hopper = (
        hopper_outer.cut(hopper_inner)
        .translate((hopper_base_x + hopper_length / 2, 0, hopper_base_z + hopper_height / 2))
    )

    asm.add(hopper, name="hopper_shell", color=cq.Color("steelblue"))

    # Create chute (cylindrical housing)
    chute_od = d.chute_diameter * mm + 2 * d.body_thickness * mm
    chute_id = d.chute_diameter * mm
    chute_length = d.chute_length * mm

    chute = (
        cq.Workplane("XZ")
        .center(0, 10.0 * mm + 6.0 * mm)  # Centered at mixing tube height
        .circle(chute_od / 2)
        .circle(chute_id / 2)
        .extrude(chute_length)
        .translate((0, 0, 0))  # Extends forward from hopper
    )

    asm.add(chute, name="chute", color=cq.Color("steelblue"))

    # Export to STEP if path provided
    if output_path:
        output_path = Path(output_path)
        if output_path.suffix.lower() in ['.step', '.stp']:
            asm.save(str(output_path))
            print(f"Exported STEP file: {output_path}")
        else:
            warnings.warn(f"Unsupported format: {output_path.suffix}. Use .step or .stp")

    return asm


def generate_build123d_frame(model: FrameModel, output_path: Optional[str] = None):
    """
    Generate complete frame model using build123d.

    Alternative to CadQuery implementation.

    Args:
        model: FrameModel with all dimensions and tube paths
        output_path: Optional path to export STEP file

    Returns:
        build123d Compound object

    Raises:
        ImportError: If build123d is not installed
    """
    if not BUILD123D_AVAILABLE:
        raise ImportError(
            "build123d is not installed. Install with: pip install build123d\n"
            "Or use generate_cadquery_frame() instead."
        )

    mm = INCH_TO_MM
    d = model.dimensions

    parts = []

    # Generate frame tubes
    tube_od = d.tube_od * mm
    tube_id = d.tube_schedule.id_inches * mm

    for path in model.tube_paths:
        start = tuple(c * mm for c in path.start_point)
        end = tuple(c * mm for c in path.end_point)

        # Create line for tube path
        with bd.BuildLine() as tube_path:
            bd.Line(start, end)

        # Create tube profile
        with bd.BuildSketch(bd.Plane.XY) as tube_profile:
            bd.Circle(tube_od / 2)
            bd.Circle(tube_id / 2, mode=bd.Mode.SUBTRACT)

        # Sweep to create tube
        with bd.BuildPart() as tube:
            bd.sweep(tube_profile.sketch, tube_path.line)

        parts.append(tube.part)

    # Combine all parts
    result = bd.Compound(parts)

    # Export to STEP if path provided
    if output_path:
        output_path = Path(output_path)
        if output_path.suffix.lower() in ['.step', '.stp']:
            result.export_step(str(output_path))
            print(f"Exported STEP file: {output_path}")

    return result


def generate_openscad_frame(model: FrameModel) -> str:
    """
    Generate OpenSCAD code for the frame model.

    Creates parametric frame that can be rendered in OpenSCAD.

    Args:
        model: FrameModel with all dimensions and tube paths

    Returns:
        OpenSCAD code as string
    """
    mm = INCH_TO_MM
    d = model.dimensions

    code = f'''// MudMixer Frame - Parametric Model
// Generated from validated specifications
// Overall: {d.overall_length}" L x {d.overall_width}" W x {d.overall_height}" H

$fn = 32;  // Resolution for tubes

// Dimensions (in mm)
tube_od = {d.tube_od * mm};
tube_wall = {d.tube_wall * mm};
tube_id = tube_od - 2 * tube_wall;

body_thickness = {d.body_thickness * mm};

overall_length = {d.overall_length * mm};
overall_width = {d.overall_width * mm};
overall_height = {d.overall_height * mm};

// Module for creating a tube between two points
module tube(start, end) {{
    hull() {{
        translate(start) sphere(d = tube_od);
        translate(end) sphere(d = tube_od);
    }}
}}

// Module for hollow tube along path
module hollow_tube(start, end) {{
    difference() {{
        tube(start, end);
        hull() {{
            translate(start) sphere(d = tube_id);
            translate(end) sphere(d = tube_id);
        }}
    }}
}}

// Frame tubes
module frame_tubes() {{
    color("DimGray") {{
'''

    # Add each tube path
    for path in model.tube_paths:
        start = [c * mm for c in path.start_point]
        end = [c * mm for c in path.end_point]
        code += f'''
        // {path.description}
        hollow_tube([{start[0]:.1f}, {start[1]:.1f}, {start[2]:.1f}],
                    [{end[0]:.1f}, {end[1]:.1f}, {end[2]:.1f}]);
'''

    code += f'''
    }}
}}

// Hopper shell (simplified)
module hopper() {{
    hopper_length = {d.hopper_length * mm};
    hopper_width = {d.hopper_width * mm};
    hopper_height = {d.hopper_height * mm};
    base_x = {18.0 * mm};
    base_z = {10.0 * mm};

    color("SteelBlue", 0.7)
    translate([base_x + hopper_length/2, 0, base_z + hopper_height/2])
    difference() {{
        cube([hopper_length, hopper_width, hopper_height], center=true);
        translate([0, 0, body_thickness])
            cube([hopper_length - 2*body_thickness,
                  hopper_width - 2*body_thickness,
                  hopper_height], center=true);
    }}
}}

// Chute (cylindrical)
module chute() {{
    chute_length = {d.chute_length * mm};
    chute_od = {d.chute_diameter * mm + 2 * d.body_thickness * mm};
    chute_id = {d.chute_diameter * mm};
    chute_z = {16.0 * mm};  // Height of mixing tube center

    color("SteelBlue", 0.7)
    translate([0, 0, chute_z])
    rotate([0, 90, 0])
    difference() {{
        cylinder(h = chute_length, d = chute_od);
        translate([0, 0, -1])
            cylinder(h = chute_length + 2, d = chute_id);
    }}
}}

// Motor mount plate
module motor_mount() {{
    plate_x = {(18.0 + d.hopper_length) * mm};
    plate_z = {14.0 * mm};
    plate_length = {d.motor_mount_length * mm};
    plate_width = {d.motor_mount_width * mm};
    plate_thickness = {0.25 * mm};
    bolt_pattern = {d.motor_bolt_pattern * mm};

    color("DarkSlateGray")
    translate([plate_x, 0, plate_z])
    difference() {{
        cube([plate_length, plate_width, plate_thickness], center=true);
        // Bolt holes
        for (x = [-1, 1], y = [-1, 1])
            translate([x * bolt_pattern/2, y * bolt_pattern/2, 0])
                cylinder(h = plate_thickness + 1, d = 8, center=true);
    }}
}}

// Complete frame assembly
module frame_assembly() {{
    frame_tubes();
    hopper();
    chute();
    motor_mount();
}}

// Render
frame_assembly();
'''

    return code


def export_frame_step(model: FrameModel, output_path: str) -> bool:
    """
    Export frame to STEP format using available CAD library.

    Args:
        model: FrameModel with all parameters
        output_path: Path for STEP output file

    Returns:
        True if export successful, False otherwise
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if CADQUERY_AVAILABLE:
        try:
            generate_cadquery_frame(model, str(output_path))
            return True
        except Exception as e:
            warnings.warn(f"CadQuery export failed: {e}")

    if BUILD123D_AVAILABLE:
        try:
            generate_build123d_frame(model, str(output_path))
            return True
        except Exception as e:
            warnings.warn(f"build123d export failed: {e}")

    print(
        "STEP export requires CadQuery or build123d.\n"
        "Install with: pip install cadquery\n"
        "         or: pip install build123d\n"
        "\n"
        "OpenSCAD output is available without additional dependencies.\n"
        "Use generate_openscad_frame(model) to create .scad file."
    )
    return False


def calculate_frame_weight(model: FrameModel) -> Dict[str, float]:
    """
    Estimate frame weight based on geometry.

    Args:
        model: FrameModel with dimensions

    Returns:
        Dictionary with weight breakdown in lbs and kg
    """
    d = model.dimensions

    # Steel density: 0.284 lb/in^3
    steel_density = 0.284

    # Calculate tube volume
    tube_area = math.pi * ((d.tube_od / 2)**2 - (d.tube_schedule.id_inches / 2)**2)
    total_tube_length = sum(
        math.sqrt(
            (p.end_point[0] - p.start_point[0])**2 +
            (p.end_point[1] - p.start_point[1])**2 +
            (p.end_point[2] - p.start_point[2])**2
        )
        for p in model.tube_paths
    )
    tube_volume = tube_area * total_tube_length
    tube_weight = tube_volume * steel_density

    # Calculate sheet metal volume (hopper + chute approximation)
    hopper_surface = 2 * (d.hopper_length * d.hopper_height +
                          d.hopper_width * d.hopper_height +
                          d.hopper_length * d.hopper_width)
    hopper_volume = hopper_surface * d.body_thickness
    hopper_weight = hopper_volume * steel_density

    chute_surface = math.pi * d.chute_diameter * d.chute_length
    chute_volume = chute_surface * d.body_thickness
    chute_weight = chute_volume * steel_density

    total_weight_lbs = tube_weight + hopper_weight + chute_weight
    total_weight_kg = total_weight_lbs * 0.453592

    return {
        "tube_weight_lbs": tube_weight,
        "hopper_weight_lbs": hopper_weight,
        "chute_weight_lbs": chute_weight,
        "total_weight_lbs": total_weight_lbs,
        "total_weight_kg": total_weight_kg,
        "spec_weight_lbs": 145.0,  # From validated specs
        "difference_pct": ((total_weight_lbs - 145.0) / 145.0) * 100,
    }


def main():
    """Generate MudMixer frame model and export files."""

    print("=" * 60)
    print("MudMixer Frame - Parametric Generator")
    print("=" * 60)

    # Create model from validated specifications
    model = FrameModel()

    # Validate against specs
    issues = model.validate()
    if issues:
        print("\nValidation Issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n[OK] Frame validates against specifications")

    # Print dimensions
    d = model.dimensions
    print("\nOverall Dimensions:")
    print(f"   Length: {d.overall_length}\" ({d.overall_length * INCH_TO_MM:.0f} mm)")
    print(f"   Width: {d.overall_width}\" ({d.overall_width * INCH_TO_MM:.0f} mm)")
    print(f"   Height: {d.overall_height}\" ({d.overall_height * INCH_TO_MM:.0f} mm)")

    print("\nFrame Tube:")
    print(f"   {d.tube_schedule.schedule_name}")
    print(f"   OD: {d.tube_od}\" ({d.tube_od * INCH_TO_MM:.1f} mm)")
    print(f"   Wall: {d.tube_wall}\" ({d.tube_wall * INCH_TO_MM:.2f} mm)")

    print(f"\nBody Material: {d.body_gauge.gauge_num} gauge "
          f"({d.body_thickness}\" / {d.body_thickness * INCH_TO_MM:.2f} mm)")

    print(f"\nFrame Tubes: {len(model.tube_paths)} segments")
    for path in model.tube_paths[:5]:  # Show first 5
        print(f"   - {path.name}: {path.description}")
    if len(model.tube_paths) > 5:
        print(f"   ... and {len(model.tube_paths) - 5} more")

    # Calculate weight
    weight = calculate_frame_weight(model)
    print(f"\nEstimated Weight:")
    print(f"   Tubes: {weight['tube_weight_lbs']:.1f} lbs")
    print(f"   Hopper: {weight['hopper_weight_lbs']:.1f} lbs")
    print(f"   Chute: {weight['chute_weight_lbs']:.1f} lbs")
    print(f"   Total: {weight['total_weight_lbs']:.1f} lbs ({weight['total_weight_kg']:.1f} kg)")
    print(f"   Spec: {weight['spec_weight_lbs']} lbs (difference: {weight['difference_pct']:+.1f}%)")

    # Generate OpenSCAD
    scad_code = generate_openscad_frame(model)
    scad_path = "/home/user/concretemixer/src/mudmixer_frame.scad"
    with open(scad_path, "w") as f:
        f.write(scad_code)
    print(f"\nGenerated: {scad_path}")

    # Export dimensions JSON
    json_path = "/home/user/concretemixer/src/frame_spec.json"
    with open(json_path, "w") as f:
        json.dump(model.dimensions.to_dict(), f, indent=2)
    print(f"Generated: {json_path}")

    # Attempt STEP export
    step_path = "/home/user/concretemixer/src/mudmixer_frame.step"
    if CADQUERY_AVAILABLE or BUILD123D_AVAILABLE:
        print("\nAttempting STEP export...")
        if export_frame_step(model, step_path):
            print(f"Generated: {step_path}")
    else:
        print("\nNote: STEP export requires cadquery or build123d.")
        print("      Install with: pip install cadquery")
        print("      OpenSCAD output generated as alternative.")

    print("\n" + "=" * 60)
    print("Frame generation complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
