"""
Controls Scene Module.
"""

from typing import Optional

from ...consts import CONTROLS_TITLE, HEIGHT, WIDTH
from ...graphics.animations import SinusoidalWave
from ...utils import Label
from ...utils.menus import ControlsMenu, ControlSubMenu
from ..scene import Scene


class ControlScene(Scene):
    """
    Controls Scene. Contains configurable controls.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-controls",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'ControlScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        controls = ControlsMenu()
        controls.show_return = True
        self.add_menu(controls)

        subcontrols = ControlSubMenu()
        self.add_menu(subcontrols)

        self.add_label(Label(int(WIDTH * 0.130666),
                             (HEIGHT // 15),
                             CONTROLS_TITLE,
                             size=(HEIGHT // 235),
                             fill_name="TEXT_COLOR_1",
                             justify='c'))

        self.add_animation(SinusoidalWave(x1=WIDTH / 75,
                                          y1=-HEIGHT / 70,
                                          x2=WIDTH * 0.25,
                                          y2=HEIGHT * 1.1,
                                          dot_density=200,
                                          bulge_frequency=4,
                                          dot_radius=4))
        self.add_animation(SinusoidalWave(x1=WIDTH / 75,
                                          y1=-HEIGHT / 70,
                                          x2=WIDTH * 0.25,
                                          y2=HEIGHT * 1.1,
                                          bulge_frequency=4,
                                          wave_speed=2.0,
                                          dot_radius=15,
                                          initial_phase=50,
                                          fill_name='',
                                          outline_name="MENU COLOR 2",
                                          width=4))
