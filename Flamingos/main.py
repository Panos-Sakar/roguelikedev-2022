#!/usr/bin/env python3
import tcod
import time
from engine import Engine
from input_handlers import EventHandler
from generators.procgen import generate_dungeon, generate_dungeon_2
from data_classes.entity import Entity
ART_PATH = 'Assets/Art/'


def main() -> None:
    screen_width = 120
    map_width = screen_width * 3
    screen_height = 80
    map_height = screen_height * 3

    room_max_size = 20
    room_min_size = 10
    max_rooms = 25




    tileset = tcod.tileset.load_tilesheet(
        ART_PATH + "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    event_handler = EventHandler()
    player = Entity(int(screen_width/2), int(screen_height/2), "@", (255, 0, 255))
    npc = Entity(int(screen_width/2) - 5, int(screen_height/2), "@", (255, 255, 0))
    entities = {npc}

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    # game_map = generate_dungeon_2(
    #     room_min_size=room_min_size,
    #     room_max_size=room_max_size,
    #     map_width=map_width,
    #     map_height=map_height,
    #     player=player
    # )

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
            start_time = time.time()  # start time of the loop
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)
            print("FPS: ", 1.0 / (time.time() - start_time))


if __name__ == "__main__":
    main()
