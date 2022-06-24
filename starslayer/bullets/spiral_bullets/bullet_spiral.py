"""
Bullets with spiral trajectory.
"""

from ..bullet import Bullet, BulletKwargs


class BulletSpiralSimple(Bullet):
    """
    A bullet of spiral trajectory.
    """

    def __init__(self,
                 *,
                 clockwise: bool=False,
                 curvature_speed: float = 0.05,
                 starting_angle: float=0.0, # in radians
                 radius_speed: float=0.5,
                 initial_radius: float=0.0,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletSpiralSimple'.
        """

        super().__init__(**kwargs)

        if curvature_speed <= 0:
            raise ValueError("curvature must be of value above zero.")

        if radius_speed <= 0:
            raise ValueError("radius speed must be of value above zero.")

        self.clockwise: bool = clockwise
        self.curvature_speed: float = curvature_speed
        self.angle: float = starting_angle
        self.radius_speed: float = radius_speed
        self.radius_increment: float = initial_radius


    def trajectory(self) -> None:
        """
        Defines the trajectory of a simple spiral bullet.
        """

        direction = (-1 if self.clockwise else 1)

        self.move_rad(self.radius_increment * self.speed,
                      direction * self.angle,
                      freely=True)

        self.radius_increment += self.radius_speed
        self.angle += self.curvature_speed
