"""
Color Profiles Scene Module.
"""

from typing import Optional

from ...consts import HEIGHT, PROFILES_TITLE, WIDTH
from ...graphics.animations import Circumference, SinusoidalWave
from ...utils import Label
from ...utils.menus import ProfilesMenu, ProfileSubMenu
from ..scene import Scene


class ProfileScene(Scene):
    """
    Porfiles Scene. Contains configurable color profiles.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-profiles",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'ProfileScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        profiles = ProfilesMenu()
        profiles.show_return = True
        self.add_menu(profiles)

        subprofiles = ProfileSubMenu()
        self.add_menu(subprofiles)

        self.add_label(Label(int(WIDTH * 0.893333),
                             (HEIGHT // 15),
                             PROFILES_TITLE,
                             size=(HEIGHT // 235),
                             fill_name="TEXT_COLOR_1",
                             justify='c'))

        self.add_animation(SinusoidalWave(x1=WIDTH * 0.78,
                                          y1=-HEIGHT / 70,
                                          x2=WIDTH * 0.99,
                                          y2=HEIGHT * 1.1,
                                          dot_density=175,
                                          bulge_frequency=2,
                                          wave_speed=1.1,
                                          translation_speed=-30.0,
                                          dot_radius=4))
        self.add_animation(SinusoidalWave(x1=WIDTH * 0.78,
                                          y1=-HEIGHT / 70,
                                          x2=WIDTH * 0.99,
                                          y2=HEIGHT * 1.1,
                                          bulge_frequency=2,
                                          wave_speed=-3.0,
                                          translation_speed=-30.0,
                                          dot_radius=15,
                                          initial_phase=50,
                                          fill_name='',
                                          outline_name="MENU COLOR 2",
                                          width=4))

        self.add_animation(Circumference(cx=0.0,
                                         cy=0.0,
                                         dot_density=150,
                                         dot_speed=-1.0,
                                         from_top=True,
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
