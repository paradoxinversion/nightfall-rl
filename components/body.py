from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class BodyPart(BaseComponent):
    parent: Body
    def __init__(self, *, name: str, hp: int, base_defense: int):
        self.name: name
        self.hp = hp
        base_defense = base_defense

class Leg(BodyPart):
    def __init__(self, hp: int, base_defense: int):
        self.parent: Body

class Arm(BodyPart):
    def __init__(self, hp: int, base_defense: int):
        self.parent: Body

class Head( BodyPart):
    def __init__(self, hp: int, base_defense: int):
        self.parent: Body

class Torso(BodyPart):
    def __init__(self, hp: int, base_defense: int):
        self.parent: Body

class BodyTemplate():
    def __init__(self, parent, bodyParts):
        self.parent = parent

class BodyTemplate_Human(BodyTemplate):
    def __init__(
        self,
        body,
        parent,
        head: Head,
        left_arm: Arm, 
        right_arm: Arm,
        left_leg: Leg,
        right_leg: Leg,
        torso: Torso
    ):
        body = {
            'Head': head,
            'Left Arm': left_arm,
            'Right Arm': right_arm,
            'Left Leg': right_leg,
            'Right Leg': left_leg,
            'Torso':
        }
        self.head = head
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.left_leg = left_leg
        self.right_leg = right_leg
        self.torso = torso

class Body(BaseComponent):
    """A body def for a coporeal or incorporeal entity """
    parent: Actor
    body_template: BodyTemplate
    def __init__(self, race="human"):
        if (race == "human"):
            self.body_template = BodyTemplate_Human
        self.foo = 1
        