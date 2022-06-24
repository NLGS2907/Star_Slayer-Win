"""
Bullet Sprites Types Module.
"""

from enum import Enum


class BulletSprites(Enum):
    """
    Diferent types of bullet sprites.
    """

    PLAIN = 0
    SPECIAL = 1
    SHINY = 2
    INVISIBLE = 3
    ELECTRIC = 4
