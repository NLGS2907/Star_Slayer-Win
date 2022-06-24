"""
Coords traveler Animation Module.
"""

from math import sqrt
from typing import List, Tuple

from ...consts import HEIGHT, WIDTH
from ...gamelib import draw_oval
from .animation import Animation

DotsList = List[Tuple[Tuple[float, float], int]]


# pylint: disable=invalid-name
class CoordsTraveler(Animation):
    """
    Animation for a dot traveling of given coordinates.
    """

    def __init__(self,
                 coords_pairs: Tuple[float, ...],
                 *,
                 unhinged: bool=True,
                 max_x1: float=0.0,
                 max_y1: float=0.0,
                 max_x2: float=WIDTH,
                 max_y2: float=HEIGHT,
                 dot_density: int=1,
                 dot_radius: float=5.0,
                 dot_speed: float=1.0,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'CoordsTraveler'.
        """

        super().__init__(max_x1, max_y1, max_x2, max_y2, **kwargs)
        self.unhinged: bool = unhinged
        self._check_coord_pairs(coords_pairs)

        self.coords_pairs: Tuple[float, ...] = self.split_in_pairs(coords_pairs)
        self.dot_density: float = dot_density
        self.dot_radius: float = dot_radius
        self.dot_speed: float = abs(dot_speed)
        self.dots: DotsList = self.generate_dots()


    def generate_dots(self) -> DotsList:
        """
        Generates the dots and their coordinates.
        """

        dots = []

        for _ in range(self.dot_density):
            dots.append((self.coords_pairs[0], 0))
            dots = self.process_dots_movement(dots, 10)

        return dots


    def split_in_pairs(self, coords_tuple: Tuple[float, ...]) -> Tuple[Tuple[float, float], ...]:
        """
        Splits a coords tuple into pairs.
        """

        return tuple(coords_tuple[i: i + 2]
                     for i in range(0, len(coords_tuple), 2))


    def _check_coord_pairs(self, coord_pairs: Tuple[float, ...]) -> None:
        """
        Checks if the coordinates are in a valid format.
        """

        if len(coord_pairs) % 2 != 0:
            raise ValueError("The coordinates must come in pairs.")

        if self.unhinged:
            return

        for coord_x, coord_y in self.split_in_pairs(coord_pairs):

            if self.x1 < coord_x < self.x2:
                raise ValueError(f"Value {coord_x} is outside of the boundaries of the screen.")

            if self.y1 < coord_y < self.y2:
                raise ValueError(f"Value {coord_y} is outside of the boundaries of the screen.")


    @property
    def space_between_dots(self) -> float:
        """
        Returns the space between dots.
        """

        return self.perimeter() / self.dot_density


    def distance_between(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Returns the distance between (x1, y1) and (x2, y2).
        """

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def perimeter(self) -> float:
        """
        Returns the total perimeter between all coordinates pairs.
        """

        perimeter = 0.0

        for i, _ in enumerate(self.coords_pairs):
            (x1, y1), (x2, y2) = self.coords_pairs[i], self.coords_pairs[self.next_index(i)]
            perimeter += self.distance_between(x1, y1, x2, y2)

        return perimeter


    def next_index(self, cur_index: int) -> int:
        """
        Changes the coords index for the next one.
        It also returns said new index.
        """

        return (cur_index + 1) % len(self.coords_pairs)


    def process_dots_movement(self,
                              dots_list: DotsList,
                              speed_cons: float=100.0) -> DotsList:
        """
        Processes all the dots movements.
        """

        new_dots = []

        for (dot_x, dot_y), cur_index in dots_list:
            x1, y1 = self.coords_pairs[cur_index]
            x2, y2 = self.coords_pairs[self.next_index(cur_index)]
            dx = ((x2 - x1) / speed_cons) * self.dot_speed
            dy = ((y2 - y1) / speed_cons) * self.dot_speed

            next_index = cur_index
            new_x = dot_x + dx
            new_y = dot_y + dy

            if all((round(new_x) == round(x2),
                    round(new_y) == round(y2))):
                next_index = self.next_index(cur_index)

            new_dots.append(((new_x, new_y), next_index))

        return new_dots


    def animate(self, **_kwargs) -> None:
        """
        Proceeds with the animation.
        """

        for (dot_x, dot_y), _ in self.dots:
            draw_oval(x1=dot_x - self.dot_radius,
                      y1=dot_y - self.dot_radius,
                      x2=dot_x + self.dot_radius,
                      y2=dot_y + self.dot_radius,
                      **self.properties)


    def post_hook(self, **_kwargs) -> None:
        """
        Moves each dot into its next coords.
        """

        self.dots = self.process_dots_movement(self.dots)
