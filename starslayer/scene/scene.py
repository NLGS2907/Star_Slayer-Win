"""
Scenes Module. Dictates how a scene contains menus and
the content on display.
"""

from typing import TYPE_CHECKING, Dict, List, Optional

from ..utils import ButtonKwargs, Label, Menu, Timer

MenuList = List[Menu]
LabelList = List[Label]
SceneDict = Dict[str, "Scene"]

if TYPE_CHECKING:

    from ..state import Game


class Scene:
    """
    A scene that contains elements.
    """

    def __init__(self, name_id: str, **kwargs) -> None:
        """
        Initializes an instance of 'Scene'.
        """

        self._name_id: str = name_id
        self._selected_menu_index: int = -1
        self._menus: MenuList = []
        self._labels: LabelList = []
        self.parent: Optional["Scene"] = kwargs.get("parent", None)

        # Timers
        self.press_cooldown = Timer(20)


    def __eq__(self, other: "Scene") -> bool:
        """
        Checks if the scene has the same id as 'other'.
        """

        if not isinstance(other, __class__):
            return False

        return self.id == other.id


    @property
    #pylint: disable=invalid-name
    def id(self) -> str:
        """
        Returns the unique name of the scene.
        """

        return self._name_id


    @property
    def menus(self) -> MenuList:
        """
        Returns all the menus of the scene.
        """

        return self._menus


    @property
    def selected_menu(self) -> Optional[Menu]:
        """
        Returns the selected menu, if any.
        """

        if self._selected_menu_index < 0:
            return None

        return self.menus[self._selected_menu_index]


    @property
    def labels(self) -> LabelList:
        """
        Returns all the labels of the scene.
        """

        return self._labels


    def add_menu(self, menu: Menu) -> None:
        """
        Adds a new menu to the scene.
        """

        if not self.selected_menu:

            self._selected_menu_index = 0

        self.menus.append(menu)


    def add_label(self, label: Optional[Label]=None, **kwargs) -> None:
        """
        Adds a label to the scene.
        """

        if label:
            self.labels.append(label)
        else:
            self.labels.append(Label(
                x=kwargs.get("x"),
                y=kwargs.get("y"),
                text=kwargs.get("text", ''),
                **kwargs
            ))


    def change_selection(self, reverse: bool=False) -> None:
        """
        Changes the current selected menu.
        """

        if self.menus:

            i = (-1 if reverse else 1)
            self._selected_menu_index = (self._selected_menu_index + i) % len(self.menus)


    # pylint: disable=invalid-name
    def execute_button(self, game: "Game", x: int, y: int, **kwargs: ButtonKwargs) -> bool:
        """
        Tries to execute a button from a menu it has.
        """

        for m in self.menus:

            if m.hidden:
                continue

            if m.execute_btn(game, self, x, y, **kwargs):
                return True

        return False


    def prompt(self, *args, **kwargs) -> None:
        """
        Searches if any menu can prompt the user.
        """

        for menu in self.menus:
            if menu.prompt(*args, **kwargs):
                return


    def resfresh_sub_menus(self, game: "Game") -> None:
        """
        Attemps to refresh a sub-menu for every menus the scene has.
        """

        for menu in self.menus:
            menu.refresh_sub_menu(game)
