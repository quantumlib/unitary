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

import copy
import io
import unitary.alpha as alpha
import unitary.examples.quantum_rpg.ascii_art as ascii_art
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.item as item
import unitary.examples.quantum_rpg.main_loop as main_loop
import unitary.examples.quantum_rpg.npcs as npcs
import unitary.examples.quantum_rpg.world as world

_COUNTER = "counter"


def _press_button(state: game_state.GameState, world: world.World) -> str:
    counter = state.state_dict.get(_COUNTER, "0")
    state.state_dict[_COUNTER] = str(int(counter) + 1)
    return f"You've pressed the button {counter} times before!"


SIGN = item.Item(
    keyword_actions=[("read", "sign", "This is an example world!")],
    description="A helpful sign is here.",
)
BUTTON = item.Item(
    keyword_actions=[("press", "button", _press_button)],
)


def example_world():
    return [
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


_TITLE = r"""
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

-----------------------------------------------
1) Begin new adventure
2) Load existing adventure
3) Help
4) Quit
-----------------------------------------------
"""


def test_parse_commands() -> None:
    assert main_loop.Command.parse("x") is None
    assert main_loop.Command.parse("q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Q") is main_loop.Command.QUIT
    assert main_loop.Command.parse("Quit") is main_loop.Command.QUIT
    assert main_loop.Command.parse("quit") is main_loop.Command.QUIT


def test_simple_main_loop() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(party=[c], user_input=["quit"], file=io.StringIO())
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.
""".strip()
    )


def test_empty_command() -> None:
    state = game_state.GameState(
        party=[], user_input=["", "", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

I did not understand the command .
I did not understand the command .
""".strip()
    )


def test_status() -> None:
    c = classes.Analyst("Nova")
    c.add_quantum_effect(alpha.Flip(), 1)
    c2 = classes.Engineer("Maxwell")
    c2.add_hp()
    c2.add_quantum_effect(alpha.Superposition(), 1)
    c2.add_quantum_effect(alpha.Flip(effect_fraction=0.5), 2)
    state = game_state.GameState(
        party=[c, c2], user_input=["status", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop(user_input=["quit"])
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

1) Nova: Level 1 Analyst
Qaracter sheet:
Nova_1: ───X───
2) Maxwell: Level 2 Engineer
Qaracter sheet:
Maxwell_1: ───H───────

Maxwell_2: ───X^0.5───
""".strip()
    )


def test_do_simple_move() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "read sign", "w", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(world.World(example_world()), state)
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
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


def test_save() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "save", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(world.World(example_world()), state)
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
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

Use this code to return to this point in the game:
2;1;Mensing#Analyst#1
""".strip()
    )


def test_load() -> None:
    c = classes.Analyst("Broglie")
    state = game_state.GameState(
        party=[c],
        user_input=["load", "2;1;Mensing#Analyst#1", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert loop.game_state.party[0].name == "Mensing"
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

Paste the save file here to load the game from that point.
Disorganized Lab

Tables are here with tons of electronics.
The lab continues to the south.
A helpful sign is here.

Exits: south, west.
""".strip()
    )


def test_bad_load() -> None:
    c = classes.Analyst("Broglie")
    state = game_state.GameState(
        party=[c],
        user_input=["load", "", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.

Paste the save file here to load the game from that point.
Unrecognized save file.
Lab Entrance

You stand before the entrance to the premier quantum lab.
Double doors lead east.

Exits: east.
""".strip()
    )


def test_battle() -> None:
    c = classes.Analyst("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "south", "m", "1", "1", "quit"], file=io.StringIO()
    )
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
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
------------------------------------------------------------
Mensing Analyst                         1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Mensing turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
You have won the battle!
Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.

Exits: north.
""".strip()
    )


def test_lost_battle() -> None:
    c = classes.Engineer("Mensing")
    state = game_state.GameState(
        party=[c], user_input=["e", "south", "x", "1", "1", "quit"], file=io.StringIO()
    )
    assert state.party[0].name == "Mensing"
    assert len(state.party[0].active_qubits()) == 1
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert state.party[0].name == "Mensing"
    assert len(state.party[0].active_qubits()) == 1

    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""Lab Entrance

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
------------------------------------------------------------
Mensing Engineer                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Mensing turn:
x) Attack with X gate.
q) Read Quantopedia.
?) Help.
Observer watcher measures Mensing_1 as HURT.
You have been defeated!
"""
        + ascii_art.RIP_TOP
        + "\n"
        + "     |       |     Mensing      |\n"
        + ascii_art.RIP_BOTTOM
        + """
You have been measured and were found wanting.
Better luck next repetition."""
    )


