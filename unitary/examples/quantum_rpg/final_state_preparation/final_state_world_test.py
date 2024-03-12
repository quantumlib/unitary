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
"""Various consistency checks to make sure the world is correctly built."""
import pytest
import io

import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.exceptions as exceptions
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.final_state_preparation.final_state_world as final_state
from unitary.examples.quantum_rpg.world import Direction, World


OPPOSITE_DIR = {
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
}

# Rooms that purposely do not have a way back.
_ONE_WAY_ROOMS = {"hadamard1", "hadamard4_0", "hadamard4_1", "hadamard5", "perimeter1"}


def find_room(room_name: str):
    for location in final_state.WORLD:
        if location.label == room_name:
            return location


def go_directions(path: str) -> World:
    """Parse one letter directions from the start point."""
    example_world = World(final_state.WORLD)
    for cmd in path:
        cur_room = example_world.current_location.label
        direction = Direction.parse(cmd)
        assert direction is not None
        result = example_world.move(direction)
        assert cmd is not None, f"Moving {cmd} in room {cur_room} not valid"
    return example_world


def test_consistent_exits():
    """Test that going to and from all exits is consistent."""
    for location in final_state.WORLD:
        if location.label in _ONE_WAY_ROOMS:
            continue
        for direction, room_name in location.exits.items():
            nearby_room = find_room(room_name)
            assert nearby_room is not None, f"Missing room {room_name}"
            try:
                return_exit = nearby_room.exits[OPPOSITE_DIR[direction]]
            except KeyError as e:
                raise KeyError(
                    f"{room_name} does not have a return exit in {direction} to {location.label}"
                )
            assert (
                return_exit == location.label
            ), f"Inconsistent {direction} exit in {location.label}"


@pytest.mark.parametrize(
    "path, expected_location",
    [
        ("ns", "classical1"),
        ("nn", "classical3"),
        ("nnee", "classical5"),
        ("nneee", "oxtail1"),
        ("nneeee", "quad4"),
        ("nneeeeeen", "quad3"),
        ("nneeeeees", "quad9"),
        ("nneeeenen", "comms1"),
        ("nneeeenenuu", "comms3"),
        ("nneeeeee", "quad6"),
        ("nneeeeeee", "nmr_lab1"),
        ("nneeeeeeeeu", "nmr_lab3"),
    ],
)
def test_classical_realm_paths(path, expected_location):
    test_world = go_directions(path)
    assert test_world.current_location.label == expected_location


def test_engineer_joins_the_party():
    """Test that the engineer (second qaracter) propoerly joins the party.

    This should happen when you talk to the engineer in the NMR lab.
    """
    c = classes.Analyst("Mensing")
    state = game_state.GameState(party=[c], user_input=["Hamilton"], file=io.StringIO())
    test_world = go_directions("nneeeeeeeeu")
    action = test_world.current_location.get_action("talk engineer")
    assert callable(action)
    msg = action(state, test_world)
    assert msg == "Hamilton has joined the group!"
    assert len(state.party) == 2
    # Make sure that the engineer can't join the party twice.
    msg = action(state, test_world)
    assert msg == "The engineer reminisces about his former experiment."
    assert len(state.party) == 2


def test_hole():
    test_world = go_directions("nnen")
    assert test_world.current_location.title == "Near a Pixelated Hole"
    state = game_state.GameState(party=[], user_input=[""], file=io.StringIO())
    action = test_world.current_location.get_action("enter hole")
    assert callable(action)
    with pytest.raises(
        exceptions.UntimelyDeathException,
        match="You feel your entire existence dissolve into errors",
    ):
        _ = action(state, test_world)


def test_bridge():
    c = classes.Analyst("Mensing")
    state = game_state.GameState(party=[c], user_input=["Hamilton"], file=io.StringIO())
    state.current_location_label = "classical12"
    test_world = go_directions("nnwnnnne")
    bridge_location = test_world.get("classical12")
    fix = test_world.current_location.get_action("fix bridge")
    examine = test_world.current_location.get_action("examine bridge")

    # The world and the game state are at the location of the broken bridge, which can be fixed and examined.
    assert test_world.current_location.title == "At a Broken Bridge"
    assert (
        test_world.current_location.label
        == state.current_location_label
        == bridge_location.label
    )
    assert callable(fix)
    assert callable(examine)

    # The bridge is not yet fixed
    assert Direction.NORTH not in bridge_location.exits

    # Examining the bridge doesn't fix it, nor can it be fixed without an engineer.
    msg = examine(state, test_world)
    assert Direction.NORTH not in bridge_location.exits

    msg = fix(state, test_world)
    assert msg == "You do not have the required skills to fix the bridge."
    assert Direction.NORTH not in bridge_location.exits

    # The engineer is able to fix the bridge,
    # and the fix is saved in the game state.
    c = classes.Engineer("Tesla")
    state.party.append(c)
    msg = fix(state, test_world)
    assert (
        msg
        == "The engineer uses nearby logs to repair the bridge and provide a safe passage."
    )
    assert Direction.NORTH in bridge_location.exits
    assert state.state_dict["hbridgestate"] == "fixed"

    # The bridge is already fixed,
    # fixing it or examining it doesn't change that.
    msg = fix(state, test_world)
    assert msg == "You have already fixed the bridge."

    msg = examine(state, test_world)
    assert msg == "You have already fixed the bridge."

    assert Direction.NORTH in bridge_location.exits

    # Remove North direction to simulate restarting the game
    # with bridge fix in the save file.
    bridge_location.exits.pop(Direction.NORTH)

    # The bridge doesn't appear fixed,
    # but on further examination we learn that it had been fixed,
    # so now we know it can be used to exit North.
    assert Direction.NORTH not in bridge_location.exits
    msg = examine(state, test_world)
    assert msg == "You have already fixed the bridge."
    assert Direction.NORTH in bridge_location.exits
