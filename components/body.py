from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from components.base_component import BaseComponent
from copy import deepcopy
if TYPE_CHECKING:
    from entity import Actor

class BodyPart():
    parent: Body
    def __init__(self, name: str, hp: int, max_damage_lethal=False):
        self._name = name
        self._hp = hp
        self.max_hp = hp
        self.max_damage_lethal = max_damage_lethal

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def actor(self) -> Actor:
        return self.parent.parent

    @property
    def body(self) -> Body:
        return self.parent

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

body_template_humanoid = {
    "head": BodyPart("Head", 20, max_damage_lethal=True),
    "torso": BodyPart("Torso", 30, max_damage_lethal=True),
    "left_arm": BodyPart("Left Arm", 10),
    "right_arm": BodyPart("Right Arm", 10),
    "left_leg": BodyPart("Left Leg", 15),
    "right_leg": BodyPart("Rigt Leg", 15),
}
class Body(BaseComponent):
    """A body def for a coporeal or incorporeal entity """
    parent: Actor
    def __init__(self, race="human"):
        if (race == "human"):
            body_template = deepcopy(body_template_humanoid)
        else:
            body_template = deepcopy(body_template_humanoid) # The default body template is humanoid
        self.body_parts = body_template
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
