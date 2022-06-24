"""
Swift Enemy Module.
"""

from math import pi as PI
from typing import TYPE_CHECKING, List, Optional

from ...bullets import BulletHoming
from ...consts import ENEMY_SWIFT_REL_PATH, HEIGHT, PLAYABLE_WIDTH, WIDTH
from ...drops import MedKit, RadialBomb, SpiralBomb
from ...entity import EntityDict
from ...utils import Timer
from ..enemy import Enemy

if TYPE_CHECKING:
    from ...drops import Drop
    from ...state import BulletsList
    from ...utils import BoundingShape

class EnemySwift(Enemy):
    """
    A swift enemy.
    """

    def __init__(self,
                 *,
                 health=2,
                 how_hard=4,
                 speed=4,
                 shooting_cooldown=110,
                 trajectory_radius: float=PLAYABLE_WIDTH / 2,
                 clockwise: bool=False,
                 homing_target: "BoundingShape",
                 **kwargs: EntityDict) -> None:
        """
        Initializes an instance of type 'EnemySwift'.
        """

        super().__init__(health=health,
                         how_hard=how_hard,
                         speed=speed,
                         shooting_cooldown=shooting_cooldown,
                         texture_path=ENEMY_SWIFT_REL_PATH,
                         **kwargs)

        self.target: "BoundingShape" = homing_target
        self.clockwise: bool = clockwise
        self.trajectory_radius: float = trajectory_radius
        self.angle_timer: Timer = Timer(350)
        self.angle: float = PI # 180 degrees


    def trajectory(self) -> None:
        """
        Defines the movement of a swift enemy.
        """

        self.angle_timer.count(1.0)

        if self.angle_timer.time_is_up():
            self.move(0.0, -self.speed,
                      freely=True)

        else:
            self.angle += 0.0025 * self.speed * (-1 if self.clockwise else 1)
            self.move_orbit((PLAYABLE_WIDTH / 2, 0.0),
                            self.angle,
                            self.trajectory_radius)


    @property
    def points_worth(self) -> int:
        """
        How many points should this enemy be worth at dying.
        """

        return 73


    @property
    def loot_drops(self) -> List[Optional["Drop"]]:
        """
        Returns the possible drops for this enemy.
        """

        return [None, MedKit, RadialBomb, SpiralBomb]


    @property
    def loot_weights(self) -> Optional[List[float]]:
        """
        Returns the weights of the loot drops,
        and it must be of the same length.
        """

        return [70.0, 20.0, 5.5, 4.5]


    def shoot_bullets(self, bullets: "BulletsList") -> None:
        """
        Shoots the bullets specially made for this enemy.
        """

        center_x, center_y = self.center
        aux_y = HEIGHT / 46.6667
        rad_aux = WIDTH // 150

        bullets.append(BulletHoming(cx=center_x,
                                    cy=center_y + aux_y,
                                    radius=rad_aux,
                                    speed=4,
                                    how_hard=2,
                                    can_spawn_outside=True,
                                    homing_target=self.target))
