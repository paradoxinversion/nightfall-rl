from __future__ import annotations
from enum import Enum
from typing import Dict, Tuple, List, TYPE_CHECKING
from components.base_component import BaseComponent
from copy import deepcopy
if TYPE_CHECKING:
    from entity import Actor, Item

class BodyPartTypes(Enum):
    HEAD = 0
    TORSO = 1
    ARM = 2
    LEG = 3
    TAIL = 4

class BodyPart():
    parent: Body
    def __init__(self, name: str, bodypart_type: BodyPartTypes, hp: int, max_damage_lethal=False, attacks=False, energy=100):
        self._name = name
        self._hp = hp
        self.max_hp = hp
        self.max_damage_lethal = max_damage_lethal
        self.bodypart_type = bodypart_type
        self._attacks = attacks
        self.worn_article = None
        self.held_object = None
        self.energy = energy

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        """Return the BodyPart's current HP"""
        return self._hp

    @property
    def actor(self) -> Actor:
        """Return the BodyPart's Actor"""
        return self.parent.parent

    @property
    def equipped_items(self) -> List[Item]:
        """Return the body part's worn article and held object"""
        return [self.worn_article, self.held_object]

    @property
    def body(self) -> Body:
        """Return the BodyPart's Body"""
        return self.parent

    @property
    def attacks(self) -> bool:
        """True if this BodyPart can be used to attack, false otherwise"""
        return self._attacks

    def heal(self, amount: int) -> int:
        if self._hp == self.max_hp:
            return 0

        new_hp_value = self._hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self._hp
        self._hp = new_hp_value
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self._hp -= amount
        # If the body is at zero hp, the entity should die
        if self.parent.total_hp <= 0:
            self.actor.fighter.die()
        # If the body has taken lethal damage, the entity should die
        if self._hp <= 0 and self.max_damage_lethal == True:
            self.actor.fighter.die()

    @property
    def can_attack(self):
        if self.attacks == False:
            return False
        if self.hp <= 0:
            return False
        return True

    @property
    def targetable(self):
        """Return True if the body part can be targeted, False if not"""
        if (self._hp > 0):
            return True
        return False

class BT_Head(BodyPart):
    def __init__(self, name="Head") -> None:
        super().__init__(name=name, bodypart_type=BodyPartTypes.HEAD, hp=20, max_damage_lethal=True, attacks=False)

class BT_Torso(BodyPart):
    def __init__(self, name="Torso") -> None:
        super().__init__(name=name, bodypart_type=BodyPartTypes.TORSO, hp=30, max_damage_lethal=True, attacks=False)

class BT_Arm(BodyPart):
    def __init__(self, name="Arm") -> None:
        super().__init__(name=name, bodypart_type=BodyPartTypes.ARM, hp=10, max_damage_lethal=False, attacks=True)

class BT_Leg(BodyPart):
    def __init__(self, name="Leg") -> None:
        super().__init__(name=name, bodypart_type=BodyPartTypes.LEG, hp=20, max_damage_lethal=False, attacks=True)

body_template_humanoid = {
    "head": BT_Head(),
    "torso": BT_Torso(),
    "left_arm": BT_Arm("Left Arm"),
    "right_arm": BT_Arm("Right Arm"),
    "left_leg": BT_Leg("Left Leg"),
    "right_leg": BT_Leg("Rigt Leg"),
}
class Body(BaseComponent):
    """A body def for a coporeal or incorporeal entity """
    parent: Actor
    def __init__(self, race="human"):
        if (race == "human"):
            body_template = deepcopy(body_template_humanoid)
        else:
            body_template = deepcopy(body_template_humanoid) # The default body template is humanoid
        self.body_parts: dict[str, BodyPart] = body_template
        for part in body_template.values():
            part.parent = self
    
    @property
    def total_hp(self):
        total_hp = 0
        for body_part in self.body_parts.values():
            total_hp += body_part.max_hp
        return total_hp

    @property
    def current_hp(self):
        current_total_hp = 0
        for body_part in self.body_parts.values():
            current_total_hp += body_part.hp
        return current_total_hp
    
    @property
    def targetable_body_parts(self) -> List[BodyPart]:
        """Return a list of body parts for combat."""
        body_parts = []
        for body_part in self.body_parts.values():
            if body_part.targetable:
                body_parts.append(body_part)
        return body_parts

    @property
    def usable_body_parts(self) -> List[BodyPart]:
        """Returns a list of body parts this character is capable of attacking with"""
        usable_part = []
        for body_part in self.body_parts.values():
            if body_part.can_attack:
                usable_part.append(body_part)
        return usable_part

    def get_parts_of_type(self, part_type: BodyPartTypes) -> List[BodyPart]:
        """Returns a list of body parts that match a given part_type"""
        parts = []
        for body_part in self.body_parts.values():
            if body_part.bodypart_type == part_type:
                parts.append(body_part)
        return parts