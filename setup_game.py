"""Handle the loading and initialization of game sessions."""
from __future__ import annotations
import copy
import lzma
import pickle
import traceback
from typing import Optional
import tcod
import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers
from time_cycles import TimeCycle
from namegen import NameGenerator
from game_settings import GameConfig
from generators.equipment import generate_pants, generate_jacket, generate_weapon
import random
from entity_factories import create_person
# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game(
    player_first_name,
    player_last_name,
    player_age
) -> Engine:
    """Return a brand new game session as an Engine instance."""
    config = GameConfig.load_config_json()
    map_width = config["game"]["map"]["width"]
    map_height = config["game"]["map"]["height"]

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)
    time_cycle = TimeCycle(
        phase_ticks_dawn = config["game"]["time_cycles"]["phase_ticks_dawn"], 
        phase_ticks_daytime = config["game"]["time_cycles"]["phase_ticks_daytime"], 
        phase_ticks_dusk = config["game"]["time_cycles"]["phase_ticks_dusk"],
        phase_ticks_nighttime = config["game"]["time_cycles"]["phase_ticks_nighttime"]
    )

    engine = Engine(player=player, time_cycle=time_cycle)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Welcome to Nightfall. Do your best to survive.", color.welcome_text
    )
    player.parent = engine.game_map
    # dagger = copy.deepcopy(entity_factories.dagger)
    dagger = generate_weapon()
    # leather_jacket = copy.deepcopy(entity_factories.leather_jacket)
    leather_jacket = generate_jacket()
    # pants = copy.deepcopy(entity_factories.pants)
    pants = copy.deepcopy(generate_pants())


    dagger.parent = player.inventory
    leather_jacket.parent = player.inventory
    pants.parent = player.inventory

    player.inventory.items.append(pants)
    player.equipment.toggle_equip_bp(pants, add_message=False)

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip_bp(dagger, add_message=False)

    player.inventory.items.append(leather_jacket)
    player.equipment.toggle_equip_bp(leather_jacket, add_message=False)

    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    """A handler for the main menu, covering rendering and input."""
    NameGenerator.load_names()
    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        # console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "Nightfall",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Jedai Saboteur",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            # return input_handlers.MainGameEventHandler(new_game())
            return CharacterCreationMenu()

        return None

class CharacterCreationMenu(input_handlers.BaseEventHandler):
    """A handler for the main menu, covering rendering and input."""
    def __init__(self) -> None:
        super().__init__()
        self.player_character =  create_person()
        self.player_character.initialize()
        self.player_gender_options = ["male", "female", "nonbinary", "bigender"]
        self.player_gender = random.choice(self.player_gender_options)
        self.player_age = random.choice(range(18,50))
        if (self.player_gender == "male"):
            player_name_pool = NameGenerator.amab_names
        elif (self.player_gender == "female"):
            player_name_pool = NameGenerator.afab_names
        else:
            player_name_pool = NameGenerator.afab_names + NameGenerator.amab_names
        self.player_first_name = random.choice(player_name_pool)
        self.player_last_name = NameGenerator.get_last_name()
        
    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        # console.draw_semigraphics(background_image, 0, 0)
        console.print_frame(
            x=0,
            y=0,
            width=console.width,
            height=console.height
        )
        y_cursor = 1
        with open("raw/character_creation/intro.txt") as intro_text:
            intro_text_line = intro_text.read()
            intro_height = console.print_box(
                x=1,
                y=y_cursor,
                width=console.width - 1,
                height=5,
                string=intro_text_line
            )
            y_cursor = y_cursor + intro_height + 2


        gender_height = console.print_box(
                x=1,
                y=y_cursor,
                width=console.width - 1,
                height=5,
                string=f"You are {self.player_gender}"
            )
        y_cursor = y_cursor + gender_height + 2

        name_prompt_height = console.print_box(
            x=1,
            y=y_cursor,
            width=console.width - 1,
            height=console.height,
            string=f"Your name is {self.player_character.name}"
        )

        y_cursor = y_cursor + name_prompt_height + 2

        age_height = console.print_box(
            x=1,
            y=y_cursor,
            width=console.width - 1,
            height=console.height,
            string=f"You are {self.player_age} years old"
        )
        y_cursor = y_cursor + name_prompt_height + 2

        continue_height = console.print_box(
            x=1,
            y=y_cursor,
            width=console.width - 1,
            height=console.height,
            string=f"Press c to continue"
        )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(new_game(
                    player_first_name=self.player_first_name,
                    player_last_name=self.player_first_name, 
                    player_age=self.player_age
                    ))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_a:
            return input_handlers.MainGameEventHandler(new_game())

        return None

