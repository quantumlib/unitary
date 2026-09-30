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

import re

from . import item


def test_item_str():
    sign = item.Item(
        keyword_actions=[
            (["read", "examine"], ["sign", "message"], "Keep out"),
            ("pass", [], "Or enter, Im a sign, not a cop"),
        ],
        description="A sign blocks the way forward.",
    )
    assert sign.get_action("read") == "read what?"
    assert sign.get_action("examine") == "examine what?"
    assert sign.get_action("READ SIGN") == "Keep out"
    assert sign.get_action("READ MESSAGE") == "Keep out"
    assert sign.get_action("read letter") is None
    assert sign.get_action("pass") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("pass sign") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("pass by") == "Or enter, Im a sign, not a cop"
    assert sign.get_action("eat sign") is None
    assert sign.description == "A sign blocks the way forward."

    assert sign.get_action("") is None


def test_item_re():
    number_pad = item.Item(
        keyword_actions=[
            (["type"], re.compile("[0-9]+"), "valid number"),
            (["press"], [re.compile("a+"), re.compile("b+")], "letter pressed"),
        ],
        description="A numeric keypad.",
    )
    assert number_pad.get_action("type") == "type what?"
    assert number_pad.get_action("type abcde") is None
    assert number_pad.get_action("type 01234") == "valid number"
    assert number_pad.get_action("press") == "press what?"
    assert number_pad.get_action("press cdef") is None
    assert number_pad.get_action("press aaa") == "letter pressed"
    assert number_pad.get_action("press bbbb") == "letter pressed"
