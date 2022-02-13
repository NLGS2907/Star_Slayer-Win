"""
Graphics Module. Draws anything that the player
sees on screen.
"""

from ..lib import gamelib
from ..files import files
from ..state.game_state import Game
from ..controls.game_controls import GameControls as Controls
from ..utils.utils import Button, Menu
from ..selector.selector import ColorSelector
from ..characters.characters import Ship
from ..constants.consts import DEBUG_TEXT, KEYS_PATH, PROFILES_DELETER, PROFILES_TITLE, WIDTH, HEIGHT, GUI_SPACE, DEBUG_LINES, PROFILES_CHANGER, SPECIAL_CHARS, GAME_TITLE, OPTIONS_TITLE, CONTROLS_TITLE


def get_color(game: Game, name: str) -> str:
    """
    Wrapper for searching colors in game profile.
    """

    return game.color_profile.get('_'.join(name.split()))


def draw_background(game: Game) -> None:
    """
    Draws the background of the game (duh).
    """

    gamelib.draw_rectangle(0, 0, WIDTH, HEIGHT, fill=get_color(game, "BG_COLOR"))


def draw_GUI(game: Game) -> None:
    """
    Draws the User Interface.
    """

    aux_cons = (HEIGHT // 70)

    gamelib.draw_rectangle(WIDTH - GUI_SPACE, 0, WIDTH, HEIGHT, outline=get_color(game, "GUI_OUTLINE_1"), fill=get_color(game, "GUI_COLOR_1"))

    # Power Level
    gamelib.draw_text("Current Power Level:", WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.73, size=(WIDTH // 50), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text(f"{game.power_level}", WIDTH - aux_cons, HEIGHT * 0.73, size=(WIDTH // 50), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    gamelib.draw_line(WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.765, WIDTH - aux_cons, HEIGHT * 0.765, width=(aux_cons // 2), fill=get_color(game, "GUI_COLOR_2"))

    # Hardness
    gamelib.draw_text("Current Hardness:", WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.8, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text(f"{game.player.hardness}", WIDTH - aux_cons, HEIGHT * 0.8, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    # Speed
    gamelib.draw_text("Current Speed:", WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.85, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text(f"{game.player.speed}", WIDTH - aux_cons, HEIGHT * 0.85, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    # Health
    gamelib.draw_text("Remaining health:", WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.9, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text(f"{game.player.hp}  /  {game.player.max_hp}", WIDTH - aux_cons, HEIGHT * 0.9, size=(WIDTH // 62), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    # Health Bar
    gamelib.draw_rectangle(WIDTH - GUI_SPACE + aux_cons, HEIGHT * 0.93, WIDTH - aux_cons, HEIGHT - aux_cons, width=(aux_cons // 2), outline=get_color(game, "GUI_OUTLINE_2"), fill=get_color(game, "GUI_OUTLINE_1"))

    if not game.player.has_no_health():

        hp_percentage = (game.player.hp / game.player.max_hp) * 100

        bar_start = WIDTH - GUI_SPACE + (2 * aux_cons)
        bar_end = WIDTH - (2 * aux_cons)

        augment = ((bar_end - bar_start) / 100) * hp_percentage

        gamelib.draw_rectangle(bar_start, HEIGHT * 0.945, bar_start + augment, HEIGHT - (2 * aux_cons), outline=get_color(game, "GUI_OUTLINE_1"), fill=get_color(game, "GUI_COLOR_3"))


def draw_menus(game: Game, controls: Controls) -> None:
    """
    Draws in the screen the current selected menu.
    """

    menu = game.current_menu

    draw_menu_buttons(game, menu)

    if menu is game.main_menu:

        gamelib.draw_text(GAME_TITLE, WIDTH // 2, HEIGHT // 4, size=(WIDTH // 90), fill=get_color(game, "TEXT_COLOR_1"), justify='c')

    elif menu is game.options_menu:

        gamelib.draw_text(OPTIONS_TITLE, WIDTH // 2, HEIGHT // 4, size=(WIDTH // 90), fill=get_color(game, "TEXT_COLOR_1"), justify='c')

    elif menu is game.controls_menu:

        gamelib.draw_text(CONTROLS_TITLE, int(WIDTH * 0.130666), (HEIGHT // 15), size=(HEIGHT // 235), fill=get_color(game, "TEXT_COLOR_1"), justify='c')
        draw_changeable_buttons(game, controls)

    elif menu is game.profiles_menu:

        gamelib.draw_text(PROFILES_TITLE, int(WIDTH * 0.893333), (HEIGHT // 15), size=(HEIGHT // 235), fill=get_color(game, "TEXT_COLOR_1"), justify='c')
        draw_profile_attributes(game, controls)


def draw_changeable_buttons(game: Game, controls: Controls) -> None:
    """
    Draws the information of the action and its assigned keys.
    If possible, it also allows it to edit said information.
    """

    aux_cons = (HEIGHT // 70)

    gamelib.draw_rectangle((WIDTH // 4) + aux_cons, aux_cons, WIDTH - aux_cons, HEIGHT - aux_cons, width=(HEIGHT // 87), outline=get_color(game, "MENU_OUTLINE_1"), fill=get_color(game, "MENU_COLOR_1"))
    gamelib.draw_text(game.action_to_show, int(WIDTH * (5 / 8)), (HEIGHT // 8), fill=get_color(game, "TEXT_COLOR_1"), size=(WIDTH // 10), justify='c')

    keys_assigned = files.list_repeated_keys(game.action_to_show, files.load_json(KEYS_PATH))

    if '' in keys_assigned: keys_assigned.remove('')

    if not keys_assigned:

        gamelib.draw_text("Action is currently not binded to any key", (WIDTH * (5 / 8)), (HEIGHT / 3.5), fill=get_color(game, "TEXT_COLOR_1"), size=(WIDTH // 34), justify='c')

    else:

        gamelib.draw_text(' - '.join(keys_assigned),
                        int(WIDTH * (5 / 8)), int(HEIGHT / 2.5), fill=get_color(game, "TEXT_COLOR_1"), size=(HEIGHT // 20), justify='c')

        gamelib.draw_text(f"Action is currently bound to the key{'s' if len(keys_assigned) > 1 else ''}", (WIDTH * (5 / 8)), (HEIGHT / 3.5), fill=get_color(game, "TEXT_COLOR_1"), size=(WIDTH // 34), justify='c')

    draw_menu_buttons(game, game.sub_menu)

    if controls.is_on_prompt:

        draw_key_changing_prompt(game)


def draw_key_changing_prompt(game: Game) -> None:
    """
    It draws a prompt in the screen that warns the player that a key is
    being changed and they need to press any key to try to bind it.
    """

    aux_cons = (HEIGHT // 10)

    gamelib.draw_rectangle(aux_cons, (HEIGHT // 2) - aux_cons, WIDTH - aux_cons, (HEIGHT // 2) + aux_cons, width=(HEIGHT // 90), outline=get_color(game, "MENU_OUTLINE_1"), fill=get_color(game, "MENU_COLOR_1"))
    gamelib.draw_text(f"Press any key to bind it to '{game.action_to_show}'", (WIDTH // 2), (HEIGHT // 2), fill=get_color(game, "TEXT_COLOR_1"), size=(HEIGHT // 30), justify='c')


def draw_profile_attributes(game: Game, controls: Controls) -> None:
    """
    Shows the user the current values for each attributes of a
    selected color profile.
    If possible, they can also edit such values.
    """

    theme_name = ' '.join(game.selected_theme.split('_'))
    gamelib.draw_text(f"Current Profile: {theme_name}", int(WIDTH * 0.066666), (HEIGHT // 9), fill=get_color(game, "TEXT_COLOR_1"), size=(WIDTH // 27), anchor='w', justify='c')

    draw_menu_buttons(game, game.sub_menu)

    for button in game.sub_menu.buttons_on_screen:

        if button.msg in SPECIAL_CHARS:

            continue

        width_extra = (button.width // 30)
        height_extra = (button.height // 4)

        oval_x = (button.width // 30)
        oval_y = (button.height // 30)

        x1 = button.x2 - width_extra * 5
        y1 = button.y1 + height_extra
        x2 = button.x2 - width_extra
        y2 = button.y2 - height_extra

        button_color = game.color_profile.get(button.msg, None)
        button_outline = get_color(game, "TEXT_COLOR_1")

        if button.msg not in [PROFILES_CHANGER, PROFILES_DELETER]:

            if button_color == '':

                gamelib.draw_line(x2 - oval_x,
                                  y1 + oval_y,
                                  x1 + oval_x,
                                  y2 - oval_y,
                                  fill=button_outline, width=(WIDTH // 375))

            gamelib.draw_oval(x1, y1, x2, y2,
                              outline=button_outline,
                              fill=button_color)

    if controls.is_on_prompt:

        draw_attribute_prompt(game)


def draw_attribute_prompt(game: Game) -> None:
    """
    Draws a prompt that asks the user to select a new color value
    for the attribute selected.
    """

    selector: ColorSelector = game.color_selector
    x1, y1, x2, y2 = selector.area

    gamelib.draw_rectangle(x1, y1, x2, y2,
                           width=(WIDTH // 375),
                           outline=get_color(game, "MENU_OUTLINE_1"),
                           fill=get_color(game, "MENU_COLOR_1"))

    draw_color_table(game)
    draw_hue_bar(game)
    draw_selector_details(game)
    draw_selector_buttons(game)


def draw_color_table(game: Game) -> None:
    """
    Draws the color table of the selector prompt.
    """

    selector = game.color_selector
    p_x1, p_y1, _, _ = selector.palette_area
    selection_width = (WIDTH // 160)

    for row in range(selector.rows):

        for col in range(selector.cols):

            gamelib.draw_rectangle(p_x1 + (col * selector.augment_x),
                                   p_y1 + (row * selector.augment_y),
                                   p_x1 + ((col + 1) * selector.augment_x),
                                   p_y1 + ((row + 1) * selector.augment_y),
                                   outline='',
                                   fill=selector.color_palette[(col, row)])

    extra_x = (WIDTH // 200)
    extra_y = (HEIGHT // 180)

    if selector.selection and not selector.is_transparent:

        i, j = selector.selection

        gamelib.draw_rectangle(p_x1 + i * (selector.augment_x) - extra_x,
                               p_y1 + j * (selector.augment_y) - extra_y,
                               p_x1 + (i + 1) * (selector.augment_x) + extra_x,
                               p_y1 + (j + 1) * (selector.augment_y) + extra_y,
                               width=selection_width,
                               outline=get_color(game, "TEXT_COLOR_1"),
                               fill=selector.get_selected_color())


def draw_hue_bar(game: Game) -> None:
    """
    Draws he hue bar of the selector prompt.
    """

    selector = game.color_selector
    hue_x1, hue_y1, _, hue_y2 = selector.hue_bar_area
    hue_augment = selector.hue_augment

    for i, (_, hue) in enumerate(selector.hue_bar):

        gamelib.draw_rectangle(hue_x1 + (i * hue_augment),
                               hue_y1,
                               hue_x1 + ((i + 1) * hue_augment),
                               hue_y2,
                               outline='',
                               fill=hue)

    hue_i = selector.hue_index
    _, hue_color = selector.hue_bar[hue_i]
    extra_x = (WIDTH // 150)
    extra_y = (HEIGHT // 140)

    if not selector.is_transparent:

        gamelib.draw_rectangle(hue_x1 + (hue_i * hue_augment) - extra_x,
                               hue_y1 - extra_y,
                               hue_x1 + ((hue_i + 1) * hue_augment) + extra_x,
                               hue_y2 + extra_y,
                               width=int(extra_x * 0.6),
                               outline=get_color(game, "TEXT_COLOR_1"),
                               fill=hue_color)


def draw_button_hitbox(game: Game, btn: Button) -> None:
    """
    Draws a single button square.
    """

    x1, y1, x2, y2 = btn.all_coords

    gamelib.draw_rectangle(x1, y1, x2, y2,
                            width=((y2 - y1) // 25),
                            outline=get_color(game, "TEXT_COLOR_1"),
                            fill=get_color(game, "BUTTON_COLOR_1"),
                            activefill=get_color(game, "BUTTON_COLOR_2"))


def draw_selector_buttons(game: Game) -> None:
    """
    Draws on the screen the buttons that the color selector has.
    """

    selector = game.color_selector

    for button in selector.buttons:

        draw_button_hitbox(game, button)

        cx, cy = button.center
        gamelib.draw_text(' '.join(button.msg.split('_')),
                        cx, cy,
                        size=int((button.y2 - button.y1) // (2 if button.msg in SPECIAL_CHARS else 4)),
                        fill=get_color(game, "TEXT_COLOR_1"),
                        justify='c')


def draw_selector_details(game: Game) -> None:
    """
    Draws details of the selector like the color selected,
    or the RGB indicator.
    """

    selector = game.color_selector

    aux_x = (WIDTH // 75)
    aux_y = (HEIGHT // 70)
    aux_font = (WIDTH // 150)

    x1 = selector.x2 - (WIDTH * 0.293333)
    y1 = selector.hue_bar_area[3] + (HEIGHT * 0.021428)
    x2 = selector.p_x2
    y2 = selector.y2 - (HEIGHT * 0.094285)

    gamelib.draw_rectangle(selector.x1 + (aux_x * 0.5),
                           y1 - (aux_y * 0.5),
                           selector.x2 - (aux_x * 0.5),
                           selector.x2 - (aux_y * 0.5),
                           width=(aux_x // 10),
                           outline=get_color(game, "MENU_OUTLINE_1"),
                           fill=get_color(game, "MENU_COLOR_2"))

    # Invisible Color
    inv_x1, inv_y1, inv_x2, inv_y2 = selector.inv_color_area
    oval_x = ((inv_x2 - inv_x1) // 7)
    oval_y = ((inv_y2 - inv_y1) // 7)

    gamelib.draw_oval(inv_x1, inv_y1, inv_x2, inv_y2,
                      width=((aux_x // 2) if selector.is_transparent else (aux_x // 5)),
                      outline=get_color(game, "TEXT_COLOR_1"),
                      fill='')

    gamelib.draw_line(inv_x2 - oval_x,
                      inv_y1 + oval_y,
                      inv_x1 + oval_x,
                      inv_y2 - oval_x,
                      width=(aux_x // 5),
                      fill=get_color(game, "TEXT_COLOR_1"))

    # Color Preview
    gamelib.draw_rectangle(x1, y1, x2, y2,
                           outline='',
                           fill=selector.get_selected_color())

    red, green, blue = (("N/A", "N/A", "N/A") if selector.is_transparent else selector.hex_to_dec(selector.get_selected_color()))

    upper_rgb = y1 + (y2 - y1) * 0.2
    bottom_rgb = upper_rgb + (3 * aux_y)
    middle_rgb = (upper_rgb + bottom_rgb) / 2

    # --- RGB --- #

    gamelib.draw_rectangle(selector.x1 + (aux_x * 0.7),
                           upper_rgb - (aux_y * 0.5),
                           selector.x1 + (36.5 * aux_x),
                           bottom_rgb + (aux_y * 0.5),
                           width=(aux_x // 5),
                           outline=get_color(game, "MENU_OUTLINE_1"),
                           fill='')

    gamelib.draw_line(selector.x1 + (9 * aux_x),
                      upper_rgb - (aux_y * 0.5),
                      selector.x1 + (9 * aux_x),
                      bottom_rgb + (aux_y * 0.5),
                      width=(aux_x // 3),
                      fill=get_color(game, "MENU_OUTLINE_1"))

    gamelib.draw_line(selector.x1 + (18.3 * aux_x),
                      upper_rgb - (aux_y * 0.5),
                      selector.x1 + (18.3 * aux_x),
                      bottom_rgb + (aux_y * 0.5),
                      width=(aux_x // 5),
                      fill=get_color(game, "MENU_OUTLINE_1"))

    gamelib.draw_line(selector.x1 + (27.3 * aux_x),
                      upper_rgb - (aux_y * 0.5),
                      selector.x1 + (27.3 * aux_x),
                      bottom_rgb + (aux_y * 0.5),
                      width=(aux_x // 5),
                      fill=get_color(game, "MENU_OUTLINE_1"))

    gamelib.draw_text("RGB",
                      selector.x1 + aux_x, middle_rgb,
                      size=(5 * aux_font),
                      anchor='w',
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')

    # Red
    gamelib.draw_oval(selector.x1 + (10 * aux_x),
                      upper_rgb,
                      selector.x1 + (13 * aux_x),
                      bottom_rgb,
                      width=(aux_x // 5),
                      outline=get_color(game, "TEXT_COLOR_1"),
                      fill="#ff0000")

    gamelib.draw_text(red,
                      selector.x1 + (16 * aux_x), middle_rgb,
                      size=(3 * aux_font),
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')

    # Green
    gamelib.draw_oval(selector.x1 + (19 * aux_x),
                      upper_rgb,
                      selector.x1 + (22 * aux_x),
                      bottom_rgb,
                      width=(aux_x // 5),
                      outline=get_color(game, "TEXT_COLOR_1"),
                      fill="#00ff00")

    gamelib.draw_text(green,
                      selector.x1 + (25 * aux_x), middle_rgb,
                      size=(3 * aux_font),
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')

    # Blue
    gamelib.draw_oval(selector.x1 + (28 * aux_x),
                      upper_rgb,
                      selector.x1 + (31 * aux_x),
                      bottom_rgb,
                      width=(aux_x // 5),
                      outline=get_color(game, "TEXT_COLOR_1"),
                      fill="#0000ff")

    gamelib.draw_text(blue,
                      selector.x1 + (34 * aux_x), middle_rgb,
                      size=(3 * aux_font),
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')

    # --- HSV --- #

    middle_hsv = (y1 + (y2 - y1) * 0.737373)

    gamelib.draw_rectangle(selector.x1 + (aux_x * 0.7),
                           middle_hsv - (2 * aux_y),
                           selector.x1 + (36.5 * aux_x),
                           middle_hsv + (2 * aux_y),
                           width=(aux_x // 5),
                           outline=get_color(game, "MENU_OUTLINE_1"),
                           fill='')

    gamelib.draw_line(selector.x1 + (9 * aux_x),
                      middle_hsv - (2 * aux_y),
                      selector.x1 + (9 * aux_x),
                      middle_hsv + (2 * aux_y),
                      width=(aux_x // 3),
                      fill=get_color(game, "MENU_OUTLINE_1"))

    gamelib.draw_text("HSV",
                      selector.x1 + aux_x, middle_hsv,
                      size=(5 * aux_font),
                      anchor='w',
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')

    i, j = selector.selection
    cols, rows = selector.cols, selector.rows

    hue = int(selector.hue_bar[selector.hue_index][0] * 360)
    saturation = int(i * (1.0 / cols) * 100)
    value = 100 - int(j * (1.0 / rows) * 100)

    gamelib.draw_text(("N/A   -   N/A   -   N/A" if selector.is_transparent else f"{hue}°  -  {saturation}%  -  {value}%"),
                      selector.x1 + (10 * aux_x), middle_hsv,
                      size=(4 * aux_font),
                      anchor='w',
                      fill=get_color(game, "TEXT_COLOR_1"),
                      justify='c')


def draw_menu_buttons(game: Game, menu: Menu) -> None:
    """
    Draws all the buttons of a given menu.
    """

    for button in menu.buttons_on_screen:

        draw_button_hitbox(game, button)

        if button.msg:

            x_coord, y_coord = button.center
            btn_anchor = menu.button_anchor

            if button.msg in SPECIAL_CHARS or button.msg in [PROFILES_CHANGER, PROFILES_DELETER]:
            
                btn_anchor = 'c'

            else:

                if menu.button_anchor == 'c':

                    x_coord += menu.offset_x
                    y_coord += menu.offset_y

                else:

                    width_extra = (button.width // 50)
                    height_extra = (button.height // 50)

                    if 'n' in menu.button_anchor:

                        y_coord = button.y1 + height_extra

                    elif 's' in menu.button_anchor:

                        y_coord = button.y2 - height_extra

                    if 'w' in menu.button_anchor:

                        x_coord = button.x1 + width_extra

                    elif 'e' in menu.button_anchor:

                        x_coord = button.x2 - width_extra

            gamelib.draw_text(' '.join(button.msg.split('_')),
                              x_coord, y_coord,
                              size=int((button.y2 - button.y1) // (2 if button.msg in SPECIAL_CHARS else 4)),
                              fill=get_color(game, "TEXT_COLOR_1"),
                              anchor=btn_anchor,
                              justify='c')


def draw_ship(game: Game, ship: Ship, which_one: int=0) -> None:
    """
    Draws the sprite of a ship.

    'which_one' refers to which frame to draw.
    """

    if ship.sprites == None:

        gamelib.draw_rectangle(ship.x1, ship.y1, ship.x2, ship.y2, fill=get_color(game, "DEBUG_LINES_1"))

    else:

        gamelib.draw_image(ship.sprites[which_one], ship.x1, ship.y1)


def draw_bullets(game: Game) -> None:
    """
    Draws every single bullet currently on screen.
    """

    bullets = game.bullets

    for bullet in bullets:

        gamelib.draw_oval(bullet.x1, bullet.y1, bullet.x2, bullet.y2, outline=get_color(game, "GUI_OUTLINE_1"), fill=get_color(game, "TEXT_COLOR_1"))


def draw_debug_info(game: Game) -> None:
    """
    Draws debug information about the current game.
    """

    if game.show_debug_info:

        player = game.player
        cx, cy = player.center
        debug_cons = (HEIGHT // 70)

        debug_text = DEBUG_TEXT.format(player_x1=player.x1,
                                       player_y1=player.y1,
                                       player_x2=player.x2,
                                       player_y2=player.y2,

                                       hitbox_center=f"({cx}, {cy})",
                                       shooting_cooldown=("Ready!" if game.shooting_cooldown.is_zero_or_less() else game.shooting_cooldown.current_time),
                                       inv_cooldown=("Ready!" if game.invulnerability.is_zero_or_less() else game.invulnerability.current_time),

                                       level_timer=game.level_timer.current_time,
                                       power_level=game.power_level,

                                       health=game.player.hp,
                                       hardness=game.player.hardness,
                                       speed=game.player.speed,

                                       enemies=len(game.enemies),
                                       bullets=len(game.bullets))

        gamelib.draw_text(debug_text, debug_cons, debug_cons, size=debug_cons, fill=get_color(game, "TEXT_COLOR_1"), anchor="nw")

        if DEBUG_LINES:

            draw_debug_lines(game)

            aux = (WIDTH // 30)

            for bullet in game.bullets:

                x, y = bullet.center
                gamelib.draw_line(x, y - aux, x, y + aux, fill=get_color(game, "DEBUG_LINES_2"))
                gamelib.draw_line(x - aux, y, x + aux, y, fill=get_color(game, "DEBUG_LINES_2"))

            for enem in game.enemies:

                aux2 = int(aux * 1.67)

                x, y = enem.center
                gamelib.draw_line(x, y - aux2, x, y + aux2, fill=get_color(game, "DEBUG_LINES_2"))
                gamelib.draw_line(x - aux2, y, x + aux2, y, fill=get_color(game, "DEBUG_LINES_2"))


def draw_debug_lines(game: Game) -> None:
    """
    Marks the limit of hitboxes and additional debug info through lines.
    """

    player = game.player
    cx, cy = player.center
    aux = (WIDTH // 150)

    # Upper Lines
    gamelib.draw_line(cx, 0, cx, player.y1, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(cx - aux, player.y1, cx + aux, player.y1, fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom Lines
    gamelib.draw_line(cx, player.y2, cx, HEIGHT, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(cx - aux, player.y2, cx + aux, player.y2, fill=get_color(game, "DEBUG_LINES_1"))

    # Left Lines
    gamelib.draw_line(0, cy, player.x1, cy, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x1, cy - aux, player.x1, cy + aux, fill=get_color(game, "DEBUG_LINES_1"))

    # Right Lines
    gamelib.draw_line(player.x2, cy, WIDTH, cy, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x2, cy - aux, player.x2, cy + aux, fill=get_color(game, "DEBUG_LINES_1"))


    # Upper-Left Corner
    gamelib.draw_line(player.x1, player.y1, player.x1 + (aux * 2), player.y1, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x1, player.y1, player.x1, player.y1 + (aux * 2), fill=get_color(game, "DEBUG_LINES_1"))

    # Upper-Right Corner
    gamelib.draw_line(player.x2, player.y1, player.x2 - (aux * 2), player.y1, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x2, player.y1, player.x2, player.y1 + (aux * 2), fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom-Left Corner
    gamelib.draw_line(player.x1, player.y2, player.x1 + (aux * 2), player.y2, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x1, player.y2, player.x1, player.y2 - (aux * 2), fill=get_color(game, "DEBUG_LINES_1"))

    # Bottom-Right Corner
    gamelib.draw_line(player.x2, player.y2, player.x2 - (aux * 2), player.y2, fill=get_color(game, "DEBUG_LINES_1"))
    gamelib.draw_line(player.x2, player.y2, player.x2, player.y2 - (aux * 2), fill=get_color(game, "DEBUG_LINES_1"))


def draw_about(game: Game) -> None:
    """
    Shows the information about the people involved in this game.
    """

    aux_cons = (WIDTH // 10)

    gamelib.draw_rectangle(0, 0, WIDTH, HEIGHT, width=(HEIGHT // 87), outline=get_color(game, "ABOUT_OUTLINE_1"), fill=get_color(game, "ABOUT_COLOR_1"))

    gamelib.draw_text("SO, ABOUT\nTHIS GAME...", (WIDTH // 2), (HEIGHT // 6), size=(HEIGHT // 12), fill=get_color(game, "TEXT_COLOR_1"), justify='c')

    # Pixel-Art
    gamelib.draw_text("Pixel-Art:", aux_cons, HEIGHT * 0.4, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text("Franco 'NLGS' Lighterman", WIDTH - aux_cons, HEIGHT * 0.4, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    # Coding
    gamelib.draw_text("Coding:", aux_cons, HEIGHT * 0.6, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text("Franco 'NLGS' Lighterman", WIDTH - aux_cons, HEIGHT * 0.6, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    # Gamelib
    gamelib.draw_text("Gamelib Library:", aux_cons, HEIGHT * 0.8, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='w')
    gamelib.draw_text("Diego Essaya", WIDTH - aux_cons, HEIGHT * 0.8, size=(HEIGHT // 30), fill=get_color(game, "TEXT_COLOR_1"), anchor='e')

    gamelib.draw_text("Press 'RETURN' to return", (WIDTH // 2), HEIGHT - 20, size=(HEIGHT // 50), fill=get_color(game, "TEXT_COLOR_1"), justify='c')


def draw_exiting_bar(game: Game, controls: Controls) -> None:
    """
    Draws a mini-bar that shows how much time is left until it exits the game.
    """
    aux_cons = (HEIGHT // 60)

    gamelib.draw_rectangle(aux_cons, aux_cons, (10 * aux_cons), (3 * aux_cons), width=(aux_cons // 3), outline=get_color(game, "TEXT_COLOR_1"), fill=get_color(game, "GUI_OUTLINE_1"))

    percentage = 100 - ((controls.exiting_cooldown.current_time / controls.exiting_cooldown.initial_time) * 100)

    bar_start = (1.5 * aux_cons)
    bar_end = (9.5 * aux_cons)

    augment = ((bar_end - bar_start) / 100) * percentage

    gamelib.draw_rectangle(bar_start, (1.5 * aux_cons), bar_start + augment, (2.5 * aux_cons), outline=get_color(game, "GUI_OUTLINE_1"), fill=get_color(game, "TEXT_COLOR_1"))

    gamelib.draw_text("Exiting Game...", (5.5 * aux_cons), (4.5 * aux_cons), size=aux_cons, anchor='c')


def draw_screen(game: Game, controls: Controls) -> None:
    """
    Draws the entirety of the elements on the screen.
    """
    draw_background(game)
    draw_bullets(game)
    draw_debug_info(game)

    if game.is_in_game:

        draw_ship(game, game.player, (0 if game.invulnerability.is_zero_or_less() else 1))

        for enem in game.enemies:

            draw_ship(game, enem)

        draw_GUI(game)

    elif controls.show_about:

        draw_about(game)

    else:

        draw_menus(game, controls)

    if controls.exiting:

        draw_exiting_bar(game, controls)
