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
from unitary.examples.quantum_rpg.final_state_preparation.monsters import (
    blue_foam,
    red_foam,
    purple_foam,
)

CHARLES = Item(
    keyword_actions=[
        (
            TALK,
            ["man", "charles", "elder", "physicist"],
            (
                "The physicist introduces himself as Charles.  'I am working on a\n"
                "device to communicate in the quantum realm.  I am currently testing\n"
                "a sensitive receiver to detect a laser beam from across the hills.\n"
                "The communication is immune to eavesdropping, but the receiver has\n"
                "to measure in either the computational basis (I) or the Hadamard (H)\n"
                "basis. The receiver cannot know which basis the laser beam was sent in.\n"
                "If I can figure this protocol out, I think it can be used to create\n"
                "bank notes immune to counterfeiting.' Charles says hopefully."
            ),
        )
    ],
    description="A balding physicist with short gray hair sits behind the desk.",
)

GILLES = Item(
    keyword_actions=[
        (
            TALK,
            ["man", "gilles", "elder", "physicist"],
            (
                "The physicist introduces himself as Gilles.  'I am working on a\n"
                "device to communicate in the quantum realm.  I am currently testing\n"
                "it by shining a laser beam across the hills to a receiver on the other\n"
                "side of the valley.  Each bit (either a 1 or 0) is encoded in either the\n"
                "computational basis, using an identity (I) gate or in the Hadamard basis\n"
                "using a H gate.  That way, no one can eaesdrop or corrupt the channel\n"
                "without a measurement being detected!'  Gilles cackles at his invention."
            ),
        )
    ],
    description="An elder physicist with long, flowing gray hair sits behind the desk.",
)

EAST_EGG = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["painting"],
            (
                "A painting of a colonial mansion takes up most of the wall.\n"
                "The cheerful red and white Georgian Colonial overlooks a misty\n"
                "bay.  A wooden dock with a green light extends into the water."
            ),
        )
    ],
    description="A painting of a colonial mansion hangs on one wall.",
)


