from __future__ import annotations
from typing import Tuple, List, TYPE_CHECKING
from xml.sax.handler import property_interning_dict
from components.base_component import BaseComponent
from copy import deepcopy
if TYPE_CHECKING:
    from entity import Actor

class BodyPart():
    parent: Body
    def __init__(self, name: str, bodypart_type: str, hp: int, max_damage_lethal=False, attacks=False):
        self._name = name
        self._hp = hp
        self.max_hp = hp
        self.max_damage_lethal = max_damage_lethal
        self.bodypart_type = bodypart_type
        self._attacks = attacks

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


body_template_humanoid = {
    "head": BodyPart("Head", "head", 20, True, False),
    "torso": BodyPart("Torso", "torso", 30, True, False),
    "left_arm": BodyPart("Left Arm", "arm", 10, False, True),
    "right_arm": BodyPart("Right Arm", "arm", 10, False, True),
    "left_leg": BodyPart("Left Leg", "leg", 15, False, False),
    "right_leg": BodyPart("Rigt Leg", "leg", 15, False, False),
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
    
    @property
    def targetable_body_parts(self) -> List[BodyPart]:
        """Return a list of body parts for combat."""
        body_parts = []
        for body_part in self.body_parts.values():
            if body_part.targetable:
                body_parts.append(body_part)
        return body_parts

    @property
    def dangerous_body_parts(self) -> List[BodyPart]:
        """Returns a list of body parts this character is capable of attacking with"""
        dbp = []
        for body_part in self.body_parts.values():
            if body_part.can_attack:
                dbp.append(body_part)
        return dbp