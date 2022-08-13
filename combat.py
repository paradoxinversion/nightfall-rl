from __future__ import annotations
import json
from typing import TYPE_CHECKING, Dict
import color
import random
from entity import Actor
if TYPE_CHECKING:
    from engine import Engine
    from components.body import BodyPart

class Attack():
    """A basic attack class"""
    @staticmethod
    def attack(engine: Engine, attacker: Actor, target: Actor):
        # Determine what body parts the attacker can use to attack
        # Keep a list of the keys ['arms', 'legs', ...etc]
        attacker_viable_body_parts = []
        
        for body_part in attacker.body.dangerous_body_parts:
            attacker_viable_body_parts.append(body_part.bodypart_type)
        # Most entities will have duplicates in the above list,
        # So we turn it into a set
        # parts = [*set(available_attack_body_part_types)]
        # Choose an attacking bodypart from the set of part keys
        chosen_part = random.choice(attacker_viable_body_parts)
        if chosen_part is not None and attack_templates.get(chosen_part) is not None:
            possible_attacks = attack_templates.get(chosen_part).values()
            chosen_attack = dict(random.choice(list(possible_attacks)))
            damage = chosen_attack["base_damage"] - target.fighter.defense
            
            # Choose a target body part to strike
            targetable_body_parts = target.body.targetable_body_parts
            target_body_part = random.choice(list(targetable_body_parts))
            if target is engine.player:
                attack_color = color.player_atk
            else:
                attack_color = color.enemy_atk
            if (damage <= 0):
                damage = 1
            attack_name = chosen_attack.get("name")
            attack_desc = f"{attacker.name.capitalize()} attacks {target.name}'s {target_body_part.name} with a {attack_name}, dealing {damage} damage!"
            engine.message_log.add_message(attack_desc, attack_color)
            target_body_part.take_damage(damage)

attack_templates = {
    "arm": {
        "punch": {
            "name": "Punch",
            "base_damage": 5,
            "body_part": "arm"
        }
    }
}