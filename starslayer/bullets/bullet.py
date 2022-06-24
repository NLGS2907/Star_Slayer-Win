"""
Bullets Module. Here are stored the classes for the
different types of bullets.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..entity import Entity
from ..utils import HitCircle
from .bullet_sprites_types import BulletSprites

BulletKwargs = dict[str, Optional[int | str | bool]]


class Bullet(Entity, HitCircle, ABC):
    """
    Class for defining a bullet that is shot
    from a ship, enemy or not.
    """

    def __init__(self,
                 *,
                 health: int=1,
                 acceleration: int=1,
                 ethereal: bool=False,
                 sprite_type: Optional[BulletSprites]=None,
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'Bullet'.
        """

        super().__init__(health=health,
                         ethereal=ethereal,
                         **kwargs)
        self.accel: int = acceleration
        self.sprite_type: BulletSprites = (BulletSprites.PLAIN
                                           if sprite_type is None
                                           else sprite_type)


    @abstractmethod
    def trajectory(self) -> None:
        """
        Defines the trajectory of the bullet.
        """

        raise NotImplementedError
