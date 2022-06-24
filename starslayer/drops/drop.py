"""
Generic Drop Module.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

from ..utils import Chronometer, HitBox

if TYPE_CHECKING:
    from ..state import Game
    from ..utils import BoundingShape

DropsList = List["Drop"]


class Drop(HitBox, ABC):
    """
    Abstract class for defining a loot drop.
    """

    @classmethod
    def from_shape(cls,
                   shape: "BoundingShape",
                   *,
                   width: float=30.0,
                   height: float=30.0) -> "Drop":
        """
        Creates a drop from the coordinates of a shape.
        """

        shp_x, shp_y = shape.center
        diff_w = width / 2
        diff_h = height / 2

        return cls(x1=shp_x - diff_w,
                   y1=shp_y - diff_h,
                   x2=shp_x + diff_w,
                   y2=shp_y + diff_h,
                   **shape.properties)


    # pylint: disable=invalid-name
    def __init__(self,
                 *,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 texture_path: Optional[str]=None,
                 accel: float=0.0,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Drop'.
        """

        super().__init__(x1=x1,
                         y1=y1,
                         x2=x2,
                         y2=y2,
                         texture_path=texture_path,
                         can_spawn_outside=True,
                         **kwargs)

        self.accel: float = accel
        self.chrono: Chronometer = Chronometer()


    @abstractmethod
    def trajectory(self) -> None:
        """
        Moves the drop.
        """

        raise NotImplementedError


    @abstractmethod
    def effect(self, game: "Game") -> None:
        """
        Defines the effect of the drop on the game
        if ti collides with something.
        """

        raise NotImplementedError
