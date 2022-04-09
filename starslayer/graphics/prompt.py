"""
Prompt Graphics Module.
"""

from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..consts import DEBUG_LINES, DEBUG_TEXT, HEIGHT, WIDTH
from ..gamelib import draw_line, draw_rectangle, draw_text
from .color_selector import (draw_color_table, draw_hue_bar,
                             draw_selector_buttons, draw_selector_details)
from .gameplay import draw_debug_lines

if TYPE_CHECKING:

    from ..selector import ColorSelector
    from ..state import Game


def draw_debug_info(game: "Game") -> None:
    """
    Draws debug information about the current game.
    """

    player = game.player
    debug_cons = (HEIGHT // 70)

    settings = {"player_x1": player.x1,
               "player_y1": player.y1,
               "player_x2": player.x2,
               "player_y2": player.y2,

               "hitbox_center": player.center,
               "shooting_cooldown": ("Ready!" if game.shooting_cooldown.is_zero_or_less()
                                     else game.shooting_cooldown.current_time),
               "inv_cooldown": ("Ready!" if game.invulnerability.is_zero_or_less()
                                else game.invulnerability.current_time),

               "level_timer": game.level_timer.current_time,
               "power_level": game.power_level,

               "health": game.player.hp,
               "hardness": game.player.hardness,
               "speed": game.player.speed,

               "enemies": len(game.enemies),
               "bullets": len(game.bullets)}

    debug_text = DEBUG_TEXT.format(**settings)

    draw_text(debug_text,
                      debug_cons,
                      debug_cons,
                      size=debug_cons,
                      fill=get_color(game, "TEXT_COLOR_1"),
                      anchor="nw")

    if DEBUG_LINES:
        return

    draw_debug_lines(game)

    aux = (WIDTH // 30)

    for bullet in game.bullets:

        x, y = bullet.center # pylint: disable=invalid-name
        draw_line(x, y - aux,
                  x, y + aux,
                  fill=get_color(game, "DEBUG_LINES_2"))
        draw_line(x - aux, y,
                  x + aux, y,
                  fill=get_color(game, "DEBUG_LINES_2"))

    for enem in game.enemies:

        aux2 = int(aux * 1.67)

        x, y = enem.center # pylint: disable=invalid-name
        draw_line(x, y - aux2, x,
                  y + aux2,
                  fill=get_color(game, "DEBUG_LINES_2"))
        draw_line(x - aux2,
                  y, x + aux2,
                  y, fill=get_color(game, "DEBUG_LINES_2"))


def draw_about(game: "Game") -> None:
    """
    Shows the information about the people involved in this game.
    """

    myself = "Franco 'NLGS' Lighterman"
    aux_cons = (WIDTH // 10)

    draw_rectangle(0,
                   0,
                   WIDTH,
                   HEIGHT,
                   width=(HEIGHT // 87),
                   outline=get_color(game, "ABOUT_OUTLINE_1"),
                   fill=get_color(game, "ABOUT_COLOR_1"))

    draw_text("SO, ABOUT\nTHIS GAME...",
              (WIDTH // 2),
              (HEIGHT // 6),
              size=(HEIGHT // 12),
              fill=get_color(game, "TEXT_COLOR_1"),
              justify='c')

    # Pixel-Art
    draw_text("Pixel-Art:",
              aux_cons,
              HEIGHT * 0.4,
              size=(HEIGHT // 30),
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor='w')
    draw_text(myself,
              WIDTH - aux_cons,
              HEIGHT * 0.4,
              size=(HEIGHT // 30),
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor='e')

    # Coding
    draw_text("Coding:",
              aux_cons,
              HEIGHT * 0.6,
              size=(HEIGHT // 30),
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor='w')
    draw_text(myself,
             WIDTH - aux_cons,
             HEIGHT * 0.6,
             size=(HEIGHT // 30),
             fill=get_color(game, "TEXT_COLOR_1"),
             anchor='e')

    # Gamelib
    draw_text("Gamelib Library:",
              aux_cons,
              HEIGHT * 0.8,
              size=(HEIGHT // 30),
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor='w')
    draw_text("Diego Essaya",
              WIDTH - aux_cons,
              HEIGHT * 0.8,
              size=(HEIGHT // 30),
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor='e')

    draw_text("Press 'RETURN' to return",
             (WIDTH // 2),
             HEIGHT - 20,
             size=(HEIGHT // 50),
             fill=get_color(game, "TEXT_COLOR_1"),
             justify='c')


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
