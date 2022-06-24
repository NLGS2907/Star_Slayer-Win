"""
Bullet that homes in the player.
"""

from math import pi as PI
from typing import TYPE_CHECKING, List, Optional

from ...auxiliar import get_closest_coordinates
from ...utils import Timer
from ..bullet import Bullet, BulletKwargs

if TYPE_CHECKING:
    from ...utils import BoundingShape


class BulletHoming(Bullet):
    """
    A bullet that homes in the player.
    """

    def __init__(self,
                 *,
                 homing_target: Optional["BoundingShape"]=None,
                 target_pool: Optional[List["BoundingShape"]]=None,
                 homing_time: float=0.0,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletHoming'.
        """

        super().__init__(**kwargs)

        if target_pool is not None and target_pool == []:
            raise ValueError("The target pool must contain at least one member (homing target).")

        if target_pool is None and homing_target is None:
            TypeError("Both the homing target and the target pool cannot be None.")

        self.target: "BoundingShape" = homing_target or get_closest_coordinates(self,
                                                                                target_pool)
        self.target_pool: Optional[List["BoundingShape"]] = target_pool or [self.target]
        self.homing_time: Timer = Timer(homing_time)
        self.nominal_angle: float = self.angle_towards(self.target)
        self.actual_angle: float = self.nominal_angle


    def change_target(self, new_target: "BoundingShape") -> None:
        """
        Changes the target of the bullet.
        """

        self.target = new_target


    def target_exists(self) -> bool:
        """
        Checks if the target is still.
        """

        return self.target in self.target_pool


    def _correct_angle(self, angle: float) -> float:
        """
        Makes sure an angle is a value always between
        0 and 2 * PI.
        """

        return angle % (2 * PI)


    def _add_to_actual_angle(self, angle: float) -> None:
        """
        Changes the direction modifying the actual
        angle used by adding.
        """

        self.actual_angle += angle

        if self.actual_angle > self.nominal_angle:
            self.actual_angle = self.nominal_angle


    def _deduct_to_actual_angle(self, angle: float) -> None:
        """
        Changes the direction modifying the actual
        angle used by substracting.
        """

        self.actual_angle -= angle

        if self.actual_angle < self.nominal_angle:
            self.actual_angle = self.nominal_angle


    def _modify_actual_angle(self, angle: float) -> None:
        """
        Changes the direction modifying the actual
        angle used.
        """

        self.nominal_angle = self._correct_angle(self.nominal_angle)
        self.actual_angle = self._correct_angle(self.actual_angle)

        if self.nominal_angle == self.actual_angle:
            return

        if self.actual_angle < self.nominal_angle:
            self._add_to_actual_angle(angle)

        elif self.actual_angle > self.nominal_angle:
            self._deduct_to_actual_angle(angle)


    def trajectory(self) -> None:
        """
        Defines the trajectory of a homing bullet.
        """

        if not self.target_exists():

            if self.target_pool:
                self.change_target(get_closest_coordinates(self, self.target_pool))

            else:
                self.homing_time.drop()

        self.homing_time.count(1.0)

        if not self.homing_time.time_is_up():
            self.nominal_angle = self.angle_towards(self.target)

        self._modify_actual_angle(0.03)

        self.move_rad(self.speed * self.accel,
                      self.actual_angle,
                      freely=True)
