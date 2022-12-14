from __future__ import annotations
from typing import TYPE_CHECKING
import color
from components.base_component import BaseComponent
from render_order import RenderOrder
import exceptions
import random
from combat import Attack
import components.ai
if TYPE_CHECKING:
    from entity import Actor
    from body import BodyPart
    from combat import Attack

class Fighter(BaseComponent):
    parent: Actor
    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp: int = hp
        self._hp: int = hp
        self.base_defense: int = base_defense
        self.base_power: int = base_power
        self.previous_target: Actor = None

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai is not None:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def die(self) -> None:
        print(f"{self.parent.name} has died")
        if self.engine.player is self.parent:
            death_message: str = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die
        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE
        self.engine.message_log.add_message(death_message, death_message_color)
        self.parent.alive = False
        # self.engine.player.level.add_xp(self.parent.level.xp_given)

    def simple_attack(self, target: Actor):
        # If either this character or their target is dead, skip the attack
        if not self.parent.alive or not target.alive:
            return

        # If this in an NPC, ensure their AI is set to combatant
        if self.parent.player_character == False and not isinstance(self.parent.ai, components.ai.Combatant):
            previous_ai = self.parent.ai
            self.parent.ai = components.ai.Combatant(entity=self.parent, target=target, previous_ai=previous_ai)
            print(f"Set {self.parent.name}'s previous AI to {previous_ai}")
        if not isinstance(target.ai, components.ai.Combatant):
            target_previous_ai = target.ai
            target.ai = components.ai.Combatant(entity=target, target=self.parent, previous_ai=target_previous_ai)
            print(f"Set {target.name}'s previous AI to {target_previous_ai}")
        
         # Raise an exception if there's no target
        if not target:
            raise exceptions.Impossible("Nothing to attack.")
        
        # Determine if it's an armed or unarmed attack
        attacker_equipped_weapon = self.parent.equipment.weapon
        if attacker_equipped_weapon is None:
            attack = Attack("uarmed attack", 5)
        else:
            attack = Attack("weapon attack", attacker_equipped_weapon.equippable.power_bonus)
        
        # Start the message 
        msg: str = f"{self.parent.name} attacks {target.name} with {attack.name}! "

        # determine hit
        attacker_fighting: float = self.parent.skills.get("fighting").value
        target_fighting: float = target.skills.get("fighting").value
        hit = True
        # deal damage
        if hit:
            skill_damage_bonus: int = random.randint(0, int(attacker_fighting))
            total_damage: int = attack._damage + skill_damage_bonus + self.parent.equipment.power_bonus
            target.fighter.take_damage(total_damage)
            msg += f"{self.parent.name} deals {total_damage} damage to {target.name}!"
        # At this point, the target may be dead
        print(msg)
        self.engine.message_log.add_message(msg)

        if target.alive == False:
            # If the attacker killed the target, add to their deeds
            self.parent.deeds.characters_murdered = self.parent.deeds.characters_murdered + 1
            if target.evil:
                self.parent.deeds.evil_entities_slain = self.parent.deeds.evil_entities_slain + 1
            print(f"{self.parent.name} reverting to {self.parent.ai.previous_ai}")
            self.parent.ai = self.parent.ai.previous_ai
        
        self.previous_target = target
        self.parent.skills.get("fighting").increase(0.025)


    def attack(self, target: Actor):
        if not self.parent.alive or not target.alive:
            return
        # If this in an NPC, ensure their AI is set to combatant
        if self.parent.player_character == False and not isinstance(self.parent.ai, components.ai.Combatant):
            previous_ai = self.parent.ai
            self.parent.ai = components.ai.Combatant(entity=self.parent, target=target, previous_ai=previous_ai)
            print(f"Set {self.parent.name}'s previous AI to {previous_ai}")
        if not isinstance(target.ai, components.ai.Combatant):
            target_previous_ai = target.ai
            target.ai = components.ai.Combatant(entity=target, target=self.parent, previous_ai=target_previous_ai)
            print(f"Set {target.name}'s previous AI to {target_previous_ai}")

        # Raise an expection for nothing to attack
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        # Get attacker usable body part
        usable_body_parts = self.parent.body.usable_body_parts

        if usable_body_parts.__len__() == 0:
            msg = f"{self.parent.name} tries to attack, but is unable!"
            self.engine.message_log.add_message(msg)

        else:
            attacker_equipped_weapon = self.parent.equipment.weapon
            if attacker_equipped_weapon is not None:
                # Select a weapon attack
                attack: Attack = random.choice(attacker_equipped_weapon.equippable.attacks)
            else:
                attacking_part: BodyPart = random.choice(usable_body_parts)
                attack: Attack = random.choice(attackTypes.get(attacking_part.bodypart_type))

            # choose an enemy's body part
            target_part: BodyPart = random.choice(target.body.targetable_body_parts)
            msg: str = f"{self.parent.name} attacks {target.name}'s {target_part.name} with {attack.name}\n"

            print(msg)
            # determine hit
            attacker_fighting: float = self.parent.skills.get("fighting").value
            target_fighting: float = target.skills.get("fighting").value
            if random.randint(0, int(attacker_fighting)) > random.randint(0, int(target_fighting)):
                # deal damage
                skill_damage_bonus: int = random.randint(0, int(attacker_fighting))
                total_damage: int = attack._damage + skill_damage_bonus + self.parent.equipment.power_bonus
                target_part.take_damage(total_damage)
                # At this point, the target may be dead
                self.engine.message_log.add_message(msg)

                # If the target is dead, 
                if target.alive == False:
                    self.parent.deeds.characters_murdered = self.parent.deeds.characters_murdered + 1
                    if target.evil:
                        self.parent.deeds.evil_entities_slain = self.parent.deeds.evil_entities_slain + 1
                    print(f"{self.parent.name} reverting to {self.parent.ai.previous_ai}")
                    self.parent.ai = self.parent.ai.previous_ai
                
                self.previous_target = target
                self.parent.skills.get("fighting").increase(0.025)
            else:
                msg += f"{self.parent.name} missed!"
                self.engine.message_log.add_message(msg)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value: int = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered: int = new_hp_value - self.hp
        self.hp = new_hp_value
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
