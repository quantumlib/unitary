# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
