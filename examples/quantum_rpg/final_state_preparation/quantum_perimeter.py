from ..item import EXAMINE, Item
from ..world import Direction, Location

CONSTRUCTION_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            "sign",
            (
                "Congratulations on making it to the end of the demo!\n"
                "The following zone (Quantum Perimeter) is still under construction.\n"
                "Come back soon for updates!"
            ),
        )
    ],
    description="A yellow and black sign denotes a warning here.",
)


QUANTUM_PERIMETER = [
    Location(
        label="perimeter1",
        title="Inside the Perimeter",
        description=(
            "You have made it inside the Quantum Perimeter Research Facility.\n"
            "What once must have been a modern and extravagent reception area\n"
            "has now fallen into disrepair.  Light from a large hall seeps in\n"
            "from the north.  Double doors lead to a theatre to the east."
        ),
        encounters=[],
        items=[CONSTRUCTION_SIGN],
        exits={Direction.EAST: "perimeter2", Direction.NORTH: "perimeter3"},
    ),
    Location(
        label="perimeter2",
        title="Theatre of Ideas",
        description=(
            "A large lecture hall is filled with empty seats.  The front of\n"
            "the theatre is filled with a large stage and screen.  Light from\n"
            "a projector in the ceiling illuminates a presentation of slides\n"
            "that periodically rotate with an echoing click that reverberates\n"
            "through the empty hall."
        ),
        encounters=[],
        items=[],
        exits={Direction.WEST: "perimeter1", Direction.UP: "perimeter6"},
    ),
    Location(
        label="perimeter3",
        title="Atrium",
        description=(
            "Diffuse sunlight seeps in through an opening far above.  Several floors\n"
            "of broken windows surround the rectangular atrium, extending upwards.\n"
            "Vague pools of dissolved material and scattered glass shards are all\n"
            "that remain within this empty space."
        ),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter1", Direction.NORTH: "perimeter4"},
    ),
    Location(
        label="perimeter4",
        title="Black Hole Bistro",
        description=(
            "A sign hangs crookedly over the institute's cafeteria.\n"
            "Within, overturned chairs and tables fill the chaotically\n"
            "arranged place.  Strange radiation emanates from the\n"
            "counters and serving areas."
        ),
        encounters=[],
        items=[],
        exits={
            Direction.SOUTH: "perimeter3",
            Direction.NORTH: "perimeter5",
            Direction.UP: "perimeter9",
        },
    ),
    Location(
        label="perimeter5",
        title="Reflection Pool",
        description=("A reflection pool outside the perimeter institute."),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter4", Direction.NORTH: "perimeter20"},
    ),
    Location(
        label="perimeter6",
        title="Theatre Seating",
        description=("Second floor of the lecture hall."),
        encounters=[],
        items=[],
        exits={Direction.DOWN: "perimeter2", Direction.NORTH: "perimeter7"},
    ),
    Location(
        label="perimeter7",
        title="Reading Room",
        description=(
            "A library within the Perimeter institute. Books containing\n"
            "quantapedia entries can be found here."
        ),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter6", Direction.NORTH: "perimeter8"},
    ),
    Location(
        label="perimeter8",
        title="Stairway",
        description=("Stairs leading upwards."),
        encounters=[],
        items=[],
        exits={
            Direction.UP: "perimeter11",
            Direction.SOUTH: "perimeter7",
            Direction.WEST: "perimeter9",
        },
    ),
    Location(
        label="perimeter9",
        title="Dining Area",
        description=("Upstairs from the bistro."),
        encounters=[],
        items=[],
        exits={
            Direction.DOWN: "perimeter4",
            Direction.NORTH: "perimeter10",
            Direction.EAST: "perimeter8",
        },
    ),
    Location(
        label="perimeter10",
        title="Terrace",
        description=(
            "From the overlook, you can see the surrounding area.\n"
            "In the distance, a tunnel into the mountains of error\n"
            "correction can be seen past a large forest."
        ),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter9"},
    ),
    Location(
        label="perimeter11",
        title="Stairway",
        description=("Stairs lead up and down."),
        encounters=[],
        items=[],
        exits={
            Direction.DOWN: "perimeter8",
            Direction.NORTH: "perimeter12",
            Direction.UP: "perimeter15",
        },
    ),
    Location(
        label="perimeter12",
        title="Hallway",
        description=(""),
        encounters=[],
        items=[],
        exits={
            Direction.SOUTH: "perimeter11",
            Direction.WEST: "perimeter13",
            Direction.EAST: "perimeter14",
        },
    ),
    Location(
        label="perimeter13",
        title="Theorist Office",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.EAST: "perimeter12"},
    ),
    Location(
        label="perimeter14",
        title="Experimentalist Office",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.WEST: "perimeter12"},
    ),
    Location(
        label="perimeter15",
        title="Rooftop Garden",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.DOWN: "perimeter11"},
    ),
    Location(
        label="perimeter20",
        title="By the shores of a Silver Lake",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter5", Direction.NORTH: "perimeter21"},
    ),
    Location(
        label="perimeter21",
        title="Bridge over Silver Lake",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter20", Direction.NORTH: "perimeter22"},
    ),
    Location(
        label="perimeter22",
        title="By an old mill",
        description=(""),
        encounters=[],
        items=[],
        exits={
            Direction.SOUTH: "perimeter21",
            Direction.EAST: "perimeter23",
            Direction.NORTH: "perimeter24",
        },
    ),
    Location(
        label="perimeter23",
        title="Grist Mill",
        description=(""),
        encounters=[],
        items=[],
        exits={Direction.WEST: "perimeter22"},
    ),
    Location(
        label="perimeter24",
        title="On the edge of a twisty forest",
        description=("Entrance to the forest maze."),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter22", Direction.NORTH: "perimeter25"},
    ),
    Location(
        label="perimeter25",
        title="Maze of twisty little forest passages",
        description=("A maze of twisty forest passages, all alike."),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter24"},
    ),
    Location(
        label="perimeter99",
        title="Into the Unknown",
        description=("Entrance to the next zone."),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter25"},
    ),
]
