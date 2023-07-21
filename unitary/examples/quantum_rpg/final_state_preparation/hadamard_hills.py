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
import unitary.alpha as alpha

from unitary.examples.quantum_rpg.bb84 import ALICE, BOB, DOOR
from unitary.examples.quantum_rpg.encounter import Encounter
from unitary.examples.quantum_rpg.game_state import GameState
from unitary.examples.quantum_rpg.item import EXAMINE, TALK, Item
from unitary.examples.quantum_rpg.world import Direction, Location

CONSTRUCTION_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            "sign",
            (
                "Congratulations on making it to the end of the demo!\n"
                "The following zone (Hadamard Hills) is still under construction,\n"
                "but you can explore it while it is being built!"
            ),
        )
    ],
    description="A yellow and black sign denotes a warning here.",
)


HADAMARD_HILLS = [
    Location(
        label="hadamard1",
        title="On the Northern Bank",
        description=(
            "You have reached the northern bank of the river and are at the edge\n"
            "of the Hadamard Hills, which mark the absolute southern border of the\n"
            "quantum realm. A trail to the north leads up the hills."
        ),
        encounters=[],
        items=[CONSTRUCTION_SIGN],
        exits={Direction.SOUTH: "classical12", Direction.NORTH: "hadamard2"},
    ),
    Location(
        label="hadamard2",
        title="Bottom of Superposition Trail",
        description=(
            "You are at the bottom of a steep slope that leads up to Hadamard Hills\n"
            "proper.  There seem to be two ways that you can go up the slope."
        ),
        encounters=[],
        exits={
            Direction.SOUTH: "hadamard1",
            Direction.EAST: "hadamard3_0",
            Direction.WEST: "hadamard3_1",
        },
    ),
    Location(
        label="hadamard3_0",
        title="Bottom of Superposition Slope",
        description=(
            "You are at the bottom of a steep slope that leads up to Hadamard Hills\n"
            "proper.  The trails north lead steeply up to the top of the hills.\n"
        ),
        encounters=[],
        exits={Direction.NORTH: "hadamard4_0", Direction.WEST: "hadamard2"},
    ),
    Location(
        label="hadamard3_1",
        title="Bottom of Superposition Slope",
        description=(
            "You are at the bottom of a steep slope that leads up to Hadamard Hills\n"
            "proper.  The trails north lead steeply up to the top of the hills.\n"
        ),
        encounters=[],
        exits={Direction.NORTH: "hadamard4_1", Direction.EAST: "hadamard2"},
    ),
    Location(
        label="hadamard4_0",
        title="Superposition Slope",
        description=(
            "You are climbing up a steep slope.  To the north is the Hadamard hills,\n"
            "and to the south, the trail leads down to the river separating the\n"
            "classical realm from the Hadamard Hills."
        ),
        encounters=[],
        exits={Direction.NORTH: "hadamard5", Direction.SOUTH: "hadamard3_0"},
    ),
    Location(
        label="hadamard4_1",
        title="Superposition Slope",
        description=(
            "You are climbing up a steep slope.  To the north is the Hadamard hills,\n"
            "and to the south, the trail leads down to the river separating the\n"
            "classical realm from the Hadamard Hills."
        ),
        encounters=[],
        exits={Direction.NORTH: "hadamard5", Direction.SOUTH: "hadamard3_1"},
    ),
    Location(
        label="hadamard5",
        title="Top of Superposition Slope",
        description=(
            "You have reached the top of the Superposition Slope.  From here,\n"
            "you can see the river winding its way through the valley from the south,\n"
            "and the path downwards in that direction looks extremely steep and treacherous.\n"
            "To the north, the foothills continue.  Two prominent peaks to the north-east\n"
            "and north-west are the most obvious features, though the land slopes gradually\n"
            "towards the mountains of error correction in the northernmost distance.\n"
        ),
        encounters=[],
        exits={Direction.NORTH: "hadamard6", Direction.SOUTH: "hadamard2"},
    ),
    Location(
        label="hadamard6",
        title="Within the Foothills",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.SOUTH: "hadamard5", Direction.NORTH: "hadamard7"},
    ),
    Location(
        label="hadamard7",
        title="Between the Foothills",
        description=("Room description forthcoming."),
        encounters=[],
        exits={
            Direction.NORTH: "hadamard16",
            Direction.SOUTH: "hadamard6",
            Direction.EAST: "hadamard8_0",
            Direction.WEST: "hadamard8_1",
        },
    ),
    Location(
        label="hadamard8_0",
        title="At the Foot of the East Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.WEST: "hadamard7", Direction.EAST: "hadamard9_0"},
    ),
    Location(
        label="hadamard8_1",
        title="At the Foot of the West Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.EAST: "hadamard7", Direction.WEST: "hadamard9_1"},
    ),
    Location(
        label="hadamard9_0",
        title="The Slope of the East Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.WEST: "hadamard8_0", Direction.EAST: "hadamard10_0"},
    ),
    Location(
        label="hadamard9_1",
        title="The Slope of the West Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.EAST: "hadamard8_1", Direction.WEST: "hadamard10_1"},
    ),
    Location(
        label="hadamard10_0",
        title="In front of the East Hut",
        description=("Room description forthcoming."),
        encounters=[],
        exits={
            Direction.WEST: "hadamard9_0",
            Direction.SOUTH: "hadamard11_0",
            Direction.EAST: "hadamard12_0",
        },
    ),
    Location(
        label="hadamard10_1",
        title="In front of the West Hut",
        description=("Room description forthcoming."),
        encounters=[],
        exits={
            Direction.EAST: "hadamard9_1",
            Direction.SOUTH: "hadamard11_1",
            Direction.WEST: "hadamard12_1",
        },
    ),
    Location(
        label="hadamard11_0",
        title="East Hut",
        description=("Room description forthcoming."),
        encounters=[],
        items=[],  # TODO: Charles, egg
        exits={Direction.NORTH: "hadamard10_0"},
    ),
    Location(
        label="hadamard11_1",
        title="West Hut",
        description=("Room description forthcoming."),
        encounters=[],
        items=[],  # TODO: Giles, egg
        exits={Direction.NORTH: "hadamard10_1"},
    ),
    Location(
        label="hadamard12_0",
        title="Upward Slope",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.WEST: "hadamard10_0", Direction.UP: "hadamard13_0"},
    ),
    Location(
        label="hadamard12_1",
        title="Upward Slope",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.EAST: "hadamard10_1", Direction.UP: "hadamard13_1"},
    ),
    Location(
        label="hadamard13_0",
        title="Climbing the East Slope",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.DOWN: "hadamard12_0", Direction.UP: "hadamard14_0"},
    ),
    Location(
        label="hadamard13_1",
        title="Climbing the West Slope",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.DOWN: "hadamard12_1", Direction.UP: "hadamard14_1"},
    ),
    Location(
        label="hadamard14_0",
        title="Near the Top of the East Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.DOWN: "hadamard13_0", Direction.NORTH: "hadamard15_0"},
    ),
    Location(
        label="hadamard14_1",
        title="Near the Top of the West Hill",
        description=("Room description forthcoming."),
        encounters=[],
        exits={Direction.DOWN: "hadamard13_1", Direction.NORTH: "hadamard15_1"},
    ),
    Location(
        label="hadamard15_0",
        title="East Hill Pavillion",
        description=("Room description forthcoming."),
        encounters=[],
        items=[ALICE],
        exits={Direction.SOUTH: "hadamard14_0"},
    ),
    Location(
        label="hadamard15_1",
        title="West Hill Pavillion",
        description=("Room description forthcoming."),
        encounters=[],
        items=[BOB],
        exits={Direction.SOUTH: "hadamard14_1"},
    ),
    Location(
        label="hadamard16",
        title="Path to the Research Institute",  # TODO: What's the next zone?
        description=("Room description forthcoming."),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "hadamard7", Direction.NORTH: "hadamard17"},
    ),
    Location(
        label="hadamard17",
        title="Door of the Research Institute",
        description=("Room description forthcoming."),
        encounters=[],
        items=[DOOR],
        exits={
            Direction.SOUTH: "hadamard16",
        },
    ),
]
