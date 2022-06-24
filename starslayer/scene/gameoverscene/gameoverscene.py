"""
Game Over Scene Module.
"""

from typing import Optional

from ...consts import GAMEOVER_TITLE, HEIGHT, WIDTH
from ...utils import Label
from ...utils.menus import GameOverMenu
from ..scene import Scene


class GameOverScene(Scene):
    """
    Game Over Scene. Appears when the player's
    health is depleted,
    """

    def __init__(self,
                 *,
                 name_id: str="scene-gameover",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'GameOverScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)
        gameovermenu = GameOverMenu()
        self.add_menu(gameovermenu)

        self.add_label(Label(WIDTH / 2,
                             HEIGHT / 6,
                             GAMEOVER_TITLE,
                             size=(WIDTH // 75),
                             fill_name="TEXT_COLOR_1",
                             justify='c'))
