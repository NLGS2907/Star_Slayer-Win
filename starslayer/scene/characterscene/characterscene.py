"""
Characters Selection Scene Module.
"""

from typing import Optional

from ...consts import (BILBY_TANKA_REL_PATH, CHARACTERS_TITLE, HEIGHT,
                       STAR_SLAYER_REL_PATH, VIPER_DODGER_REL_PATH, WIDTH)
from ...sprites import Sprite
from ...utils import Label
from ...utils.menus import CharactersMenu
from ..scene import Scene


class CharacterScene(Scene):
    """
    Characters Selection Scene. It shows once
    when the user must choose a player ship.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-characters",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'CharacterScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        characters = CharactersMenu()
        characters.show_return = True
        self.add_menu(characters)

        self.add_label(Label(WIDTH / 2,
                             HEIGHT / 7,
                             CHARACTERS_TITLE,
                             size=(WIDTH // 100),
                             fill_name="TEXT_COLOR_1",
                             justify='c'))

        width_aux = (WIDTH * 0.08)

        self.add_sprite(Sprite(STAR_SLAYER_REL_PATH),
                        x1=int((WIDTH / 9) * 1.2 - width_aux),
                        y1=int(HEIGHT * 0.6),
                        x2=int((WIDTH / 9) * 1.5 + width_aux),
                        y2=int(HEIGHT * 0.84))
        self.add_sprite(Sprite(BILBY_TANKA_REL_PATH),
                        x1=int((WIDTH / 9) * 2.9 + width_aux),
                        y1=int(HEIGHT * 0.6),
                        x2=int((WIDTH / 9) * 4.5 + width_aux),
                        y2=int(HEIGHT * 0.84))
        self.add_sprite(Sprite(VIPER_DODGER_REL_PATH),
                        x1=int((WIDTH / 9) * 5.9 + width_aux),
                        y1=int(HEIGHT * 0.6),
                        x2=int((WIDTH / 9) * 7.8 + width_aux),
                        y2=int(HEIGHT * 0.84))
