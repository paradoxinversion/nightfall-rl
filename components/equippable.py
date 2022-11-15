from __future__ import annotations
from typing import TYPE_CHECKING, List
from enum import Enum
from components.base_component import BaseComponent
from components.body import BodyPartTypes
from equipment_types import EquipmentType
from combat import Attack

if TYPE_CHECKING:
    from entity import Item
    from combat import Attack


class EquippableType(Enum):
    WORN_ARTICLE = 0
    HELD_OBJECT = 1


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        body_slots,  # what
        equippable_type: EquippableType,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        attacks: List[Attack] = []
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.equippable_type = equippable_type
        self.body_slots = body_slots
        self._attacks = attacks

    @property
    def attacks(self):
        """A list of the weapon's available attacks"""
        return self._attacks

slash = Attack("slash", 10)

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.HELD_OBJECT,
                         equipment_type=EquipmentType.WEAPON, power_bonus=2, body_slots=[BodyPartTypes.ARM], attacks=[slash])


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.HELD_OBJECT,
                         equipment_type=EquipmentType.WEAPON, power_bonus=4, body_slots=[BodyPartTypes.ARM], attacks=[slash])


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE,
                         equipment_type=EquipmentType.ARMOR, defense_bonus=1, body_slots=[BodyPartTypes.ARM])


class Jacket(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE, equipment_type=EquipmentType.ARMOR,
                         defense_bonus=1, body_slots=[BodyPartTypes.ARM, BodyPartTypes.TORSO])


class Pants(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE,
                         equipment_type=EquipmentType.ARMOR, defense_bonus=1, body_slots=[BodyPartTypes.LEG])


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equippable_type=EquippableType.WORN_ARTICLE,
                         equipment_type=EquipmentType.ARMOR, defense_bonus=3, body_slots=[BodyPartTypes.ARM])
