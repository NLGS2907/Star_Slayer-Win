"""
Prompt Graphics Module.
"""

from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..consts import HEIGHT, WIDTH
from ..gamelib import draw_rectangle, draw_text
from .color_selector import (draw_color_table, draw_hue_bar,
                             draw_selector_buttons, draw_selector_details)

if TYPE_CHECKING:
    from ..selector import ColorSelector
    from ..state import Game


def draw_key_changing_prompt(game: "Game") -> None:
    """
    It draws a prompt in the screen that warns the player that a key is
    being changed and they need to press any key to try to bind it.
    """

    aux_cons = (HEIGHT // 10)

    draw_rectangle(aux_cons,
                   (HEIGHT // 2) - aux_cons,
                   WIDTH - aux_cons,
                   (HEIGHT // 2) + aux_cons,
                   width=(HEIGHT // 90),
                   outline=get_color(game, "MENU_OUTLINE_1"),
                   fill=get_color(game, "MENU_COLOR_1"))
    draw_text(f"Press any key to bind it to '{game.action_to_show}'",
              (WIDTH // 2),
              (HEIGHT // 2),
              fill=get_color(game, "TEXT_COLOR_1"),
              size=(HEIGHT // 30),
              justify='c')


def draw_attribute_prompt(game: "Game") -> None:
    """
    Draws a prompt that asks the user to select a new color value
    for the attribute selected.
    """

    selector: "ColorSelector" = game.color_selector
    x1, y1, x2, y2 = selector.area # pylint: disable=invalid-name

    draw_rectangle(x1, y1, x2, y2,
                           width=(WIDTH // 375),
                           outline=get_color(game, "MENU_OUTLINE_1"),
                           fill=get_color(game, "MENU_COLOR_1"))

    draw_color_table(game)
    draw_hue_bar(game)
    draw_selector_details(game)
    draw_selector_buttons(game)
