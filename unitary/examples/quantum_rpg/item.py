from typing import Any, Callable, Optional, Sequence, Tuple, TYPE_CHECKING, Union
import re

import unitary.examples.quantum_rpg.game_state as game_state

# Common synonyms for action keywords for different objects:
EXAMINE = ["read", "look", "examine", "investigate", "search"]
TALK = ["talk", "chat", "ask"]

# Note: second argument is a World, omitting to avoid circular dependency
ITEM_FUNCTION_TYPE = Callable[[game_state.GameState, Any], Optional[str]]
ITEM_ACTION_TYPE = Union[str, ITEM_FUNCTION_TYPE]


class Item:
    """An item is an object or person that can be interacted with.

    items have keywords that you can associate with them to
    interact with them, such as 'talk' for people, or press for
    button.

    Future functionality may allow these items to be picked up
    as well.

    Attributes:
        keyword_actions: Tuples of keywords and targets to actions.  A keyword
           is a single verb that can be used to interact with the item.
           An action is a string that is printed out, or a callable
           that will perform some sort of action.
        keyword_targets:  Optional list of targets.  For instance,
           ['Erwin', 'physicist'] would match 'talk Erwin' or
           'talk physicist'. If this is blank, the item will
           intercept all commands with the keyword_actions.
        description: Optional string that will be printed out as
           part of the room description.
    """

    def __init__(
        self,
        keyword_actions: Sequence[
            Tuple[
                Union[str, Sequence[str]],
                Optional[Union[str, Sequence[str]]],
                ITEM_ACTION_TYPE,
            ]
        ],
        description: Optional[str] = None,
    ):
        self.keyword_actions = keyword_actions
        self.description = description

    def get_action(self, user_input: str) -> Optional[ITEM_ACTION_TYPE]:
        words = user_input.lower().split()
        if not words:
            return None
        keyword = words[0]
        user_target = words[1] if len(words) > 1 else None
        for keywords, targets, action in self.keyword_actions:
            if not isinstance(targets, list):
                targets = [targets]
            if keyword == keywords or keyword in keywords:
                if not targets:
                    # All targets valid
                    return action
                if not user_target:
                    # No target specified
                    return f"{keyword} what?"
                for target in targets:
                    if isinstance(target, re.Pattern):
                        # REgex
                        if user_target and re.match(target, user_target):
                            return action
                    else:
                        # String
                        if user_target == target:
                            return action
        return None
