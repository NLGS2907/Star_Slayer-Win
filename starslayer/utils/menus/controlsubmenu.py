"""
Controls Sub Menu Module.
"""

from ...auxiliar import Singleton
from ...consts import SUB_MENU_RIGHT
from ..generic import IntTuple4
from ..menu import Menu, MenuDict


__all__ = ["ControlSubMenu"]


class ControlSubMenu(Menu, metaclass=Singleton):
    """
    The Controls Sub Menu.
    """

    def __init__(self,
                 area_corners: IntTuple4=SUB_MENU_RIGHT,
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'ControlSubMenu'.
        """

        kwargs.update({"how_many_columns": 2, "space_between": 20})
        super().__init__(area_corners, **kwargs)
