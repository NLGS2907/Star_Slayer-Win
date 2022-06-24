"""
Upgrades group for upgrading/evolving the player.
"""

from typing import TYPE_CHECKING

from ...checks import is_in_game, scene_is_cool
from ..hooks_group import HooksGroup

if TYPE_CHECKING:
    from ...state import Game


class Upgrades(HooksGroup):
    """
    Upgrades Group.
    """

    @HooksGroup.action(on_action="UPGRADE")
    @is_in_game()
    @scene_is_cool()
    def upgrade_player(self) -> None:
        """
        Upgrades the player properties.
        """

        for menu in self.game.current_scene.menus:
            if menu.hidden:
                return

        self.game.upgrade_character()


    @HooksGroup.action(on_action="EVOLVE")
    @is_in_game()
    @scene_is_cool()
    def evolve_player(self) -> None:
        """
        Evolves the player power level.
        """

        for menu in self.game.current_scene.menus:
            if menu.hidden:
                return

        self.game.evolve_character()


    def post_hook(self) -> None:
        """
        Resets the current scene pressing cooldown.
        """

        self.game.current_scene.press_cooldown.reset()


def setup_hook(game: "Game") -> None:
    """
    Adds the hook group in this file to the game.
    """

    game.add_group(Upgrades(game))
