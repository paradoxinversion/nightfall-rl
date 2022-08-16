entity.py



## Classes

### Entity()

#### Class Fields

#####  parent: Union[GameMap, Inventory]

Parent may be provided after the entity is created.

#### Instance Fields

##### x: int

The entity's x position on the current map.

##### y: int

The entity's y position on the current map.

##### char: str

The character that represents the entity.

##### color: Tuple[int, int, int] 

The entity's default color.

##### name: str

The name of the entity. This is displayed in the game.

##### blocks_movement: bool

Whether or not the entity prevents movement through it

##### render_order: RenderOrder

The z-order of this entity on the map. 

#### Properties

##### gameMap

A reference to the current game map.

#### Class Methods

##### spawn(self: T, gamemap: GameMap, x: int, y: int) -> T

Spawn a copy of the entity's instance at the given location.

##### place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> float

Place the entity at a new location.  Handles moving across GameMaps.

##### distance(self, x: int, y: int) -> float

Return the distance between the current entity and the given (x, y) coordinate.

##### move(self, dx: int, dy: int) -> None

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

The entity's initial x position

##### y: int

The entity's initial y position

##### char: str

The entity's representative character

##### color: 

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