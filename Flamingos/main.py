#!/usr/bin/env python3
import tcod

from engine import Engine
from input_handlers import EventHandler
from data_classes.game_map import GameMap
from data_classes.entity import Entity
ART_PATH = 'Assets/Art/'


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        ART_PATH + "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    event_handler = EventHandler()
    player = Entity(int(screen_width/2), int(screen_height/2), "@", (255, 123, 255))
    npc = Entity(int(screen_width/2) - 5, int(screen_height/2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial with flamingos!",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)
            events= tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
