"""
Main Scene Module.
"""

from ..consts import GAME_TITLE, WIDTH, HEIGHT
from ..utils import Label
from ..utils.menus import MainMenu
from .scene import Scene


class MainScene(Scene):
    """
    Main Scene. Contains primarly the main menu.
    """

    def __init__(self, name_id: str="scene-main", **kwargs) -> None:
        """
        Initializes an instance of 'MainScene'.
        """

        super().__init__(name_id, **kwargs)
        self.add_menu(MainMenu())

        self.add_label(Label(WIDTH // 2,
                             HEIGHT // 4,
                             GAME_TITLE,
                             size=(WIDTH // 90),
                             color_name="TEXT_COLOR_1",
                             justify='c'))
