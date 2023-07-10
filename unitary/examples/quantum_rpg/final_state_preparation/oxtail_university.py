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

from unitary.examples.quantum_rpg.classes import Engineer
from unitary.examples.quantum_rpg.encounter import Encounter
from unitary.examples.quantum_rpg.game_state import GameState
from unitary.examples.quantum_rpg.input_helpers import get_user_input_qaracter_name
from unitary.examples.quantum_rpg.final_state_preparation.monsters import (
    green_foam,
    blue_foam,
)
from unitary.examples.quantum_rpg.item import EXAMINE, TALK, Item
from unitary.examples.quantum_rpg.npcs import BlueFoam, GreenFoam, Observer
from unitary.examples.quantum_rpg.xp_utils import EncounterXp
from unitary.examples.quantum_rpg.world import Direction, Location


def _engineer_joins(state: GameState, world) -> str:
    if len(state.party) > 1:
        return f"The engineer reminisces about his former experiment."
    print("The engineer looks at the apparatus that dominates the room.")
    print("'NMR has been a promising technology for quantum computing,'")
    print("the engineer says.  'And we have learned a lot.  But, ultimately,")
    print("I can already see that this technology is not scalable and will")
    print("not solve the problems that plague us today.  I will leave this")
    print("for the scientists working in other disciplines and join you")
    print("on the journey towards quantum error correction!")

    name = get_user_input_qaracter_name(
        state.get_user_input, "the engineer", file=state.file
    )
    qar = Engineer(name)
    state.party.append(qar)

    return f"{name} has joined the group!"


ENGINEER = Item(
    keyword_actions=[
        (
            TALK,
            ["engineer"],
            _engineer_joins,
        )
    ],
    description="The engineer stands here wondering how to build a better quantum computer.",
)

OXTAIL_RUINS = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["ruins", "gateway", "arch", "archway", "entrance", "wall"],
            ("Faded letters inscribed on the archway spell 'Ox+ai1 Un_ver__ty'"),
        )
    ]
)


DAVID = Item(
    keyword_actions=[
        (
            TALK,
            ["david", "man", "deutsch"],
            (
                "David turns to you.  'Welcome to Oxtail University.' David says.\n"
                "'You seem to have come at an interesting time.  Our university was\n"
                "founded here at the forefront of the quantum realm, and we have been\n"
                "researching quantum computation in search of a computational theory of\n"
                "everything.  Unfortunately, our university has been less of an invariant\n"
                "than hoped.  Quantum fluctuations and errors have infiltrated this whole\n"
                "place, and we are in dire straits, I fear.  Look for my student Artur.\n"
                "If he is still alive, he will be in the communications outpust.'\n"
            ),
        )
    ],
    description="David, a grey-haired man with glasses, is looking up at the buildings.",
)

ARTUR = Item(
    keyword_actions=[
        (
            TALK,
            ["artur", "ekert", "professor", "teacher"],
            (
                "Artur stands up tall and address you.  'We have lost contact\n"
                "with our field researchers in the quantum realm.  They were exploring\n"
                "techniques of communicating using quantum states.  If you can find them,\n"
                "they may be able to help figure out a way to stop the quantum errors\n"
                "that are destroying our campus.'\n"
            ),
        ),
        (
            EXAMINE,
            ["laser", "comms", "antenna", "antennae", "equipment"],
            (
                "A large array of communications-related equipment takes up most of the\n"
                "room on the roof of this building.  Antenna and unusual  photon detectorsr\n"
                "for receiving messages as well as equipment for generating signals.  A large\n"
                "laser actively being repaired by a bald professor points off the north end\n"
                "of the roof towards a hill deeper in the quantum realm.\n"
            ),
        ),
    ],
    description="A bald stern professor is adjusting a large laser.",
)


