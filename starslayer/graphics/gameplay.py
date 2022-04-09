"""
Gmaeplay Graphics Module.
"""

from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..characters import Entity
from ..consts import HEIGHT, WIDTH
from ..gamelib import draw_image, draw_line, draw_oval, draw_rectangle

if TYPE_CHECKING:

    from ..state import Game


def draw_ship(game: "Game", ship: Entity, which_one: int=0) -> None:
    """
    Draws the sprite of a ship.

    'which_one' refers to which frame to draw.
    """

    if ship.sprites is None:

        draw_rectangle(ship.x1, ship.y1, ship.x2, ship.y2, fill=get_color(game, "DEBUG_LINES_1"))

    else:

        draw_image(ship.sprites[which_one], ship.x1, ship.y1)


def draw_bullets(game: "Game") -> None:
    """
    Draws every single bullet currently on screen.
    """

    bullets = game.bullets

    for bullet in bullets:

        draw_oval(bullet.x1,
                  bullet.y1,
                  bullet.x2,
                  bullet.y2,
                  outline=get_color(game, "GUI_OUTLINE_1"),
                  fill=get_color(game, "TEXT_COLOR_1"))


def draw_debug_lines(game: "Game") -> None:
    """
    Marks the limit of hitboxes and additional debug info through lines.
    """

    player = game.player
    cx, cy = player.center # pylint: disable=invalid-name
    aux = (WIDTH // 150)

    # Upper Lines
    draw_line(cx,
              0,
              cx,
              player.y1,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(cx - aux,
              player.y1,
              cx + aux,
              player.y1,
              fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom Lines
    draw_line(cx,
              player.y2,
              cx,
              HEIGHT,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(cx - aux,
              player.y2,
              cx + aux,
              player.y2,
              fill=get_color(game, "DEBUG_LINES_1"))

    # Left Lines
    draw_line(0,
              cy,
              player.x1,
              cy,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x1,
              cy - aux,
              player.x1,
              cy + aux,
              fill=get_color(game, "DEBUG_LINES_1"))

    # Right Lines
    draw_line(player.x2,
              cy, WIDTH,
              cy,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x2,
              cy - aux,
              player.x2,
              cy + aux,
              fill=get_color(game, "DEBUG_LINES_1"))


    # Upper-Left Corner
    draw_line(player.x1,
              player.y1,
              player.x1 + (aux * 2),
              player.y1,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x1,
              player.y1,
              player.x1,
              player.y1 + (aux * 2),
              fill=get_color(game, "DEBUG_LINES_1"))

    # Upper-Right Corner
    draw_line(player.x2,
              player.y1,
              player.x2 - (aux * 2),
              player.y1,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x2,
              player.y1,
              player.x2,
              player.y1 + (aux * 2),
              fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom-Left Corner
    draw_line(player.x1,
              player.y2,
              player.x1 + (aux * 2),
              player.y2,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x1,
              player.y2,
              player.x1,
              player.y2 - (aux * 2),
              fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom-Right Corner
    draw_line(player.x2,
              player.y2,
              player.x2 - (aux * 2),
              player.y2,
              fill=get_color(game, "DEBUG_LINES_1"))
    draw_line(player.x2,
              player.y2,
              player.x2,
              player.y2 - (aux * 2),
              fill=get_color(game, "DEBUG_LINES_1"))
