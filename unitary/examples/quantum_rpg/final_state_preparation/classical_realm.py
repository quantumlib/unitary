import unitary.alpha as alpha

from unitary.examples.quantum_rpg.classes import Engineer
from unitary.examples.quantum_rpg.encounter import Encounter
from unitary.examples.quantum_rpg.game_state import GameState
from unitary.examples.quantum_rpg.input_helpers import get_user_input_qaracter_name
from unitary.examples.quantum_rpg.item import EXAMINE, TALK, Item
from unitary.examples.quantum_rpg.npcs import BlueFoam, GreenFoam, Observer
from unitary.examples.quantum_rpg.xp_utils import EncounterXp
from unitary.examples.quantum_rpg.world import Direction, Location

_BLUE_XP = EncounterXp(
    [
        [],
        [alpha.Flip(effect_fraction=0.5)],
        [alpha.Flip(effect_fraction=0.25)],
        [alpha.Flip(effect_fraction=0.125)],
        [alpha.Superposition()],
        [alpha.Phase(effect_fraction=0.375)],
    ],
    [0.35, 0.05, 0.20, 0.20, 0.10, 0.10],
)

_GREEN_XP = EncounterXp(
    [
        [],
        [alpha.Phase(effect_fraction=0.5)],
        [alpha.Phase(effect_fraction=0.25)],
        [alpha.Phase(effect_fraction=0.125)],
        [alpha.Superposition()],
        [alpha.Flip(effect_fraction=0.375)],
    ],
    [0.35, 0.05, 0.20, 0.20, 0.10, 0.10],
)


def _blue_foam(number: int, prob: float = 0.5, xp=_BLUE_XP):
    return Encounter(
        [BlueFoam(f"bluey gooey {idx}") for idx in range(number)],
        probability=prob,
        description="Some blue quantum foam oozes towards you!",
        xp=xp,
    )


def _green_foam(number: int, prob: float = 0.5, xp=_GREEN_XP):
    return Encounter(
        [GreenFoam(f"green goo {idx}") for idx in range(number)],
        probability=prob,
        description="Some green quantum foam oozes towards you!",
        xp=xp,
    )


def _engineer_joins(state: GameState) -> str:
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


RICHARD = Item(
    keyword_actions=[
        (
            TALK,
            ["richard", "feynmann", "physicist"],
            (
                "Richard excitedly talks, as if continuing a lecture in progress.\n"
                "Modern computers are truly powerful and wondrous, but if want to\n"
                "truly understand nature and the laws of the world around, we are\n"
                "going to need a much more powerful device.\n"
                "Nature isn't classical, dammit, and if you want to make a simulation\n"
                "of nature, you'd better make it quantum mechanical!  By golly, it's\n"
                "a wonderful problem, but it doesn't look easy.  I would start by\n"
                "searching for an abandoned nuclear lab on the ruins of Oxtail university.\n"
            ),
        )
    ],
    description="It is only natural that Richard is here to help start your journey.",
)

HUT_DESK = Item(
    keyword_actions=[
        (
            EXAMINE,
            "desk",
            (
                "Folders and binders piled on the desk contain "
                "material and warnings\n about the incursion of quantum "
                "errors and foam into the realm.\n"
            ),
        )
    ]
)

HUT_CHALKBOARD = Item(
    keyword_actions=[
        (
            EXAMINE,
            "chalkboard",
            (
                "The chalkboard seems to show the evolution of a \n"
                "Hamiltonian towards some final waveform."
            ),
        )
    ]
)

BENT_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            "sign",
            (
                "The top of the sign contains a warning symbol with a pictorial of\n"
                "An image of a sphere with poles labeled with |0> and |1>.\n"
                "Below it reads: Beware of quantum fluctuations ahead!\n"
            ),
        )
    ],
    description="A bent sign sticks out of the ground at an angle.",
)

LOOPED_PATH = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["path", "road", "circuit"],
            (
                "When you stand back and look at the path, it seems to form the shape\n"
                "of an electrical circuit of some kind.\n"
            ),
        )
    ]
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
                "David turns to you.  'Welcome to Oxtail University.'\n"
                "'You seems to have come at an interesting time.  Our university was\n"
                "founded here at the forefront of the quantum realm, and we have been\n"
                "researching quantum computation in search of a computational thoery of\n"
                "everything.  Unfortunately, our university has been less of an invariant\n"
                "than hoped.  Quantum fluctuations and errors have infiltrated this whole\n"
                "place, and we are in dire straits I fear.  Look for my student Artur.\n"
                "If he still survives, he will be in the communications outpust.\n"
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
                "techniques of communicating in the quantum realm.  If you can find them,\n"
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


