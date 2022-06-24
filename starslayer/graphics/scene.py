"""
Scene Graphics Module.
"""

from typing import TYPE_CHECKING

from ..auxiliar import get_color
from ..consts import (ACTIONS_PATH, BILBY_TANKA_INFO, GAME_VERSION, HEIGHT,
                      SCORES_PATH, STAR_SLAYER_INFO, VIPER_DODGER_INFO, WIDTH)
from ..files import action_description, list_action_keys, load_json
from ..gamelib import draw_line, draw_oval, draw_rectangle, draw_text
from .menus import draw_menu_buttons
from .prompt import draw_attribute_prompt, draw_key_changing_prompt
from .sprites import draw_sprite

if TYPE_CHECKING:
    from ..scene import AnimationsDict
    from ..state import Game


class SceneDrawer:
    """
    Class for drawing extra things on the scene.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initializes an instance of type 'SceneDrawer'.
        """

        self.game: "Game" = game


    def draw_scene(self) -> None:
        """
        Draws in the screen the current scene.
        """

        draw_handler_bg = getattr(SceneDrawer,
                                  f"draw_{self.game.current_scene.id.replace('-', '_')}_bg",
                                  None)

        if draw_handler_bg:
            draw_handler_bg(self)

        self.draw_scene_rear_animations()
        self.draw_scene_buttons()
        self.draw_scene_labels()
        self.draw_scene_sprites()

        draw_handler = getattr(SceneDrawer,
                               f"draw_{self.game.current_scene.id.replace('-', '_')}",
                               None)

        if draw_handler:
            draw_handler(self)

        self.draw_scene_front_animations()


    def draw_scene_buttons(self) -> None:
        """
        Draws in the screen the current scene buttons.
        """

        scene = self.game.current_scene
        for menu in scene.menus:
            draw_menu_buttons(self.game, menu)


    def draw_scene_labels(self) -> None:
        """
        Draws in the screen the current scene labels.
        """

        scene = self.game.current_scene
        for label in scene.labels.values():

            if not "fill" in label.properties or "fill_name" in label.properties:
                fill_name = label.properties.pop("fill_name", "TEXT_COLOR_1")
                label.properties.update(fill=get_color(self.game, fill_name))

            draw_text(label.text, label.x, label.y, **label.properties)

            label.properties.update(fill_name=fill_name)


    def draw_scene_sprites(self) -> None:
        """
        Draws in the screen the current scene sprites.
        """

        scene = self.game.current_scene
        for sprite_properties in scene.sprites.values():
            sprite = sprite_properties.get("sprite")
            draw_sprite(sprite,
                        sprite_properties.get("x1"),
                        sprite_properties.get("y1"),
                        sprite_properties.get("x2"),
                        sprite_properties.get("y2"),
                        sprite_type=sprite_properties.get("spr_type", "BOX"))

            sprite.next_frame()


    def draw_scene_animations(self, anim_dict: "AnimationsDict") -> None:
        """
        Draws animations in the screen, without caring if
        they are rear or front.
        """

        for anim in anim_dict.values():

            fill_name = None
            outline_name = None

            if "fill" not in anim.properties or "fill_name" in anim.properties:
                fill_name = anim.properties.pop("fill_name", "MENU COLOR 1")
                anim.properties.update(fill=get_color(self.game, fill_name))

            if (not anim.is_text and
                ("outline" not in anim.properties or "outline_name" in anim.properties)):
                outline_name = anim.properties.pop("outline_name", "BG COLOR")
                anim.properties.update(outline=get_color(self.game, outline_name))

            anim.animate()
            if self.game.is_time_flowing():
                anim.post_hook()

            if fill_name:
                anim.properties.update(fill_name=fill_name)

            if outline_name:
                anim.properties.update(outline_name=outline_name)


    def draw_scene_rear_animations(self) -> None:
        """
        Draws in the screen the current scene rear animations.
        """

        self.draw_scene_animations(self.game.current_scene.rear_animations)


    def draw_scene_front_animations(self) -> None:
        """
        Draws in the screen the current scene front animations.
        """

        self.draw_scene_animations(self.game.current_scene.front_animations)


    def draw_scene_main(self) -> None:
        """
        Draws the info about the game version.
        """

        x_aux = WIDTH / 75
        y_aux = HEIGHT * 0.995
        size_aux = WIDTH // 75

        draw_text(f"v{GAME_VERSION}",
                  x_aux, y_aux,
                  size=size_aux,
                  anchor="sw")


    def draw_scene_characters(self) -> None:
        """
        Draws information about the characters.
        """

        aux_y = HEIGHT * 0.3
        size_aux = WIDTH // 60

        draw_text(STAR_SLAYER_INFO,
                  WIDTH * 0.17,
                  aux_y,
                  size=size_aux,
                  anchor='n',
                  justify="left",
                  italic=True)

        draw_text(BILBY_TANKA_INFO,
                  WIDTH * 0.5,
                  aux_y,
                  size=size_aux,
                  anchor='n',
                  justify="left",
                  italic=True)

        draw_text(VIPER_DODGER_INFO,
                  WIDTH * 0.85,
                  aux_y,
                  size=size_aux,
                  anchor='n',
                  justify="left",
                  italic=True)


    def draw_scene_controls(self) -> None:
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
                       outline=get_color(self.game, "MENU_OUTLINE_1"),
                       fill=get_color(self.game, "MENU_COLOR_1"))

        action_title = ' '.join(self.game.action_to_show.split('_'))

        draw_text(action_title,
                  int(WIDTH * (5 / 8)),
                  int(HEIGHT * 0.07),
                  fill=get_color(self.game, "TEXT_COLOR_1"),
                  size=(WIDTH // 30),
                  justify='c')

        actions = load_json(ACTIONS_PATH)
        keys_assigned = list_action_keys(self.game.action_to_show, actions)
        description = action_description(self.game.action_to_show, actions)

        if '' in keys_assigned:
            keys_assigned.remove('')

        if description:
            draw_text(description,
                      (WIDTH * 0.3),
                      (HEIGHT * 0.17),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=(WIDTH // 45),
                      justify="left",
                      anchor='nw',
                      italic=True)

        if not keys_assigned:
            draw_text("Action is currently not binded to any key",
                      (WIDTH * (5 / 8)),
                      (HEIGHT * 0.6),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=(WIDTH // 34),
                      justify='c')

        else:
            draw_text("Action is currently bound to the " +
                      f"key{'s' if len(keys_assigned) > 1 else ''}",
                      (WIDTH * (5 / 8)),
                      (HEIGHT * 0.6),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=(WIDTH // 34),
                      justify='c')
            draw_text(" - ".join(keys_assigned),
                      int(WIDTH * (5 / 8)),
                      (HEIGHT * 0.7),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=(HEIGHT // 20),
                      justify='c')

        self.draw_scene_buttons() # re-draw on top

        if self.game.is_on_prompt:

            draw_key_changing_prompt(self.game)


    def draw_scene_profiles(self) -> None:
        """
        Shows the user the current values for each attributes of a
        selected color profile.
        If possible, they can also edit such values.
        """

        theme_name = ' '.join(self.game.selected_theme.split('_'))
        draw_text(f"Current Profile: {theme_name}",
                int(WIDTH * 0.066666),
                (HEIGHT // 9),
                fill=get_color(self.game, "TEXT_COLOR_1"),
                size=(WIDTH // 27),
                anchor='w',
                justify='c')

        for menu in self.game.current_scene.menus:

            if menu.hidden:
                continue

            for button in menu.buttons_on_screen:

                if button.msg not in self.game.color_profile:
                    continue

                width_extra = (button.width // 30)
                height_extra = (button.height // 4)

                oval_x = (button.width // 30)
                oval_y = (button.height // 30)

                btn_x1 = button.x2 - width_extra * 5
                btn_y1 = button.y1 + height_extra
                btn_x2 = button.x2 - width_extra
                btn_y2 = button.y2 - height_extra

                button_color = get_color(self.game, button.msg)
                button_outline = get_color(self.game, "TEXT_COLOR_1")

                if button_color == '':

                    draw_line(btn_x2 - oval_x,
                              btn_y1 + oval_y,
                              btn_x1 + oval_x,
                              btn_y2 - oval_y,
                              fill=button_outline,
                              width=(WIDTH // 375))

                draw_oval(btn_x1, btn_y1, btn_x2, btn_y2,
                          outline=button_outline,
                          fill=button_color)

        if self.game.is_on_prompt:
            draw_attribute_prompt(self.game)


    def draw_scene_about_bg(self) -> None:
        """
        Draws the about message background.
        """

        draw_rectangle(0,
                       0,
                       WIDTH,
                       HEIGHT,
                       width=(HEIGHT // 87),
                       outline=get_color(self.game, "ABOUT_OUTLINE_1"),
                       fill=get_color(self.game, "ABOUT_COLOR_1"))


    def draw_scene_scoreboard_bg(self) -> None:
        """
        Draws the scoreboard background.
        """

        draw_rectangle(0,
                       0,
                       WIDTH,
                       HEIGHT,
                       width=(HEIGHT // 87),
                       outline=get_color(self.game, "SCORES_OUTLINE_1"),
                       fill=get_color(self.game, "SCORES_COLOR_1"))


    def draw_scene_scoreboard(self) -> None:
        """
        Draws the scoreboard of the game.
        """

        scores = load_json(SCORES_PATH).get("scores", None)

        if scores is None:
            return

        area_y1 = HEIGHT * 0.2
        return_aux = HEIGHT * 0.04
        augment_y = ((HEIGHT - (1.2 * return_aux)) - area_y1) / 11 # The 10 scores + the header
        aux_y = augment_y / 2
        font_size = HEIGHT // 45
        line_width = WIDTH // 250

        get_value = lambda val, default : (val if val is not None else default)

        draw_text("Press 'RETURN' to go back",
                  WIDTH / 2,
                  HEIGHT - return_aux,
                  size=font_size)

        if not scores:
            draw_text("Nothing yet...",
                      WIDTH / 2,
                      HEIGHT / 2,
                      size=font_size,
                      italic=True)
            return

        for i, (name, power, level, score) in enumerate([(None, None, None, None)]
                                                        + scores):
            draw_rectangle(WIDTH * 0.01,
                           area_y1 + (augment_y * i) - aux_y,
                           WIDTH * 0.99,
                           area_y1 + (augment_y * i) + aux_y,
                           fill=get_color(self.game, "SCORES_COLOR_2"),
                           outline=get_color(self.game, "SCORES_OUTLINE_1"),
                           width=line_width)

            draw_text((i if i > 0 else ''),
                      WIDTH * 0.05,
                      area_y1 + (augment_y * i),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=font_size,
                      anchor='c')

            draw_line(WIDTH * 0.09,
                      area_y1 + (augment_y * i) - aux_y,
                      WIDTH * 0.09,
                      area_y1 + (augment_y * i) + aux_y,
                      fill=get_color(self.game, "SCORES_OUTLINE_1"),
                      width=line_width)


            draw_text(get_value(name, "PLAYER NAME"),
                      WIDTH * 0.275,
                      area_y1 + (augment_y * i),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=font_size,
                      anchor='c')

            draw_line(WIDTH * 0.45,
                      area_y1 + (augment_y * i) - aux_y,
                      WIDTH * 0.45,
                      area_y1 + (augment_y * i) + aux_y,
                      fill=get_color(self.game, "SCORES_OUTLINE_1"),
                      width=line_width)


            draw_text(get_value(power, "MAX POWER"),
                      WIDTH * 0.55,
                      area_y1 + (augment_y * i),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=font_size,
                      anchor='c')

            draw_line(WIDTH * 0.65,
                      area_y1 + (augment_y * i) - aux_y,
                      WIDTH * 0.65,
                      area_y1 + (augment_y * i) + aux_y,
                      fill=get_color(self.game, "SCORES_OUTLINE_1"),
                      width=line_width)

            draw_text(get_value(level, "MAX LVL"),
                      WIDTH * 0.725,
                      area_y1 + (augment_y * i),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=font_size,
                      anchor='c')

            draw_line(WIDTH * 0.8,
                      area_y1 + (augment_y * i) - aux_y,
                      WIDTH * 0.8,
                      area_y1 + (augment_y * i) + aux_y,
                      fill=get_color(self.game, "SCORES_OUTLINE_1"),
                      width=line_width)


            draw_text(get_value(score, "SCORE"),
                      WIDTH * 0.9,
                      area_y1 + (augment_y * i),
                      fill=get_color(self.game, "TEXT_COLOR_1"),
                      size=font_size,
                      anchor='c')
