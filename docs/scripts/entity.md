entity.py

- [Classes](#classes)
  - [Entity()](#entity)
    - [Class Fields](#class-fields)
      - [entity.parent: Union[GameMap, Inventory]](#entityparent-uniongamemap-inventory)
    - [Instance Fields](#instance-fields)
      - [entity.x: int](#entityx-int)
      - [entity.y: int](#entityy-int)
      - [entity.char: str](#entitychar-str)
      - [entity.color: Tuple[int, int, int]](#entitycolor-tupleint-int-int)
      - [entity.name: str](#entityname-str)
      - [entity.blocks_movement: bool](#entityblocks_movement-bool)
      - [entity.render_order: RenderOrder](#entityrender_order-renderorder)
    - [Properties](#properties)
      - [entity.gameMap](#entitygamemap)
    - [Class Methods](#class-methods)
      - [entity.spawn(self: T, gamemap: GameMap, x: int, y: int) -> T](#entityspawnself-t-gamemap-gamemap-x-int-y-int---t)
      - [entity.place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> float](#entityplaceself-x-int-y-int-gamemap-optionalgamemap--none---float)
      - [entity.distance(self, x: int, y: int) -> float](#entitydistanceself-x-int-y-int---float)
      - [entity.move(self, dx: int, dy: int) -> None](#entitymoveself-dx-int-dy-int---none)
  - [Actor(Entity)](#actorentity)
    - [\_\_init__ params](#__init__-params)
      - [x: int](#x-int)
      - [y: int](#y-int)
      - [char: str](#char-str)
      - [color:](#color)
      - [name: str](#name-str)
      - [blocks_movement: str](#blocks_movement-str)
  - [Instance Vars](#instance-vars)

## Classes

### Entity()

#### Class Fields

#####  entity.parent: Union[GameMap, Inventory]

Parent may be provided after the entity is created.

#### Instance Fields

##### entity.x: int

The entity's x position on the current map.

##### entity.y: int

The entity's y position on the current map.

##### entity.char: str

The character that represents the entity.

##### entity.color: Tuple[int, int, int] 

The entity's default color.

##### entity.name: str

The name of the entity. This is displayed in the game.

##### entity.blocks_movement: bool

Whether or not the entity prevents movement through it

##### entity.render_order: RenderOrder

The z-order of this entity on the map. 

#### Properties

##### entity.gameMap

A reference to the current game map.

#### Class Methods

##### entity.spawn(self: T, gamemap: GameMap, x: int, y: int) -> T

Spawn a copy of the entity's instance at the given location.

##### entity.place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> float

Place the entity at a new location.  Handles moving across GameMaps.

##### entity.distance(self, x: int, y: int) -> float

Return the distance between the current entity and the given (x, y) coordinate.

##### entity.move(self, dx: int, dy: int) -> None

Moves the entity by a given amount by the next frame

### Actor(Entity)
```
__init__(
    self,
    *,
    x: int = 0,
    y: int = 0,
    char: str = "?",
    color: Tuple[int, int, int] = (255, 255, 255),
    name: str = "<Unnamed>",
    ai_cls: Type[BaseAI],
    equipment: Equipment,
    fighter: Fighter,
    inventory: Inventory,
    level: Level,
    body: Body,
    base_fov: int = 8
)
```

#### \_\_init__ params

##### x: int

See [x: int](#x-int)

##### y: int

See [y: int](#y-int)

##### char: str

See [char: str](#char-str)

##### color: 

see [color: int](#color-tupleint-int-int)

##### name: str

See [name: str](#name-str)

##### blocks_movement: str

See [name: str](#blocks-movement)

### Instance Vars

base_fov

ai: Optional[BaseAI

equipment: Equipment
equipment.parent

fighter: Fighter
fighter.parent

inventory: Inventory
inventory.parent

level: Level
level.parent

body: Body
body.parent