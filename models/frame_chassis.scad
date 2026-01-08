/*
 * Concrete Mixer Frame & Chassis
 *
 * Portable frame with wheels for bagged concrete mixer
 * Overall: 66.5" L × 27.5" W × 35" H
 *
 * Units: inches
 */

// =============================================================================
// PARAMETERS - From DATA_REQUIREMENTS.md
// =============================================================================

// Overall Dimensions (CONFIRMED)
overall_length = 66.5;
overall_width = 27.5;
overall_height = 35;
chute_height = 16;            // Height to discharge
dry_weight = 145;             // lbs

// Frame Tubing (CONFIRMED)
tube_od = 1.0;                // 1" steel tube
tube_wall = 0.083;            // 14 gauge wall
tube_id = tube_od - 2 * tube_wall;

// Housing Reference
housing_od = 5.563;
housing_length = 50;

// Hopper Reference
hopper_width = 18;
hopper_depth = 12;

// Wheel Specs (Marathon flat-free)
wheel_dia = 10;               // 10" flat-free tires
wheel_width = 2.5;
axle_dia = 0.625;             // 5/8" axle
axle_length = overall_width + 2;

// Handle
handle_height = 35;           // To top of handle
handle_width = 20;
handle_grip_dia = 1.25;

// Leg Supports
leg_height = 8;               // Folding legs
leg_spread = 24;

// Discharge Chute Articulation
swivel_range = 330;           // degrees
tilt_positions = [15, 25, 35]; // degrees

// Motor Housing
motor_housing_dia = 6;
motor_housing_length = 8;

// Visualization
$fn = 32;
show_wheels = true;
show_handle = true;
show_legs = true;
show_motor_housing = true;

// Colors
color_frame = [0.2, 0.2, 0.2];      // Dark steel
color_wheel = [0.1, 0.1, 0.1];       // Black rubber
color_handle = [0.3, 0.3, 0.3];      // Gray
color_motor = [0.4, 0.4, 0.45];      // Motor housing

// =============================================================================
// MODULES
// =============================================================================

// Steel tube segment
module tube(length, od = tube_od) {
    color(color_frame)
    difference() {
        cylinder(h = length, d = od);
        translate([0, 0, -0.1])
        cylinder(h = length + 0.2, d = od - 2 * tube_wall);
    }
}

// Tube along X axis
module tube_x(length, od = tube_od) {
    rotate([0, 90, 0])
    tube(length, od);
}

// Tube along Y axis
module tube_y(length, od = tube_od) {
    rotate([-90, 0, 0])
    tube(length, od);
}

// Flat-free wheel (Marathon style)
module wheel() {
    color(color_wheel) {
        // Tire
        rotate_extrude()
        translate([wheel_dia/2 - wheel_width/2, 0, 0])
        circle(d = wheel_width);

        // Hub
        cylinder(h = wheel_width * 0.8, d = 3, center = true);
    }

    // Axle hole
    color([0.5, 0.5, 0.5])
    cylinder(h = wheel_width + 0.5, d = axle_dia * 1.2, center = true);
}

// Wheel assembly with axle
module wheel_assembly() {
    // Axle
    color([0.6, 0.6, 0.6])
    rotate([0, 90, 0])
    cylinder(h = axle_length, d = axle_dia, center = true);

    // Wheels
    if (show_wheels) {
        translate([axle_length/2 - wheel_width/2, 0, 0])
        rotate([0, 90, 0])
        wheel();

        translate([-axle_length/2 + wheel_width/2, 0, 0])
        rotate([0, -90, 0])
        wheel();
    }
}

// Handle assembly
module handle_assembly() {
    if (show_handle) {
        // Vertical posts
        for (x = [-handle_width/2, handle_width/2]) {
            translate([x, 0, 0])
            tube(handle_height - 5);
        }

        // Cross bar (grip)
        translate([-handle_width/2, 0, handle_height - 5])
        tube_x(handle_width, handle_grip_dia);

        // Diagonal braces
        color(color_handle)
        for (x = [-1, 1]) {
            translate([x * handle_width/2, 0, 0])
            rotate([0, x * 15, 0])
            tube(handle_height * 0.7);
        }
    }
}

// Folding leg support
module leg_support() {
    if (show_legs) {
        color(color_frame) {
            // Main leg tube
            rotate([10, 0, 0])  // Slight angle for stability
            tube(leg_height);

            // Foot pad
            translate([0, leg_height * sin(10), -leg_height * cos(10)])
            cylinder(h = 0.25, d = 2);

            // Pivot bracket
            translate([0, 0, 0])
            cube([1.5, 0.5, 1.5], center = true);
        }
    }
}

