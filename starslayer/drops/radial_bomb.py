"""
Radial Bomb Drop Module.
"""

from math import pi as PI
from typing import TYPE_CHECKING

from ..bullets import BulletRadial
from ..consts import RADIAL_BOMB_REL_PATH, WIDTH
from .drop import Drop

if TYPE_CHECKING:
    from ..state import Game

class RadialBomb(Drop):
    """
    Med Kit Drop class.
    """

    # pylint: disable=invalid-name
    def __init__(self,
                 *,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'RadialBomb'.
        """

        super().__init__(x1=x1,
                         y1=y1,
                         x2=x2,
                         y2=y2,
                         texture_path=RADIAL_BOMB_REL_PATH,
                         accel=2.0,
                         **kwargs)


    def trajectory(self) -> None:
        """
        Moves the drop.
        """

        self.move(0, (self.chrono.current_time * self.accel),
                  freely=True)

        self.chrono.count(0.08)


    def effect(self, game: "Game") -> None:
        """
        Defines the effect of the drop on the game
        if ti collides with something.
        """

        how_many = 24
        augment  = (2 * PI) / how_many
        center_x, center_y = game.player.center
        rad_aux = WIDTH // 150

        for i in range(how_many):
            game.player_bullets.append(BulletRadial(cx=center_x,
                                                       cy=center_y,
                                                       radius=rad_aux,
                                                       health=5,
                                                       speed=4.4,
                                                       how_hard=game.player.hardness,
                                                       angle=(i * augment)))
            game.player_bullets.append(BulletRadial(cx=center_x,
                                                       cy=center_y,
                                                       radius=rad_aux,
                                                       health=5,
                                                       speed=5,
                                                       how_hard=game.player.hardness,
                                                       angle=(i * 1.5 * augment)))
            game.player_bullets.append(BulletRadial(cx=center_x,
                                                       cy=center_y,
                                                       radius=rad_aux,
                                                       health=5,
                                                       speed=5.6,
                                                       how_hard=game.player.hardness,
                                                       angle=(i * augment)))
