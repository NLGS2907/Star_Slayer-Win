"""
Action group for menus navigation.
"""

from ..hooks_group import HooksGroup
from ...checks import is_in_game, scene_has_parent, scene_is_cool


class Menus(HooksGroup):
    """
    Menus Group.
    """

    @HooksGroup.action(on_action="UP")
    @is_in_game(False)
    def menu_up(self) -> None:
        """
        Navigates UP on menus.
        """

        self.game.current_scene.selected_menu.change_page(False)


    @HooksGroup.action(on_action="DOWN")
    @is_in_game(False)
    def menu_down(self) -> None:
        """
        Navigates DOWN on menus.
        """

        self.game.current_scene.selected_menu.change_page(True)


    @HooksGroup.action(on_action="LEFT")
    @is_in_game(False)
    def menu_prev(self) -> None:
        """
        Cycles to the previous menu in the scene.
        """

        self.game.current_scene.change_selection(reverse=True)

    @HooksGroup.action(on_action="RIGHT")
    @is_in_game(False)
    def menu_next(self) -> None:
        """
        Cycles to the next menu in the scene.
        """

        self.game.current_scene.change_selection(reverse=False)


    @HooksGroup.action(on_action="RETURN")
    @is_in_game(False)
    @scene_has_parent()
    @scene_is_cool()
    def return_to_prev_menu(self) -> None:
        """
        Returns to parent menu.
        """

        self.game.current_scene.press_cooldown.reset() # First we reset the current menu
        self.game.current_scene = self.game.current_scene.parent
        self.game.current_scene.press_cooldown.reset() # Then the parent
