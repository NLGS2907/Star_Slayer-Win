"""
Common Enemy A Module.
"""

from typing import TYPE_CHECKING, List, Optional

from ...bullets import BulletAccel
from ...consts import ENEMY_COMMON_A_REL_PATH, HEIGHT, WIDTH
from ...drops import MedKit
from ...entity import EntityDict
from ...utils import Timer
from ..enemy import Enemy

if TYPE_CHECKING:
    from ...drops import Drop
    from ...state import BulletsList

class EnemyCommonA(Enemy):
    """
    A common enemy (A version).
    """

    def __init__(self,
                 *,
                 health=3,
                 how_hard=5,
                 speed=3,
                 internal_timer_initial: int=30,
                 initial_direction: int=0, # 0 for "LEFT", 1 for "DOWN" and 2 for "RIGHT"
                 shooting_cooldown=200,
                 **kwargs: EntityDict) -> None:
        """
        Initializes an instance of type 'EnemyCommonA'.
        """

        super().__init__(health=health,
                         how_hard=how_hard,
                         speed=speed,
                         shooting_cooldown=shooting_cooldown,
                         texture_path=ENEMY_COMMON_A_REL_PATH,
                         **kwargs)

        self.internal_timer: Timer = Timer(internal_timer_initial)
        self.direction: int = initial_direction


    def trajectory(self) -> None:
        """
        Defines the movement of a common enemy (A version).
        """

        if self.internal_timer.time_is_up():
            self.direction = (self.direction + 1) % 3
            self.internal_timer.reset()

        else:
            self.internal_timer.count(1.0)

        self.transfer((self.speed * (self.direction - 1)), # from 0..1..2 to -1..0..1
                      ((self.speed // 2) if self.direction == 1 else 0))


    @property
    def points_worth(self) -> int:
        """
        How many points should this enemy be worth at dying.
        """

        return 45


    @property
    def loot_drops(self) -> List[Optional["Drop"]]:
        """
        Returns the possible drops for this enemy.
        """

        return [None, MedKit]


    @property
    def loot_weights(self) -> Optional[List[float]]:
        """
        Returns the weights of the loot drops,
        and it must be of the same length.
        """

        return [90.0, 10.0]


    def shoot_bullets(self, bullets: "BulletsList") -> None:
        """
        Shoots the bullets specially made for this enemy.
        """

        center_x, center_y = self.center
        aux_y = HEIGHT / 46.6667
        rad_aux = WIDTH // 150

        bullets.append(BulletAccel(cx=center_x,
                                       cy=center_y + aux_y,
                                       radius=rad_aux,
                                       speed=4,
                                       how_hard=2,
                                       upwards=False,
                                       can_spawn_outside=True))
