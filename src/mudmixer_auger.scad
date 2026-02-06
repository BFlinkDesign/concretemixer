// MudMixer Shaftless Auger - Parametric Model
// Generated from validated patent specifications
// US 10,259,140 B1 and US 11,285,639 B2

$fn = 100;  // High resolution for smooth helix

// Core dimensions (converted to mm)
auger_od = 63.5;  // 2.5" outer diameter
auger_id = 28.575;  // 1.125" inner diameter (hollow center)
flight_thickness = 4.762499999999999;  // 0.1875" flight thickness
total_length = 914.4;  // 36.0" total length

// Housing
housing_id = 69.85;  // 2.750" housing ID
housing_wall = 1.9;  // 14-gauge steel

// Section parameters

// Section 1: hopper
section_0_start = 0.0;
section_0_length = 304.79999999999995;
section_0_pitch = 31.75;  // P/D = 0.5
section_0_turns = 9.60;

// Section 2: transition
section_1_start = 304.79999999999995;
section_1_length = 152.39999999999998;
section_1_pitch = 44.449999999999996;  // P/D = 0.7
section_1_turns = 3.43;

// Section 3: chute
section_2_start = 457.2;
section_2_length = 457.2;
section_2_pitch = 57.15;  // P/D = 0.9
section_2_turns = 8.00;

// Mixing fingers (4 per patent preferred embodiment)
finger_diameter = 9.524999999999999;
finger_length = 50.8;
finger_positions = [
    [152.39999999999998, 0],  // 6.0" from motor end
    [304.79999999999995, 90],  // 12.0" from motor end
    [457.2, 180],  // 18.0" from motor end
    [609.5999999999999, 270],  // 24.0" from motor end
];

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

        // HOPPER section
        translate([0, 0, section_0_start])
            helix_section(section_0_length, section_0_pitch, auger_od, auger_id, flight_thickness);

        // TRANSITION section
        translate([0, 0, section_1_start])
            helix_section(section_1_length, section_1_pitch, auger_od, auger_id, flight_thickness);

        // CHUTE section
        translate([0, 0, section_2_start])
            helix_section(section_2_length, section_2_pitch, auger_od, auger_id, flight_thickness);

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
