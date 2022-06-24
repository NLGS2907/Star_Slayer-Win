"""
Animation abstract class Module.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple


# pylint: disable=invalid-name
class Animation(ABC):
    """
    Abstract class for a defined Animation.
    """

    def __init__(self,
                 x1: Optional[float]=None,
                 y1: Optional[float]=None,
                 x2: Optional[float]=None,
                 y2: Optional[float]=None,
                 *,
                 is_text: bool=False,
                 **kwargs) -> None:
        """
        Initializes an instance of type 'Animation'.
        """

        if any(coord is None for coord in (x1, y1, x2, y2)):
            raise ValueError("All corner coordinates must be present.")

        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2

        self.is_text: bool = is_text
        self.properties = kwargs


    @property
    def area(self) -> Tuple[int, int, int, int]:
        """
        Defines the area in which the animation takes place.
        """

        return self.x1, self.y1, self.x2, self.y2


    @property
    def center_x(self) -> float:
        """
        Return the center of the X axis.
        """

        return (self.x1 + self.x2) / 2


    @property
    def center_y(self) -> float:
        """
        Return the center of the Y axis.
        """

        return (self.y1 + self.y2) / 2


    @property
    def center(self) -> Tuple[float, float]:
        """
        Returns the center of the area.
        """

        return self.center_x, self.center_y


    @abstractmethod
    def animate(self, **kwargs) -> None:
        """
        Proceeds with the animation.
        """

        raise NotImplementedError


    def post_hook(self, **_kwargs) -> None:
        """
        For anything that needs atention after an animation frame.
        It is not necessary to implement this method, but it is
        recommended.
        """

        return None
