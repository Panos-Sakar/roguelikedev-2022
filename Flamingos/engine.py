from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from data_classes.entity import Entity
from input_handlers import EventHandler
from data_classes.game_map import GameMap


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):

        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            action.perform(self, self.player)
            self.update_fov()  # Update the FOV before the players next action.

    # algorithm = 2 circular
    # algorithm = 12 default

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=10,
            algorithm=2
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console, self.player)
        console.print(self.player.x - self.game_map.camera_top_x, self.player.y - self.game_map.camera_top_y, self.player.char, fg = self.player.color)
        context.present(console)
        console.clear()
