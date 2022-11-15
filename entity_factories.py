from typing import TYPE_CHECKING

from components.ai import HostileEnemy, NPC
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.body import Body
from entity import Actor, Item
from components.skills import Skill
import generators.equipment
import random
if TYPE_CHECKING:
   from entity import Actor
   from engine import Engine
   
def create_person(
    first_name = None,
    last_name = None,
    age = None,
    color = (255, 255, 255)
) -> Actor:
    person = Actor(
        char="@",
        color=color,
        ai_cls=NPC,
        equipment=Equipment(),
        fighter=Fighter(hp=30, base_defense=1, base_power=2),
        inventory=Inventory(capacity=26),
        level=Level(level_up_base=200),
        body=Body(race="human")
    )
    person.initialize(first_name, last_name, age)
    skills = {
        "fighting": Skill(person, "fighting", random.randint(10,20))
    }
    person.skills = skills

    jacket = generators.equipment.generate_jacket()
    person.inventory.add(jacket)
    person.equipment.equip(jacket, True)

    pants = generators.equipment.generate_pants()
    person.inventory.add(pants)
    person.equipment.equip(pants, True)

    return person

player = Actor(
    char="@",
    color=(255, 255, 255),
    ai_cls=NPC,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    body=Body(race="human")
)

person = Actor(
    char="@",
    color=(63, 127, 63),
    ai_cls=NPC,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    body=Body(race="human")
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    body=Body(race="orc")
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    body=Body(race="troll")
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_jacket = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Jacket",
    equippable=equippable.Jacket(),
)

pants = Item(
    char="$", color=(139, 69, 19), name="Ragged Pants", equippable=equippable.Pants()
)

door = Item (
    char="#", name='Door', blocks_movement=True, color=(139, 69, 19)
)