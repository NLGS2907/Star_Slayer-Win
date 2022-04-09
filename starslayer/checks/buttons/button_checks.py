"""
Buttons Checks Module. Contains some pre-defined checks as well as the custom decorator.
"""

from typing import Callable, TYPE_CHECKING

from ...utils import Button, ButtonHandler

if TYPE_CHECKING:

    from ...state.game_state import Game

ButtonCheck = Callable[["Game", Button], bool]


def check(predicate: ButtonHandler) -> ButtonHandler:
    """
    Adds a check to an action function.

    The check function needs a 'Game' instance as its
    first argument, and the button itself as the second.
    """

    def inner(func: ButtonCheck) -> ButtonCheck:

        if not hasattr(func, "__btn_checks__"):

            func.__btn_checks__ = []

        func.__btn_checks__.append(predicate)
        return func

    return inner


def is_on_prompt(it_is: bool=True) -> ButtonHandler:
    """
    Adds a prompt checker.
    """

    def game_is_on_prompt(game: "Game", _btn: Button) -> bool:
        """
        Checks if the game is currently prompting the user.
        """

        return game.is_on_prompt if it_is else not game.is_on_prompt

    return check(game_is_on_prompt)
