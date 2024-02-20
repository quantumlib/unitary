"""Functions for safe and user-friendly input."""
from typing import Callable, Optional, Sequence, TextIO

import sys
from unitary.examples.quantum_rpg import qaracter

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
    message: str = "",
    max_number: Optional[int] = None,
    invalid_message: str = _INVALID_MESSAGE,
    file: TextIO = sys.stdout,
) -> int:
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
                print(e, file=file)
            continue
        if max_number is None or (user_input > 0 and user_input <= max_number):
            return user_input
        if invalid_message:
            print(invalid_message, file=file)
        else:
            print("number out of range", file=file)


def get_multiple_user_inputs(
    get_user_input: _USER_INPUT,
    *prompts: Sequence[Callable[[], int] | Callable[[], str]],
    file: TextIO = sys.stdout,
) -> Sequence[int | str]:
    """Runs multiple number or string prompts and returns their results.

    After all inputs have been provided the last prompt asks for confirmation if
    user happy with inputs, and allows to restart the sequence and change
    inputs.
    """
    while True:
        inputs = [p() for p in prompts]
        print("[enter]) Confirm selection.", file=file)
        print("r) Select again.", file=file)
        while True:
            match get_user_input("Choose your action: "):
                case "r":
                    break
                case "":
                    return inputs


def get_user_input_qaracter_name(
    get_user_input: _USER_INPUT,
    qaracter_type: str = "a new qaracter",
    file: TextIO = sys.stdout,
):
    while True:
        user_input = get_user_input(f"Please enter a name for {qaracter_type}:")
        if qaracter.Qaracter.is_valid_name(user_input):
            return user_input
        print("Invalid qaracter name", file=file)
