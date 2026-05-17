// MudMixer Frame - Parametric Model
// Generated from validated specifications
// Overall: 66.5" L x 27.5" W x 35.0" H

$fn = 32;  // Resolution for tubes

// Dimensions (in mm)
tube_od = 33.400999999999996;
tube_wall = 3.3782;
tube_id = tube_od - 2 * tube_wall;

body_thickness = 1.89738;

overall_length = 1689.1;
overall_width = 698.5;
overall_height = 889.0;

// Module for creating a tube between two points
module tube(start, end) {
    hull() {
        translate(start) sphere(d = tube_od);
        translate(end) sphere(d = tube_od);
    }
}

// Module for hollow tube along path
module hollow_tube(start, end) {
    difference() {
        tube(start, end);
        hull() {
            translate(start) sphere(d = tube_id);
            translate(end) sphere(d = tube_id);
        }
    }
}

// Frame tubes
module frame_tubes() {
    color("DimGray") {

        // Left main longitudinal tube
        hollow_tube([0.0, 174.6, 254.0],
                    [1231.9, 174.6, 254.0]);

        // Right main longitudinal tube
        hollow_tube([0.0, -174.6, 254.0],
                    [1231.9, -174.6, 254.0]);

        // Cross member 1
        hollow_tube([152.4, 174.6, 254.0],
                    [152.4, -174.6, 254.0]);

        // Cross member 2
        hollow_tube([609.6, 174.6, 254.0],
                    [609.6, -174.6, 254.0]);

        // Cross member 3
        hollow_tube([1066.8, 174.6, 254.0],
                    [1066.8, -174.6, 254.0]);

        // Left handle tube
        hollow_tube([1079.5, 254.0, 254.0],
                    [1689.1, 254.0, 762.0]);

        // Right handle tube
        hollow_tube([1079.5, -254.0, 254.0],
                    [1689.1, -254.0, 762.0]);

        // Handle crossbar
        hollow_tube([1638.3, 254.0, 711.2],
                    [1638.3, -254.0, 711.2]);

        // Left axle support
        hollow_tube([152.4, 174.6, 254.0],
                    [152.4, 225.4, 177.8]);

        // Right axle support
        hollow_tube([152.4, -174.6, 254.0],
                    [152.4, -225.4, 177.8]);

        // Hopper front vertical left
        hollow_tube([457.2, 203.2, 254.0],
                    [457.2, 203.2, 558.8]);

        // Hopper rear vertical left
        hollow_tube([965.2, 203.2, 254.0],
                    [965.2, 203.2, 558.8]);

        // Hopper front vertical right
        hollow_tube([457.2, -203.2, 254.0],
                    [457.2, -203.2, 558.8]);

        // Hopper rear vertical right
        hollow_tube([965.2, -203.2, 254.0],
                    [965.2, -203.2, 558.8]);

        // Motor mount cross support
        hollow_tube([1066.8, 149.2, 355.6],
                    [1066.8, -149.2, 355.6]);

    }
}

// Hopper shell (simplified)
module hopper() {
    hopper_length = 609.5999999999999;
    hopper_width = 508.0;
    hopper_height = 304.79999999999995;
    base_x = 457.2;
    base_z = 254.0;

    color("SteelBlue", 0.7)
    translate([base_x + hopper_length/2, 0, base_z + hopper_height/2])
    difference() {
        cube([hopper_length, hopper_width, hopper_height], center=true);
        translate([0, 0, body_thickness])
            cube([hopper_length - 2*body_thickness,
                  hopper_width - 2*body_thickness,
                  hopper_height], center=true);
    }
}

// Chute (cylindrical)
module chute() {
    chute_length = 406.4;
    chute_od = 79.99475999999999;
    chute_id = 76.19999999999999;
    chute_z = 406.4;  // Height of mixing tube center

    color("SteelBlue", 0.7)
    translate([0, 0, chute_z])
    rotate([0, 90, 0])
    difference() {
        cylinder(h = chute_length, d = chute_od);
        translate([0, 0, -1])
            cylinder(h = chute_length + 2, d = chute_id);
    }
}

// Motor mount plate
module motor_mount() {
    plate_x = 1066.8;
    plate_z = 355.59999999999997;
    plate_length = 152.39999999999998;
    plate_width = 152.39999999999998;
    plate_thickness = 6.35;
    bolt_pattern = 114.3;

    color("DarkSlateGray")
    translate([plate_x, 0, plate_z])
    difference() {
        cube([plate_length, plate_width, plate_thickness], center=true);
        // Bolt holes
        for (x = [-1, 1], y = [-1, 1])
            translate([x * bolt_pattern/2, y * bolt_pattern/2, 0])
                cylinder(h = plate_thickness + 1, d = 8, center=true);
    }
}

// Complete frame assembly
module frame_assembly() {
    frame_tubes();
    hopper();
    chute();
    motor_mount();
}

// Render
frame_assembly();
