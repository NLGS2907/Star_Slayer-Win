"""
Bullets with sinusoidal trajectories.
"""

from ...utils import SpringTimer
from ..bullet import Bullet, BulletKwargs


class BulletSinusoidalSimple(Bullet):
    """
    A bullet of sinusoidal trajectory.
    """

    def __init__(self,
                 *,
                 amplitude: float=10.0,
                 first_to_right: bool=True,
                 upwards: bool=True,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletSinusoidalSimple'.
        """

        super().__init__(**kwargs)

        self.upwards: bool = upwards
        self.oscillation = SpringTimer(-amplitude,
                                         amplitude,
                                         (amplitude
                                          if first_to_right
                                          else -amplitude))


    def trajectory(self) -> None:
        """
        Defines the trajectory of a simple sinusoidal bullet.
        """

        self.oscillation.count(1.0)
        self.move((self.oscillation.current_time * 0.5),
                  (-1 if self.upwards else 1) * self.speed,
                  freely=True)