STUDENT = [
    Item(
        keyword_actions=[
            (
                TALK,
                ["student", "students"],
                (
                    "One of the students lazily pokes her head up.\n"
                    "'I am at one with the quantum consciousness!' she declares.\n"
                ),
            ),
            (
                EXAMINE,
                ["student", "students", "foam"],
                (
                    "Irregularly shaped mats of purple quantum foam cover parts of the otherwise\n"
                    "well-manicured lawn, giving it a strangely blurred, translucent appearance.\n"
                    "Several students relaxing on the lawn seem oblivious to the fact that the\n"
                    "slimy foam has nearly covered them up.\n"
                ),
            ),
        ],
        description="Students are laying in the grass, covered by pools of quantum foam.",
    ),
    Item(
        keyword_actions=[
            (
                TALK,
                ["student", "students", "drummer", "drummers"],
                (
                    "One of the drummers tells you 'This is like totally a seminar on two\n"
                    "dimensional harmonics on a circle.  Totally rad, like radians dude.'\n"
                ),
            ),
        ],
        description="A circle of long-haired students are her, drumming on large bongo drums.",
    ),
    Item(
        keyword_actions=[
            (
                TALK,
                ["student", "math", "nerd"],
                (
                    "The student focuses on a spot about ten feet behind you.\n"
                    "'Do you know why you cannot grow wheat in Z mod 6?' the student asks.\n"
                    "'Because it is not a field!' the student's skull cackles maniacally,\n"
                    "and, for a moment, seems both alive and dead at the same time.\n"
                ),
            )
        ],
        description="A nerdy math student covered in quantum foam wanders around aimlessly.",
    ),
    Item(
        keyword_actions=[
            (
                TALK,
                ["student", "students", "grad"],
                (
                    "One grad student pauses scraping foam from the castle wall for a moment.\n"
                    "'We have lost contact with our field researchers.  I hope they are okay.\n"
                    "For that matter, I am not sure how long we can hold out.  I hope you can\n"
                    "help us find a way to reduce the quantum errors in our zone before it is\n"
                    "too late!'"
                ),
            )
        ],
    ),
]

SPECTROMETER = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["cylinder", "machine", "device", "nmr", "spectrometer"],
            (
                "Towering above you, the polished steel cylinder stands as a sentinel\n"
                "of scientific exploration. Thick cables and intricate wiring connect\n"
                "the device to the outside world.  The smooth metallic surface contrasts\n"
                "with the intricate controls and monitors nearby, displaying graphs and\n"
                "waveforms.  This sophisticated instrument holds the promise of unlocking\n"
                "profound insights from the molecules that make up our existence.\n"
            ),
        )
    ]
)


