"""
Bullet with radial movement.
"""

from math import pi as PI

from ...utils import Timer
from ..bullet import Bullet, BulletKwargs


class BulletRadial(Bullet):
    """
    A bullet of radial movement.
    """

    def __init__(self,
                 *,
                 accel_time: int=30,
                 angle: float=(PI / 2),
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletRadial'.
        """

        super().__init__(**kwargs)

        self.angle: float = angle
        self.accel_timer: Timer = Timer(accel_time)


    def trajectory(self) -> None:
        """
        Defines the trajectory of a normal radial bullet.
        """

        self.accel_timer.count(1)

        if not self.accel_timer.time_is_up():
            self.accel += 0.3

        self.move_rad(0.2 * self.speed * self.accel,
                      self.angle,
                      freely=True)
