/*
 * Concrete Mixer Auger Assembly - Parametric 3D Model
 *
 * Designed for bagged concrete mix products (Sakrete, Quikrete)
 * Shaftless helical auger with variable pitch
 *
 * Units: inches (convert to mm for STL export: scale([25.4, 25.4, 25.4]))
 */

// =============================================================================
// PARAMETERS - Modify these to adjust the model
// =============================================================================

// Auger Specifications (from DATA_REQUIREMENTS.md)
auger_od = 4.0;              // Auger outer diameter (inches) - CONFIRMED
auger_id = 3.0;              // Auger inner diameter (flight inner edge)
flight_thickness = 0.1875;   // 3/16" flight thickness
auger_length = 48;           // Total auger length (inches)

// Housing Specifications
housing_od = 5.563;          // 5" Schedule 40 pipe OD
housing_id = 5.047;          // 5" Schedule 40 pipe ID
housing_length = 50;         // Housing length (inches)
clearance = (housing_id - auger_od) / 2;  // Calculated clearance per side

// Pitch Specifications (variable pitch design)
pitch_hopper = 2.0;          // Pitch in hopper section (P/D = 0.5)
pitch_chute = 3.5;           // Pitch in chute section (P/D = 0.875)
hopper_length = 24;          // Length of hopper section
chute_length = 24;           // Length of chute section

// Finger Specifications
finger_diameter = 0.375;     // 3/8" finger diameter
finger_length = 1.5;         // Finger length into interior
finger_count = 8;            // Total fingers along auger
finger_angle = 45;           // Angle from flight surface (degrees)

// Hopper Specifications
hopper_width = 18;           // Hopper opening width
hopper_depth = 12;           // Hopper depth
hopper_angle = 45;           // Hopper side angle (degrees)

// Visualization Settings
$fn = 64;                    // Resolution for circles
show_housing = true;         // Toggle housing visibility
show_auger = true;           // Toggle auger visibility
show_fingers = true;         // Toggle finger visibility
show_hopper = true;          // Toggle hopper visibility
cross_section = false;       // Show cross-section view
exploded_view = false;       // Exploded assembly view

// Animation (for OpenSCAD Animate feature)
rotation_angle = $t * 360;   // Use View > Animate with FPS=30, Steps=360

// =============================================================================
// COLORS
// =============================================================================
color_housing = [0.7, 0.7, 0.7, 0.3];  // Semi-transparent gray
color_auger = [0.8, 0.4, 0.1];          // Orange/rust steel
color_fingers = [0.9, 0.9, 0.2];        // Yellow highlight
color_hopper = [0.5, 0.5, 0.6, 0.5];    // Semi-transparent steel

// =============================================================================
// MODULES
// =============================================================================

// Single helical flight segment
module helix_segment(od, id, pitch, length, thickness) {
    turns = length / pitch;
    segments_per_turn = 36;
    total_segments = turns * segments_per_turn;

    for (i = [0:total_segments-1]) {
        angle = i * (360 / segments_per_turn);
        z_pos = i * (pitch / segments_per_turn);
        next_angle = (i + 1) * (360 / segments_per_turn);
        next_z = (i + 1) * (pitch / segments_per_turn);

        if (z_pos < length) {
            hull() {
                rotate([0, 0, angle])
                translate([0, (od + id) / 4, z_pos])
                rotate([90, 0, 0])
                cylinder(h = (od - id) / 2, d = thickness, center = true);

                rotate([0, 0, next_angle])
                translate([0, (od + id) / 4, min(next_z, length)])
                rotate([90, 0, 0])
                cylinder(h = (od - id) / 2, d = thickness, center = true);
            }
        }
    }
}

// Simplified helical auger using linear_extrude with twist
module shaftless_auger(od, id, pitch, length, thickness) {
    turns = length / pitch;
    twist_angle = turns * 360;

    linear_extrude(height = length, twist = twist_angle, slices = length * 10, convexity = 10)
    difference() {
        circle(d = od);
        circle(d = id);
        // Create the helix profile by subtracting most of the ring
        rotate([0, 0, 0])
        translate([0, -od/2])
        square([od, od]);
    }
}

// Variable pitch auger (hopper + chute sections)
module variable_pitch_auger() {
    color(color_auger) {
        // Hopper section (lower pitch for controlled intake)
        shaftless_auger(auger_od, auger_id, pitch_hopper, hopper_length, flight_thickness);

        // Chute section (higher pitch for accelerated conveyance)
        translate([0, 0, hopper_length])
        shaftless_auger(auger_od, auger_id, pitch_chute, chute_length, flight_thickness);
    }
}

// Mixing fingers
module mixing_fingers() {
    color(color_fingers)
    for (i = [0:finger_count-1]) {
        z_pos = (i + 0.5) * (auger_length / finger_count);
        angle = i * (360 / finger_count) * 3;  // Spiral distribution

        rotate([0, 0, angle])
        translate([auger_id/2 - 0.1, 0, z_pos])
        rotate([0, -finger_angle, 0])
        cylinder(h = finger_length, d = finger_diameter);
    }
}

