#!/usr/bin/env python3
"""
G-Code Generator for Motor Mounting Plate
CNC Mill Operations for MudMixer Frame

Motor mount: 6" x 6" x 0.25" steel plate
Bolt pattern: 4.5" (114.3mm) square pattern
Material: A36 steel or equivalent

Reference: CALC-MOTOR-001 - Motor Selection Analysis
"""

import math
from datetime import datetime

# Motor mount dimensions (from frame_model.py)
PLATE_LENGTH_MM = 152.4  # 6"
PLATE_WIDTH_MM = 152.4   # 6"
PLATE_THICKNESS_MM = 6.35  # 0.25"
BOLT_PATTERN_MM = 114.3  # 4.5" square pattern
BOLT_HOLE_DIA_MM = 8.0   # 5/16" clearance
CENTER_BORE_DIA_MM = 25.0  # 1" center bore for shaft clearance

# Machining parameters for A36 steel
SPINDLE_SPEED = 1200  # RPM for HSS drill in mild steel
FEED_RATE = 100       # mm/min
PLUNGE_RATE = 50      # mm/min
SAFE_Z = 10.0         # Safe retract height
CLEARANCE_Z = 2.0     # Clearance above work

def generate_header(operation: str) -> str:
    """Generate G-code header with setup info."""
    return f"""; MudMixer Motor Mount Plate - {operation}
; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
; Material: A36 Steel, {PLATE_THICKNESS_MM}mm thick
;
; SETUP NOTES:
; - Zero X/Y at plate center
; - Zero Z at top of plate surface
; - Use cutting fluid for steel
; - Check tool length offset before running
;
; TOOLS REQUIRED:
; T1 = {BOLT_HOLE_DIA_MM}mm drill (5/16")
; T2 = {CENTER_BORE_DIA_MM}mm endmill or boring bar
; T3 = 6mm endmill (for outline if needed)

G90 G94 G17 G21   ; Absolute, mm/min, XY plane, metric
G54               ; Work coordinate system 1

"""

def generate_drilling_cycle() -> str:
    """Generate G-code for drilling bolt holes."""
    gcode = generate_header("Bolt Hole Drilling")

    # Tool change to drill
    gcode += """
; === BOLT HOLE DRILLING ===
; 4x holes on 4.5" (114.3mm) square pattern

T1 M6             ; Tool 1: 8mm drill
S{speed} M3       ; Spindle on CW
G43 H1            ; Tool length compensation

""".format(speed=SPINDLE_SPEED)

    # Calculate hole positions (square pattern centered on origin)
    half_pattern = BOLT_PATTERN_MM / 2
    holes = [
        (half_pattern, half_pattern),
        (-half_pattern, half_pattern),
        (-half_pattern, -half_pattern),
        (half_pattern, -half_pattern),
    ]

    # Peck drilling cycle for steel
    peck_depth = 2.0  # mm per peck
    total_depth = PLATE_THICKNESS_MM + 2.0  # Through + clearance

    gcode += f"""G0 Z{SAFE_Z}        ; Rapid to safe height

; Peck drilling cycle
; G83: Peck depth={peck_depth}mm, Total depth={total_depth}mm
G0 X{holes[0][0]:.3f} Y{holes[0][1]:.3f}  ; Position over hole 1
G0 Z{CLEARANCE_Z}                          ; Rapid to clearance

G83 X{holes[0][0]:.3f} Y{holes[0][1]:.3f} Z-{total_depth:.3f} R{CLEARANCE_Z} Q{peck_depth} F{PLUNGE_RATE}  ; Hole 1
X{holes[1][0]:.3f} Y{holes[1][1]:.3f}                                                                       ; Hole 2
X{holes[2][0]:.3f} Y{holes[2][1]:.3f}                                                                       ; Hole 3
X{holes[3][0]:.3f} Y{holes[3][1]:.3f}                                                                       ; Hole 4
G80                ; Cancel canned cycle

G0 Z{SAFE_Z}       ; Retract to safe height
M5                 ; Spindle off
"""

    return gcode

