from __future__ import annotations
from enum import Enum
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor

class BuildingType(Enum):
    HOUSE = 0

class Building:
    def __init__(
            self, 
            x: int, 
            y: int, 
            building_schematic: list[str], 
            owner: Optional[Actor]=None,
            building_type: BuildingType=BuildingType.HOUSE
        ):
        self.height = building_schematic.__len__()
        self.width = building_schematic[0].__len__()
        self.x = x
        self.y = y
        self.x2 = x + self.width
        self.y2 = y + self.height
        self.schematic = building_schematic
        # owners are set at spawn time
        self.owner = owner
        self.building_type = building_type
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x + self.x2) / 2)
        center_y = int((self.y + self.y2) / 2)

        return center_x, center_y
    def intersects(self, other: Building) -> bool:
        """Return True if this Building overlaps with another Building."""
        return (
            self.x <= other.x2
            and self.x2 >= other.x
            and self.y <= other.y2
            and self.y2 >= other.y
        )