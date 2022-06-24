"""
Bullet that is invisible, and has no effects.
"""

from math import pi as PI

from ..bullet import BulletKwargs, BulletSprites
from .bullet_rad import BulletRadial


class BulletInvisible(BulletRadial):
    """
    A bullet that has no sprite, and no effects whatsoever.
    Its main purpose is to be an anchor to other types.
    """

    def __init__(self,
                 *,
                 accel_time: int=30,
                 angle: float=(PI / 2),
                 **kwargs: BulletKwargs) -> None:
        """
        Initializes an instance of type 'BulletInvisible'.
        """

        super().__init__(accel_time=accel_time,
                         angle=angle,
                         health=1,
                         how_hard=0,
                         ethereal=True,
                         sprite_type=BulletSprites.INVISIBLE,
                         **kwargs)
