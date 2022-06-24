"""
In-Game Menu Module.
"""

from typing import TYPE_CHECKING

from ....auxiliar import Singleton
from ....checks import left_click, on_press
from ....consts import HEIGHT, WIDTH
from ...menu import ButtonKwargs, Menu, MenuDict
from ...shapes import FloatTuple4

if TYPE_CHECKING:
    from ....scene import Scene
    from ....state import Game
    from ...button import Button


__all__ = ["InGameMenu"] # We DON'T want the local variable 'ingamemenu' to be exported


class InGameMenu(Menu, metaclass=Singleton):
    """
    The in-game menu of the game.
    """

    def __init__(self,
                 area_corners: FloatTuple4=(
                    WIDTH * 0.675,
                    HEIGHT * 0.12,
                    WIDTH * 0.99,
                    HEIGHT * 0.18
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'InGameMenu'.
        It is hidden by default.
        """

        super().__init__(area_corners, hidden=True, **kwargs)


ingamemenu = InGameMenu() # instantiated temporarily

@ingamemenu.button(message="Upgrade",
                   x1=WIDTH * 0.675,
                   y1=HEIGHT * 0.12,
                   x2=WIDTH * 0.83,
                   y2=HEIGHT * 0.18)
@left_click()
@on_press()
def upgrade_char(game: "Game",
                 _scene: "Scene",
                 _btn: "Button",
                 **_kwargs: ButtonKwargs) -> None:
    """
    Upgrades the character, enhancing its speed and hardness.
    """

    game.upgrade_character()


@ingamemenu.button(message="Evolve",
                   x1=WIDTH * 0.835,
                   y1=HEIGHT * 0.12,
                   x2=WIDTH * 0.99,
                   y2=HEIGHT * 0.18)
@left_click()
@on_press()
def evolve_char(game: "Game",
                _scene: "Scene",
                _btn: "Button",
                **_kwargs: ButtonKwargs) -> None:
    """
    Evolves the character into a new power level.
    """

    game.evolve_character()
