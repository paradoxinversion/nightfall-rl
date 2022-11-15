from __future__ import annotations
import copy
import math
# from entity_factories import pants
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union, List, Dict
from render_order import RenderOrder
from namegen import NameGenerator
from components.deeds import Deeds
if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from components.body import Body
    from components.deeds import Deeds
    from components.skills import Skill
    from game_map import GameMap
    from building import Building

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    parent: Union[GameMap, Inventory]
    def __init__(
       self,
       parent: Optional[GameMap] = None,
       x: int = 0,
       y: int = 0,
       char: str = "?",
       color: Tuple[int, int, int] = (255, 255, 255),
       name: str = "<Unnamed>",
       blocks_movement: bool = False,
       render_order: RenderOrder = RenderOrder.CORPSE
   ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self._name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)
    @property
    def name(self):
        """The entity's name"""
        return self._name

    @name.setter
    def name(self, name) -> str:
        self._name = name
        
    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int, spawn_items: List[Item] = []) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
    #    if isinstance(self, Actor):
    #         for i in spawn_items:
    #             if i.equippable:
    #                 equippable_item = copy.deepcopy(i)
    #                 equippable_item.parent = clone.inventory
    #                 clone.inventory.items.append(equippable_item)
    #                 clone.equipment.toggle_equip(equippable_item)
        clone.initialize()
        return clone 

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            
    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def initialize(self):
        pass

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        level: Level,
        body: Body,
        base_fov: int = 8,
        evil: bool = False,
        friends: list[Actor] = [],
        player_character: bool = False
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )
        self.first_name: str = "<Unnamed>"
        self.last_name: str = "<Unnamed>"
        self.base_fov = base_fov

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.body: Body = body
        self.body.parent = self

        self.equipment: Equipment = equipment
        self.equipment.parent = self
        self.equipment.worn_articles: dict[str, Equippable | None] = dict.fromkeys(self.body.body_parts.keys(), None)

        self.fighter: Fighter= fighter
        self.fighter.parent = self
        
        self.inventory: Inventory = inventory
        self.inventory.parent = self

        self.level: Level = level
        self.level.parent = self 
        self.owned_building: Building = None
        self.evil = False
        self.player_character = player_character

        self.deeds: Deeds = Deeds()
        self.skills: Dict[str, Skill] = {}
        self.friends = friends
        self.alive = True

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)

    def initialize(self, first_name: str = None, last_name: str = None, age: int = None):
        if not first_name:
            self.first_name: str = NameGenerator.get_first_name()
        else:
            self.first_name = first_name
        
        if not last_name:
            self.last_name: str = NameGenerator.get_last_name()
        else:
            self.last_name = last_name
        full_name = f"{self.first_name} {self.last_name}"
        self._name = full_name
        
        self.fighter.max_hp = self.body.total_hp
        self.fighter.hp = self.body.total_hp
        print (f"Initialized Character - {self._name} at {self.x},{self.y}")

    def set_ai(self, ai: Type[BaseAI]):
        self.ai = ai(self)

class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
        blocks_movement: bool= False
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=blocks_movement,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self