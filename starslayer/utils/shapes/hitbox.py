"""
Generic Module for storing base HitBox class.
"""

from typing import TYPE_CHECKING, Optional

from ...auxiliar import is_out_bounds_aux
from .bounding_shape import BoundingShape, FloatTuple2, FloatTuple4

if TYPE_CHECKING:
    from .hitcircle import HitCircle


class HitBox(BoundingShape):
    """
    Generic class for defining a bounding box.

    This is a basic class that is not used by itself.
    It serves as superclass of many others.
    """

    # pylint: disable=invalid-name
    def __init__(self,
                 *,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 texture_path: Optional[str]=None,
                 can_spawn_outside: bool=False,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'HitBox'.

        It should always be true that 'x1 <= x2 && y1 <= y2'. If
        it is not the case, those variables are inverted.
        """

        if x1 > x2:
            x1, x2 = x2, x1

        if y1 > y2:
            y1, y2 = y2, y1

        if (not can_spawn_outside
            and is_out_bounds_aux(x1, y1, x2, y2)):
            raise ValueError(f"Coordinates {x1, y1}, {x2, y2} are not " +
                             "valid, as they are outside of the boundaries of the screen")

        super().__init__(texture_path=texture_path,
                         **kwargs)

        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2


    def __eq__(self, other: "HitBox") -> bool:
        """
        Tests if all cordinates are the same.
        """

        return all((self.x1 == other.x1,
                    self.y1 == other.y1,
                    self.x2 == other.x2,
                    self.y2 == other.y2))


    @property
    def all_coords(self) -> FloatTuple4:
        """
        Returns a tuple with all the coordiantes of its hitbox.
        """

        return self.x1, self.y1, self.x2, self.y2


    @property
    def upper_left(self) -> FloatTuple2:
        """
        Returns the UPPER LEFT coordinates of its hitbox.
        """

        return self.x1, self.y1


    @property
    def upper_right(self) -> FloatTuple2:
        """
        Returns the UPPER RIGHT coordinates of its hitbox.
        """

        return self.x1, self.y1


    @property
    def bottom_left(self) -> FloatTuple2:
        """
        Returns the BOTTOM LEFT coordinates of its hitbox.
        """

        return self.x1, self.y2


    @property
    def bottom_right(self) -> FloatTuple2:
        """
        Returns the BOTTOM RIGHT coordinates of its hitbox.
        """

        return self.x2, self.y2


    @property
    def center(self) -> FloatTuple2:
        """
        Return the CENTER coordinates of its hitbox.
        """

        return ((self.x2 + self.x1) / 2), ((self.y2 + self.y1) / 2)


    @property
    def width(self) -> int:
        """
        Returns the WIDTH of its hitbox.
        """

        return self.x2 - self.x1


    @property
    def height(self) -> int:
        """
        Returns the HEIGHT of its hitbox.
        """

        return self.y2 - self.y1


    def is_over(self, line: float) -> bool:
        """
        Tests if the box is over a line.
        """

        return self.y2 < line


    def is_left_of(self, line: float) -> bool:
        """
        Tests if the box is left of a line.
        """

        return self.x2 < line


    def is_right_of(self, line: float) -> bool:
        """
        Tests if the box is right of a line.
        """

        return self.x1 > line


    def is_below(self, line: float) -> bool:
        """
        Tests if the box is below a line.
        """

        return self.y1 > line


    def collides_with_box(self, other_box: "HitBox") -> bool:
        """
        Tests if the hitbox is colliding with another given one.
        """

        return all((self.x2 >= other_box.x1,
                    self.x1 <= other_box.x2,
                    self.y2 >= other_box.y1,
                    self.y1 <= other_box.y2))


    def collides_with_circle(self, other_circle: "HitCircle") -> bool:
        """
        Tests if the hitbox is colliding with a HitCircle.
        """

        return other_circle.collides_with_box(self)


    def transfer(self, dx: float, dy: float) -> None:
        """
        Changes hitbox coordinates from '(x1, y1), (x2, y2)' to
        '(x1 + dx, y1 + dy), (x2 + dx, y2 + dy)'.
        """

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy


    def transfer_to(self, x: float, y: float) -> None:
        """
        Changes hitbox coordinates from '(x1, y1), (x2, y2)' to
        '(x - width / 2, y - height / 2), (x + width / 2, y + height / 2)'.
        """

        w_aux = self.width / 2
        h_aux = self.height / 2

        self.x1 = x - w_aux
        self.y1 = y - h_aux
        self.x2 = x + w_aux
        self.y2 = y + h_aux


    def move(self, dx: float, dy: float, freely: bool=False) -> bool:
        """
        Moves the hitbox around inside the boundaries of the screen.

        Returns 'False' if the atempted move is invalid, or 'True' if it is
        valid. Either way, invalid moves are ignored.
        """

        if not freely and is_out_bounds_aux(self.x1 + dx,
                                            self.y1 + dy,
                                            self.x2 + dx,
                                            self.y2 + dy):
            return False

        self.transfer(dx, dy)
        return True


    def move_rad(self, drad: float, dtheta: float, freely: bool=False) -> None:
        """
        Moves the hitbox around inside the boundaries of the screen,
        in a radial movement.

        Returns 'False' if the atempted move is invalid, or 'True' if it is
        valid. Either way, invalid moves are ignored.
        """

        dx, dy = self.dpolar_to_dcart(drad, dtheta)

        if not freely and is_out_bounds_aux(self.x1 + dx,
                                            self.y1 + dy,
                                            self.x2 + dx,
                                            self.y2 + dy):
            return False

        self.transfer_rad(drad, dtheta)
        return True
