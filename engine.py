from __future__ import annotations
import lzma
import pickle
from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.map import compute_fov
from tcod import FOV_DIAMOND
import exceptions
from message_log import MessageLog
from time_cycles import TimeCycle, NIGHT_FOV_RANGE
import render_functions
from components.ai import EvilNPC
if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    from components.ai import EvilNPC

class Engine:
    game_map: GameMap
    game_world: GameWorld
    time_cycle: TimeCycle

    def __init__(self, time_cycle: TimeCycle):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player: Actor = None
        self.time_cycle = time_cycle
        self.current_fov_radius = 4

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            hunger = entity.body._hunger
            entity.body._hunger = hunger + 1
            if entity.ai:
                # check hunger levels
                hungry = False
                if entity.body.hunger >= entity.body.max_hunger:
                    hungry = True
                    if hungry:
                        for bp in entity.body.body_parts:
                            bp
                try:
                    entity.ai.perform()
                    if isinstance(entity.ai, EvilNPC):
                        if self.game_map.engine.time_cycle.tick_day == 0:
                            entity.ai.murder_cooldown = entity.ai.murder_cooldown -1
                            print(f"MC is {entity.ai.murder_cooldown}")
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        daytime_base_fov = int(self.game_map.height / 2)

        if self.time_cycle.current_phase_name == "dawn":
            self.current_fov_radius += 1
            if self.current_fov_radius > daytime_base_fov:
                self.current_fov_radius = daytime_base_fov
        
        if self.time_cycle.current_phase_name == "dusk":
            self.current_fov_radius -= 1
            if self.current_fov_radius < 4:
                self.current_fov_radius = 4

        # if self.time_cycle.current_phase_name == "nighttime":
        #     current_radius = 4
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=int(self.current_fov_radius),
            algorithm=FOV_DIAMOND
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)
        # render_functions.render_bar(
        #     console=console,
        #     current_value=self.player.fighter.hp,
        #     maximum_value=self.player.fighter.max_hp,
        #     total_width=20,
        # )
        render_functions.render_bar(
            console=console,
            x=0,
            y=45,
            text="HP",
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )
        render_functions.render_bar(
            console=console,
            x=0,
            y=46,
            text="Hunger",
            current_value=self.player.body.hunger,
            maximum_value=self.player.body.max_hunger,
            total_width=20,
        )
        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

        render_functions.render_time_cycles(
            console=console, x=62, y=45, engine=self
        )
        