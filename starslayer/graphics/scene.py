"""
Scene Graphics Module.
"""

from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..consts import HEIGHT, KEYS_PATH, WIDTH
from ..files import list_repeated_keys, load_json
from ..gamelib import draw_line, draw_oval, draw_rectangle, draw_text
from .menus import draw_menu_buttons
from .prompt import draw_attribute_prompt, draw_key_changing_prompt

if TYPE_CHECKING:

    from ..state import Game


def draw_scene(game: "Game") -> None:
    """
    Draws in the screen the current scene.
    """

    draw_scene_buttons(game)
    draw_scene_labels(game)

    match game.current_scene.id:

        case "scene-controls":

            draw_changeable_buttons_text(game)

        case "scene-profiles":

            draw_profile_attributes(game)


def draw_scene_buttons(game: "Game") -> None:
    """
    Draws in the screen the current scene buttons.
    """

    scene = game.current_scene
    for menu in scene.menus:
        draw_menu_buttons(game, menu)


def draw_scene_labels(game: "Game") -> None:
    """
    Draws in the screen the current scene labels.
    """

    scene = game.current_scene
    for label in scene.labels:
        color_name = label.properties.pop("color_name", "TEXT_COLOR_1")
        label.properties.update(fill=get_color(game, color_name))
        draw_text(label.text, label.x, label.y, **label.properties)


def draw_changeable_buttons_text(game: "Game") -> None:
    """
    Draws the information of the action and its assigned keys.
    If possible, it also allows it to edit said information.
    """

    aux_cons = (HEIGHT // 70)

    draw_rectangle((WIDTH // 4) + aux_cons,
                   aux_cons,
                   WIDTH - aux_cons,
                   HEIGHT - aux_cons,
                   width=(HEIGHT // 87),
                   outline=get_color(game, "MENU_OUTLINE_1"),
                   fill=get_color(game, "MENU_COLOR_1"))
    draw_text(game.action_to_show,
              int(WIDTH * (5 / 8)),
              (HEIGHT // 8),
              fill=get_color(game, "TEXT_COLOR_1"),
              size=(WIDTH // 10),
              justify='c')

    keys_assigned = list_repeated_keys(game.action_to_show, load_json(KEYS_PATH))

    if '' in keys_assigned:

        keys_assigned.remove('')

    if not keys_assigned:

        draw_text("Action is currently not binded to any key",
                  (WIDTH * (5 / 8)),
                  (HEIGHT / 3.5),
                  fill=get_color(game, "TEXT_COLOR_1"),
                  size=(WIDTH // 34),
                  justify='c')

    else:

        draw_text(" - ".join(keys_assigned),
                  int(WIDTH * (5 / 8)),
                  int(HEIGHT / 2.5),
                  fill=get_color(game, "TEXT_COLOR_1"),
                  size=(HEIGHT // 20),
                  justify='c')

        draw_text(f"Action is currently bound to the key{'s' if len(keys_assigned) > 1 else ''}",
                  (WIDTH * (5 / 8)),
                  (HEIGHT / 3.5),
                  fill=get_color(game, "TEXT_COLOR_1"),
                  size=(WIDTH // 34),
                  justify='c')

    draw_scene_buttons(game) # re-draw on top

    if game.is_on_prompt:

        draw_key_changing_prompt(game)


def draw_profile_attributes(game: "Game") -> None:
    """
    Shows the user the current values for each attributes of a
    selected color profile.
    If possible, they can also edit such values.
    """

    theme_name = ' '.join(game.selected_theme.split('_'))
    draw_text(f"Current Profile: {theme_name}",
              int(WIDTH * 0.066666),
              (HEIGHT // 9),
              fill=get_color(game, "TEXT_COLOR_1"),
              size=(WIDTH // 27),
              anchor='w',
              justify='c')

    for menu in game.current_scene.menus:

        if menu.hidden:
            continue

        for button in menu.buttons_on_screen:

            if button.msg not in game.color_profile:
                continue

            width_extra = (button.width // 30)
            height_extra = (button.height // 4)

            oval_x = (button.width // 30)
            oval_y = (button.height // 30)

            btn_x1 = button.x2 - width_extra * 5
            btn_y1 = button.y1 + height_extra
            btn_x2 = button.x2 - width_extra
            btn_y2 = button.y2 - height_extra

            button_color = game.color_profile.get(button.msg, None)
            button_outline = get_color(game, "TEXT_COLOR_1")
        
            if button_color == '':

                draw_line(btn_x2 - oval_x,
                          btn_y1 + oval_y,
                          btn_x1 + oval_x,
                          btn_y2 - oval_y,
                          fill=button_outline, width=(WIDTH // 375))

            draw_oval(btn_x1, btn_y1, btn_x2, btn_y2,
                      outline=button_outline,
                      fill=button_color)

    if game.is_on_prompt:

        draw_attribute_prompt(game)
