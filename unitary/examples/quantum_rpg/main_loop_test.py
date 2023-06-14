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

import io
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.item as item
import unitary.examples.quantum_rpg.main_loop as main_loop
import unitary.examples.quantum_rpg.npcs as npcs
import unitary.examples.quantum_rpg.world as world

_COUNTER = "counter"


def _press_button(state: game_state.GameState) -> str:
    counter = state.state_dict.get(_COUNTER, 0)
    state.state_dict[_COUNTER] = counter + 1
    return f"You've pressed the button {counter} times before!"


SIGN = item.Item(
    keyword_actions=[("read", "sign", "This is an example world!")],
    description="A helpful sign is here.",
)
BUTTON = item.Item(
    keyword_actions=[("press", "button", _press_button)],
)


EXAMPLE_WORLD = [
    world.Location(
        label="1",
        title="Lab Entrance",
        description="You stand before the entrance to the premier quantum lab.\nDouble doors lead east.",
        items=[BUTTON],
        exits={world.Direction.EAST: "2"},
    ),
    world.Location(
        label="2",
        title="Disorganized Lab",
        description="Tables are here with tons of electronics.\nThe lab continues to the south.",
        items=[SIGN],
        exits={world.Direction.SOUTH: "3", world.Direction.WEST: "1"},
    ),
    world.Location(
        label="3",
        title="Cryostats",
        description="Giant aluminum cylinders hang suspended by large frames.\nRhythmic whirring of a pulse tube can be heard overhead.",
        encounters=[
            encounter.Encounter(
                [npcs.Observer("watcher")],
                description="A weird security guard approaches!",
                probability=1.0,
            )
        ],
        exits={world.Direction.NORTH: "2"},
    ),
]


def test_parse_commands() -> None:
    assert main_loop.Command.parse("x") is None
    assert main_loop.Command.parse("q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Quit") is main_loop.Command.QUIT
    assert main_loop.Command.parse("quit") is main_loop.Command.QUIT


def test_simple_main_loop() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(party=[c], user_input=["quit"], file=io.StringIO())
    loop = main_loop.MainLoop(state=state, world=world.World(EXAMPLE_WORLD))
    loop.loop(user_input=["quit"])
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.
""".strip()
    )


def test_do_simple_move() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "read sign", "w", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(world.World(EXAMPLE_WORLD), state)
    loop.loop()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

Disorganized Lab

Tables are here with tons of electronics.
The lab continues to the south.
A helpful sign is here.

Exits: south, west.

This is an example world!
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.


""".strip()
    )


def test_battle() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "south", "s", "1", "1", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(state=state, world=world.World(EXAMPLE_WORLD))
    loop.loop()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

Disorganized Lab

Tables are here with tons of electronics.
The lab continues to the south.
A helpful sign is here.

Exits: south, west.

Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.

Exits: north.

A weird security guard approaches!
-----------------------------------------------
Mensing Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Mensing turn:
s
m
Sample result HealthPoint.HURT
Observer watcher measures Mensing at qubit Mensing_1
Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.

Exits: north.
""".strip()
    )


def test_item_function():
    c = classes.Analyst("michalakis")
    state = game_state.GameState(
        party=[c],
        user_input=["press button", "press button", "press button", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.MainLoop(world.World(EXAMPLE_WORLD), state)
    loop.loop()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

You've pressed the button 0 times before!
You've pressed the button 1 times before!
You've pressed the button 2 times before!
""".strip()
    )


def test_title_screen():
    state = game_state.GameState(party=[], user_input=[], file=io.StringIO())
    loop = main_loop.MainLoop(state=state, world=world.World(EXAMPLE_WORLD))
    loop.print_title_screen()

    assert (
        state.file.getvalue()
        == r"""
______  _                _             _____  _           _
|  ___|(_)              | |           /  ___|| |         | |
| |_    _  _ __    __ _ | |    __     \ `--. | |_   __ _ | |_   ___
|  _|  | || '_ \  / _` || |    ()      `--. \| __| / _` || __| / _ \
| |    | || | | || (_| || |    )(     /\__/ /| |_ | (_| || |_ |  __/
\_|    |_||_| |_| \__,_||_|    )(     \____/  \__| \__,_| \__| \___|
                            o======o
                               ||
______                         ||              _    _
| ___ \                        ||             | |  (_)
| |_/ / _ __   ___  _ __    __ _| _ __   __ _ | |_  _   ___   _ __
|  __/ | '__| / _ \| '_ \  / _` || '__| / _` || __|| | / _ \ | '_ \
| |    | |   |  __/| |_) || (_| || |   | (_| || |_ | || (_) || | | |
\_|    |_|    \___|| .__/  \__,_||_|    \__,_| \__||_| \___/ |_| |_|
                   | |         ||
                   |_|         \/

"""
    )
