"""
Circumference Animation Module.
"""

from math import cos
from math import pi as PI
from math import sin
from typing import List, Optional, Tuple

from ...gamelib import draw_oval
from ...utils import SpringTimer
from .animation import Animation


class Circumference(Animation):
    """
    Animation for a circular trajectory.
    """

    def __init__(self,
                 cx: float,
                 cy: float,
                 *,
                 initial_radius: float=50.0,
                 initial_angle: float=0.0,
                 max_radius: Optional[float]=None,
                 dot_density: int=1,
                 dot_radius: float=5.0,
                 dot_speed: float=0.05,
                 variance_speed: float=1.0,
                 from_top: bool=False,
                 from_bottom: bool=False,
                 **kwargs) -> None:
        """
        Initializes an instance of types 'Circumference'.
        """

        super().__init__(cx - initial_radius,
                         cy - initial_radius,
                         cx + initial_radius,
                         cy + initial_radius,
                         is_text=False,
                         **kwargs)
        self.dot_coords: List[Tuple[float, float]] = [] # polar coordinates, mind you
        self.radius: float = initial_radius
        self.initial_angle: float = self._degrees_to_radians(initial_angle)
        self.max_radius: float = None
        if max_radius is not None and max_radius >= self.radius:
            self.max_radius = 2 * self.radius

        self.dot_density: int = dot_density
        self.dot_raidus: float = dot_radius
        self.dot_speed: float = abs(dot_speed)
        self.where_to_start: float = 0.0

        if from_top:
            self.where_to_start = self.radius_distance

        elif from_bottom:
            self.where_to_start = -self.radius_distance

        self.radius_timer: Optional[SpringTimer] = (None
                                                    if self.max_radius is None
                                                else SpringTimer(-self.radius_distance,
                                                                 self.radius_distance,
                                                        where_to_start=self.where_to_start))
        self.variance_speed: float = abs(variance_speed)

        self.generate_circumference()


    def _degrees_to_radians(self, deg: float) -> float:
        """
        Converts degrees to radians.
        """

        return deg * (PI / 180)

    @property
    def angle_density(self) -> float:
        """
        Returns the angle distance between each dot.
        """

        return (2 * PI) / self.dot_density


    @property
    def radius_distance(self) -> float:
        """
        Returns the distance between the radius and the maximum radius.
        """

        return (0.0 if self.max_radius is None else self.max_radius - self.radius)


    @property
    def current_radius(self) -> float:
        """
        Returns the current radius variance.
        """

        return (0.0 if not self.radius_timer else self.radius_timer.current_time)


    def polar_to_cartesian(self, radius: float, theta: float) -> Tuple[float, float]:
        """
        Converts polar coordinates to cartesian ones.
        """

        return radius * cos(theta), radius * sin(theta)


    def generate_dot_coordinates(self, dot_num: int) -> Tuple[float, float]:
        """
        Generates the POLAR coordinates of a dot.
        """

        return self.radius, dot_num * self.angle_density + self.initial_angle


    def generate_circumference(self) -> None:
        """
        Generates the dots coordinates.
        """

        for dot_num in range(self.dot_density):
            radius, theta = self.generate_dot_coordinates(dot_num)
            self.dot_coords.append((radius, theta))


    def get_hitcircles(self, dot_x: float, dot_y: float) -> Tuple[float, float, float, float]:
        """
        Returns the real coordinates to be used in the game screen.
        """

        cart_x, cart_y = self.polar_to_cartesian(dot_x, dot_y)
        return (cart_x - self.dot_raidus + self.center_x,
                cart_y - self.dot_raidus + self.center_y,
                cart_x + self.dot_raidus + self.center_x,
                cart_y + self.dot_raidus + self.center_y)


    # pylint: disable=invalid-name
    def animate(self, **_kwargs) -> None:
        """
        Proceeds with the animation.
        """

        for x, y in self.dot_coords:
            x1, y1, x2, y2 = self.get_hitcircles(x, y)
            draw_oval(x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      **self.properties)


    def post_hook(self, **_kwargs) -> None:
        """
        Moves each dot into its next coords.
        """

        new_dots = []

        for _, theta in self.dot_coords:
            new_dots.append((self.radius + self.current_radius,
                             theta + self.dot_speed))

        self.dot_coords = new_dots
        if self.radius_timer:
            speed = (1.0 - (abs(self.current_radius) / self.radius_distance)) * self.variance_speed
            bottom_limit = 0.4
            self.radius_timer.count(speed if speed > bottom_limit else bottom_limit)
