"""
Actions Group Module. Provides a way to organize actions in separate groups.
"""

from typing import Any, Callable, List, Optional, TYPE_CHECKING

from ..logger import GameLogger

if TYPE_CHECKING:

    from ..state import Game


ActionHandler = Callable[["HooksGroup"], Any]
ActionsDict = dict[str, List[Callable]]


class HooksGroup:
    """
    A group for organizing actions and buttons better.

    It can be inherited for further organization, or it
    can be plainly instantiated if a single, quick instance
    is needed instead.
    """

    cls_actions: ActionsDict = {}


    def __init__(self, game: "Game") -> None:
        """
        Initializes an instance of 'ActionGroup'.
        """

        self.game: "Game" = game
        self.ins_actions: ActionsDict = {}


    def __init_subclass__(cls) -> None:
        """
        Translates the progress of the actions register
        and 'prints it' to the subclass.
        """

        original_cls = __class__
        cls.cls_actions = original_cls.cls_actions.copy()
        original_cls.cls_actions.clear()


    @property
    def log(self) -> GameLogger:
        """
        Returns the GameLogger instance.
        """

        return GameLogger()


    @classmethod
    def action(cls, *, on_action: Optional[str]) -> ActionHandler:
        """
        Adds a new executable action.
        """

        def decorator(func: ActionHandler) -> ActionHandler:

            if on_action not in cls.cls_actions:

                cls.cls_actions[on_action] = []

            cls.cls_actions[on_action].append(func)

            return func

        return decorator


    def ins_action(self, *, on_action: Optional[str]) -> ActionHandler:
        """
        Adds a new executable action.
        This only applies to this specific instance.
        """

        def decorator(func: ActionHandler) -> ActionHandler:

            if on_action not in self.ins_actions:

                self.ins_actions[on_action] = []

            self.ins_actions[on_action].append(func)

            return func

        return decorator


    # @classmethod
    # # pylint: disable=invalid-name
    # def button(cls, *, x1: int, y1: int, x2: int, y2: int, message: str='') -> ButtonHandler:
    #     """
    #     Creates a button, and registers a handler.
    #     """

    #     button = Button(x1=x1, y1=y1, x2=x2, y2=y2, message=message)

    #     def decorator(handler_func: ButtonHandler) -> ButtonHandler:
    #         """
    #         Decorates the button to add its handler.
    #         """

    #         if button not in cls.cls_buttons:

    #             button.handler = handler_func
    #             cls.cls_buttons.append(button)

    #         return handler_func

    #     return decorator


    def execute_act(self, action_type: str) -> bool:
        """
        Executes a specified action.
        """

        if self.ins_actions:

            # Actions specific to this instance should override those of its class.
            return self._execute_act(self.ins_actions, action_type)

        return self._execute_act(self.cls_actions, action_type)


    def _execute_act(self, act_dict: ActionsDict, action_type: str) -> bool:
        """
        Ultimately executes the corresponding actions.
        If it is successful, it returns 'True', otherwise 'False'.
        """

        if action_type in act_dict:

            for action in act_dict[action_type]:

                if (hasattr(action, "__checks__")
                    and not all(checked(self.game) for checked in action.__checks__)):

                    continue

                action(self)
                return True

        return False


    # #pylint: disable=invalid-name
    # def execute_btn(self, x: int, y: int, **kwargs: ButtonKwargs) -> bool:
    #     """
    #     Tries to execute the first button handler it finds if the
    #     coordinates are correct.
    #     """

    #     if self.ins_buttons:

    #         # Buttons specific to this instance should override those of its class.
    #         return self._execute_btn(self.ins_buttons, x, y, **kwargs)

    #     return self._execute_btn(self.cls_buttons, x, y, **kwargs)


    # def _execute_btn(self, btn_list: ButtonsList, x: int, y: int, **kwargs: ButtonKwargs) -> bool:
    #     """
    #     Ultimately execute the buttons handler, if possible.
    #     If it is successful, it returns 'True', otherwise 'False'.
    #     """

    #     for btn in btn_list:

    #         if (btn.is_inside(x, y) and hasattr(btn, "__btn_checks__")
    #             and all(checker(self.game, btn) for checker in btn.__btn_checks__)):

    #             btn.handler(self, btn, **kwargs)
    #             return True

    #     return False
