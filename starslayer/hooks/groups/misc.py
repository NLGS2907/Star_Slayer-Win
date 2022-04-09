"""
Miscellaneous group for miscellaneous stuff.
"""

from ..hooks_group import HooksGroup
from ...checks import can_exit, can_show_debug, is_in_game


class Miscellaneous(HooksGroup):
    """
    Misc Group.
    """

    @HooksGroup.action(on_action="RETURN")
    def close_about_msg(self) -> None:
        """
        Exits the about message, if possible.
        """

        if self.game.show_about:

            self.game.show_about = False


    @HooksGroup.action(on_action="DEBUG")
    @is_in_game()
    @can_show_debug()
    def show_debug_msg(self) -> None:
        """
        Shows or not debug information on screen.
        """

        self.game.show_debug_info = not self.game.show_debug_info
        self.game.debug_cooldown.reset()


    @HooksGroup.action(on_action="EXIT")
    @can_exit()
    def exit_game(self) -> None:
        """
        Exits the game for good.
        """

        self.game.exit = True
