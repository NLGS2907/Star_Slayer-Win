"""
Options Scene Module.
"""

from typing import Optional

from ...consts import HEIGHT, OPTIONS_TITLE, WIDTH
from ...graphics.animations import Circumference
from ...utils import Label
from ...utils.menus import OptionsMenu
from ..scene import Scene


class OptionScene(Scene):
    """
    Options Scene. Contains configurable settings.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-options",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'OptionScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        options = OptionsMenu()
        options.show_return = True
        self.add_menu(options)

        self.add_label(Label(WIDTH // 2,
                       HEIGHT // 4,
                       OPTIONS_TITLE,
                       size=(WIDTH // 90),
                       fill_name="TEXT_COLOR_1",
                       justify='c'))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=HEIGHT,
                                         dot_density=150,
                                         dot_speed=-1.0,
                                         from_top=True,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3))
        self.add_animation(Circumference(cx=0.0,
                                         cy=0.0,
                                         dot_density=150,
                                         dot_speed=-1.0,
                                         from_top=True,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=0.0,
                                         dot_density=150,
                                         dot_speed=1.0,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3))
        self.add_animation(Circumference(cx=0.0,
                                         cy=HEIGHT,
                                         dot_density=150,
                                         dot_speed=1.0,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3))
        self.add_animation(Circumference(cx=0.0,
                                         cy=0.0,
                                         dot_speed=0.02,
                                         from_top=True,
                                         initial_radius=300.0,
                                         initial_angle=0.0))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=0.0,
                                         dot_speed=0.02,
                                         initial_radius=300.0,
                                         initial_angle=180.0))
        self.add_animation(Circumference(cx=0.0,
                                         cy=HEIGHT,
                                         dot_speed=0.02,
                                         initial_radius=300.0,
                                         initial_angle=180.0))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=HEIGHT,
                                         dot_speed=0.02,
                                         initial_radius=300.0,
                                         initial_angle=0.0))
