from __future__ import annotations

class Skill:
    def __init__(self, parent, name, value):
        self.parent = parent
        self.name = name
        self.value = value
        self.bonus = 0
        self.penalty = 0
    
    def increase(self, amt):
        self.value += amt
