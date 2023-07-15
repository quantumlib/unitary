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
from typing import Tuple
import random


from unitary.examples.quantum_rpg.game_state import GameState
from unitary.examples.quantum_rpg.item import EXAMINE, TALK, Item
from unitary.examples.quantum_rpg.world import Direction, Location


_WORDS = [
    "QEC",
    "ket",
    "Arc",
    "sum",
    "sin",
    "cos",
    "QED",
    "log",
    "add",
    "BQP",
    "HOG",
    "QFT",
    "QKD",
    "VQE",
    "RSA",
]
_BASIS = ["I", "H"]
_VALUES = ["0", "1"]


def to_bin(c: str) -> str:
    """Converts a single character to a binary ASCII string.

    This returns a str of length 8 that corresponds to the
    ASCII value of the character.
    """
    return ("00000000" + bin(ord(c)).replace("0b", ""))[-8:]


def gen_bb84(word: str) -> Tuple[str, str]:
    alice = ""
    bob = ""
    key = "".join(to_bin(c) for c in word)
    c = 0
    while c < len(key):
        alice_base = random.choice(_BASIS)
        bob_base = random.choice(_BASIS)
        if alice_base == bob_base:
            alice_sent = key[c]
            bob_recv = key[c]
            c += 1
        else:
            alice_sent = random.choice(_VALUES)
            bob_recv = random.choice(_VALUES)
        alice += alice_base + alice_sent
        bob += bob_base + bob_recv
    return (alice, bob)


def solve_bb84(alice: str, bob: str):
    """Hey, no cheating!

    This solves a alice/bob BB84 riddle.  Used for testing
    or for if you get stuck.
    """

    assert len(alice) == len(bob), "Alice or Bob are missing bits!"
    key = ""
    for idx in range(0, len(alice), 2):
        if alice[idx] == bob[idx]:
            assert alice[idx + 1] == bob[idx + 1], "Eve has measured a qubit!"
            key += alice[idx + 1]
    word = ""
    for idx in range(0, len(key), 8):
        word += chr(int(key[idx : idx + 8], 2))
    return word


def _gen_keys(state: GameState):
    if "alice" not in state.state_dict:
        word = random.choice(_WORDS)
        alice, bob = gen_bb84(word)
        state.state_dict["alice"] = alice
        state.state_dict["bob"] = bob


def _view_alice(state: GameState, world):
    if "astatus" not in state.state_dict:
        return "The display is blank."
    if state.state_dict["astatus"] == "on":
        return "The display reads 'Ready to TRANSMIT'"
    if state.state_dict["astatus"] == "success":
        return f"The display reads 'Transmission Successful:'\n'{state.state_dict['alice']}'"
    return f"The display reads 'Error transmitting data.'"


def _view_bob(state: GameState, world):
    if "bstatus" not in state.state_dict:
        return "The display is blank."
    if state.state_dict["bstatus"] == "on":
        return "The display reads 'Ready to Receive'"
    if state.state_dict["bstatus"] == "success":
        return f"The display reads 'Received data:'\n'{state.state_dict['bob']}'"
    return f"The display reads 'Error receiving data.'"


def _power_on_alice(state: GameState, world):
    _gen_keys(state)
    if "astatus" in state.state_dict:
        return "The device is already turned on."
    state.state_dict["astatus"] = "on"
    return "The device whirs as it turns on."


def _power_on_bob(state: GameState, world):
    _gen_keys(state)
    if "bstatus" in state.state_dict:
        return "The device is already turned on."
    state.state_dict["bstatus"] = "on"
    return "The device whirs as it turns on."


def _send_alice(state: GameState, world):
    if "astatus" not in state.state_dict:
        return "Nothing happens."
    if state.state_dict["astatus"] != "success":
        if "bstatus" not in state.state_dict:
            # Bob is turned off.
            state.state_dict["astatus"] = "error"
            return "The device emits a long and sad beep."
        state.state_dict["astatus"] = "success"
        state.state_dict["bstatus"] = "success"
        return "The device chimes happily."
    return "The device chimes again."


ALICE = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["machine", "laser", "device", "alice"],
            (
                "This machine seems to be a strange laser placed on a pedestal.\n"
                "The machine is safely protected from the elements by an awning that\n"
                "hangs over it.  The device is mounted so that it is pointed towards\n"
                "a hill to the west.  The device is connected to a rack of electronics\n"
                "that have a status display.  There are two buttons: POWER and TRANSMIT.\n"
                "A sticky note attached to the device has the word 'Alice'"
            ),
        ),
        (
            EXAMINE,
            ["display", "status", "electronics"],
            _view_alice,
        ),
        (
            ["press", "use", "tap", "touch"],
            ["power"],
            _power_on_alice,
        ),
        (
            ["press", "use", "tap", "touch"],
            ["transmit"],
            _send_alice,
        ),
    ],
    description="A strange looking machine is mounted under an awning.",
)

BOB = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["machine", "laser", "receiver", "device", "bob"],
            (
                "This machine seems to be a strange receiving device vaguely\n"
                "resembling a photovoltaic cell set on a pedestal.\n"
                "The machine is safely protected from the elements by an awning that\n"
                "hangs over it.  The device is mounted so that the receiving panel\n"
                "is pointed towards a hill to the east.  The device is connected\n"
                "to a rack of electronics that have a status display.  A button\n"
                "labeled POWER seems to be the only visible button.\n"
                "A sticky note attached to the device has the word 'Bob'"
            ),
        ),
        (
            EXAMINE,
            ["display", "status", "electronics"],
            _view_bob,
        ),
        (
            ["press", "use", "tap", "touch"],
            ["power"],
            _power_on_bob,
        ),
    ],
    description="A strange looking machine is mounted under an awning.",
)