def generate_center_bore() -> str:
    """Generate G-code for center bore (motor shaft clearance)."""
    gcode = """
; === CENTER BORE ===
; 25mm (1") bore for motor shaft clearance

T2 M6             ; Tool 2: 25mm endmill or boring bar
S800 M3           ; Lower speed for larger tool
G43 H2            ; Tool length compensation

G0 Z{safe}        ; Rapid to safe height
G0 X0 Y0          ; Center of plate
G0 Z{clear}       ; Rapid to clearance

; Helical interpolation to create bore
; (Alternative to boring bar - uses endmill)
""".format(safe=SAFE_Z, clear=CLEARANCE_Z)

    # Helical bore using smaller endmill
    endmill_dia = 12.0  # Use 12mm endmill
    bore_radius = CENTER_BORE_DIA_MM / 2
    helix_radius = bore_radius - endmill_dia / 2

    # Helical plunge
    gcode += f"""
; Helical plunge with {endmill_dia}mm endmill
G0 X{helix_radius:.3f} Y0         ; Start position
G0 Z{CLEARANCE_Z}

; Helical interpolation (1mm per revolution)
G2 X{helix_radius:.3f} Y0 Z-1.0 I-{helix_radius:.3f} J0 F{FEED_RATE}
G2 X{helix_radius:.3f} Y0 Z-2.0 I-{helix_radius:.3f} J0
G2 X{helix_radius:.3f} Y0 Z-3.0 I-{helix_radius:.3f} J0
G2 X{helix_radius:.3f} Y0 Z-4.0 I-{helix_radius:.3f} J0
G2 X{helix_radius:.3f} Y0 Z-5.0 I-{helix_radius:.3f} J0
G2 X{helix_radius:.3f} Y0 Z-6.0 I-{helix_radius:.3f} J0
G2 X{helix_radius:.3f} Y0 Z-7.0 I-{helix_radius:.3f} J0  ; Through plate

; Final cleanup pass at full depth
G1 Z-{PLATE_THICKNESS_MM + 1:.3f}
G2 X{helix_radius:.3f} Y0 I-{helix_radius:.3f} J0

G0 Z{SAFE_Z}       ; Retract
M5                 ; Spindle off
"""

    return gcode

def generate_footer() -> str:
    """Generate G-code footer."""
    return """
; === PROGRAM END ===
G0 Z{safe}         ; Retract to safe height
G0 X0 Y0           ; Return to center
M5                 ; Spindle off
M9                 ; Coolant off
M30                ; Program end and rewind

; END OF PROGRAM
""".format(safe=SAFE_Z)

def generate_full_program() -> str:
    """Generate complete G-code program for motor mount plate."""
    gcode = "%\n"  # Program start
    gcode += "O1001 (MUDMIXER MOTOR MOUNT)\n"
    gcode += generate_drilling_cycle()
    gcode += generate_center_bore()
    gcode += generate_footer()
    gcode += "%\n"  # Program end
    return gcode

def main():
    """Generate G-code files for motor mount machining."""
    print("=" * 60)
    print("MudMixer Motor Mount - G-Code Generator")
    print("=" * 60)

    print(f"\nPlate dimensions: {PLATE_LENGTH_MM}mm x {PLATE_WIDTH_MM}mm x {PLATE_THICKNESS_MM}mm")
    print(f"Bolt pattern: {BOLT_PATTERN_MM}mm square ({BOLT_PATTERN_MM/25.4:.2f}\")")
    print(f"Bolt holes: 4x Ø{BOLT_HOLE_DIA_MM}mm")
    print(f"Center bore: Ø{CENTER_BORE_DIA_MM}mm")

    # Generate full program
    gcode = generate_full_program()

    output_file = "/home/user/concretemixer/manufacturing/motor_mount.nc"
    with open(output_file, 'w') as f:
        f.write(gcode)

    print(f"\nGenerated: {output_file}")
    print(f"Lines: {len(gcode.splitlines())}")

    # Also generate drilling-only version
    drill_only = "%\n"
    drill_only += "O1002 (MOTOR MOUNT - DRILLING ONLY)\n"
    drill_only += generate_drilling_cycle()
    drill_only += generate_footer()
    drill_only += "%\n"

    drill_file = "/home/user/concretemixer/manufacturing/motor_mount_drill.nc"
    with open(drill_file, 'w') as f:
        f.write(drill_only)

    print(f"Generated: {drill_file}")

    print("\n" + "=" * 60)
    print("Setup Notes:")
    print("  - Zero X/Y at plate center")
    print("  - Zero Z at plate top surface")
    print("  - Use cutting fluid for steel")
    print("  - Verify tool lengths before running")
    print("=" * 60)

if __name__ == "__main__":
    main()
