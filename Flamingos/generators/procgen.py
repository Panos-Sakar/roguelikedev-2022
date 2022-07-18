from __future__ import annotations
import random

from typing import Iterator, Tuple, List, TYPE_CHECKING
import tcod
from data_classes.game_map import GameMap
import data_classes.tile_types as tile_types

if TYPE_CHECKING:
    from data_classes.entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )

    def place_doors(self, dungeon: GameMap):
        last_was_door = False
        for x in range(self.x1, self.x2+1):
            if dungeon.tiles[x][self.y1] == tile_types.wall:
                last_was_door = False
            if dungeon.tiles[x][self.y1] == tile_types.hallway and not last_was_door:
                dungeon.tiles[x][self.y1] = tile_types.door
                last_was_door = True
        last_was_door = False
        for x in range(self.x1, self.x2 + 1):
            if dungeon.tiles[x][self.y2] == tile_types.wall:
                last_was_door = False
            if dungeon.tiles[x][self.y2] == tile_types.hallway and not last_was_door:
                dungeon.tiles[x][self.y2] = tile_types.door
                last_was_door = True
        last_was_door = False
        for y in range(self.y1, self.y2 + 1):
            if dungeon.tiles[self.x1][y] == tile_types.wall:
                last_was_door = False
            if dungeon.tiles[self.x1][y] == tile_types.hallway and not last_was_door:
                dungeon.tiles[self.x1][y] = tile_types.door
                last_was_door = True
        last_was_door = False
        for y in range(self.y1, self.y2 + 1):
            if dungeon.tiles[self.x2][y] == tile_types.wall:
                last_was_door = False
            if dungeon.tiles[self.x2][y] == tile_types.hallway and not last_was_door:
                dungeon.tiles[self.x2][y] = tile_types.door
                last_was_door = True


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this room's inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.

            # BUGGY CODE TO ADD DOORS, DELETE ALL LINES FROM 99-115 BUT KEEP LINE 112
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                if dungeon.tiles[x, y] == tile_types.wall:
                    dungeon.tiles[x, y] = tile_types.hallway

        # Finally, append the new room to the list.
        rooms.append(new_room)
    for room in rooms:
        room.place_doors(dungeon)
    return dungeon

# doesnt work pls dont use


def generate_dungeon_2(
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    room_width = random.randint(room_min_size, room_max_size)
    room_height = random.randint(room_min_size, room_max_size)

    first_room_x = int(map_width / 2 - room_width / 2)
    first_room_y = int(map_height / 2 - room_height / 2)

    player.x = int(map_width / 2)
    player.y = int(map_height / 2)

    new_room = RectangularRoom(first_room_x, first_room_y, room_width, room_height)
    dungeon.tiles[new_room.inner] = tile_types.floor

    rooms.append(new_room)

    while True:
        dungeon.tiles[new_room.pick_random_wall()] = tile_types.door

    return dungeon
