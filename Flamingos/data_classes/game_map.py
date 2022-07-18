import numpy as np
from tcod.console import Console
from data_classes.entity import Entity
from data_classes import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before
        self.camera_top_x = 0
        self.camera_bottom_x = 0
        self.camera_top_y = 0
        self.camera_bottom_y = 0

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




