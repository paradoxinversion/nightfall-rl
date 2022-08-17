from __future__ import annotations
from typing import TYPE_CHECKING, List
from enum import Enum
from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item

class EquippableType(Enum):
    WORN_ARTICLE = 0
    HELD_OBJECT = 1

class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        body_slots,
        equippable_type: EquippableType,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.equippable_type = equippable_type
        self.body_slots = body_slots

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.HELD_OBJECT, equipment_type=EquipmentType.WEAPON, power_bonus=2, body_slots=["arm"])


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.HELD_OBJECT, equipment_type=EquipmentType.WEAPON, power_bonus=4, body_slots=["arm"])


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE, equipment_type=EquipmentType.ARMOR, defense_bonus=1, body_slots=["arm"])

class Jacket(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE, equipment_type=EquipmentType.ARMOR, defense_bonus=1, body_slots=["arm", "torso"])

class Pants(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE, equipment_type=EquipmentType.ARMOR, defense_bonus=1, body_slots=["leg"])

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE, equipment_type=EquipmentType.ARMOR, defense_bonus=3, body_slots=["arm"])