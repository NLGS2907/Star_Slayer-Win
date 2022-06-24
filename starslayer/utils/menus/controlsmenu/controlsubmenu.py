"""
Controls Sub Menu Module.
"""

from ....auxiliar import Singleton
from ....consts import HEIGHT, WIDTH
from ...menu import Menu, MenuDict
from ...shapes import FloatTuple4

__all__ = ["ControlSubMenu"]


class ControlSubMenu(Menu, metaclass=Singleton):
    """
    The Controls Sub Menu.
    """

    def __init__(self,
                 area_corners: FloatTuple4=(
                     (WIDTH * 0.29),
                     int(HEIGHT * 0.8),
                     (WIDTH * 0.96),
                     int(HEIGHT * 0.97)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'ControlSubMenu'.
        """

        super().__init__(area_corners,
                         how_many_columns=2,
                         space_between=10,
                         max_rows=2,
                         **kwargs)