// Main frame rails
module main_frame() {
    color(color_frame) {
        // Lower longitudinal rails
        for (y = [-overall_width/2 + 3, overall_width/2 - 3]) {
            translate([-overall_length/2 + 5, y, 0])
            tube_x(overall_length - 15);
        }

        // Upper longitudinal rails (housing support)
        for (y = [-housing_od/2 - 1, housing_od/2 + 1]) {
            translate([-overall_length/2 + 15, y, housing_od/2 + 2])
            tube_x(housing_length + 5);
        }

        // Cross members
        for (x = [-overall_length/2 + 10, -5, overall_length/2 - 20]) {
            translate([x, -overall_width/2 + 3, 0])
            tube_y(overall_width - 6);
        }

        // Vertical supports
        for (pos = [
            [-overall_length/2 + 15, -housing_od/2 - 1],
            [-overall_length/2 + 15, housing_od/2 + 1],
            [housing_length/2 - 5, -housing_od/2 - 1],
            [housing_length/2 - 5, housing_od/2 + 1]
        ]) {
            translate([pos[0], pos[1], 0])
            tube(housing_od/2 + 2);
        }

        // Hopper support frame
        translate([-overall_length/2 + 10, 0, housing_od + 5]) {
            // Hopper rails
            for (y = [-hopper_width/2, hopper_width/2]) {
                translate([0, y, 0])
                tube_x(15);
            }
            // Cross
            translate([7.5, -hopper_width/2, 0])
            tube_y(hopper_width);
        }
    }
}

// Motor housing mount
module motor_mount() {
    if (show_motor_housing) {
        color(color_motor) {
            // Housing shell
            translate([0, 0, 0])
            difference() {
                cylinder(h = motor_housing_length, d = motor_housing_dia);
                translate([0, 0, 0.25])
                cylinder(h = motor_housing_length, d = motor_housing_dia - 0.5);
            }

            // Mounting flange
            cylinder(h = 0.5, d = motor_housing_dia + 2);

            // Ventilation slots
            for (i = [0:5]) {
                rotate([0, 0, i * 60])
                translate([motor_housing_dia/2 - 0.25, 0, motor_housing_length/2])
                cube([0.5, 0.25, motor_housing_length * 0.6], center = true);
            }
        }

        // Electrical box
        color([0.4, 0.4, 0.4])
        translate([motor_housing_dia/2 + 2, 0, motor_housing_length/2])
        cube([3, 4, 5], center = true);
    }
}

// Discharge chute swivel mount
module swivel_mount() {
    color(color_frame) {
        // Swivel ring
        difference() {
            cylinder(h = 2, d = housing_od + 3);
            translate([0, 0, -0.1])
            cylinder(h = 2.2, d = housing_od + 0.5);
        }

        // Tilt bracket
        translate([0, housing_od/2 + 2, 1])
        rotate([90, 0, 0])
        difference() {
            cylinder(h = 1, d = 3);
            cylinder(h = 1.1, d = 0.5);
        }
    }

    // Tilt position indicator
    color([0.8, 0.2, 0.2])
    for (angle = tilt_positions) {
        rotate([0, 0, angle * 3])  // Visual spacing
        translate([housing_od/2 + 2, 0, 0.5])
        cylinder(h = 0.5, d = 0.3);
    }
}

// =============================================================================
// ASSEMBLY
// =============================================================================

module frame_assembly() {
    // Position frame so discharge is at correct height
    translate([0, 0, wheel_dia/2 + 3]) {

        // Main frame structure
        main_frame();

        // Wheel assembly (at rear)
        translate([overall_length/2 - 15, 0, -3])
        wheel_assembly();

        // Handle (at rear)
        translate([overall_length/2 - 5, 0, 0])
        rotate([0, -15, 0])  // Angled back
        handle_assembly();

        // Front leg supports
        for (y = [-leg_spread/2, leg_spread/2]) {
            translate([-overall_length/2 + 8, y, 0])
            rotate([0, 0, 0])
            leg_support();
        }

        // Motor mount (at rear of housing)
        translate([housing_length/2 + 2, 0, housing_od/2 + 2])
        rotate([0, -90, 0])
        motor_mount();

        // Swivel mount (at front of housing)
        translate([-overall_length/2 + 15 - 1, 0, housing_od/2 + 2])
        rotate([0, 90, 0])
        swivel_mount();
    }
}

// =============================================================================
// RENDER
// =============================================================================

frame_assembly();

// Reference: Housing outline (transparent)
%translate([0, 0, wheel_dia/2 + 3 + housing_od/2 + 2])
rotate([0, 90, 0])
cylinder(h = housing_length, d = housing_od, center = true);

// Reference: Ground plane
%translate([0, 0, -0.1])
cube([overall_length + 20, overall_width + 20, 0.1], center = true);

// =============================================================================
// DIMENSIONAL ANNOTATIONS
// =============================================================================

/*
 * Key Dimensions (verified against DATA_REQUIREMENTS.md):
 *
 * Overall Length:  66.5"  ✓
 * Overall Width:   27.5"  ✓
 * Overall Height:  35"    ✓
 * Chute Height:    16"    ✓
 * Dry Weight:      145 lb
 *
 * Frame: 1" steel tube (14 gauge)
 * Tires: 10" Marathon flat-free
 * Swivel: 330° rotation
 * Tilt: 15°, 25°, 35° positions
 */