CLASSICAL_REALM = [
    Location(
        label="classical1",
        title="Science Hut",
        description=(
            "At the edge of the classical frontier, a solitary hut\n"
            "looks north towards the mountains in the distance.\n"
            "Though still in the classical realm, it is clear the\n"
            "researchers in this humble abode have aspirations for\n"
            "the future.  Desks and chalkboards filled with diagrams\n"
            "fill this room."
        ),
        items=[RICHARD, HUT_DESK, HUT_CHALKBOARD],
        exits={Direction.NORTH: "classical2"},
    ),
    Location(
        label="classical2",
        title="Edge of the Classical Frontier",
        description=(
            "You are standing outside a hut near the end of the classical domain.\n"
            "This wild place which separates the classical from the quantum\n"
            "realms. To the north is the frontier, where quantum phenomena are\n"
            "studied and classified.  Far off in the distance are the fabled mountains\n"
            "of error-correction, the subject of many theories and discussion.\n"
        ),
        items=[BENT_SIGN],
        exits={Direction.SOUTH: "classical1", Direction.NORTH: "classical3"},
    ),
    Location(
        label="classical3",
        title="The Classical Frontier",
        description=(
            "Here, the frontier between the classical and quantum realms begins.\n"
            "Farther north, you can see faint undulations, as if the way is blurred\n"
            "by some mirage.  To proceed, you will need to move around this strange\n"
            "occurance."
        ),
        items=[],
        exits={
            Direction.SOUTH: "classical2",
            Direction.EAST: "classical4",
            Direction.WEST: "classical7",
        },
    ),
    Location(
        label="classical4",
        title="A Twisted Road",
        description=(
            "A twisted path winds its way through this area, though its path seems\n"
            "to curve back on itself and loops around to connect to itself.\n"
            "Further to the north, the frontier curves around a strange disturbance.\n"
            "To the east, some ruined buildings can be seen on the other side of an\n"
            "open field.\n"
        ),
        items=[LOOPED_PATH],
        encounters=[_blue_foam(1, 0.2), _green_foam(1, 0.2)],
        exits={
            Direction.EAST: "classical5",
            Direction.NORTH: "classical6",
            Direction.WEST: "classical3",
        },
    ),
    Location(
        label="classical5",
        title="A Finite Field",
        description=(
            "Here, an open field lies between the wild frontier to the west, and\n"
            "a group of ruined buildings to the east.  The field itself is unkempt\n"
            "and filled with tangles of weeds and bramble.  In spots, you can see\n"
            "spots covered in iridicent colored slime roughly in the shape of waterdrops.\n"
        ),
        encounters=[
            _blue_foam(2, 0.4),
            _green_foam(2, 0.4),
            _blue_foam(3, 0.1),
            _green_foam(3, 0.1),
        ],
        exits={Direction.WEST: "classical4", Direction.EAST: "oxtail1"},
    ),
    Location(
        label="classical6",
        title="Near a Pixelated Hole",
        description=(
            "The rolling land here drops steeply into what looks like a missing piece\n"
            "of the world.  Where there should be another room, or at least a description\n"
            "is instead filled with a pixelated static darkness.  The entire vista is quite\n"
            "disturbing, and you wonder at the cruel force that may have destroyed the\n"
            "coherence of the landscape in this area."
        ),
        # TODO: don't enter the hole!
        exits={Direction.SOUTH: "classical4"},
    ),
    Location(
        label="classical7",
        title="A Wild Frontier",
        description=(
            "The land here slopes along a ridge and climbs steadily towards\n"
            "the north, where the foothills begin to slowly climb in altitude."
        ),
        encounters=[_blue_foam(2, 0.4), _green_foam(3, 0.3), _blue_foam(1, 0.1)],
        exits={Direction.EAST: "classical3", Direction.NORTH: "classical8"},
    ),
    Location(
        label="classical8",
        title="Vantage Point",
        description=(
            "The ground slopes upwards in this area on its eventual rise towards\n"
            "the foothills.  From here, you can see the surrounding area.  Most\n"
            "striking is a disturbing hole below you to the east, that seems to be filled\n"
            "with static and broken pixels.  Scattered across the frontier to the north,\n"
            "you can see other similar holes, where quantum errors have crept in.\n"
            "Farther to the east, you can see the cathedral-like buildings of a baroque\n"
            "college campus."
        ),
        encounters=[_blue_foam(2, 0.3), _green_foam(2, 0.2)],
        exits={Direction.SOUTH: "classical7"},
        # TODO: Connect to the next zone.
    ),
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
        encounters=[_blue_foam(1, 0.3), _green_foam(3, 0.2), _blue_foam(3, 0.1)],
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
        encounters=[_blue_foam(3, 0.3), _green_foam(3, 0.2)],
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
            "A statue stands in this corner of campus dedicated to Stephen Hawking,"
            "one of the pioneers of theoretical physics.  A pool of quantum foam\n"
            "surrounds the statue, and nearby, an unnerving tenebrous spot reminiscent\n"
            "of the black holes Hawking was famous for casts a dark shadow on the wall."
        ),
        items=[],
        encounters=[_blue_foam(4, 0.1)],
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
            _blue_foam(2, 0.1),
            _green_foam(2, 0.1),
            _blue_foam(1, 0.1),
            _blue_foam(3, 0.1),
            _green_foam(1, 0.2),
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
        encounters=[_blue_foam(2, 0.2)],
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
            _blue_foam(1, 0.2),
            _blue_foam(2, 0.1),
            _green_foam(1, 0.2),
            _green_foam(2, 0.1),
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
        encounters=[_blue_foam(3, 0.3), _green_foam(3, 0.1)],
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
            "A plan for this room, who needs one?"
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
            "Yoiu stand on a narrow walk way that circles around the massive\n"
            "spectrometer.  From up here, you can see the entirety of the lab\n"
            "supporting the NMR research effort.  Wires and cables lead from\n"
            "the machine up to the ceiling and snake outward, connecting to all\n"
            "manner of machinery.  A whirring hum echoes throughout the space.\n"
        ),
        items=[SPECTROMETER, ENGINEER],
        exits={Direction.DOWN: "nmr_lab2"},
    ),
]
