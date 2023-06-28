"""Functions for safe and user-friendly input."""
from typing import Callable, Optional, Sequence, TextIO

import sys

_USER_INPUT = Callable[[str], str]
_INVALID_MESSAGE = "Invalid number selected."



def get_user_input_function(user_input: Optional[Sequence[str]] = None) -> _USER_INPUT:
    """Returns a lambda for getting user input.

    If user input is provided as a list (ie. for tests or scripts),
    then consume that list.
    If not, use stdin.
    """
    if user_input is not None:
        iter_input = iter(user_input)
        return lambda _: next(iter_input)
    else:
        return input


def get_user_input_number(
    get_user_input: _USER_INPUT,
    message: Optional[str] = "",
    max_number: Optional[int] = None,
    invalid_message: Optional[str] = _INVALID_MESSAGE,
    file: TextIO = sys.stdout,
):
    """Helper to get a valid number from the user.

    This will only accept valid numbers from the user from 1 to max_number.
    If max_number is not supplied, any number will be accepted.

    User will be prompted until a valid number is returned.
    """
    while True:
        try:
          user_input = int(get_user_input(message or ""))
        except ValueError as e:
            if invalid_message:
                print(invalid_message, file=file)
            else:
                print(e)
            continue
        if max_number is None or (user_input > 0 and user_input <= max_number):
            return user_input
        if invalid_message:
            print(invalid_message, file=file)
        else:
            print("number out of range", file=file)
