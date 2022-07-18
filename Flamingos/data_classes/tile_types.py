from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),   # Unicode codepoint.
        ("fg", "3B"),       # 3 unsigned bytes, for RGB colors.
        ("bg", "3B")
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
        *,      # Enforce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (128, 128, 128)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (60, 60, 60)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord(" "), (164, 120, 0), (102, 51, 0)),
    light=(ord(" "), (255, 188, 0), (153, 76, 0)),
)

hallway = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (128, 128, 128)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)