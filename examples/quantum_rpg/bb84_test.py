# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import cast
import io

import pytest

from . import bb84
from . import game_state
from . import input_helpers
from . import main_loop
from . import world


def test_to_bin():
    assert bb84.to_bin("a") == "01100001"


@pytest.mark.parametrize("word", bb84._WORDS)
def test_bb84(word):
    (alice, bob) = bb84.gen_bb84(word)
    assert bb84.solve_bb84(alice, bob) == word


def test_alice_bob():
    example_world = world.World(
        [
            world.Location(
                label="1",
                title="Quantum Communication Sending Facility",
                description="",
                items=[bb84.ALICE],
                exits={world.Direction.WEST: "2"},
            ),
            world.Location(
                label="2",
                title="Quantum Communication Receiving Facility",
                description="",
                items=[bb84.BOB, bb84.DOOR],
                exits={world.Direction.EAST: "1"},
            ),
            world.Location(
                label="perimeter1",
                title="Inside the Perimeter",
                description="",
                items=[],
                exits={world.Direction.SOUTH: "2"},
            ),
        ]
    )
    state = game_state.GameState(
        party=[],
        user_input=[
            "look electronics",
            "w",
            "look display",
            "e",
            "press power",
            "look display",
            "press transmit",
            "look display",
            "w",
            "press power",
            "look display",
            "e",
            "look display",
            "press transmit",
            "look display",
            "w",
            "look display",
            "look keyboard",
            "type aaaa",
            "Quit",
        ],
        file=io.StringIO(),
    )
    loop = main_loop.MainLoop(example_world, state)
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == f"""
Quantum Communication Sending Facility


A strange looking machine is mounted under an awning.

Exits: west.

The display is blank.
Quantum Communication Receiving Facility


A strange looking machine is mounted under an awning.
An imposing door is here with an alphabetic keyboard lock.

Exits: east.

The display is blank.
Quantum Communication Sending Facility


A strange looking machine is mounted under an awning.

Exits: west.

The device whirs as it turns on.
The display reads 'Ready to TRANSMIT'
The device emits a long and sad beep.
The display reads 'Error transmitting data.'
Quantum Communication Receiving Facility


A strange looking machine is mounted under an awning.
An imposing door is here with an alphabetic keyboard lock.

Exits: east.

The device whirs as it turns on.
The display reads 'Ready to Receive'
Quantum Communication Sending Facility


A strange looking machine is mounted under an awning.

Exits: west.

The display reads 'Error transmitting data.'
The device chimes happily.
The display reads 'Transmission Successful:'
'{state.state_dict['alice']}'
Quantum Communication Receiving Facility


A strange looking machine is mounted under an awning.
An imposing door is here with an alphabetic keyboard lock.

Exits: east.

The display reads 'Received data:'
'{state.state_dict['bob']}'
This seems to be a solid metal security door guarding the entrance
to the research facility.  A lock with a keyboard that you can TYPE
letters into to open the door is on the right side of the entrance.
The keypad beeps and a light flashes red.
""".strip()
    )
    # Reset input and get the keys
    state.file = file = io.StringIO()
    key = bb84.solve_bb84(state.state_dict["alice"], state.state_dict["bob"])
    state.get_user_input = input_helpers.get_user_input_function(
        [f"type {key}", "north", "south", "Quit"]
    )
    loop = main_loop.MainLoop(example_world, state)
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == f"""
Quantum Communication Receiving Facility


A strange looking machine is mounted under an awning.
An imposing door is here with an alphabetic keyboard lock.

Exits: east.

A light flashes green and the door unlocks!
Inside the Perimeter



Exits: south.

Quantum Communication Receiving Facility


A strange looking machine is mounted under an awning.
An imposing door is here with an alphabetic keyboard lock.

Exits: east, north.
""".strip()
    )
