from __future__ import annotations
from enum import Enum
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor
    from building import Building


class Plot:
    """Represents a plot of land"""
    def __init__(
            self, 
            x: int, 
            y: int, 
            width: int,
            height: int,
            building: Optional[Building]=None, 
            owner: Optional[Actor]=None,
        ):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.x2 = x + self.width
        self.y2 = y + self.height
        self.building:Building=building
        # owners are set at spawn time
        self.owner = owner
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x + self.x2) / 2)
        center_y = int((self.y + self.y2) / 2)

        return center_x, center_y
    def intersects(self, other: Plot) -> bool:
        """Return True if this Plot overlaps with another Plot."""
        return (
            self.x <= other.x2
            and self.x2 >= other.x
            and self.y <= other.y2
            and self.y2 >= other.y
        )
    def set_building(self, building: Building):
        self.building = building