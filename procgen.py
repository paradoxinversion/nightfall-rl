from __future__ import annotations
import copy
import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING, Optional
import tcod
import entity_factories
from game_map import GameMap
import tile_types
from entity import Actor
from building import Building, BuildingType
from generators.equipment import generate_pants
from plot import Plot
if TYPE_CHECKING:
   from engine import Engine
   from entity import Entity, Actor

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.pants, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 80)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}

actor_type_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.person, 80)]
}

house = [
    "#####",
    "#...#",
    "#...#",
    "#...#",
    "###D#"
]

big_house = [
    "########",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "###D####"
]

odd_house = [
    '####D###....',
    '#......#....',
    '#......#....',
    '#......#####',
    '#..........#',
    '#..........#',
    '#..........#',
    '#......#####',
    '#......#....',
    '#......#....',
    '########....'
]

building_schematics = [house, big_house, odd_house]

building_plot_size = 10

def get_max_value_for_floor(
    max_value_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

class Area:
    def __init__(self, width: int, height: int, game_map: GameMap):
        self._game_map: GameMap = game_map
        self._width = width
        self._height = height
        self.buildings: List[Building] = []
        self.plots: List[Plot] = []

    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(0, self._width), slice(0, self._height)

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int(self._width / 2)
        center_y = int(self._height / 2)

        return center_x, center_y

def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )
    # for entity in monsters + items:
    for entity in items:
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x, y)

def place_actors(area: Area) -> None:
    # get houses
    for plot in area.plots:
        building = plot.building
        if building.building_type == BuildingType.HOUSE:
            # Spawn entity here
            actor: Entity = entity_factories.person
            x,y = building.center
            actor.spawn(area._game_map, x, y, [generate_pants()])
            actor.owned_building = building
def place_entities_area(area_map: GameMap) -> None:
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, 1)
    )
    actors: List[Entity] = get_entities_at_random(
        actor_type_chances, 3, 0
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, 1
    )
    for entity in items + actors:
            x = random.randint(0, area_map.width - 1)
            y = random.randint(0, area_map.height - 1)
            if isinstance(entity, Actor):
                entity.spawn(area_map, x, y, [entity_factories.pants])
            else:
                if not any(entity.x == x and entity.y == y for entity in area_map.entities):
                    entity.spawn(area_map, x, y)
                
