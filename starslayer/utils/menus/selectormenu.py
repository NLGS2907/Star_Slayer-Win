"""
Color Selector Menu Module.
"""

from typing import TYPE_CHECKING

from ...auxiliar import Singleton
from ...consts import HEIGHT, KEYS_PATH, WIDTH
from ...files import dump_json, list_actions, list_repeated_keys, load_json
from ...gamelib import EventType
from ...gamelib import say as lib_say
from ...gamelib import wait as lib_wait
from ..button import Button
from ..generic import IntTuple4
from ..menu import Menu, MenuDict
from .controlsubmenu import ControlSubMenu

if TYPE_CHECKING:
    from ...scene import Scene
    from ...state import Game

__all__ = ["SelectorMenu"] # We DON'T want the local variable 'selectormenu' to be exported


class SelectorMenu(Menu, metaclass=Singleton):
    """
    The Selector Menu of the game.
    """

    def __init__(self,
                 area_corners: IntTuple4=(
                    (WIDTH // 15),
                    (HEIGHT * 0.065714),
                    (WIDTH * 0.866666),
                    (HEIGHT * 0.928571)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'ControlsMenu'.
        """

        super().__init__(area_corners, **kwargs)


selectormenu = SelectorMenu() # instantiated temporarily