// Housing/chute tube
module housing_tube() {
    color(color_housing)
    difference() {
        cylinder(h = housing_length, d = housing_od);
        translate([0, 0, -0.1])
        cylinder(h = housing_length + 0.2, d = housing_id);

        // Cross-section cut if enabled
        if (cross_section) {
            translate([0, -housing_od, -1])
            cube([housing_od, housing_od * 2, housing_length + 2]);
        }
    }
}

// Hopper
module hopper() {
    color(color_hopper)
    translate([0, 0, -1])
    difference() {
        // Outer hopper shape
        hull() {
            translate([0, 0, hopper_depth])
            cube([hopper_width, hopper_width, 0.1], center = true);

            cylinder(h = 0.1, d = housing_od + 0.5);
        }

        // Inner cavity
        hull() {
            translate([0, 0, hopper_depth - 0.5])
            cube([hopper_width - 1, hopper_width - 1, 0.1], center = true);

            translate([0, 0, -0.1])
            cylinder(h = 0.2, d = housing_id);
        }

        // Opening to housing
        translate([0, 0, -0.5])
        cylinder(h = 2, d = housing_id);
    }
}

// Discharge chute extension
module discharge_chute() {
    color(color_housing)
    translate([0, 0, housing_length])
    rotate([0, 15, 0])  // 15 degree discharge angle
    difference() {
        cylinder(h = 12, d = housing_od);
        translate([0, 0, -0.1])
        cylinder(h = 12.2, d = housing_id);
    }
}

// Motor coupling end
module motor_coupling() {
    color([0.3, 0.3, 0.3])
    translate([0, 0, -2]) {
        // Coupling adapter
        cylinder(h = 2, d = 2);

        // Acme thread representation
        translate([0, 0, -1])
        cylinder(h = 1, d = 0.625);  // 5/8" thread
    }
}

// Water nozzle
module water_nozzle(pos) {
    color([0.2, 0.2, 0.8])
    translate(pos)
    rotate([90, 0, 0]) {
        cylinder(h = 1, d = 0.5);
        translate([0, 0, 1])
        sphere(d = 0.3);
    }
}

// Aggregate particle (for visualization)
module aggregate_particle(size) {
    color([0.6, 0.5, 0.4, 0.8])
    hull() {
        sphere(d = size);
        translate([size * 0.3, size * 0.2, size * 0.1])
        sphere(d = size * 0.7);
    }
}

// Sample aggregate particles in hopper
module sample_aggregate() {
    for (i = [0:20]) {
        x = (rands(-5, 5, 1)[0]);
        y = (rands(-5, 5, 1)[0]);
        z = (rands(2, 10, 1)[0]);
        size = rands(0.25, 0.5, 1)[0];  // 1/4" to 1/2" aggregate

        translate([x, y, z])
        aggregate_particle(size);
    }
}

// =============================================================================
// ASSEMBLY
// =============================================================================

module complete_assembly() {
    explode_offset = exploded_view ? 10 : 0;

    // Housing
    if (show_housing) {
        translate([0, 0, explode_offset])
        housing_tube();

        discharge_chute();
    }

    // Hopper
    if (show_hopper) {
        translate([0, 0, -explode_offset])
        hopper();
    }

    // Auger (with rotation animation)
    if (show_auger) {
        translate([0, 0, (housing_length - auger_length) / 2])
        rotate([0, 0, rotation_angle])
        variable_pitch_auger();
    }

    // Fingers
    if (show_fingers) {
        translate([0, 0, (housing_length - auger_length) / 2])
        rotate([0, 0, rotation_angle])
        mixing_fingers();
    }

    // Motor coupling
    motor_coupling();

    // Water nozzles
    water_nozzle([housing_od/2 + 0.5, 0, 5]);
    water_nozzle([housing_od/2 + 0.5, 0, 15]);
}

// =============================================================================
// RENDER
// =============================================================================

// Main render
complete_assembly();

// Dimensional annotations (for reference)
if (false) {  // Set to true to show dimensions
    // Auger OD annotation
    color("red")
    translate([auger_od/2 + 1, 0, auger_length/2])
    rotate([0, 90, 0])
    text(str("OD: ", auger_od, "\""), size = 0.5);

    // Housing ID annotation
    color("blue")
    translate([housing_id/2 + 1.5, 0, housing_length/2])
    rotate([0, 90, 0])
    text(str("Housing ID: ", housing_id, "\""), size = 0.5);
}

// =============================================================================
// EXPORT HELPERS
// =============================================================================

// For STL export in millimeters, uncomment:
// scale([25.4, 25.4, 25.4]) complete_assembly();

// Individual component exports:
// variable_pitch_auger();
// housing_tube();
// hopper();
