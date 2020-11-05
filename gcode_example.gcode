G21         ; Set units to mm
G90         ; Absolute positioning
G1 Z1.9999999999999998 F2540      ; Move to clearance level

;
; Operation:    0
; Name:         
; Type:         Engrave
; Paths:        1
; Direction:    Conventional
; Cut Depth:    0.9999999999999999
; Pass Depth:   3.175
; Plunge rate:  127
; Cut rate:     1016
;

; Path 0
; Rapid to initial position
G1 X289.5298 Y189.7441 F2540
G1 Z1.0000
; plunge
G1 Z0.0000 F127
; cut
G1 X0.0000 Y189.7441 F1016
G1 X0.0000 Y0.0000
G1 X289.5298 Y0.0000
G1 X289.5298 Y189.7441
G1 X289.5298 Y189.7441
; Retract
G1 Z2.0000 F2540
M2
