"""
Special Cheats Group for having a fun time.
"""

from math import inf
from typing import TYPE_CHECKING

from ...checks import is_in_game
from ...consts import SFX_TIME_CONTINUE, SFX_TIME_STOP
from ..hooks_group import HooksGroup

if TYPE_CHECKING:
    from ...state import Game


class SpecialCheats(HooksGroup):
    """
    Special Cheats Group.
    """

    @HooksGroup.combination(with_name="ZA WARUDO")
    @is_in_game()
    def the_world(self) -> None:
        """
        Stops time.
        """

        self.game.player.time_awareness = inf
        self.game.player.can_change_awareness = False
        self.game.play_sound(SFX_TIME_STOP)


    @HooksGroup.combination(with_name="ZA-WARUDONT")
    @is_in_game()
    def the_world_is_back(self) -> None:
        """
        Resumes the time flow.
        """

        self.game.player.time_awareness = 1
        self.game.player.can_change_awareness = True
        self.game.play_sound(SFX_TIME_CONTINUE)


    def post_hook(self) -> None:
        """
        Ensures that the special cheats  also count as a cheat.
        """

        self.game.used_cheats = True


def setup_hook(game: "Game") -> None:
    """
    Adds the hook group in this file to the game.
    """

    game.add_group(SpecialCheats(game))
