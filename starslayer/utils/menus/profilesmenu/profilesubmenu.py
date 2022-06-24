"""
Profiles Sub Menu Module.
"""

from ....auxiliar import Singleton
from ....consts import HEIGHT, WIDTH
from ...menu import Menu, MenuDict
from ...shapes import FloatTuple4

__all__ = ["ProfileSubMenu"]


class ProfileSubMenu(Menu, metaclass=Singleton):
    """
    The Controls Sub Menu.
    """


    def __init__(self,
                 area_corners: FloatTuple4=(
                     (WIDTH * 0.066666),
                     (HEIGHT * 0.195714),
                     (WIDTH * 0.766666),
                     (HEIGHT * 0.964285)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'ProfileSubMenu'.
        """

        super().__init__(area_corners,
                         max_rows=7,
                         how_many_columns=2,
                         space_between_x=20,
                         space_between_y=15,
                         button_anchor='w',
                         special_btn_on_right=False,
                         **kwargs)
