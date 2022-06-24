"""
Bullets that explode into anothers.
"""

from math import pi as PI
from math import radians
from random import randrange
from typing import TYPE_CHECKING, List

from ...utils import Timer
from ..bullet import BulletKwargs
from ..normal_bullets import BulletRadial

if TYPE_CHECKING:
    from ..bullet import Bullet


class BulletFirework(BulletRadial):
    """
    A Bullet with a trajectory similar to that
    of fireworks.
    """

    def __init__(self,
                 *,
                 accel_time: int=30,
                 angle: float=(PI / 2),
                 time_until_boom: float=30.0,
                 bullets_pool: List["Bullet"],
                 how_many_children: int=4,
                 initial_phase: float=(PI / 2),
                 reset: bool=True,
                 child_type: "Bullet"=BulletRadial,
                 recursive_divisions: int=1,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletFirework'.
        """

        super().__init__(accel_time=accel_time,
                         angle=angle,
                         **kwargs)

        self.time_until_boom: Timer = Timer(time_until_boom)
        self.bullets_pool: List["Bullet"] = bullets_pool
        self.children: int = how_many_children
        self.initial_phase: float = initial_phase
        self.reset: bool = reset
        self.child_type: "Bullet" = child_type
        self.divisions: int = recursive_divisions


    def trajectory(self) -> None:
        """
        Defines the trajectory of a firework bullet.
        """

        self.time_until_boom.count(1, reset=self.reset)

        if not self.time_until_boom.time_is_up():
            super().trajectory()
            return

        augment = (2 * PI) / self.children
        self.divisions -= 1
        type_to_use: "Bullet" = (__class__ if self.divisions > 0 else self.child_type)
        self.initial_phase += radians(randrange(45, 91, 1))
        self.speed *= 1.2

        for child in range(self.children):
            self.bullets_pool.append(type_to_use(cx=self.cx,
                                                 cy=self.cy,
                                                 radius=self.radius,
                                                 health=self.hp,
                                                 how_hard=self.hardness,
                                                 speed=self.speed,
                                                 sprite_type=self.sprite_type,
                                                 can_spawn_outside=True,

                                                  # Division
                                                  accel_time=self.accel,
                                                  angle=child * augment + self.initial_phase,
                                                  time_until_boom=self.time_until_boom.base_time,
                                                  bullets_pool=self.bullets_pool,
                                                  how_many_children=self.children,
                                                  initial_phase=self.initial_phase,
                                                  reset=self.reset,
                                                  child_type=self.child_type,
                                                  recursive_divisions=self.divisions,

                                                  **self.properties))
