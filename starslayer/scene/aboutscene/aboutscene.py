"""
About Scene Module.
"""

from typing import Optional

from ...consts import HEIGHT, WIDTH
from ...utils import Label
from ..scene import Scene


class AboutScene(Scene):
    """
    About Scene. Shows information about the game.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-about",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'AboutScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)

        myself = "Franco 'NLGS' Lighterman"
        aux_cons = (WIDTH // 10)

        self.add_label(Label((WIDTH // 2),
                             (HEIGHT // 6),
                             "SO, ABOUT\nTHIS GAME...",
                             size=(HEIGHT // 12),
                             fill_name="TEXT COLOR 1",
                             justify='c'))

        # Pixel-Art
        self.add_label(Label(aux_cons,
                             HEIGHT * 0.4,
                             "Pixel-Art:",
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='w'))
        self.add_label(Label(WIDTH - aux_cons,
                             HEIGHT * 0.4,
                             myself,
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='e'))

        # Coding
        self.add_label(Label(aux_cons,
                             HEIGHT * 0.6,
                             "Coding:",
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='w'))
        self.add_label(Label(WIDTH - aux_cons,
                             HEIGHT * 0.6,
                             myself,
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='e'))

        # Gamelib
        self.add_label(Label(aux_cons,
                             HEIGHT * 0.8,
                             "Gamelib Library:",
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='w'))
        self.add_label(Label(WIDTH - aux_cons,
                             HEIGHT * 0.8,
                             "Diego Essaya",
                             size=(HEIGHT // 30),
                             fill_name="TEXT COLOR 1",
                             anchor='e'))

        self.add_label(Label((WIDTH // 2),
                             HEIGHT - 20,
                             "Press 'RETURN' to return",
                             size=(HEIGHT // 50),
                             fill_name="TEXT COLOR 1",
                             justify='c'))
