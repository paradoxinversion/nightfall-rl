import random
from entity import Item
from components.equippable import Equippable, EquipmentType, EquippableType
from components.body import BodyPartTypes

clothing_colors = ["Black", "Gray", "Red", "Green", "Blue"]

def generate_pants():
    color = random.choice(clothing_colors)
    generated_equippable=Equippable(
        equippable_type=EquippableType.WORN_ARTICLE,
        equipment_type=EquipmentType.CLOTHES,
        power_bonus=2,
        body_slots=[BodyPartTypes.LEG]
    )

    pants = Item(
        char="[",
        color=(139, 69, 19),
        name=f"{color} Pants",
        equippable=generated_equippable
    )
    return pants

def generate_jacket():
    color = random.choice(clothing_colors)
    generated_equippable=Equippable(
        equippable_type=EquippableType.WORN_ARTICLE,
        equipment_type=EquipmentType.CLOTHES,
        power_bonus=2,
        body_slots=[BodyPartTypes.ARM, BodyPartTypes.TORSO]
    )

    jacket = Item(
        char="[",
        color=(139, 69, 19),
        name=f"{color} Jacket",
        equippable=generated_equippable,
    )
    return jacket

def generate_weapon():
    generated_equippable=Equippable(
        equippable_type=EquippableType.HELD_OBJECT,
        equipment_type=EquipmentType.WEAPON,
        power_bonus=15,
        body_slots=[BodyPartTypes.ARM]
    )
    weapon = Item(
        char="/", 
        color=(0, 191, 255), 
        name="Knife", 
        equippable=generated_equippable
    )
    return weapon