"""
Gmaeplay Graphics Module.
"""

from random import choice
from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..bullets import BulletElectric, BulletSprites
from ..consts import DEBUG_LINES, DEBUG_TEXT, HEIGHT, WIDTH
from ..gamelib import draw_line, draw_oval, draw_rectangle, draw_text
from .gui import draw_bar_percentage

if TYPE_CHECKING:
    from ..state import Game


def draw_bullets(game: "Game") -> None:
    """
    Draws every single bullet currently on screen.
    """

    for bullet in game.all_bullets:

        x1, y1, x2, y2 = bullet.all_coords # pylint: disable=invalid-name

        match bullet.sprite_type:

            case BulletSprites.PLAIN:
                draw_oval(x1=x1,
                          y1=y1,
                          x2=x2,
                          y2=y2,
                          outline=get_color(game, "GUI OUTLINE 1"),
                          fill=get_color(game, "BULLET PLAIN 1"))

            case BulletSprites.SPECIAL:
                draw_oval(x1=x1,
                          y1=y1,
                          x2=x2,
                          y2=y2,
                          outline=get_color(game, "GUI OUTLINE 1"),
                          fill=get_color(game, "BULLET SPECIAL 1"))

            case BulletSprites.SHINY:
                draw_oval(x1=x1,
                          y1=y1,
                          x2=x2,
                          y2=y2,
                          outline=get_color(game, "GUI OUTLINE 1"),
                          fill=get_color(game, "BULLET SHINY 1"))

            case BulletSprites.INVISIBLE:
                pass # Do nothing

            case BulletSprites.ELECTRIC:
                electric_colors = (get_color(game, "BULLET ELECTRIC 1"),
                                   get_color(game, "BULLET ELECTRIC 2"))
                cx, cy = bullet.center # pylint: disable=invalid-name
                field_x1 = cx - bullet.field_radius
                field_y1 = cy - bullet.field_radius
                field_x2 = cx + bullet.field_radius
                field_y2 = cy + bullet.field_radius
                dash_size = WIDTH // 10

                draw_oval(x1=x1,
                          y1=y1,
                          x2=x2,
                          y2=y2,
                          outline=get_color(game, "GUI OUTLINE 1"),
                          fill=choice(electric_colors))

                if isinstance(bullet, BulletElectric):
                    draw_oval(x1=field_x1,
                              y1=field_y1,
                              x2=field_x2,
                              y2=field_y2,
                              outline=choice(electric_colors),
                              fill=get_color(game, "GUI OUTLINE 1"),
                              dash=choice(((dash_size, dash_size),
                                            (dash_size // 2, dash_size ),
                                            (dash_size, dash_size, dash_size // 3, dash_size))))

                    draw_electric_bullets_arcs(game, bullet)


def draw_electric_bullets_arcs(game: "Game", bullet: BulletElectric) -> None:
    """
    Draws the arcs of the electric bullets.
    """

    if not bullet.arcs_pivots:
        return

    cx, cy = bullet.center # pylint: disable=invalid-name
    electric_colors = (get_color(game, "BULLET ELECTRIC 1"),
                       get_color(game, "BULLET ELECTRIC 2"))
    size_aux = HEIGHT / 700

    for piv in bullet.arcs_pivots: # We don't want to cross the last one
        range_to_use = len(piv) - 1

        for piv_i in range(range_to_use):
            piv_x1, piv_y1 = piv[piv_i]
            piv_x2, piv_y2 = piv[piv_i + 1]

            draw_line(cx + piv_x1,
                      cy + piv_y1,
                      cx + piv_x2,
                      cy + piv_y2,
                      fill=choice(electric_colors),
                      width=size_aux)


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

    aux2 = (WIDTH // 30)
    aux3 = int(aux2 * 1.67)

    if player.satellite:
        sh_x1, sh_y1, sh_x2, sh_y2 = player.satellite.all_coords
        draw_circle_case(game,
                         sh_x1,
                         sh_y1,
                         sh_x2,
                         sh_y2,
                         aux=aux3)

    for bullet in game.all_bullets:

        bullet_x1, bullet_y1, bullet_x2, bullet_y2 = bullet.all_coords
        draw_circle_case(game,
                         bullet_x1,
                         bullet_y1,
                         bullet_x2,
                         bullet_y2,
                         aux=aux2)

    for enem in game.enemies:

        enem_x1, enem_y1, enem_x2, enem_y2 = enem.all_coords
        draw_box_case(game,
                      enem_x1,
                      enem_y1,
                      enem_x2,
                      enem_y2,
                      aux=aux3)


# pylint: disable=invalid-name
def draw_box_case(game: "Game",
                  x1: float,
                  y1: float,
                  x2: float,
                  y2: float,
                  aux: float) -> None:
    """
    Draws a box case around a hitbox.
    """

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    debug_color = get_color(game, "DEBUG_LINES_2")

    draw_rectangle(x1, y1, x2, y2,
                   fill='',
                   outline=debug_color)
    draw_line(cx, cy - aux,
              cx, cy + aux,
              fill=debug_color)
    draw_line(cx - aux,
              cy, cx + aux,
              cy, fill=debug_color)


# pylint: disable=invalid-name
def draw_circle_case(game: "Game",
                     x1: float,
                     y1: float,
                     x2: float,
                     y2: float,
                     aux: float) -> None:
    """
    Draws a box case around a hitcircle.
    """

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    debug_color = get_color(game, "DEBUG_LINES_2")

    draw_oval(x1, y1, x2, y2,
              fill='',
              outline=debug_color)
    draw_line(cx, cy - aux,
              cx, cy + aux,
              fill=debug_color)
    draw_line(cx - aux, cy,
              cx + aux, cy,
              fill=debug_color)


def draw_lifebars(game: "Game") -> None:
    """
    Draws the lifebar of all relevant entities on the screen.
    """

    all_entities = game.all_bullets + game.enemies + [game.player.satellite]

    for entity in all_entities:

        if not entity:
            continue

        center_x, _ = entity.center
        entity_x1, entity_y1, entity_x2, _ = entity.all_coords
        aux = HEIGHT / 70
        bar_aux_x = (entity_x2 - entity_x1) / 3
        bar_aux_y = HEIGHT / 350

        draw_bar_percentage(game,
                            center_x - bar_aux_x,
                            entity_y1 - aux - bar_aux_y,
                            center_x + bar_aux_x,
                            entity_y1 - aux,
                            entity.health_percentage(),
                            health_colors=True)


def draw_debug_info(game: "Game") -> None:
    """
    Draws debug information about the current game.
    """

    player = game.player
    debug_cons = (HEIGHT // 70)

    debug_text = DEBUG_TEXT.format(
                    player_x1=f"{player.x1:.2f}",
                    player_y1=f"{player.y1:.2f}",
                    player_x2=f"{player.x2:.2f}",
                    player_y2=f"{player.y2:.2f}",

                    hitbox_center=player.center,
                    shooting_cooldown=("Ready!" if game.player.shooting_cooldown.time_is_up()
                                                else game.player.shooting_cooldown.current_time),
                    inv_cooldown=("Ready!" if game.player.invulnerability.time_is_up()
                                           else game.player.invulnerability.current_time),

                    real_time=str(game.real_time.current_time),
                    game_level=game.game_level,
                    power_level=game.player.power_level.name,
                    times_upgraded=game.times_upgraded,

                    health=f"{game.player.hp} / {game.player.max_hp}",
                    hardness=game.player.hardness,
                    speed=game.player.speed,
                    ethereal=game.player.is_ethereal,
                    ability_gauge=(f"{round(game.player.ability_gauge, 3)} / " +
                                   f"{game.player.ability_threshold}"),

                    enemies=len(game.enemies),
                    bullets=len(game.all_bullets),
                    drops=len(game.drops))

    draw_text(debug_text,
              debug_cons,
              debug_cons,
              size=debug_cons,
              fill=get_color(game, "TEXT_COLOR_1"),
              anchor="nw")

    if not DEBUG_LINES:
        return

    draw_debug_lines(game)
    draw_lifebars(game)
