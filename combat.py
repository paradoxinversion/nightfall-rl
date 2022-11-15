from __future__ import annotations
import json
from typing import TYPE_CHECKING, Dict
import color
import random
from entity import Actor
from components.body import BodyPartTypes

if TYPE_CHECKING:
    from engine import Engine
    from components.body import BodyPart, BodyPartTypes

class Attack():
    def __init__(self, name,  damage) -> None:
        self._name = name
        self._damage = damage
    
    @property
    def name(self):
        """The name of the attack"""
        return self._name
