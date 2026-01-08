/*
 * Concrete Mixer Water Injection System
 *
 * Dual-nozzle water system for bagged concrete mixing
 * Minimum 30 PSI supply pressure required
 *
 * Units: inches
 */

// =============================================================================
// PARAMETERS
// =============================================================================

// From main assembly
housing_od = 5.563;
housing_id = 5.047;

// Water System Specs (from DATA_REQUIREMENTS.md)
min_pressure_psi = 30;
nozzle_count = 2;
nozzle_spacing = 10;          // inches between nozzles

// Manifold
manifold_length = 14;         // inches
manifold_od = 0.75;           // 3/4" copper tube OD
manifold_id = 0.625;          // 3/4" copper tube ID
manifold_offset = 3.0;        // Distance from housing

// Nozzles
nozzle_thread = 0.25;         // 1/4" NPT assumed
nozzle_length = 0.75;
nozzle_tip_dia = 0.125;       // 1/8" spray orifice
spray_angle = 65;             // Full cone spray angle (degrees)

// Inlet
inlet_thread = 0.75;          // 3/4" garden hose thread
inlet_length = 1.5;

// Control Valve
valve_body_dia = 1.5;
valve_body_length = 2.0;
valve_handle_length = 2.5;

// Visualization
$fn = 48;
show_spray_pattern = true;
spray_length = 6;             // Visualization only

// Colors
color_copper = [0.72, 0.45, 0.20];
color_brass = [0.80, 0.60, 0.20];
color_chrome = [0.75, 0.75, 0.80];
color_spray = [0.3, 0.5, 0.9, 0.3];

// =============================================================================
// MODULES
// =============================================================================

// Single spray nozzle
module spray_nozzle() {
    color(color_brass) {
        // Thread body
        cylinder(h = nozzle_length * 0.6, d = nozzle_thread * 1.3);

        // Nozzle body
        translate([0, 0, nozzle_length * 0.6])
        cylinder(h = nozzle_length * 0.3, d1 = nozzle_thread * 1.3, d2 = nozzle_thread * 0.8);

        // Tip
        translate([0, 0, nozzle_length * 0.9])
        cylinder(h = nozzle_length * 0.1, d = nozzle_tip_dia * 2);
    }

    // Spray pattern visualization
    if (show_spray_pattern) {
        color(color_spray)
        translate([0, 0, nozzle_length])
        cylinder(h = spray_length, d1 = nozzle_tip_dia, d2 = spray_length * tan(spray_angle/2) * 2);
    }
}

// Water manifold
module water_manifold() {
    color(color_copper) {
        // Main tube
        difference() {
            cylinder(h = manifold_length, d = manifold_od);
            translate([0, 0, -0.1])
            cylinder(h = manifold_length + 0.2, d = manifold_id);
        }

        // End caps
        cylinder(h = 0.1, d = manifold_od + 0.1);
        translate([0, 0, manifold_length - 0.1])
        cylinder(h = 0.1, d = manifold_od + 0.1);
    }

    // Nozzle bosses
    color(color_brass)
    for (i = [0:nozzle_count-1]) {
        z_pos = (manifold_length - nozzle_spacing) / 2 + i * nozzle_spacing;
        translate([0, -manifold_od/2, z_pos])
        rotate([90, 0, 0]) {
            cylinder(h = 0.5, d = nozzle_thread * 1.5);
        }
    }
}

// Control valve (ball valve style)
module control_valve() {
    // Valve body
    color(color_brass) {
        // Main body
        rotate([0, 90, 0])
        cylinder(h = valve_body_length, d = valve_body_dia, center = true);

        // Inlet/outlet ports
        for (x = [-1, 1]) {
            translate([x * valve_body_length/2, 0, 0])
            rotate([0, x * 90, 0])
            cylinder(h = 0.75, d = manifold_od);
        }

        // Stem housing
        translate([0, 0, valve_body_dia/2])
        cylinder(h = 0.5, d = 0.5);
    }

