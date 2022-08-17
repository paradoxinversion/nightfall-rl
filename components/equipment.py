from __future__ import annotations
from operator import add
from typing import Optional, List, TYPE_CHECKING
from components.base_component import BaseComponent
from components.equippable import EquippableType
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item
    from body import BodyPartTypes, BodyPart
    from equippable import EquippableType

class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None, item: Optional[Item] = None,):
        self.weapon = weapon
        self.armor = armor
        self.worn_articles = {}

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.defense_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.power_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def equip_to_bp(self, body_part: BodyPart, item: Item, add_message: bool) -> None:
        """Equip the current item to the appropriate body slot"""

        current_item = body_part.worn_article if item.equippable.equipment_type == EquipmentType.CLOTHES else body_part.held_object

        if current_item is not None:
            self.unequip_from_bp(body_part, item, add_message)

        if item.equippable.equippable_type == EquippableType.WORN_ARTICLE:
            body_part.worn_article = item
        else:
            body_part.held_object = item

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def unequip_from_bp(self, body_part: BodyPart, item: Item, add_message: bool) -> None:
        current_item = body_part.worn_article if item.equippable.equippable_type == EquippableType.WORN_ARTICLE else body_part.held_object

        if add_message:
            self.unequip_message(current_item.name)

        body_part.worn_article = None
    
    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)

    def toggle_equip_bp(self, item: Item, add_message: bool = True) -> None:
        for body_slot in item.equippable.body_slots:
            actor_body_parts = self.parent.body.get_parts_of_type(body_slot) #might be null
            for body_part in actor_body_parts:
                if item.equippable.equippable_type == EquippableType.WORN_ARTICLE:
                    slot = "worn_article"
                else:
                    slot = "held_object"
                
                if getattr(body_part, slot):
                    self.unequip_from_bp(body_part=body_part, item=item, add_message=add_message)
                else:
                    self.equip_to_bp(body_part, item, add_message)