OXTAIL_UNIVERSITY = [
    Location(
        label="oxtail1",
        title="Corroded Gateway",
        description=(
            "What once must have been a glorius gothic archway now lies in ruins.\n"
            "Parts of the gate have fallen, and a great stone wall running north and south\n"
            "has fallen into disrepair, with bits and pieces missing throughout.\n"
        ),
        items=[OXTAIL_RUINS],
        exits={Direction.WEST: "classical5", Direction.EAST: "quad4"},
    ),
    Location(
        label="quad4",
        title="Ruined Entryway",
        description=(
            "A broken and decrepit sidewalk leads through what once must have been a great\n"
            "and imposing campus filled with baroque and gothic style buildings.  Now, the\n"
            "buildings are clearly in disrepair, with chunks of stone missing.  On some of\n"
            "the walls, you can see glowing flourescent slime oozing with scintillating\n"
            "color that seems to reflect multiple shade of light simultaneously.\n"
        ),
        items=[DAVID],
        exits={
            Direction.WEST: "oxtail1",
            Direction.EAST: "quad5",
            Direction.NORTH: "quad1",
            Direction.SOUTH: "quad7",
        },
    ),
    Location(
        label="quad1",
        title="Collapsing Cloisters",
        description=(
            "A covered walkway lined with pillars travels around the edge of\n"
            "the quad.  Through occasional holes in the wall to the west, you\n"
            "can see the fields outside of the university campus. Corrosive\n"
            "purple ooze seems to be eating away at the pillars and walls, and\n"
            "one entire section has collapsed into a pile of rubble.\n"
        ),
        encounters=[blue_foam(1, 0.3), green_foam(3, 0.2), blue_foam(3, 0.1)],
        items=[],
        exits={Direction.SOUTH: "quad4", Direction.EAST: "quad2"},
    ),
    Location(
        label="quad2",
        title="Imposing Drawbridge",
        description=(
            "A large wooden drawbridge lies on the ground, leading to a gothic castle.\n"
            "Beside it, corroded chains that once held it in place now lie in a tangled\n"
            "slimy mess on the ground. To the north, a tall gray building with stone battlements\n"
            "and crenulations rises above the rest of the campus. Quantum foam can be seen\n"
            "dripping out of its open windows."
        ),
        items=[],
        encounters=[blue_foam(3, 0.3), green_foam(3, 0.2)],
        exits={
            Direction.NORTH: "comms1",
            Direction.WEST: "quad1",
            Direction.SOUTH: "quad5",
            Direction.EAST: "quad3",
        },
    ),
    Location(
        label="quad3",
        title="Lone Monument",
        description=(
            "A statue dedicated to Stephen Hawking stands in this corner of the campus,\n"
            "He was one of the pioneers of theoretical physics.  A pool of quantum foam\n"
            "surrounds the statue and, nearby, an unnerving tenebrous spot reminiscent\n"
            "of the black holes Hawking was famous for casts a dark shadow on the wall."
        ),
        items=[],
        encounters=[blue_foam(4, 0.1)],
        exits={Direction.SOUTH: "quad6", Direction.WEST: "quad2"},
    ),
    Location(
        label="quad5",
        title="The Quad",
        description=(
            "The middle of the campus is framed by a rectangle of green grass.\n"
            "Grey sidewalks cross the lawn in the pattern of an X.  Puddles of\n"
            "coruscating, multi-colored slime dot the lawn in irregular shapes,\n"
            "contrasting sharply with the green grass.\n"
        ),
        items=[STUDENT[0]],
        encounters=[
            blue_foam(2, 0.1),
            green_foam(2, 0.1),
            blue_foam(1, 0.1),
            blue_foam(3, 0.1),
            green_foam(1, 0.2),
        ],
        exits={
            Direction.NORTH: "quad2",
            Direction.EAST: "quad6",
            Direction.SOUTH: "quad8",
            Direction.WEST: "quad4",
        },
    ),
    Location(
        label="quad6",
        title="Lab Entrance",
        description=(
            "A stone building here seems mostly untouched by the corrosion evident\n"
            "across most of the rest of the campus.  Etched into the arched doorway\n"
            "are the words 'Chemistry Research Laboratory' and below that reads,\n"
            "'Nuclear Magnetic Resonance Facility'."
        ),
        items=[],
        exits={
            Direction.WEST: "quad5",
            Direction.NORTH: "quad3",
            Direction.SOUTH: "quad9",
            Direction.EAST: "nmr_lab1",
        },
    ),
    Location(
        label="quad7",
        title="Student Lawn",
        description=(
            "Outside of what used to be the student center and cafe\n"
            "is a lawn criss-crossed by sidewalks.  Under a smattering\n"
            "of trees, circles of lounging students are hanging around.\n"
        ),
        items=[STUDENT[1]],
        exits={Direction.NORTH: "quad4", Direction.EAST: "quad8"},
    ),
    Location(
        label="quad8",
        title="South end",
        description=(
            "Here on the south end of campus is the mathematics\n"
            "department.  Most of the windows and doors have been\n"
            "boarded up or blocked.  A hastily drawn sign on the\n"
            "entrance proclaims: 'QUIET PLEASE! THEOREM CREATION IN PROGRESS.'"
        ),
        items=[STUDENT[2]],
        encounters=[blue_foam(2, 0.2)],
        exits={
            Direction.WEST: "quad7",
            Direction.NORTH: "quad5",
            Direction.EAST: "quad9",
        },
    ),
    Location(
        label="quad9",
        title="Collapsed Building",
        description=(
            "Rubble completely blocks the way here.  Whatever building this\n"
            "once was has now been consumed by slime and quantum errors.\n"
            "From within the piles of rubble, bits of static and open holes\n"
            "in reality form irregular disjointed cavities.\n"
        ),
        items=[],
        encounters=[
            blue_foam(1, 0.2),
            blue_foam(2, 0.1),
            green_foam(1, 0.2),
            green_foam(2, 0.1),
        ],
        exits={Direction.NORTH: "quad6", Direction.WEST: "quad8"},
    ),
    Location(
        label="comms1",
        title="Communication Castle",
        description=(
            "Though thee outside of this building resembles a castle,\n"
            "the inside seems to be filled with classrooms, offices, and\n"
            "lab spaces.  Slimy foam drips down from a stairway leading upwards.\n"
        ),
        items=[],
        encounters=[blue_foam(3, 0.3), green_foam(3, 0.1)],
        exits={Direction.SOUTH: "quad2", Direction.UP: "comms2"},
    ),
    Location(
        label="comms2",
        title="Castle Landing",
        description=(
            "This level of the castle is completely overrun with\n"
            "quantum slime.  The quantum foam covers the walls and floors\n"
            "everyhere.  Everything seems to glowing with a shifting light,\n"
            "and it seems like parts of the building are phasing in and out of\n"
            "existence."
        ),
        items=[],
        encounters=[
            Encounter(
                [
                    BlueFoam("Blue Foamy"),
                    BlueFoam("Blue Slimy"),
                    GreenFoam("Green Gooey"),
                    GreenFoam("Green Foamy"),
                    Observer("The Observer"),
                ],
                probability=1.0,
                description="The quantum slime oozes off all the walls and surrounds you!",
                xp=EncounterXp([[alpha.Flip()]]),
            )
        ],
        exits={Direction.DOWN: "comms1", Direction.UP: "comms3"},
    ),
    Location(
        label="comms3",
        title="Communication Battlements",
        description=(
            "The top of the castle seems to be an outpost of some sort,\n"
            "largely devoid of the quantum foam that plagues the rest of\n"
            "the campus.  Antennae and communication gear of all sorts clutters\n"
            "the roof.  Students scurry back and forth, trying to keep the\n"
            "equipment running and the roof clean of the encroaching foam.\n"
        ),
        items=[ARTUR, STUDENT[3]],
        exits={Direction.DOWN: "comms2"},
    ),
    Location(
        label="nmr_lab1",
        title="Lab Building Entrance",
        description=(
            "As you step inside this building, the smell of solvents, ozone, and other\n"
            "chemicals pervades.  A subtle tingling of anticipation seems to infect this\n"
            "area.  The sterile white walls, impeccably clean and illuminated by the warm\n"
            "glow of recessed lights, creates an atmosphere of precision and meticulousness.\n"
            "A low hum of machinery comes from a larger room to the east.\n"
        ),
        items=[],
        exits={Direction.WEST: "quad6", Direction.EAST: "nmr_lab2"},
    ),
    Location(
        label="nmr_lab2",
        title="Sprawling Lab Space",
        description=(
            "This immense workspace is packed with machinery, desks, workbenches,\n"
            "and equipment.  Rows of cabinets line the walls next to signs extolling\n"
            "the virtues of a safe lab environment.  In the middle of the room, a\n"
            "massive metallic cylinder dominates the area, rising towards the vaulted\n"
            "ceiling.  This must be the nuclear magnetic resonance spectrometer.\n"
            "A metal ladder leads upwards to an access way on the top of the device.\n"
        ),
        items=[SPECTROMETER],  # TODO: add items
        exits={Direction.WEST: "nmr_lab1", Direction.UP: "nmr_lab3"},
    ),
    Location(
        label="nmr_lab3",
        title="Atop the NMR Spectrometer",
        description=(
            "You stand on a narrow walk way that circles around the massive\n"
            "spectrometer.  From up here, you can see the entirety of the lab\n"
            "supporting the NMR research effort.  Wires and cables lead from\n"
            "the machine up to the ceiling and snake outward, connecting to all\n"
            "manner of machinery.  A whirring hum echoes throughout the space.\n"
        ),
        items=[SPECTROMETER, ENGINEER],
        exits={Direction.DOWN: "nmr_lab2"},
    ),
]
