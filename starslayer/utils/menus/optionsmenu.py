"""
Options Menu Module.
"""

from typing import TYPE_CHECKING

from ...auxiliar import Singleton
from ...consts import HEIGHT, WIDTH
from ..button import Button
from ..generic import IntTuple4
from ..menu import Menu, MenuDict

if TYPE_CHECKING:
    from ...scene import Scene
    from ...state import Game


__all__ = ["OptionsMenu"] # We DON'T want the local variable 'optionsmenu' to be exported


class OptionsMenu(Menu, metaclass=Singleton):
    """
    The Options Menu of the game.
    """

    def __init__(self,
                 area_corners: IntTuple4=(
                    int(WIDTH / 3.75),
                    int(HEIGHT / 2),
                    int(WIDTH / 1.363636),
                    int(HEIGHT / 1.076923)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'OptionsMenu'.
        """

        kwargs.update({"max_rows": 4})
        super().__init__(area_corners, **kwargs)


optionsmenu = OptionsMenu() # instantiated temporarily

@optionsmenu.button(message="Configure Controls")
def configure_controls(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Goes to the controls menu.
    """

    game.change_scene("scene-controls")


@optionsmenu.button(message="Edit Color Profiles")
def edit_profiles(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Goes to the profiles menu.
    """

    game.change_scene("scene-profiles")
