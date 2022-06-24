"""
Actions Group Module. Provides a way to organize actions in separate groups.
"""

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

if TYPE_CHECKING:
    from ..state import Game


ActionHandler = Callable[["HooksGroup"], Any]
ActionsDict = Dict[str, List[Callable]]
CombinationHandler = ActionHandler
CombinationsDict = ActionsDict


class HooksGroup:
    """
    A group for organizing actions and buttons better.

    It can be inherited for further organization, or it
    can be plainly instantiated if a single, quick instance
    is needed instead.
    """

    cls_actions: ActionsDict = {}
    combinations: CombinationsDict = {}


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
        cls.combinations = original_cls.combinations.copy()
        original_cls.combinations.clear()


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


    @classmethod
    def combination(cls, *, with_name: str) -> CombinationHandler:
        """
        Adds a new executable combination of characters.
        """

        def decorator(func: CombinationHandler) -> CombinationHandler:
            if with_name not in cls.combinations:
                cls.combinations[with_name] = []

            cls.combinations[with_name].append(func)
            return func

        return decorator


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

        if action_type not in act_dict:
            return False

        for action_handler in act_dict[action_type]:
            if (hasattr(action_handler, "__checks__")
                and not all(checked(self.game) for checked in action_handler.__checks__)):
                continue

            self.pre_hook()
            action_handler(self)
            self.post_hook()

        return True


    def execute_combination(self, comb_name: str) -> bool:
        """
        Ultimately executes the corresponding actions.
        If it is successful, it returns 'True', otherwise 'False'.
        """

        if comb_name not in self.combinations:
            return False

        for comb_handler in self.combinations[comb_name]:
            if (hasattr(comb_handler, "__checks__")
                and not all(checked(self.game) for checked in comb_handler.__checks__)):
                continue

            self.pre_hook()
            comb_handler(self)
            self.post_hook()

        return True


    def pre_hook(self) -> None:
        """
        Executes before an action handler is called.

        Must be inherited to do something.
        """

        return None


    def post_hook(self) -> None:
        """
        Executes before an action handler is called.

        Must be inherited to do something.
        """

        return None
