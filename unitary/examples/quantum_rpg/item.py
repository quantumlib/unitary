from typing import Callable, Optional, Sequence, Tuple, TYPE_CHECKING, Union

# Common synonyms for action keywords for different objects:
EXAMINE = ["read", "look", "examine", "investigate", "search"]
TALK = ["talk", "chat", "ask"]

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
                Union[str, Callable],
            ]
        ],
        description: Optional[str] = None,
    ):
        self.keyword_actions = keyword_actions
        self.description = description

    def get_action(self, user_input: str) -> Optional[Union[str, Callable]]:
        words = user_input.lower().split()
        if not words:
            return None
        keyword = words[0]
        target = words[1] if len(words) > 1 else None
        for keywords, targets, action in self.keyword_actions:
            if isinstance(targets, str):
                targets = [targets]
            if keyword == keywords or keyword in keywords:
                if not targets or target in targets:
                    return action
                if target is None and targets:
                    return f"{keyword} what?"
        return None
