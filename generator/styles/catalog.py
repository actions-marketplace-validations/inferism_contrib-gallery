"""The list of ready styles: id, title, gallery category and a one-line description.

build_samples.py turns this into samples/styles.json (what the gallery loads) and the table in the README.
To add a style: write generator/styles/<name>.py, register it in __init__.py, and add a line here.
"""

CATALOG = [
    ("spiral-galaxy", "spiral galaxy", "Space", "Your year winds out from the center along a spiral arm. Brighter stars are busier days."),
    ("constellation", "constellation", "Space", "Active days are stars. Close days connect into constellations."),
    ("htop-monitor", "htop monitor", "Dev", "Months as system-monitor bars with percentages. Shows how busy each month was."),
    ("ridgeline", "ridgeline mountains", "3D", "One jagged line per month stacked on black, like the Unknown Pleasures album cover. Peaks are busy days."),
    ("vinyl-record", "vinyl record", "Music", "A record with one ring of grooves per month. Every active day is a blip along its ring."),
    ("piano-roll", "piano roll", "Music", "Weekdays are piano keys, weeks run left to right, and every active day is a note. Longer notes are busier days."),
    ("tree-growth", "tree", "Nature", "A tree grows a branch for every active week. Longer branches are busier weeks, and each leaf is an active day."),
    ("ocean-waves", "ocean waves", "Nature", "One wave per month, stacked in the sea. Taller swells are busier days."),
    ("space-invaders", "space invaders", "Games", "Every active day is an invader. Busier days are bigger, brighter invaders."),
    ("rpg-status", "RPG status", "Games", "A character sheet built from your year: level, XP and stat bars like HP and mana."),
    ("skyline", "3D skyline", "3D", "A 3D city floating in space. One building per day, taller and brighter when you were busier."),
    ("terrain-mesh", "terrain mesh", "3D", "A wireframe landscape. Weeks run left to right, weekdays go into the distance, and height is how busy you were."),
    ("dig-site", "dig site", "Games", "A cross-section of the ground. Every active week digs a shaft, deeper when busier, with a gem at the bottom."),
    ("obby-course", "obby course", "Games", "An obstacle course of floating platforms, one for each active week. Higher platforms are busier weeks."),
    ("block-stack", "block stack", "Games", "A falling-block puzzle. One column per month, stacked as high as the month was busy."),
    ("farm-plots", "farm plots", "Games", "A farm where every day is a plot. Busy days grow from a seed to a ripe crop."),
]
