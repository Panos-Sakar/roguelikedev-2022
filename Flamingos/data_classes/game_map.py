from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING
import numpy as np
from tcod.console import Console
from data_classes.entity import Entity
from data_classes import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.entities = set(entities)
        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before
        self.camera_top_x = 0
        self.camera_bottom_x = 0
        self.camera_top_y = 0
        self.camera_bottom_y = 0

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console, player: Entity) -> None:

        self.update_camera_points(console, player)

        dummy_visible = self.visible[self.camera_top_x : self.camera_bottom_x, self.camera_top_y : self.camera_bottom_y]
        dummy_explored = self.explored[self.camera_top_x : self.camera_bottom_x, self.camera_top_y : self.camera_bottom_y]
        dummy_tiles = self.tiles[self.camera_top_x : self.camera_bottom_x, self.camera_top_y : self.camera_bottom_y]

        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[dummy_visible, dummy_explored],
            choicelist=[dummy_tiles["light"], dummy_tiles["dark"]],
            default=tile_types.SHROUD
        )
        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(entity.x - self.camera_top_x, entity.y - self.camera_top_y, entity.char, fg=entity.color)

    def update_camera_points(self, console: Console, player: Entity) -> None:
        self.camera_top_x = (player.x - int(console.width / 2))
        self.camera_bottom_x = (player.x + int(console.width / 2))
        self.camera_top_y = (player.y - int(console.height / 2))
        self.camera_bottom_y = (player.y + int(console.height / 2))

        if self.camera_top_x < 0:
            self.camera_top_x = 0
            self.camera_bottom_x = console.width
        if self.camera_bottom_x > self.width:
            self.camera_bottom_x = self.width
            self.camera_top_x = self.width - console.width
        if self.camera_top_y < 0:
            self.camera_top_y = 0
            self.camera_bottom_y = console.height
        if self.camera_bottom_y > self.height:
            self.camera_bottom_y = self.height
            self.camera_top_y = self.height - console.height

        #print(self.camera_top_x, " ", self.camera_bottom_x, " ", self.camera_top_y, " ", self.camera_bottom_y)




