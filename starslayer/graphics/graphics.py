"""
Graphics Module. Draws anything that the player
sees on screen.
"""

from sys import version_info
from typing import TYPE_CHECKING

from .background import draw_background, draw_default_background
from .gameplay import draw_bullets, draw_ship
from .gui import draw_exiting_bar, draw_gui
from .prompt import draw_about, draw_debug_info
from .scene import draw_scene

if TYPE_CHECKING:

    from ..state import Game


def draw_screen(game: "Game") -> None:
    """
    Draws the entirety of the elements on the screen.
    """

    if version_info < (3, 10, 0): # Inferior to v3.10.0

        draw_default_background()
        return

    draw_background(game)
    draw_bullets(game)

    if game.show_debug_info:

        draw_debug_info(game)

    if game.is_in_game:

        draw_ship(game, game.player, (0 if game.invulnerability.is_zero_or_less() else 1))

        for enem in game.enemies:

            draw_ship(game, enem)

        draw_gui(game)

    elif game.show_about:

        draw_about(game)

    else:

        draw_scene(game)

    if game.exiting:

        draw_exiting_bar(game)
