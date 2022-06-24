"""
Game Over Menu Module.
"""

from random import choice
from typing import TYPE_CHECKING

from ....auxiliar import Singleton
from ....checks import left_click, on_press
from ....consts import HEIGHT, USED_CHEATS_LINES, WIDTH
from ....gamelib import input as lib_input
from ....gamelib import say as lib_say
from ...menu import ButtonKwargs, FloatTuple4, Menu, MenuDict

if TYPE_CHECKING:
    from ....scene import Scene
    from ....state import Game
    from ...button import Button

__all__ = ["GameOverMenu"]


class GameOverMenu(Menu, metaclass=Singleton):
    """
    The Game Over Menu of the game.
    """

    def __init__(self,
                 area_corners: FloatTuple4=(
                    int(WIDTH * 0.4),
                    int(HEIGHT * 0.7),
                    int(WIDTH * 0.6),
                    int(HEIGHT * 0.9)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'OptionsMenu'.
        """

        super().__init__(area_corners,
                         max_rows=2,
                         **kwargs)


gameovermenu = GameOverMenu() # instantiated temporarily

@gameovermenu.button(message="Continue")
@left_click()
@on_press()
def continue_to_scoreboard(game: "Game",
                           _scene: "Scene",
                           _btn: "Button",
                           **_kwargs: ButtonKwargs) -> None:
    """
    Goes to scoreboard.
    """

    if game.used_cheats:
        lib_say(choice(USED_CHEATS_LINES))

    else:
        name = lib_input("What is your name?")

        if name and game.score > 0:
            game.add_score_to_board(name,
                                    game.player.power_level.name,
                                    game.game_level,
                                    game.score)

    game.change_scene("scene-scoreboard")
