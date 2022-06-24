"""
Main Scene Module.
"""

from typing import Optional

from ...consts import GAME_TITLE, HEIGHT, WIDTH
from ...graphics.animations import Circumference, SinusoidalWave
from ...utils import Label
from ...utils.menus import MainMenu
from ..scene import Scene


class MainScene(Scene):
    """
    Main Scene. Contains primarly the main menu.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-main",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'MainScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        self.add_menu(MainMenu())

        self.add_label(Label(WIDTH // 2,
                             HEIGHT // 4,
                             GAME_TITLE,
                             size=(WIDTH // 90),
                             fill_name="TEXT_COLOR_1",
                             justify='c'))
        self.add_animation(SinusoidalWave(x1=WIDTH / 75,
                                          y1=-HEIGHT / 70,
                                          x2=WIDTH / 7.5,
                                          y2=HEIGHT * 1.1,
                                          dot_density=175,
                                          bulge_frequency=3,
                                          dot_radius=4))
        self.add_animation(SinusoidalWave(x1=-WIDTH / 75,
                                          y1=HEIGHT / 70,
                                          x2=WIDTH * 1.1,
                                          y2=HEIGHT / 7,
                                          dot_density=175,
                                          bulge_frequency=3,
                                          translation_speed=60.0,
                                          dot_radius=4,
                                          vertical=False,
                                          initial_phase=65))
        self.add_animation(SinusoidalWave(x1=WIDTH / 75,
                                          y1=HEIGHT * 0.15,
                                          x2=WIDTH / 7.5,
                                          y2=HEIGHT * 0.2,
                                          bulge_frequency=3,
                                          wave_speed=0.0,
                                          translation_speed=30.0,
                                          dot_radius=20,
                                          initial_phase=50,
                                          fill_name='',
                                          outline_name="MENU COLOR 2",
                                          width=4))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=HEIGHT,
                                         dot_density=150,
                                         dot_speed=-1.0,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3))
        self.add_animation(Circumference(cx=WIDTH,
                                         cy=HEIGHT,
                                         dot_density=1,
                                         dot_speed=-0.01,
                                         dot_radius=20.0,
                                         initial_radius=100.0,
                                         max_radius=200.0,
                                         variance_speed=5.3,
                                         fill_name='',
                                         outline_name="MENU COLOR 2",
                                         width=4))