def test_escaped_battle():
    c = classes.Engineer("Mensing")
    c.add_quantum_effect(alpha.Flip(), 1)
    state = game_state.GameState(
        party=[c], user_input=["e", "south", "x", "1", "1", "quit"], file=io.StringIO()
    )
    assert state.party[0].name == "Mensing"
    assert len(state.party[0].active_qubits()) == 1
    loop = main_loop.MainLoop(state=state, world=world.World(example_world()))
    loop.loop()
    assert state.party[0].name == "Mensing"
    assert len(state.party[0].active_qubits()) == 1

    assert (
        cast(io.StringIO, state.file).getvalue().replace("\t", " ").strip()
        == r"""Lab Entrance

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
------------------------------------------------------------
Mensing Engineer                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Mensing turn:
x) Attack with X gate.
q) Read Quantopedia.
?) Help.
Observer watcher measures Mensing_1 as HEALTHY.
You have escaped the battle!
Cryostats

Giant aluminum cylinders hang suspended by large frames.
Rhythmic whirring of a pulse tube can be heard overhead.

Exits: north."""
    )


def test_item_function():
    c = classes.Analyst("michalakis")
    state = game_state.GameState(
        party=[c],
        user_input=["press button", "press button", "press button", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.MainLoop(world.World(example_world()), state)
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


def test_main_quit():
    state = game_state.GameState(party=[], user_input=["4"], file=io.StringIO())
    loop = main_loop.main(state)

    assert state.file.getvalue() == _TITLE


def test_main_help():
    state = game_state.GameState(party=[], user_input=["3", "4"], file=io.StringIO())
    loop = main_loop.main(state)

    assert (
        state.file.getvalue()
        == _TITLE + ascii_art.HELP + "\n" + ascii_art.START_MENU + "\n"
    )


def test_main_begin():
    state = game_state.GameState(
        party=[], user_input=["1", "nova", "n", "quit"], file=io.StringIO()
    )
    loop = main_loop.main(state)

    assert (
        state.file.getvalue()
        == _TITLE
        + ascii_art.INTRO_STORY
        + r"""
Science Hut

At the edge of the classical frontier, a solitary hut
looks north towards the mountains in the distance.
Though still in the classical realm, it is clear the
researchers in this humble abode have aspirations for
the future.  Desks and chalkboards filled with diagrams
fill this room.
It is only natural that Richard is here to help start your journey.

Exits: north.

Edge of the Classical Frontier

You are standing outside a hut near the end of the classical domain.
This wild place which separates the classical from the quantum
realms. To the north is the frontier, where quantum phenomena are
studied and classified.  Far off in the distance are the fabled mountains
of error-correction, the subject of many theories and discussion.

A bent sign sticks out of the ground at an angle.

Exits: south, north.

"""
    )


def test_main_load():
    state = game_state.GameState(
        party=[],
        user_input=["2", "classical3;1;Doug#Analyst#1", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.main(state)

    assert (
        state.file.getvalue()
        == _TITLE
        + r"""Paste the save file here to load the game from that point.
The Classical Frontier

Here, the frontier between the classical and quantum realms begins.
Farther north, you can see faint undulations, as if the way is blurred
by some mirage.  To proceed, you will need to move around this strange
occurance.

Exits: south, east, west.

"""
    )


def test_main_bad_save_file():
    state = game_state.GameState(
        party=[],
        user_input=["2", "", "2", "classical3;1;Doug#Analyst#1", "quit"],
        file=io.StringIO(),
    )
    loop = main_loop.main(state)

    assert (
        state.file.getvalue()
        == _TITLE
        + r"""Paste the save file here to load the game from that point.
Unrecognized save file.
-----------------------------------------------
1) Begin new adventure
2) Load existing adventure
3) Help
4) Quit
-----------------------------------------------
Paste the save file here to load the game from that point.
The Classical Frontier

Here, the frontier between the classical and quantum realms begins.
Farther north, you can see faint undulations, as if the way is blurred
by some mirage.  To proceed, you will need to move around this strange
occurance.

Exits: south, east, west.

"""
    )
