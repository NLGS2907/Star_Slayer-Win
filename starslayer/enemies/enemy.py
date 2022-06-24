"""
Generic Enemy class module.
"""

from abc import ABC, abstractmethod
from random import choices
from typing import TYPE_CHECKING, Dict, List, Optional

from ..consts import HEIGHT, WIDTH
from ..drops import DropsList
from ..entity import Entity
from ..utils import HitBox, Timer

if TYPE_CHECKING:
    from ..drops import Drop
    from ..state import BulletsList


class Enemy(Entity, HitBox, ABC):
    """
    Class for defining a NPC ship that attacks
    the player.
    """

    default: "Enemy"
    types: Dict[str, "Enemy"]

    def __init_subclass__(cls) -> None:
        """
        Registers sublcasses into an internal list.
        """

        try:

            Enemy.types[cls.__name__] = cls

        except AttributeError:

            Enemy.default = cls
            Enemy.types = {cls.__name__: cls}


    def __init__(self,
                 *,
                 shooting_cooldown: int=300,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Enemy'.
        """

        super().__init__(**kwargs)

        self._shooting_cooldown: int = Timer(shooting_cooldown)


    def __contains__(self, enemy: "Enemy") -> bool:
        """
        Returns if a specified enemy type is present.
        """

        return enemy in Enemy.types.values()


    @abstractmethod
    def trajectory(self) -> None:
        """
        Abstract method for sub-class responsability enforcement.
        """

        raise NotImplementedError


    @property
    def shooting_cooldown(self) -> Timer:
        """
        The shooting cooldown of the enemy.
        """

        return self._shooting_cooldown


    @property
    def loot_drops(self) -> List[Optional["Drop"]]:
        """
        Returns the possible drops for this enemy.

        This must be overriden to be useful.
        """

        return [None]


    @property
    def loot_weights(self) -> Optional[List[float]]:
        """
        Returns the weights of the loot drops,
        and it must be of the same length.

        This must be overriden to be useful.
        """

        return None


    def give_loot(self, container: DropsList) -> None:
        """
        Checks the possibility of adding a drop
        to a container.
        """

        weights_to_use = self.loot_weights

        if weights_to_use is not None:
            drops_amount = len(self.loot_drops)
            weights_amount = len(weights_to_use)

            if weights_amount > drops_amount:
                weights_to_use = weights_to_use[:drops_amount]

            elif weights_amount < drops_amount:
                for _ in range(drops_amount - weights_amount):
                    weights_to_use.append(1)

        drop = choices(self.loot_drops, weights_to_use)[0] # we only want one element

        if drop is not None:
            enemy_cx, enemy_cy = self.center
            width = WIDTH / 25
            height = HEIGHT / 23

            container.append(drop(x1=enemy_cx - (width / 2),
                                  y1=enemy_cy - (height / 2),
                                  x2=enemy_cx + (width / 2),
                                  y2=enemy_cy + (height / 2)))


    def try_shoot(self, bullets: "BulletsList") -> None:
        """
        Tries to fire bullets.
        """

        self.shooting_cooldown.deduct(1)
        self.shoot_extra_bullets(bullets)

        if not self.shooting_cooldown.time_is_up():
            return

        self.shoot_bullets(bullets)
        self.shooting_cooldown.reset()


    def shoot_bullets(self, _bullets: "BulletsList") -> None:
        """
        Shoots the bullets specially made for this enemy.

        It is recommended to inherit this method to be useful.
        """

        return None


    def shoot_extra_bullets(self, _bullets: "BulletsList") -> None:
        """
        Shoots extra bullets for this enemy, in case more are needed.

        It is recommended to inherit this method to be useful.
        """

        return None