def tunnel_between(
  start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
  """Return an L-shaped tunnel between these two points."""
  x1, y1 = start
  x2, y2 = end
  if random.random() < 0.5:  # 50% chance.
      # Move horizontally, then vertically.
      corner_x, corner_y = x2, y1
  else:
      # Move vertically, then horizontally.
      corner_x, corner_y = x1, y2

  # Generate the coordinates for this tunnel.
  for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
      yield x, y
  for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
      yield x, y

def generate_dungeon(
   max_rooms: int,
   room_min_size: int,
   room_max_size: int,
   map_width: int,
   map_height: int,
   engine: Engine,
) -> GameMap:
  """Generate a new dungeon map."""
  player = engine.player
  dungeon = GameMap(engine, map_width, map_height, entities=[player])

  rooms: List[RectangularRoom] = []
  center_of_last_room = (0, 0)

  for r in range(max_rooms):
      room_width = random.randint(room_min_size, room_max_size)
      room_height = random.randint(room_min_size, room_max_size)

      x = random.randint(0, dungeon.width - room_width - 1)
      y = random.randint(0, dungeon.height - room_height - 1)

      # "RectangularRoom" class makes rectangles easier to work with
      new_room = RectangularRoom(x, y, room_width, room_height)

      # Run through the other rooms and see if they intersect with this one.
      if any(new_room.intersects(other_room) for other_room in rooms):
          continue  # This room intersects, so go to the next attempt.
      # If there are no intersections then the room is valid.

      # Dig out this rooms inner area.
      dungeon.tiles[new_room.inner] = tile_types.floor

      if len(rooms) == 0:
          # The first room, where the player starts.
          player.place(*new_room.center, dungeon)
      else:  # All rooms after the first.
          # Dig out a tunnel between this room and the previous one.
          for x, y in tunnel_between(rooms[-1].center, new_room.center):
              dungeon.tiles[x, y] = tile_types.floor
          center_of_last_room = new_room.center
      place_entities(new_room, dungeon, engine.game_world.current_floor)
      dungeon.tiles[center_of_last_room] = tile_types.down_stairs
      dungeon.downstairs_location = center_of_last_room
      # Finally, append the new room to the list.
      rooms.append(new_room)

  return dungeon

def _generate_area_map(
   map_width: int,
   map_height: int,
   engine: Engine,
#    max_buildings: int
) -> GameMap:
    """Generate a new area map."""
    player = engine.player
    area = GameMap(engine, map_width, map_height, entities=[player])
    new_area = Area(map_width, map_height)
    area.tiles[new_area.inner()] = tile_types.floor
    buildings: List[Building] = []

    max_buildings = 10
    player.place(5, 5, area)


    for b in range(max_buildings):
        schematic = random.choice(list(building_schematics))
        schematic_h = len(schematic)
        schematic_w = len(schematic[0])
        x = random.randint(0, area.width - schematic_w - 5)
        y = random.randint(0, area.height - schematic_h - 5)
        new_building = Building(x, y, schematic)
        placement_attempts = 0
        # FIXME: Buildings that can't be placed are put into `buildings`, prevent that
        while placement_attempts < 10:
            placement_attempts += 1
            if any(new_building.intersects(other_room) for other_room in buildings):
                continue
            for by in range(schematic_h):
                for bx in range(schematic_w):
                    if new_building.schematic[by][bx] == "#":
                        area.tiles[bx + x][y + by] = tile_types.wall
                    if new_building.schematic[by][bx] == "D":
                        door = copy.deepcopy(entity_factories.door)
                        door_x = x+bx
                        door_y = y+by
                        door.spawn(area, door_x, door_y)
                        area.tiles["transparent"][door_x][door_y] = False
            buildings.append(new_building)
            break

    print(f"Created {len(buildings)} buildings")
    area.buildings = buildings
    place_actors(area)
    return area

def generate_area_map(
   map_width: int,
   map_height: int,
   engine: Engine,
#    max_buildings: int
) -> GameMap:
    """Generate a new area map."""
    player = engine.player
    area_map = GameMap(engine, map_width, map_height, entities=[player])
    new_area = Area(map_width, map_height, area_map)
    area_map.tiles[new_area.inner()] = tile_types.floor
    buildings: List[Building] = []
    plots: List[Plot] = []
    # Player Placement
    player.place(5, 5, area_map)

    # each building is on a plot that has a square size
    standard_plot = 12 #for now, every plot is this size

    horizontal_plots = int(map_width  / (standard_plot + 1) )
    vertical_plots = int(map_height / (standard_plot + 1))

    # Set our starting point
    plot_start_x = 2
    plot_start_y = 2

    # Create vertical and horizontal plots
    # There should be 1 tile of space between each plot
    for vp in range(vertical_plots):
        for hp in range(horizontal_plots):
            # Set this plot's top-right corner
            x = plot_start_x
            y = plot_start_y

            print (f"Creating a new plot at {x} {y}")
            # Create the plot object
            newPlot = Plot(x,y,standard_plot, standard_plot)
           
            # Fill in the plot with grass tiles
            # Mostly for debug purposes
            # for by in range(standard_plot):
            #         for bx in range(standard_plot):
            #             area.tiles[bx + x][y + by] = tile_types.grass
            
            # -- Create a building originating at the top-right of this plot
            # Select the schematic, capture width and height
            schematic = random.choice(list(building_schematics))
            schematic_h = len(schematic)
            schematic_w = len(schematic[0])

            # Set the building's origin to the plot's top-right corner
            building_origin_x = plot_start_x
            building_origin_y = plot_start_y

            # Create a new building object at this origin
            new_building = Building(building_origin_x, building_origin_y, schematic)
            newPlot.set_building(new_building)
            for by in range(schematic_h):
                for bx in range(schematic_w):
                    if new_building.schematic[by][bx] == "#":
                        area_map.tiles[bx + building_origin_x][building_origin_y + by] = tile_types.wall
                    if new_building.schematic[by][bx] == "D":
                        door = copy.deepcopy(entity_factories.door)
                        door_x = building_origin_x+bx
                        door_y = building_origin_y+by
                        door.spawn(area_map, door_x, door_y)
                        area_map.tiles["transparent"][door_x][door_y] = False
            buildings.append(new_building)
            plots.append(newPlot)
            plot_start_x = 1 + ((standard_plot + 1) * hp + 1 )
            plot_start_y = 1 + ((standard_plot + 1) * vp + 1)


        
                    
    print(f"Created {len(buildings)} buildings")
    # This should be removed
    area_map.buildings = buildings
    new_area.buildings = buildings
    new_area.plots = plots
    new_area._game_map = area_map
    place_actors(new_area)
    return area_map