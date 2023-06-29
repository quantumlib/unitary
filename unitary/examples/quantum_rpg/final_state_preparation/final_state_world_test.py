"""Various consistency checks to make sure the world is correctly built."""
import pytest
import io

import unitary.examples.quantum_rpg.classes as classes
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
        for direction, room_name in location.exits.items():
            nearby_room = find_room(room_name)
            assert nearby_room is not None, f"Missing room {room_name}"
            return_exit = nearby_room.exits[OPPOSITE_DIR[direction]]
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


def test_engineer():
    c = classes.Analyst("Mensing")
    state = game_state.GameState(party=[c], user_input=["Hamilton"], file=io.StringIO())
    test_world = go_directions("nneeeeeeeeu")
    action = test_world.current_location.get_action("talk engineer")
    assert callable(action)
    msg = action(state)
    assert msg == "Hamilton has joined the group!"
    assert len(state.party) == 2
