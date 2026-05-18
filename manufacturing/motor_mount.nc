%
O1001 (MUDMIXER MOTOR MOUNT)
; MudMixer Motor Mount Plate - Bolt Hole Drilling
; Generated: 2026-05-17 04:45
; Material: A36 Steel, 6.35mm thick
;
; SETUP NOTES:
; - Zero X/Y at plate center
; - Zero Z at top of plate surface
; - Use cutting fluid for steel
; - Check tool length offset before running
;
; TOOLS REQUIRED:
; T1 = 8.0mm drill (5/16")
; T2 = 25.0mm endmill or boring bar
; T3 = 6mm endmill (for outline if needed)

G90 G94 G17 G21   ; Absolute, mm/min, XY plane, metric
G54               ; Work coordinate system 1


; === BOLT HOLE DRILLING ===
; 4x holes on 4.5" (114.3mm) square pattern

T1 M6             ; Tool 1: 8mm drill
S1200 M3       ; Spindle on CW
G43 H1            ; Tool length compensation

G0 Z10.0        ; Rapid to safe height

; Peck drilling cycle
; G83: Peck depth=2.0mm, Total depth=8.35mm
G0 X57.150 Y57.150  ; Position over hole 1
G0 Z2.0                          ; Rapid to clearance

G83 X57.150 Y57.150 Z-8.350 R2.0 Q2.0 F50  ; Hole 1
X-57.150 Y57.150                                                                       ; Hole 2
X-57.150 Y-57.150                                                                       ; Hole 3
X57.150 Y-57.150                                                                       ; Hole 4
G80                ; Cancel canned cycle

G0 Z10.0       ; Retract to safe height
M5                 ; Spindle off

; === CENTER BORE ===
; 25mm (1") bore for motor shaft clearance

T2 M6             ; Tool 2: 25mm endmill or boring bar
S800 M3           ; Lower speed for larger tool
G43 H2            ; Tool length compensation

G0 Z10.0        ; Rapid to safe height
G0 X0 Y0          ; Center of plate
G0 Z2.0       ; Rapid to clearance

; Helical interpolation to create bore
; (Alternative to boring bar - uses endmill)

; Helical plunge with 12.0mm endmill
G0 X6.500 Y0         ; Start position
G0 Z2.0

; Helical interpolation (1mm per revolution)
G2 X6.500 Y0 Z-1.0 I-6.500 J0 F100
G2 X6.500 Y0 Z-2.0 I-6.500 J0
G2 X6.500 Y0 Z-3.0 I-6.500 J0
G2 X6.500 Y0 Z-4.0 I-6.500 J0
G2 X6.500 Y0 Z-5.0 I-6.500 J0
G2 X6.500 Y0 Z-6.0 I-6.500 J0
G2 X6.500 Y0 Z-7.0 I-6.500 J0  ; Through plate

; Final cleanup pass at full depth
G1 Z-7.350
G2 X6.500 Y0 I-6.500 J0

G0 Z10.0       ; Retract
M5                 ; Spindle off

; === PROGRAM END ===
G0 Z10.0         ; Retract to safe height
G0 X0 Y0           ; Return to center
M5                 ; Spindle off
M9                 ; Coolant off
M30                ; Program end and rewind

; END OF PROGRAM
%
