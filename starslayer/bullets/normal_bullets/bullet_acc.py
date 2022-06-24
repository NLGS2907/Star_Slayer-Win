"""
Bullets with normal acceleration.
"""

from ...utils import Timer
from ..bullet import Bullet, BulletKwargs


class BulletAccel(Bullet):
    """
    A bullet of normal acceleration.
    """

    def __init__(self,
                 *,
                 accel_time: int=30,
                 upwards: bool=True,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletAccel'.
        """

        super().__init__(**kwargs)

        self.upwards: bool = upwards
        self.accel_timer = Timer(accel_time)


    def trajectory(self) -> None:
        """
        Defines the trajectory of a normal acceleration bullet.
        """

        if self.accel_timer.current_time > 0:
            self.accel_timer.deduct(1)
            self.accel += 0.3

        self.move(0.0,
                  (-1.0 if self.upwards else 1.0) * 0.2 * self.speed * self.accel,
                  freely=True)
