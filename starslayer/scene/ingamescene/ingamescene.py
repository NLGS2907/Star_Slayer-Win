"""
In-Game Scene.
"""

from typing import Optional

from ...consts import HEIGHT, PLAYABLE_WIDTH, PLAYER_HEALTH_BAR_ANIM, WIDTH
from ...graphics.animations import SinusoidalWave
from ...utils.menus import InGameMenu
from ..scene import Scene


class InGameScene(Scene):
    """
    In-Game Scene. Contains the gameplay
    part of the game.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-in-game",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'InGameScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        ingamemenu = InGameMenu()
        self.add_menu(ingamemenu)

        aux_cons = (HEIGHT / 70)
        aux_cons_2 = (HEIGHT / 175)
        bar_start = PLAYABLE_WIDTH + aux_cons
        bar_end = WIDTH - aux_cons
        bar_anim_x1 = bar_start + aux_cons_2
        bar_anim_y1 = (HEIGHT * 0.902) + aux_cons_2
        bar_anim_x2 = bar_end
        bar_anim_y2 = (HEIGHT * 0.995) - aux_cons - aux_cons_2

        self.add_animation(SinusoidalWave(x1=bar_anim_x1,
                                          y1=bar_anim_y1,
                                          x2=bar_anim_x2,
                                          y2=bar_anim_y2,
                                          vertical=False,
                                          dot_density=45.0,
                                          dot_radius=2.5,
                                          wave_speed=1.5,
                                          bulge_frequency=8,
                                          fill_name="HEALTH_COLOR_2",
                                          outline_name=''),
                           name=f"{PLAYER_HEALTH_BAR_ANIM}_1",
                           is_front=True)
        self.add_animation(SinusoidalWave(x1=bar_anim_x1,
                                          y1=bar_anim_y1,
                                          x2=bar_anim_x2,
                                          y2=bar_anim_y2,
                                          vertical=False,
                                          initial_phase=20.0,
                                          dot_density=45.0,
                                          dot_radius=2.5,
                                          wave_speed=1.5,
                                          bulge_frequency=8,
                                          fill_name="HEALTH_COLOR_2",
                                          outline_name=''),
                           name=f"{PLAYER_HEALTH_BAR_ANIM}_2",
                           is_front=True)
        self.add_animation(SinusoidalWave(x1=bar_anim_x1,
                                          y1=bar_anim_y1,
                                          x2=bar_anim_x2,
                                          y2=bar_anim_y2,
                                          vertical=False,
                                          dot_density=40.0,
                                          dot_radius=2.5,
                                          wave_speed=3.5,
                                          translation_speed=60.0,
                                          bulge_frequency=4,
                                          fill_name="HEALTH_COLOR_2",
                                          outline_name=''),
                           name=f"{PLAYER_HEALTH_BAR_ANIM}_3",
                           is_front=True)
