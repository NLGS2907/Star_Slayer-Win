"""
GUI Module.
"""

from typing import TYPE_CHECKING, Optional

from ..auxiliar import get_color
from ..consts import HEIGHT, PLAYABLE_WIDTH, WIDTH
from ..gamelib import draw_line, draw_rectangle, draw_text

if TYPE_CHECKING:
    from ..state import Game
    from ..utils import Button, Menu


def draw_gui(game: "Game") -> None:
    """
    Draws the User Interface.
    """

    aux_cons = (HEIGHT // 70)
    size_aux = (WIDTH // 150)
    prop_name_x = PLAYABLE_WIDTH + aux_cons
    prop_value_x = WIDTH - aux_cons

    draw_rectangle(PLAYABLE_WIDTH,
                   0,
                   WIDTH + 50,
                   HEIGHT + 50,
                   outline=get_color(game, "GUI OUTLINE 1"),
                   fill=get_color(game, "GUI COLOR 1"))

    # Game Score
    draw_text("Score:",
              prop_name_x,
              HEIGHT * 0.03,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='w')
    draw_text(f"{game.score}",
              prop_value_x,
              HEIGHT * 0.03,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='e')

    # Power Level
    draw_text("Power Level:",
              prop_name_x,
              HEIGHT * 0.08,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='w')
    draw_text(game.player.power_level.name,
              prop_value_x,
              HEIGHT * 0.08,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='e')

    # Ability Gauge
    draw_bar_percentage(game,
                        x1=prop_name_x,
                        y1=HEIGHT * 0.64,
                        x2=prop_value_x,
                        y2=HEIGHT * 0.68,
                        percentage=game.player.ability_percentage(),
                        fill_color=(get_color(game, "ABILITY READY")
                                    if game.player.can_use_ability()
                                    else get_color(game, "ABILITY LOADING")))
    draw_rectangle(x1=prop_name_x,
                    y1=HEIGHT * 0.64,
                    x2=prop_value_x,
                    y2=HEIGHT * 0.68,
                    width=size_aux,
                    fill=get_color(game, "GUI OUTLINE 1"),
                    outline=get_color(game, "GUI OUTLINE 2"))

    # Game Level
    draw_text("Current Level:",
              prop_name_x,
              HEIGHT * 0.73,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='w')
    draw_text(game.game_level,
              prop_value_x,
              HEIGHT * 0.73,
              size=(WIDTH // 50),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='e')

    draw_line(prop_name_x,
              HEIGHT * 0.765,
              prop_value_x,
              HEIGHT * 0.765,
              width=(aux_cons // 2),
              fill=get_color(game, "GUI COLOR 2"))

    # Hardness
    draw_text("Current Hardness:",
              prop_name_x,
              HEIGHT * 0.8,
              size=(WIDTH // 62),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='w')
    draw_text(f"{game.player.hardness}",
              prop_value_x,
              HEIGHT * 0.8,
              size=(WIDTH // 62),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='e')

    # Speed
    draw_text("Current Speed:",
              prop_name_x,
              HEIGHT * 0.85,
              size=(WIDTH // 62),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='w')
    draw_text(f"{game.player.speed}",
              prop_value_x,
              HEIGHT * 0.85,
              size=(WIDTH // 62),
              fill=get_color(game, "TEXT COLOR 1"),
              anchor='e')

    # Health
    if not game.player.is_dead():
        draw_bar_percentage(game=game,
                            x1=prop_name_x,
                            y1=HEIGHT * 0.9,
                            x2=prop_value_x,
                            y2=HEIGHT - aux_cons,
                            percentage=game.player.health_percentage(),
                            health_colors=True)
    draw_rectangle(x1=prop_name_x,
                    y1=HEIGHT * 0.9,
                    x2=prop_value_x,
                    y2=HEIGHT - aux_cons,
                    width=size_aux,
                    fill=get_color(game, "GUI OUTLINE 1"),
                    outline=get_color(game, "GUI OUTLINE 2"))


# pylint: disable=invalid-name
def draw_bar_percentage(game: "Game",
                        x1: float,
                        y1: float,
                        x2: float,
                        y2: float,
                        percentage: float,
                        *,
                        horizontal: bool=True,
                        health_colors: bool=False,
                        outline_color: Optional[str]=None,
                        fill_color: Optional[str]=None) -> None:
    """
    Given a rectangle, if draws a part of it given a percentage.
    """

    bar_start, bar_end = ((x1, x2) if horizontal else (y1, y2))

    augment = ((bar_end - bar_start) / 100) * percentage

    if horizontal:
        bar_x1 = bar_start
        bar_y1 = y1
        bar_x2 = bar_start + augment
        bar_y2 = y2

    else:
        bar_x1 = x1
        bar_y1 = bar_start
        bar_x2 = x2
        bar_y2 = bar_start + augment

    if health_colors:
        fill_color = get_color(game, "HEALTH_COLOR_1", percentage)

    elif fill_color is None:
        fill_color = get_color(game, "BAR COLOR 1")

    if outline_color is None:
        outline_color = get_color(game, "GUI OUTLINE 1")

    draw_rectangle(x1=bar_x1,
                   y1=bar_y1,
                   x2=bar_x2,
                   y2=bar_y2,
                   outline=outline_color,
                   fill=fill_color)


def draw_button_hitbox(game: "Game", menu: "Menu", btn: "Button") -> None:
    """
    Draws a single button square.
    """

    x1, y1, x2, y2 = btn.all_coords # pylint: disable=invalid-name
    fill_color = (get_color(game, "BUTTON_COLOR_1")
                  if menu is game.current_scene.selected_menu
                  else get_color(game, "BUTTON_COLOR_3"))

    draw_rectangle(x1, y1, x2, y2,
                   width=((y2 - y1) // 25),
                   outline=get_color(game, "TEXT_COLOR_1"),
                   fill=fill_color,
                   activefill=get_color(game, "BUTTON_COLOR_2"))


def draw_exiting_bar(game: "Game") -> None:
    """
    Draws a mini-bar that shows how much time is left until it exits the game.
    """
    aux_cons = (HEIGHT // 60)
    initial = game.exiting_cooldown.base_time
    current = game.exiting_cooldown.current_time

    draw_rectangle(aux_cons,
                   aux_cons,
                   (10 * aux_cons),
                   (3 * aux_cons),
                   width=(aux_cons // 3),
                   outline=get_color(game, "TEXT_COLOR_1"),
                   fill=get_color(game, "GUI_OUTLINE_1"))

    percentage = 100 - ((current / initial) * 100)
    bar_start = (1.5 * aux_cons)
    bar_end = (9.5 * aux_cons)
    augment = ((bar_end - bar_start) / 100) * percentage

    draw_rectangle(bar_start,
                   (1.5 * aux_cons),
                   bar_start + augment,
                   (2.5 * aux_cons),
                   outline=get_color(game, "GUI_OUTLINE_1"),
                   fill=get_color(game, "TEXT_COLOR_1"))

    how_many_dots = 3
    dots_augment = initial // how_many_dots
    dots_to_use = how_many_dots

    for n in range(how_many_dots, 0, -1):
        if current < n * dots_augment:
            dots_to_use = (how_many_dots + 1) - n

    draw_text(f"Exiting Game{'.' * dots_to_use}",
              (5.5 * aux_cons),
              (4.5 * aux_cons), size=aux_cons, anchor='c')
