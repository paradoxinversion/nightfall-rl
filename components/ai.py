from __future__ import annotations
import pdb
import random
from typing import Callable, Optional, Tuple, TYPE_CHECKING, List
from enum import auto, Enum
import numpy as np  # type: ignore
import tcod
from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction, AttackAction

if TYPE_CHECKING:
    from entity import Actor, Entity

class NPCActivity(Enum):
    WANDER = auto()
    GO_HOME = auto()
    SEEK_VICTIM = auto()


class BaseAI(Action):
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI] = None ):
        super().__init__(entity)
        self.previous_ai = previous_ai
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]
class WanderingAI(BaseAI):
    """A wandering enemy will rander aimlessly until their AI type changes"""
    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)

    def perform(self) -> None:
        direction_x, direction_y = random.choice(
            [
                (-1, -1),  # Northwest
                (0, -1),  # North
                (1, -1),  # Northeast
                (-1, 0),  # West
                (1, 0),  # East
                (-1, 1),  # Southwest
                (0, 1),  # South
                (1, 1),  # Southeast
            ]
        )
        return BumpAction(self.entity, direction_x, direction_y,).perform()
class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y,).perform()

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI] = None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy, False).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y, False
            ).perform()

        return WaitAction(self.entity).perform()

class Combatant(BaseAI):
    def __init__(self, entity: Actor, target: Actor, previous_ai: Optional[BaseAI] = None):
        super().__init__(entity, previous_ai)
        self.path: List[Tuple[int, int]] = []
        self.target = target

    def perform(self) -> None:
        if self.target and self.target.is_alive:
            dx = self.target.x - self.entity.x
            dy = self.target.y - self.entity.y
            distance = max(abs(dx), abs(dy))  # Chebyshev distance.
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy, False).perform()

            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(
                    self.entity, dest_x - self.entity.x, dest_y - self.entity.y, False
                ).perform()

        return WaitAction(self.entity).perform()
    

class NPC(BaseAI):
    """NPCs wander their maps during the day and go home at night."""
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI] = None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.current_action: NPCActivity = NPCActivity.WANDER
        self.previous_ai = previous_ai

    def go_to_location(self, x, y) -> None:
        """Move the NPC toward a map tile"""
        self.current_action = "moving to location"
        self.path = self.get_path_to(x, y)
        if len(self.path) > 0:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y, False
            ).perform()

    def go_home(self):
        """The character will move until they are on their plot"""
        if (self.entity.owned_building):
            target_home_tile_x = self.entity.owned_building.x
            target_home_tile_y = self.entity.owned_building.y
            self.current_action = "going home"
            self.go_to_location(target_home_tile_x, target_home_tile_y)

    def wander(self):
        direction_x, direction_y = random.choice(
            [
                (-1, -1),  # Northwest
                (0, -1),  # North
                (1, -1),  # Northeast
                (-1, 0),  # West
                (1, 0),  # East
                (-1, 1),  # Southwest
                (0, 1),  # South
                (1, 1),  # Southeast
            ]
        )
        return BumpAction(self.entity, direction_x, direction_y, False).perform()

    def perform(self) -> None:
        # NPCs wander by default, unless they are going home or home for the night
        if self.engine.time_cycle._current_phase < 3:
            self.wander()
        else:
            self.go_home()


class EvilNPC(NPC):
    """NPCs wander their maps during the day and go home at night."""
    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI] = None):
        super().__init__(entity)
        self.current_target: Actor = None
        self.murder_cooldown = 0
        self.current_target = None
    def seek_victim(self):
        # if (self.murder_cooldown > 0):
        #     self.wander()
        # select a victim
        if self.current_target == None:
            possible_victims = []
            for actor in self.engine.game_map.actors:
                if actor is not self.entity and actor.is_alive and actor.player_character == False and actor not in self.entity.friends:
                    possible_victims.append(actor)
            victim = random.choice(list(possible_victims))
            self.current_target = victim
            print(f"{self.entity.name} is hunting {self.current_target.name}")
        # pathfind to that victim
        x = self.current_target.x
        y = self.current_target.y
        self.path = self.go_to_location(x, y)
        dx = x - self.entity.x
        dy = y - self.entity.y
        distance = max(abs(dx), abs(dy))
        if distance <= 1:
        # attack victim
            AttackAction(self.entity, self.current_target).perform()
            if not self.current_target.alive:
                print("Setting murder cooldown to 3")
                self.murder_cooldown = 3 # wait three days for the next murder
                self.current_target = None 

    def perform(self) -> None:
        # NPCs wander by default, unless they are going home or home for the night
        self.seek_victim()
        
            