    // Handle
    color(color_chrome) {
        translate([0, 0, valve_body_dia/2 + 0.5]) {
            // Handle base
            cylinder(h = 0.3, d = 0.75);

            // Handle lever
            translate([0, 0, 0.3])
            hull() {
                cylinder(h = 0.2, d = 0.5);
                translate([valve_handle_length, 0, 0])
                cylinder(h = 0.2, d = 0.3);
            }
        }
    }
}

// Garden hose inlet connector
module hose_inlet() {
    color(color_brass) {
        // Hose thread (female)
        difference() {
            cylinder(h = inlet_length, d = inlet_thread * 1.4);
            translate([0, 0, 0.2])
            cylinder(h = inlet_length, d = inlet_thread);
        }

        // Barb to manifold
        translate([0, 0, inlet_length])
        cylinder(h = 0.75, d1 = inlet_thread * 1.2, d2 = manifold_od);
    }
}

// Mounting bracket
module mounting_bracket() {
    color([0.3, 0.3, 0.3])
    difference() {
        union() {
            // Clamp around housing
            rotate([0, 90, 0])
            difference() {
                cylinder(h = 1.5, d = housing_od + 0.5, center = true);
                cylinder(h = 2, d = housing_od, center = true);
                translate([0, -housing_od, 0])
                cube([housing_od * 2, housing_od * 2, 2], center = true);
            }

            // Arm to manifold
            translate([0, housing_od/2 + manifold_offset/2, 0])
            cube([1.5, manifold_offset, 0.25], center = true);

            // Manifold clamp
            translate([0, housing_od/2 + manifold_offset, 0])
            rotate([0, 90, 0])
            difference() {
                cylinder(h = 1.5, d = manifold_od + 0.3, center = true);
                cylinder(h = 2, d = manifold_od, center = true);
            }
        }

        // Bolt holes
        for (x = [-0.5, 0.5]) {
            translate([x, housing_od/2 + 0.25, 0])
            cylinder(h = 1, d = 0.2, center = true);
        }
    }
}

// =============================================================================
// ASSEMBLY
// =============================================================================

module water_system_assembly() {
    // Position relative to housing centerline
    manifold_y = housing_od/2 + manifold_offset;

    // Manifold
    translate([0, manifold_y, 2])
    rotate([0, 0, 0])
    water_manifold();

    // Nozzles (pointing at housing)
    for (i = [0:nozzle_count-1]) {
        z_pos = 2 + (manifold_length - nozzle_spacing) / 2 + i * nozzle_spacing;
        translate([0, manifold_y - manifold_od/2 - 0.5, z_pos])
        rotate([90, 0, 0])
        spray_nozzle();
    }

    // Control valve
    translate([0, manifold_y + 1.5, 2 + manifold_length + 1])
    control_valve();

    // Inlet connector
    translate([0, manifold_y, 2 + manifold_length + 3])
    rotate([180, 0, 0])
    hose_inlet();

    // Mounting brackets
    for (z = [5, 12]) {
        translate([0, 0, z])
        mounting_bracket();
    }
}

// =============================================================================
// WATER FLOW CALCULATIONS (Reference)
// =============================================================================

/*
 * Flow Rate Estimation:
 *
 * For full cone nozzles at 30 PSI:
 *   Q = Cv × sqrt(ΔP)
 *
 * Typical 1/8" orifice nozzle:
 *   Cv ≈ 0.5 GPM/sqrt(PSI)
 *   Q = 0.5 × sqrt(30) ≈ 2.7 GPM per nozzle
 *
 * With 2 nozzles:
 *   Total flow ≈ 5.4 GPM = 20.4 L/min
 *
 * Water/Cement Ratio:
 *   Typical bagged mix: 6 pints per 80 lb bag = 0.75 gal/bag
 *   At 45 bags/hr: 33.75 gal/hr = 0.56 GPM average
 *
 * System is oversized for intermittent spray control
 */

// =============================================================================
// RENDER
// =============================================================================

water_system_assembly();

// Housing reference (transparent)
%cylinder(h = 20, d = housing_od);
