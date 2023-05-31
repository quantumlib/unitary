from typing import Callable, Optional, Sequence, Tuple, TYPE_CHECKING, Union


class Item:
    """An item is an object or person that can be interacted with.

    items have keywords that you can associate with them to
    interact with them, such as 'talk' for people, or press for
    button.

    Future functionality may allow these items to be picked up
    as well.

    Attributes:
        keyword_actions: Tuples of keywords to actions.  A keyword
           is a single verb that can be used to interact with the item.
           An action is a string that is printed out, or a callable
           that will perform some sort of action.
        description: Optional string that will be printed out as
           part of the room description.
    """

    def __init__(
        self,
        keyword_actions: Sequence[
            Tuple[Union[str, Sequence[str]], Union[str, Callable]]
        ],
        description: Optional[str] = None,
    ):
        self.keyword_actions = keyword_actions
        self.description = description

    def get_action(self, keyword: str) -> Optional[Union[str, Callable]]:
        for keywords, action in self.keyword_actions:
            if keyword == keywords or keyword in keywords:
                return action
        return None
