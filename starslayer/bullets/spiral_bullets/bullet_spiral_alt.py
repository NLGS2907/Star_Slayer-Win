"""
Bullets with alternating spiral trajectory.
"""

from math import radians

from ...utils import Timer
from ..bullet import Bullet, BulletKwargs


class BulletSpiralAlt(Bullet):
    """
    A bullet of spiral trajectory.
    """

    def __init__(self,
                 *,
                 alternating_time: float=12.5,
                 first_to_right: bool=True,
                 curvature_speed: float = 0.05,
                 starting_angle: float=radians(90.0), # in radians
                 radius_speed: float=0.05,
                 initial_radius: float=0.0,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletSpiralAlt'.
        """

        super().__init__(**kwargs)

        if curvature_speed <= 0:
            raise ValueError("curvature must be of value above zero.")

        if radius_speed <= 0:
            raise ValueError("radius speed must be of value above zero.")

        self.alternating: Timer = Timer(alternating_time)
        self.direction_coefficient: int = (-1 if first_to_right else 1)
        self.curvature_speed: float = curvature_speed
        self.angle: float = starting_angle
        self.radius_speed: float = radius_speed
        self.trajectory_radius: float = initial_radius


    def _change_direction(self) -> None:
        """
        Alternates the bullet direction.
        """

        self.direction_coefficient = -self.direction_coefficient
        # self.angle = -self.angle


    def trajectory(self) -> None:
        """
        Defines the trajectory of a simple spiral bullet.
        """

        self.alternating.count(1.0, reset=True)

        self.move_rad(self.trajectory_radius + self.speed * self.accel,
                      self.angle,
                      freely=True)

        self.trajectory_radius += self.radius_speed
        self.angle += self.curvature_speed * self.direction_coefficient

        if self.alternating.time_is_up():
            self._change_direction()
