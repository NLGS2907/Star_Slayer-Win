"""
Main Menu Module.
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


__all__ = ["MainMenu"] # We DON'T want the local variable 'mainmenu' to be exported


class MainMenu(Menu, metaclass=Singleton):
    """
    The Main Menu of the game.
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
        Initializes an instance of 'MainMenu'.
        """

        super().__init__(area_corners, **kwargs)


mainmenu = MainMenu() # instantiated temporarily

@mainmenu.button(message="Play")
def play_game(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Lets the player play the game.
    """

    game.change_scene("scene-in-game")


@mainmenu.button(message="Options")
def go_to_options(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Goes to the options menu.
    """

    game.change_scene("scene-options")


@mainmenu.button(message="About")
def about_game(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Shows information about the game.
    """

    game.show_about = True


@mainmenu.button(message="Exit")
def exit_game(game: "Game", _scene: "Scene", _btn: Button) -> None:
    """
    Exits the game.
    """

    game.exit = True
