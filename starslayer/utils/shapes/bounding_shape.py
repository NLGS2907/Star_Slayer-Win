"""
Generic Module for defining an abstract class
for a bounding shape.
"""

from abc import ABC, abstractmethod
from math import atan2, cos, sin, sqrt
from typing import TYPE_CHECKING, Literal, Optional, Tuple

from ...sprites import Sprite

if TYPE_CHECKING:
    from .hitbox import HitBox
    from .hitcircle import HitCircle

FloatTuple4 = Tuple[float, float, float, float]
FloatTuple2 = Tuple[float, float]


# pylint: disable=invalid-name
class BoundingShape(ABC):
    """
    Generic class for a bounding polygon.
    """

    def __init__(self,
                *,
                 texture_path: Optional[str]=None,
                **kwargs) -> None:
        """
        Saves the properties of the shape.

        `texture_path` is the sprite's path, and must be a path
                      relative to the 'textures' package.
        """

        self.sprite_path: Optional[str] = texture_path
        self.sprite: Optional[Sprite] = (Sprite(self.sprite_path) if self.sprite_path else None)

        self.properties = kwargs


    @abstractmethod
    def __eq__(self, other: "BoundingShape") -> bool:
        """
        Tests if all coordinates are the same.
        """

        raise NotImplementedError


    @property
    @abstractmethod
    def all_coords(self) -> FloatTuple2 | FloatTuple4:
        """
        Returns a tuple with all the coordiantes of its shape.
        """

        raise NotImplementedError


    @property
    @abstractmethod
    def center(self) -> FloatTuple2:
        """
        Return the CENTER coordinates of its shape.
        """

        raise NotImplementedError


    def polar_to_cart(self, rad: float, theta: float) -> FloatTuple2:
        """
        Converts from polar coordinates to cartesian ones.

        `theta` must be in radians.
        """

        return (rad * cos(theta),
                rad * sin(theta))


    # pylint: disable=invalid-name
    def cart_to_polar(self, x: float, y: float) -> FloatTuple2:
        """
        Converts from cartesian coordinates to polar ones.
        """

        return (sqrt(x ** 2 + y ** 2),
                atan2(y, x))


    @abstractmethod
    def is_over(self, line: float) -> bool:
        """
        Tests if the shape is over a line.
        """

        raise NotImplementedError


    @abstractmethod
    def is_left_of(self, line: float) -> bool:
        """
        Tests if the shape is left of a line.
        """

        raise NotImplementedError


    @abstractmethod
    def is_right_of(self, line: float) -> bool:
        """
        Tests if the shape is right of a line.
        """

        raise NotImplementedError


    @abstractmethod
    def is_below(self, line: float) -> bool:
        """
        Tests if the shape is below a line.
        """

        raise NotImplementedError


    def distance_to(self, other: "BoundingShape") -> float:
        """
        Returns the distance between centers of this shape
        and another one.
        """

        cx, cy = self.center
        other_x, other_y = other.center

        return sqrt((cx - other_x) ** 2 + (cy - other_y) ** 2)


    def angle_towards(self, other: "BoundingShape") -> float:
        """
        Calculates the direction in which the center of the
        other shape is, and returns the angle.
        """

        cx, cy = self.center
        other_x, other_y = other.center

        return atan2(-(other_y - cy), (other_x - cx))


    def dpolar_to_dcart(self, drad: float, dtheta: float) -> None:
        """
        Changes shape coordinates in a radial movement.
        """

        # because the Y axis grows positive downwards, theta positive is clockwise,
        # we want it to be anti-clockwise
        dtheta = -dtheta
        dcx, dcy = self.polar_to_cart(drad, dtheta)

        return dcx, dcy


    @abstractmethod
    def collides_with_box(self, other_box: "HitBox") -> bool:
        """
        Tests if the shape is colliding with another given one.
        """

        raise NotImplementedError


    @abstractmethod
    def collides_with_circle(self, other_circle: "HitCircle") -> bool:
        """
        Tests if the shape is colliding with a HitCircle.
        """

        raise NotImplementedError


    @abstractmethod
    def transfer(self, dx: float, dy: float) -> None:
        """
        Changes shape coordinates.
        """

        raise NotImplementedError


    @abstractmethod
    def transfer_to(self, x: float, y: float) -> None:
        """
        Changes shape coordinates to a given ones.
        """

        raise NotImplementedError


    def transfer_rad(self, drad: float, dtheta: float) -> None:
        """
        Changes shape coordinates in a radial movement.
        """

        dx, dy = self.dpolar_to_dcart(drad, dtheta)
        self.transfer(dx, dy)


    def transfer_orbit(self,
                       orbit_center_x: float,
                       orbit_center_y: float,
                       radius: float,
                       theta: float) -> None:
        """
        Transfers the shape to a position within the orbit of
        the orbit center.
        """

        new_cx, new_cy = self.polar_to_cart(radius, theta)
        self.transfer_to(orbit_center_x + new_cx,
                         orbit_center_y + new_cy)


    @abstractmethod
    def move(self, dx: float, dy: float, freely: bool=False) -> bool:
        """
        Moves the shape around inside the boundaries of the screen.

        Returns 'False' if the atempted move is invalid, or 'True' if it is
        valid. Either way, invalid moves are ignored.
        """

        raise NotImplementedError


    @abstractmethod
    def move_rad(self, drad: float, dtheta: float, freely: bool=False) -> None:
        """
        Moves the shape around inside the boundaries of the screen,
        in a radial movement.

        Returns 'False' if the atempted move is invalid, or 'True' if it is
        valid. Either way, invalid moves are ignored.
        """

        raise NotImplementedError


    def move_orbit(self,
                   orbit_center: "BoundingShape" | FloatTuple2,
                   theta: float,
                   radius: Optional[float]=None) -> Literal[True]:
        """
        Moves the shape in a radial movement, with another shape as its orbit center.

        It is always a free movement, therefore it should always return `True`.
        """

        o_x, o_y = (orbit_center.center
                    if isinstance(orbit_center, BoundingShape)
                    else orbit_center)
        radius_used = radius or self.distance_to(orbit_center)
        self.transfer_orbit(o_x, o_y, radius_used, -theta)

        return True
