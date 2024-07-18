import io

import pytest

from . import input_helpers


def test_get_user_input_function():
    get_input = input_helpers.get_user_input_function()
    assert get_input == input

    get_input = input_helpers.get_user_input_function(["a", "b", "c"])
    assert get_input("") == "a"
    assert get_input("") == "b"
    assert get_input("") == "c"

    with pytest.raises(StopIteration):
        _ = get_input("")


def test_get_user_input_number():
    get_input = input_helpers.get_user_input_function(["1"])
    output = io.StringIO()
    assert input_helpers.get_user_input_number(get_input, file=output) == 1
    assert output.getvalue() == ""


def test_get_user_input_number_invalid():
    get_input = input_helpers.get_user_input_function(["a", "blah", "no", "4"])
    output = io.StringIO()
    assert input_helpers.get_user_input_number(get_input, file=output) == 4
    assert (
        output.getvalue()
        == """Invalid number selected.
Invalid number selected.
Invalid number selected.
"""
    )


def test_get_user_input_number_max():
    get_input = input_helpers.get_user_input_function(["0", "-1", "a", "7", "3"])
    output = io.StringIO()
    assert (
        input_helpers.get_user_input_number(get_input, file=output, max_number=4) == 3
    )


def test_get_multiple_user_inputs():
    get_input = input_helpers.get_user_input_function(
        ["1", "2", "r", "3", "1", ""],
    )
    output = io.StringIO()

    def p1():
        return input_helpers.get_user_input_number(
            get_input,
            max_number=4,
            file=output,
        )

    def p2():
        return input_helpers.get_user_input_number(
            get_input,
            max_number=4,
            file=output,
        )

    assert input_helpers.get_multiple_user_inputs(
        get_input,
        p1,
        p2,
        file=output,
    ) == [3, 1]
