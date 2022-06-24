"""
Scoreboard Scene Module.
"""

from typing import Optional

from ...consts import HEIGHT, SCOREBOARD_TITLE, WIDTH
from ...utils import Label
from ..scene import Scene


class ScoreBoardScene(Scene):
    """
    Scoreboard Scene. Shows all the scores of previous runs.
    """

    def __init__(self,
                 *,
                 name_id: str="scene-scoreboard",
                 parent: Optional["Scene"]=None,
                 press_cooldown: int=20,
                 **kwargs) -> None:
        """
        Initializes an instance of 'ScoreBoardScene'.
        """

        super().__init__(name_id,
                         parent=parent,
                         press_cooldown=press_cooldown,
                         **kwargs)

        self.add_label(Label(WIDTH / 2,
                             HEIGHT * 0.07,
                             SCOREBOARD_TITLE,
                             size=(WIDTH // 150)))
