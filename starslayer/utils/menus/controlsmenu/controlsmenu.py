"""
Controls Menu Module.
"""

from typing import TYPE_CHECKING

from ....auxiliar import Singleton
from ....checks import left_click, on_press
from ....consts import ACTIONS_PATH, HEIGHT, WIDTH
from ....files import (dump_json, exists_key, get_action_from_key,
                       list_actions, list_action_keys, load_json)
from ....gamelib import EventType
from ....gamelib import say as lib_say
from ....gamelib import wait as lib_wait
from ...menu import ButtonKwargs, Menu, MenuDict
from ...shapes import FloatTuple4
from .controlsubmenu import ControlSubMenu

if TYPE_CHECKING:
    from ....scene import Scene
    from ....state import Game
    from ...button import Button


__all__ = ["ControlsMenu"] # We DON'T want the local variable 'controlsmenu' to be exported


def create_buttons(menu: "ControlsMenu") -> None:
    """
    Creates the buttons of the Controls Menu.
    """

    menu.clear_buttons()

    for action in list_actions(load_json(ACTIONS_PATH)):

        @menu.button(message=action) # pylint: disable=cell-var-from-loop
        @left_click()
        @on_press()
        def select_action(game: "Game",
                          _scene: "Scene",
                          btn: "Button",
                          **_kwargs: ButtonKwargs) -> None:
            """
            Selects an action from the controls menu.
            """

            game.action_to_show = btn.msg
            controlsmenu.refresh_sub_menu(game)


class ControlsMenu(Menu, metaclass=Singleton):
    """
    The Controls Menu of the game.
    """

    def __init__(self,
                 area_corners: FloatTuple4=(
                    (WIDTH // 75),
                    (HEIGHT // 5),
                    int(WIDTH / 4.237288),
                    int(HEIGHT / 1.014492)
                 ),
                 **kwargs: MenuDict) -> None:
        """
        Initializes an instance of 'ControlsMenu'.
        """

        super().__init__(area_corners,
                         max_rows=8,
                         **kwargs)


    def refresh_sub_menu(self, game: "Game") -> None:
        """
        Refreshes the buttons of the sub menu of this particular menu.
        """

        submenu = ControlSubMenu()
        repeated_keys = list_action_keys(game.action_to_show, load_json(ACTIONS_PATH))

        submenu.clear_buttons()

        for key in repeated_keys:
            if not key:
                continue

            @submenu.button(message=f"Delete {key}") # pylint: disable=cell-var-from-loop
            @left_click()
            @on_press()
            def delete_key(game: "Game",
                           _scene: "Scene",
                           btn: "Button",
                           **_kwargs: ButtonKwargs) -> None:
                """
                Removes the key passed as an argument from the keys dictionary.
                """

                actions_dict = load_json(ACTIONS_PATH)
                del_key = btn.msg.removeprefix("Delete ")
                action_of_key = get_action_from_key(del_key, actions_dict)

                if len(list_action_keys(action_of_key, actions_dict)) == 1:

                    lib_say("You cannot delete this key, as it is the only one remaining.")
                    return

                if exists_key(del_key, actions_dict):

                    actions_dict[action_of_key]["keys"].remove(del_key)
                    game.keys_pressed.pop(del_key, None)
                    game.keys_released.pop(del_key, None)

                    dump_json(actions_dict, ACTIONS_PATH)
                    self.refresh_sub_menu(game)


        @submenu.button(message="Add Key")
        @left_click()
        @on_press()
        def add_key(game: "Game",
                    _scene: "Scene",
                    _btn: "Button",
                    **_kwargs: ButtonKwargs) -> None:
            """
            Adds a selected key to the controls.
            """

            game.go_prompt()


    def prompt(self, *_args, **kwargs) -> bool:
        """
        If valid, adds a key to a designed action.

        Returns 'True' if the function succeeded,
        else 'False' if something happened.
        """

        game: "Game" = kwargs.get("game")
        sel_action = game.action_to_show

        event = lib_wait(EventType.KeyPress)
        actions_dict = load_json(ACTIONS_PATH)
        success = False

        if not exists_key(event.key, actions_dict):
            success = True

        if success:
            actions_dict[sel_action]["keys"].append(event.key)
            dump_json(actions_dict, ACTIONS_PATH)
            self.refresh_sub_menu(game)

        game.is_on_prompt = False

        return success


controlsmenu = ControlsMenu() # instantiated temporarily
create_buttons(controlsmenu)
