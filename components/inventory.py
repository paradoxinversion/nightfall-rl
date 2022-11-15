from __future__ import annotations
from typing import List, TYPE_CHECKING
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item

class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)
        self.engine.message_log.add_message(f"You dropped the {item.name}.")
    
    def add(self, item: Item) -> None:
        """
        Adds an item to the inventory
        """
        self.items.append(item)
        item.parent = self
        item.name = self.parent.name + " " + item.name