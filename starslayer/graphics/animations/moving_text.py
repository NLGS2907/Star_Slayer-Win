"""
Moving Text Animation Module.
"""

from typing import Tuple

from ...gamelib import draw_text
from .animation import Animation


# pylint: disable=invalid-name
class MovingText(Animation):
    """
    Animation for a text box that moves around.
    """

    def __init__(self,
                 text: str,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 *,
                 origin_x: float=0.0,
                 origin_y: float=0.0,
                 dx: float=-1.0,
                 dy: float=0.0,
                 bouncy: bool=False,
                 **kwargs) -> None:
        """
        Initializes an instace of type 'MovingText'.
        """

        super().__init__(x1, y1, x2, y2, is_text=True, **kwargs)

        self.text: str = text
        self.origin_x: float = origin_x
        self.origin_y: float = origin_y
        self.current_x: float = self.origin_x
        self.current_y: float = self.origin_y
        self.dx: float = dx
        self.dy: float = dy
        self.bouncy: bool = bouncy


    @property
    def origin(self) -> Tuple[float, float]:
        """
        Returns the origin coords of the movement.
        """

        return self.origin_x, self.origin_y


    @property
    def movement(self) -> Tuple[float, float]:
        """
        Returns the differentials of the movement of each axis.
        """

        return self.dx, self.dy


    def check_normal_move(self) -> None:
        """
        Checks the bounds for a normal behaviour.
        """

        if self.current_x < self.x1:
            self.current_x = self.x2

        elif self.current_x > self.x2:
            self.current_x = self.x1

        if self.current_y < self.y1:
            self.current_y = self.y2

        elif self.current_y > self.y2:
            self.current_y = self.y1


    def check_bouncy_move(self) -> None:
        """
        Checks the bounds for a bouncy behaviour.
        """

        if self.current_x < self.x1 or self.current_x > self.x2:
            self.dx = -self.dx

        if self.current_y < self.y1 or self.current_y > self.y2:
            self.dy = -self.dy



    def move(self, dx: float, dy: float) -> None:
        """
        Moves the text by `dx` and `dy`.
        """

        self.current_x += dx
        self.current_y += dy

        if self.bouncy:
            self.check_bouncy_move()
        else:
            self.check_normal_move()


    def animate(self, **_kwargs) -> None:
        """
        Proceeds with the animation.
        """

        draw_text(text=self.text,
                  x=self.current_x,
                  y=self.current_y,
                  **self.properties)


    def post_hook(self, **_kwargs) -> None:
        """
        Moves the text.
        """

        self.move(self.dx, self.dy)
