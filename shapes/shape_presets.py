from geometry.corner_rounding import CornerRounding

# --- PRESET STYLES ---
SHARP = CornerRounding(radius=0.0, smoothing=0.0)
SOFT = CornerRounding(radius=20.0, smoothing=0.8)
DEEP = CornerRounding(radius=40.0, smoothing=1.0)
ROUND = CornerRounding(radius=35.0, smoothing=0.0)
MEDIUM_ROUOND = CornerRounding(radius=250.0, smoothing=0.0)
VERY_ROUND = CornerRounding(radius=750.0, smoothing=0.0)
SMOOTH = CornerRounding(radius=35.0, smoothing=0.8)
VALLEY = CornerRounding(radius=100.0, smoothing=1.0)

puffy_square = [
    ((0.20, 0.20), SMOOTH),
    ((0.80, 0.20), SMOOTH),
    ((0.80, 0.80), SMOOTH),
    ((0.20, 0.80), SMOOTH),
]

shield = [
    ((0.20, 0.20), ROUND),  # Top Left
    ((0.80, 0.20), ROUND),  # Top Right
    ((0.80, 0.50), SMOOTH),  # Side transition
    ((0.50, 0.90), SMOOTH),  # Bottom Point
    ((0.20, 0.50), SMOOTH),  # Side transition
]

clover_flower = [
    ((0.50, 0.05), ROUND),
    ((0.65, 0.18), ROUND),
    ((0.5, 0.50), SHARP),
    ((0.95, 0.50), ROUND),
    ((0.82, 0.65), ROUND),
    ((0.5, 0.5), SHARP),
    ((0.50, 0.95), ROUND),
    ((0.35, 0.82), ROUND),
    ((0.5, 0.5), SHARP),
    ((0.05, 0.50), ROUND),
    ((0.18, 0.35), ROUND),
    ((0.5, 0.5), SHARP),
]

star = [
    ((0.50, 0.05), SHARP),  # Top Spike
    ((0.60, 0.40), VALLEY),
    ((0.95, 0.40), SHARP),  # Right Spike
    ((0.70, 0.60), VALLEY),
    ((0.80, 0.95), SHARP),  # Bottom Right
    ((0.50, 0.75), VALLEY),
    ((0.20, 0.95), SHARP),  # Bottom Left
    ((0.30, 0.60), VALLEY),
    ((0.05, 0.40), SHARP),  # Left Spike
    ((0.40, 0.40), VALLEY),
]

pill = [
    ((0.15, 0.35), ROUND),
    ((0.85, 0.35), ROUND),
    ((0.85, 0.65), ROUND),
    ((0.15, 0.65), ROUND),
]

organic_blob = [
    ((0.50, 0.15), SMOOTH),
    ((0.85, 0.25), SMOOTH),
    ((0.75, 0.85), SMOOTH),
    ((0.25, 0.70), SMOOTH),
    ((0.10, 0.40), SMOOTH),
]

concave_rectangle = [
    ((0.10, 0.1), ROUND),  # Top Spike
    ((0.50, 0.40), VALLEY),
    ((0.9, 0.10), ROUND),  # Right Spike
    ((0.60, 0.50), VALLEY),
    ((0.9, 0.9), ROUND),  # Bottom Right
    ((0.50, 0.6), VALLEY),
    ((0.1, 0.9), ROUND),  # Bottom Left
    ((0.40, 0.50), VALLEY),
]

# A 12-pointed scalloped cookie (24 points total)
cookie_12 = [
    ((0.50, 0.05), SMOOTH),  # Peak 1 (Top)
    ((0.55, 0.40), VALLEY),  # Cave-in
    ((0.72, 0.11), SMOOTH),  # Peak 2
    ((0.65, 0.45), VALLEY),  # Cave-in
    ((0.89, 0.28), SMOOTH),  # Peak 3
    ((0.70, 0.50), VALLEY),  # Cave-in
    ((0.95, 0.50), SMOOTH),  # Peak 4 (Right)
    ((0.70, 0.55), VALLEY),  # Cave-in
    ((0.89, 0.72), SMOOTH),  # Peak 5
    ((0.65, 0.60), VALLEY),  # Cave-in
    ((0.72, 0.89), SMOOTH),  # Peak 6
    ((0.55, 0.65), VALLEY),  # Cave-in
    ((0.50, 0.95), SMOOTH),  # Peak 7 (Bottom)
    ((0.45, 0.65), VALLEY),  # Cave-in
    ((0.28, 0.89), SMOOTH),  # Peak 8
    ((0.35, 0.60), VALLEY),  # Cave-in
    ((0.11, 0.72), SMOOTH),  # Peak 9
    ((0.30, 0.55), VALLEY),  # Cave-in
    ((0.05, 0.50), SMOOTH),  # Peak 10 (Left)
    ((0.30, 0.50), VALLEY),  # Cave-in
    ((0.11, 0.28), SMOOTH),  # Peak 11
    ((0.35, 0.45), VALLEY),  # Cave-in
    ((0.28, 0.11), SMOOTH),  # Peak 12
    ((0.45, 0.40), VALLEY),  # Cave-in
]

# An 8-pointed scalloped cookie (16 points total)
cookie_8 = [
    ((0.500, 0.050), SMOOTH),  # Peak 1 (0°)
    ((0.622, 0.204), VALLEY),  # Cave-in (22.5°)
    ((0.818, 0.182), SMOOTH),  # Peak 2 (45°)
    ((0.796, 0.378), VALLEY),  # Cave-in (67.5°)
    ((0.950, 0.500), SMOOTH),  # Peak 3 (90°)
    ((0.796, 0.622), VALLEY),  # Cave-in (112.5°)
    ((0.818, 0.818), SMOOTH),  # Peak 4 (135°)
    ((0.622, 0.796), VALLEY),  # Cave-in (157.5°)
    ((0.500, 0.950), SMOOTH),  # Peak 5 (180°)
    ((0.378, 0.796), VALLEY),  # Cave-in (202.5°)
    ((0.182, 0.818), SMOOTH),  # Peak 6 (225°)
    ((0.204, 0.622), VALLEY),  # Cave-in (247.5°)
    ((0.050, 0.500), SMOOTH),  # Peak 7 (270°)
    ((0.204, 0.378), VALLEY),  # Cave-in (292.5°)
    ((0.182, 0.182), SMOOTH),  # Peak 8 (315°)
    ((0.378, 0.204), VALLEY),  # Cave-in (337.5°)
]

fan = [
    ((0.10, 0.10), MEDIUM_ROUOND),  # Bottom Pivot Point
    ((0.90, 0.10), VERY_ROUND),  # Left Blade Tip
    ((0.9, 0.9), MEDIUM_ROUOND),  # Inner Gorge
    ((0.10, 0.90), MEDIUM_ROUOND),  # Center Top Blade
]
