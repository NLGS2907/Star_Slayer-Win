"""
Bullets with an electric aura.
"""

from math import pi as PI
from math import radians
from random import choices
from random import uniform as rand_uniform
from typing import TYPE_CHECKING, List, Optional, Tuple

from ...utils import HitCircle, Timer
from ..bullet import BulletKwargs, BulletSprites, Bullet

if TYPE_CHECKING:
    from ...enemies import Enemy

ArcsPivots = List[List[Tuple[float, float]]]


class BulletElectric(Bullet):
    """
    Bullets with an electric aura that harms
    others in its radius.
    """

    def __init__(self,
                 *,
                 accel_time: int=30,
                 angle: float=(PI / 2),
                 radar_pool: List["Enemy"],
                 damage: int=1,
                 dmg_chance: float=50.0,
                 field_radius: Optional[float]=None,
                 how_many_arcs: int=3,
                 arcs_angle_variance: float=radians(10.0),
                 deviation_speed: float=0.04, # in radians
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletElectric'.
        """

        super().__init__(sprite_type=BulletSprites.ELECTRIC,
                         **kwargs)

        if dmg_chance <= 0.0 or 100.0 < dmg_chance:
            raise ValueError(f"Damage chance value {dmg_chance} should be on range (0.0, 100.0]")

        self.angle: float = angle
        self.accel_timer: Timer = Timer(accel_time)
        self.radar_pool: List["Enemy"] = radar_pool
        self.dmg: int = damage
        self.dmg_chance: float = dmg_chance
        self.arcs_pivots: ArcsPivots = []
        self.field_radius: float = (self.radius * 8 if field_radius is None else field_radius)
        self.arcs_amount: int = how_many_arcs
        self.arcs_angle_variance: float = arcs_angle_variance
        self.deviation_speed: float = deviation_speed


    def _is_within_range(self, other: "Enemy") -> None:
        """
        Detects if a certain shape is within range of the
        field radius.
        """

        return other.collides_with_circle(HitCircle(cx=self.cx,
                                                    cy=self.cy,
                                                    radius=self.field_radius,
                                                    can_spawn_outside=True))


    @property
    def pivots_amount(self) -> int:
        """
        Returns the pivots amount of the bullet.
        Pivots are always one less than the arcs.
        """

        return self.arcs_amount + 1


    def _correct_angle(self, angle: float) -> float:
        """
        Makes sure an angle is a value always between
        0 and 2 * PI.
        """

        return angle % (2 * PI)


    def _add_to_actual_angle(self, angle: float, ideal: float) -> None:
        """
        Changes the direction modifying the actual
        angle used by adding.
        """

        self.angle += angle

        if self.angle > ideal:
            self.angle = ideal


    def _deduct_to_actual_angle(self, angle: float, ideal: float) -> None:
        """
        Changes the direction modifying the actual
        angle used by substracting.
        """

        self.angle -= angle

        if self.angle < ideal:
            self.angle = ideal


    def _modify_actual_angle(self, angle: float, ideal: float) -> None:
        """
        Changes the direction modifying the actual
        angle used.
        """

        self.angle = self._correct_angle(self.angle)
        ideal = self._correct_angle(ideal)

        if self.angle == ideal:
            return

        if self.angle < ideal:
            self._add_to_actual_angle(angle, ideal)

        elif self.angle > ideal:
            self._deduct_to_actual_angle(angle, ideal)


    def update_pivots(self) -> None:
        """
        Updates the arcs pivots.
        """

        pivots = []

        for threat in self.radar_pool:
            shape_arcs = []

            if self._is_within_range(threat):

                distance = self.distance_to(threat)
                angle = self.angle_towards(threat)
                pivot_augment = distance / self.arcs_amount

                dmg =choices([0,                       self.dmg],           # Damage dealt
                             [100.0 - self.dmg_chance, self.dmg_chance])[0] # Chances
                threat.take_damage(dmg)
                self._modify_actual_angle(self.deviation_speed, angle)

                for pivot in range(self.pivots_amount):
                    rad = pivot * pivot_augment
                    theta = rand_uniform(angle - self.arcs_angle_variance,
                                         angle + self.arcs_angle_variance)

                    shape_arcs.append(self.polar_to_cart(rad, -theta))


            if shape_arcs:
                pivots.append(shape_arcs)

        self.arcs_pivots = pivots


    def trajectory(self) -> None:
        """
        Defines the trajectory of an electric bullet.
        """

        self.update_pivots()

        self.accel_timer.count(1)

        if not self.accel_timer.time_is_up():
            self.accel += 0.2

        self.move_rad(0.2 * self.speed * self.accel,
                      self.angle,
                      freely=True)
