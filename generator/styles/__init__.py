from . import (
    constellation,
    htop_monitor,
    ocean_waves,
    piano_roll,
    ridgeline,
    rpg_status,
    skyline,
    space_invaders,
    spiral_galaxy,
    terrain_mesh,
    tree_growth,
    vinyl_record,
)

STYLES = {
    "constellation": constellation.render,
    "htop-monitor": htop_monitor.render,
    "ocean-waves": ocean_waves.render,
    "piano-roll": piano_roll.render,
    "ridgeline": ridgeline.render,
    "rpg-status": rpg_status.render,
    "skyline": skyline.render,
    "space-invaders": space_invaders.render,
    "spiral-galaxy": spiral_galaxy.render,
    "terrain-mesh": terrain_mesh.render,
    "tree-growth": tree_growth.render,
    "vinyl-record": vinyl_record.render,
}
