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
    ("test-runner", "test runner", "Dev", "Test-runner output: a row per month, a dot for every active day and a dash for every quiet one."),
    ("commit-log", "commit log", "Dev", "Your ten busiest days, sorted like terminal output with a bar for each."),
    ("aurora", "aurora", "Space", "Northern lights: curtains of light that swell in the weeks you were busy."),
    ("black-hole", "black hole", "Space", "Your days orbit a black hole on an accretion disk, the newest days closest to the edge."),
    ("activity-rings", "activity rings", "Minimal", "Three rings: this week, this month against your best, and your streak against your longest."),
    ("year-sparkline", "year sparkline", "Minimal", "The whole year as one smooth line, with your busiest week and today marked."),
    ("orbit-rings", "orbit rings", "Space", "One ring per month. The dots on a ring are that month's days."),
    ("terminal-heatmap", "terminal heatmap", "Dev", "The usual grid, but drawn with text characters like command output."),
    ("radial-bars", "radial bars", "Minimal", "Every day is a spoke around a circle, longer for busier days. It starts at the top and runs clockwise."),
    ("tower", "tower", "3D", "A tower with one floor per month. Wider floors and more lit windows mean busier months."),
    ("streak-timeline", "streak timeline", "Minimal", "Every streak as a block along one year. Long streaks get a label."),
    ("moon-phases", "moon phases", "Space", "Each day is a moon: new when quiet, full when busy. Shows the last 26 weeks."),
    ("git-graph", "git graph", "Dev", "A main line with a node for every active week and branches that fork and merge back, like git log --graph."),
    ("hex-dump", "hex dump", "Dev", "Each day is one byte. Busy days are bigger hex values, like opening a binary file."),
    ("topographic-map", "topographic map", "Nature", "Contour lines rise around the weeks you were busiest, like a hiking map."),
    ("barcode", "barcode", "Minimal", "Your year as a product barcode. Thick bars are active days."),
    ("dna-helix", "DNA helix", "3D", "Two twisting strands with a rung for every active day."),
]
