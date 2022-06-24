"""
Medical Kit Drop Module.
"""

from typing import TYPE_CHECKING

from ..consts import MED_KIT_REL_PATH
from .drop import Drop

if TYPE_CHECKING:
    from ..state import Game

class MedKit(Drop):
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
        Initializes an instance of type 'MedKit'.
        """

        super().__init__(x1=x1,
                         y1=y1,
                         x2=x2,
                         y2=y2,
                         texture_path=MED_KIT_REL_PATH,
                         accel=2.0,
                         **kwargs)


    def trajectory(self) -> None:
        """
        Moves the drop.
        """

        self.move(0, (self.chrono.current_time * self.accel),
                  freely=True)

        self.chrono.count(0.06)


    def effect(self, game: "Game") -> None:
        """
        Defines the effect of the drop on the game
        if ti collides with something.
        """

        health_percentage = 15
        health_to_add = (health_percentage / 100) * game.player.base_hp

        game.player.hp += health_to_add
        game.update_health_anim()