WEST_EGG = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["painting", "hotel", "mansion", "pool", "wall"],
            (
                "A painting of a colossal lakeside building in the style of a French\n"
                "hotel takes up most of one wall.  The mansion is surrounded by gawdy\n"
                "party goers mingling around a marble pool."
            ),
        )
    ],
    description="A painting of a colossal French hotel hangs on one wall.",
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
        encounters=[red_foam(2, 0.2)],
        items=[],
        exits={Direction.SOUTH: "classical12", Direction.NORTH: "hadamard2"},
    ),
    Location(
        label="hadamard2",
        title="Bottom of Superposition Trail",
        description=(
            "You are at the bottom of a steep slope that leads up to Hadamard Hills\n"
            "proper.  There seem to be two ways that you can go up the slope."
        ),
        encounters=[purple_foam(2, 0.2), red_foam(2, 0.2)],
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
        encounters=[purple_foam(2, 0.2), red_foam(2, 0.2)],
        exits={Direction.NORTH: "hadamard4_0", Direction.WEST: "hadamard2"},
    ),
    Location(
        label="hadamard3_1",
        title="Bottom of Superposition Slope",
        description=(
            "You are at the bottom of a steep slope that leads up to Hadamard Hills\n"
            "proper.  The trails north lead steeply up to the top of the hills.\n"
        ),
        encounters=[purple_foam(2, 0.2), red_foam(2, 0.2)],
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
        encounters=[purple_foam(3, 0.3), purple_foam(2, 0.2)],
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
        encounters=[purple_foam(3, 0.3), purple_foam(2, 0.2)],
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
        encounters=[purple_foam(3, 0.2)],
        exits={Direction.NORTH: "hadamard6", Direction.SOUTH: "hadamard2"},
    ),
    Location(
        label="hadamard6",
        title="Within the Foothills",
        description=(
            "You are entering a cluster of hills that extend to the north.\n"
            "To the east and west, two identical peaks rise from the maze\n"
            "of foothills.  The mirroring of terrain on both sides gives you\n"
            "a sense of the symmetrical beauty of nature.\n"
        ),
        encounters=[purple_foam(3, 0.2), blue_foam(3, 0.1)],
        exits={Direction.SOUTH: "hadamard5", Direction.NORTH: "hadamard7"},
    ),
    Location(
        label="hadamard7",
        title="Between the Foothills",
        description=(
            "You are between two similar ranges of hills to the east\n"
            "and west.  Identical paths in either direction wind up\n"
            "the rising terrain towards the tops of the hills.  A\n"
            "path to the north leads up a slope towards a group of\n"
            "grey buildings."
        ),
        encounters=[purple_foam(3, 0.2), blue_foam(3, 0.1)],
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
        description=(
            "The trail gently slopes upwards on a winding path up towards\n"
            "the peak of the eastern hill."
        ),
        encounters=[purple_foam(4, 0.1)],
        exits={Direction.WEST: "hadamard7", Direction.EAST: "hadamard9_0"},
    ),
    Location(
        label="hadamard8_1",
        title="At the Foot of the West Hill",
        description=(
            "The trail gently slopes upwards on a winding path up towards\n"
            "the peak of the western hill."
        ),
        encounters=[purple_foam(4, 0.1)],
        exits={Direction.EAST: "hadamard7", Direction.WEST: "hadamard9_1"},
    ),
    Location(
        label="hadamard9_0",
        title="The Slope of the East Hill",
        description=(
            "The trail to the top of the eastern hill begins to\n"
            "get steeper and more strenuous as it makes its way\n"
            "up towards a ridge to the east."
        ),
        encounters=[purple_foam(3, 0.1)],
        exits={Direction.WEST: "hadamard8_0", Direction.EAST: "hadamard10_0"},
    ),
    Location(
        label="hadamard9_1",
        title="The Slope of the West Hill",
        description=(
            "The trail to the top of the western hill begins to\n"
            "get steeper and more strenuous as it makes its way\n"
            "up towards a ridge to the west."
        ),
        encounters=[purple_foam(3, 0.1)],
        exits={Direction.EAST: "hadamard8_1", Direction.WEST: "hadamard10_1"},
    ),
    Location(
        label="hadamard10_0",
        title="In front of the East Hut",
        description=(
            "At a small plateau on the way to the eastern hill,\n"
            "there is a small but well-maintained dwelling.\n"
            "Some lights from within this wooden hut to the south\n"
            "suggest that it is inhabited."
        ),
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
        description=(
            "At a small plateau on the way to the western hill,\n"
            "there is a small but well-maintained dwelling.\n"
            "Some lights from within this wooden hut to the south\n"
            "suggest that it is inhabited."
        ),
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
        description=(
            "You have entered an austere room filled with neatly organized\n"
            "booksheles and filing cabinets.  In one corner, an intricate\n"
            "optical table with many components is ready for a photonics experiment.\n"
            "A clean desk with a reading lamp takes up a large part of the room."
        ),
        encounters=[],
        items=[CHARLES, EAST_EGG],
        exits={Direction.NORTH: "hadamard10_0"},
    ),
    Location(
        label="hadamard11_1",
        title="West Hut",
        description=(
            "You have entered a cozy living space filled to the brim with\n"
            "papers and books stacked all around the room.  A large heap\n"
            "of hastily piled electronics clutters up a corner of the room.\n"
            "A desk with a lamp piled high with manuscripts and technical\n"
            "specifications takes up a big part of the room."
        ),
        encounters=[],
        items=[GILLES, WEST_EGG],
        exits={Direction.NORTH: "hadamard10_1"},
    ),
    Location(
        label="hadamard12_0",
        title="Upward Slope",
        description=(
            "The trail continues upwards towards the top of the hill.\n"
            "Here, the trail begins to get steep, with large boulders\n"
            "marking the sides of the path.  To the east, a large scree\n"
            "scramble forms the way forward."
        ),
        encounters=[purple_foam(3, 0.2)],
        exits={Direction.WEST: "hadamard10_0", Direction.UP: "hadamard13_0"},
    ),
    Location(
        label="hadamard12_1",
        title="Upward Slope",
        description=(
            "The trail continues upwards towards the top of the hill.\n"
            "Here, the trail begins to get steep, with large boulders\n"
            "marking the sides of the path.  To the east, a large scree\n"
            "scramble forms the way forward."
        ),
        encounters=[purple_foam(3, 0.2)],
        exits={Direction.EAST: "hadamard10_1", Direction.UP: "hadamard13_1"},
    ),
    Location(
        label="hadamard13_0",
        title="Climbing the East Slope",
        description=(
            "The trail gets treacherously steep here, as it climbs\n"
            "up a scree slope.  Several decrepit packed dirt stairs\n"
            "are the only footholds on the steep path, which leads\n"
            "up at a nearly forty-five degree angle."
        ),
        encounters=[purple_foam(2, 0.2)],
        exits={Direction.DOWN: "hadamard12_0", Direction.UP: "hadamard14_0"},
    ),
    Location(
        label="hadamard13_1",
        title="Climbing the West Slope",
        description=(
            "The trail gets treacherously steep here, as it climbs\n"
            "up a scree slope.  Several decrepit packed dirt stairs\n"
            "are the only footholds on the steep path, which leads\n"
            "up at a nearly forty-five degree angle."
        ),
        encounters=[purple_foam(2, 0.2)],
        exits={Direction.DOWN: "hadamard12_1", Direction.UP: "hadamard14_1"},
    ),
    Location(
        label="hadamard14_0",
        title="Near the Top of the East Hill",
        description=(
            "The trail has nearly reached the summit of the hill.\n"
            "Here, the terrain levels off with a relatively smooth\n"
            "sloping path north, where a tented pavillion is set up."
        ),
        encounters=[],
        exits={Direction.DOWN: "hadamard13_0", Direction.NORTH: "hadamard15_0"},
    ),
    Location(
        label="hadamard14_1",
        title="Near the Top of the West Hill",
        description=(
            "The trail has nearly reached the summit of the hill.\n"
            "Here, the terrain levels off with a relatively smooth\n"
            "sloping path north, where a tented pavillion is set up."
        ),
        encounters=[],
        exits={Direction.DOWN: "hadamard13_1", Direction.NORTH: "hadamard15_1"},
    ),
    Location(
        label="hadamard15_0",
        title="East Hill Pavillion",
        description=(
            "At the top of the east hill is a concrete slab.\n"
            "A post at each of the four corners supports a taut piece\n"
            "of heavy fabric that proides some shade for those that\n"
            "have made it this far."
        ),
        encounters=[],
        items=[ALICE],
        exits={Direction.SOUTH: "hadamard14_0"},
    ),
    Location(
        label="hadamard15_1",
        title="West Hill Pavillion",
        description=(
            "At the top of the west hill is a concrete slab.\n"
            "A post at each of the four corners supports a taut piece\n"
            "of heavy fabric that proides some shade for those that\n"
            "have made it this far."
        ),
        encounters=[],
        items=[BOB],
        exits={Direction.SOUTH: "hadamard14_1"},
    ),
    Location(
        label="hadamard16",
        title="Path towards the Perimeter",
        description=(
            "A path leads north out of the Hadamard Hills towards\n"
            "a group of large grey buildings.  The sun reflects\n"
            "brilliantly from the yellow-tinted windows the line\n"
            "the buildings in irregular triangular shapes."
        ),
        encounters=[purple_foam(3, 0.2)],
        items=[],
        exits={Direction.SOUTH: "hadamard7", Direction.NORTH: "hadamard17"},
    ),
    Location(
        label="hadamard17",
        title="Research Facility Entrance",
        description=(
            "As you near the imposing grey buildings, you can see that\n"
            "they form a research outpost.  What must have once been\n"
            "an impressive and state-of-the-art facility now shows\n"
            "signs of damage. Pieces of the building have been turned\n"
            "into the iridiscent static of quantum errors. Broken windows\n"
            "and pitted walls show signs of disrepair."
        ),
        encounters=[],
        items=[DOOR],
        exits={
            Direction.SOUTH: "hadamard16",
        },
    ),
]
