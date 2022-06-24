"""
Bullets with orbiting trajectory.
"""

from typing import TYPE_CHECKING

from ...utils import Timer
from ..bullet import BulletKwargs
from .bullet_spiral import BulletSpiralSimple

if TYPE_CHECKING:
    from ...utils import BoundingShape


class BulletOrbiting(BulletSpiralSimple):
    """
    A bullet of orbiting trajectory.
    """

    def __init__(self,
                 *,
                 time_until_orbit: float=10.0,
                 orbit_center: "BoundingShape",
                 clockwise: bool=False,
                 curvature_speed: float = 0.05,
                 starting_angle: float=0.0, # in radians
                 radius_speed: float=0.5,
                 initial_radius: float=0.0,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletOrbiting'.
        """

        super().__init__(clockwise=clockwise,
                         curvature_speed=curvature_speed,
                         starting_angle=starting_angle,
                         radius_speed=radius_speed,
                         initial_radius=initial_radius,
                         **kwargs)

        self.until_orbit: Timer = Timer(time_until_orbit)
        self.orbit_center: "BoundingShape" = orbit_center
        self.trajectory_radius: float = initial_radius


    def trajectory(self) -> None:
        """
        Defines the trajectory of an orbiting bullet.
        """

        self.until_orbit.count(1.0)

        if not self.until_orbit.time_is_up():
            super().trajectory()
            self.trajectory_radius: float = self.distance_to(self.orbit_center)
            return

        self.radius_speed = 0
        direction = (-1 if self.clockwise else 1)
        self.move_orbit(self.orbit_center,
                        direction * self.angle,
                        self.trajectory_radius)
        self.angle += self.curvature_speed
