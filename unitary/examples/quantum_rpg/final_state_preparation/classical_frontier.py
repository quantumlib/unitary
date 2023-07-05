import unitary.alpha as alpha

from unitary.examples.quantum_rpg.encounter import Encounter
from unitary.examples.quantum_rpg.game_state import GameState
from unitary.examples.quantum_rpg.final_state_preparation.monsters import green_foam, blue_foam
from unitary.examples.quantum_rpg.item import EXAMINE, TALK, Item
from unitary.examples.quantum_rpg.world import Direction, Location

RICHARD = Item(
    keyword_actions=[
        (
            TALK,
            ["richard", "feynmann", "physicist"],
            (
                "Richard speaks excitedly, as if continuing a lecture in progress:\n"
                "'Modern computers are truly powerful and wondrous, but if we want to\n"
                "truly understand nature and the laws of the world around us, we are\n"
                "going to need a much more powerful device.\n"
                "Nature isn't classical, damnit, and if you want to make a simulation\n"
                "of nature, you'd better make it quantum mechanical!  By golly, it's\n"
                "a wonderful problem, but it doesn't look easy.  I would start by\n"
                "searching for an abandoned nuclear lab on the ruins of Oxtail university.'\n"
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

CLASSICAL_FRONTIER = [
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
        encounters=[blue_foam(1, 0.2), green_foam(1, 0.2)],
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
            blue_foam(2, 0.4),
            green_foam(2, 0.4),
            blue_foam(3, 0.1),
            green_foam(3, 0.1),
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
        encounters=[blue_foam(2, 0.4), green_foam(3, 0.3), blue_foam(1, 0.1)],
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
        encounters=[blue_foam(2, 0.3), green_foam(2, 0.2)],
        exits={Direction.SOUTH: "classical7"},
        # TODO: Connect to the next zone.
    ),
]
