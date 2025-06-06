# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..item import EXAMINE, Item
from ..world import Direction, Location

CONSTRUCTION_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["sign", "post", "construction"],
            (
                "Congratulations on making it to the end of the demo!\n"
                "The following zone (Quantum Perimeter) is still under construction.\n"
                "Come back soon for updates!"
            ),
        )
    ],
    description="A yellow and black sign denotes a warning here.",
)

CRUMPLED_PAPER = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["paper", "crumpled paper", "note"],
            (
                "The crumpled paper has faint, water-damaged diagrams.\n"
                "You can just make out a sequence of arrows, some pointing\n"
                "left, others right, accompanied by numerical values. It\n"
                "looks like a binary sequence, perhaps related to direction.\n"
                "At the bottom, a faded inscription reads: 'Optimal search.'"
            ),
        )
    ],
    description="A piece of crumpled, damp paper lies on the ground.",
)

WORN_COMPASS = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["compass", "worn compass"],
            (
                "A tarnished brass compass. The needle spins wildly,\n"
                "never settling, but strange, faint etchings around the\n"
                "dial seem to depict a repeating pattern of small, circular\n"
                "loops. One loop is distinctly brighter than the others."
            ),
        )
    ],
    description="A broken and very old-looking compass.",
)

SMUDGED_DIAGRAM = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["diagram", "smudged diagram", "chart"],
            (
                "A smudged diagram pinned to a decaying bulletin board.\n"
                "It appears to be a flow chart with branching paths.\n"
                "Most paths are faded, but a single, bold path seems to\n"
                "emerge, emphasizing a distinct solution from many options.\n"
                "A handwritten note at the bottom is almost illegible:\n"
                "'Amplify the signal.'"
            ),
        )
    ],
    description="A smudged and faded diagram is tacked to the wall.",
)

MOSS_COVERED_STONE = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["stone", "moss-covered stone"],
            (
                "A large, moss-covered stone. Running your hand over its\n"
                "surface, you feel faint, regular indentations. They could\n"
                "be natural, or perhaps they were once part of a calculation\n"
                "or a tally of some kind, leading to a singular marked point."
            ),
        )
    ],
    description="A large stone almost swallowed by moss.",
)

RECEPTION_DESK = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["desk", "reception desk"],
            (
                "The reception desk is overturned, its once-polished surface\n"
                "scratched and scarred. A flickering computer monitor displays\n"
                "a rotating pattern, while text repeats: 'Searching... '\n"
                "'Searching... Amplification failed.' \n"
            ),
        )
    ],
    description="An old, broken reception desk.",
)

THEATRE_SCREEN = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["screen", "theatre screen"],
            (
                "The large screen displays a series of rapidly changing\n"
                "abstract patterns, interspersed with fleeting images of\n"
                "circuit diagrams. One pattern, a rotating circle with a\n"
                "single illuminated segment, reappears more frequently."
            ),
        )
    ],
    description="A vast, flickering screen at the front of the theatre.",
)

OVERTURNED_CHAIR = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["chair", "overturned chair"],
            (
                "An overturned chair, its fabric torn. On its wooden leg,\n"
                "someone has crudely etched a symbol: a circle with a dot\n"
                "in the center, and an arrow pointing out from it. On one\n"
                "side of the circle is marked a zero and the other side is\n"
                "marked one."
            ),
        )
    ],
    description="A fallen chair in the lecture hall.",
)

DISSOLVED_POOL = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["pool", "dissolved material", "puddle"],
            (
                "A viscous, dark pool of what looks like dissolved electronics\n"
                "and melted plastic. Tiny bubbles periodically rise to the\n"
                "surface, emitting a faint, high-pitched whine. It feels\n"
                "unnervingly warm to the touch."
            ),
        )
    ],
    description="A strange pool of dissolved material.",
)

SHATTERED_GLASS = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["glass", "shattered glass", "shards"],
            (
                "Numerous shards of shattered glass glint in the diffuse\n"
                "light. Examining them closely, you notice that some pieces\n"
                "have been melted and reformed, showing strange, distorted\n"
                "reflections that emphasize a single point in the chaos."
            ),
        )
    ],
    description="Scattered fragments of glass from broken windows.",
)

BLACK_HOLE_SIGN = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["counter", "broken counter"],
            (
                "A sign over the entrance reads 'Quantum Computing:'\n"
                "'The Technology of the Future'.  Graffiti painted over\n"
                "it reads 'BLACK HOLE SIGN WONT YOU COME AND WASH AWAY'"
                "'MY ERROR RATE'."
            ),
        )
    ],
    description="A discolored sign hangs over the entrance.",
)


BROKEN_COUNTER = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["counter", "broken counter"],
            (
                "The cafeteria counter is cracked and uneven. Scattered\n"
                "across its surface are various food containers, long since\n"
                "spoiled. A faded, sticky note is adhered to a corner,\n"
                "listing 'Ingredients: 0 or 1. Recipe: Repeat & find.'"
            ),
        )
    ],
    description="A broken and dirty counter in the bistro.",
)

RUSTED_TRAY = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["tray", "rusted tray"],
            (
                "A heavily rusted serving tray. The pattern of the rust\n"
                "on its surface appears to form a faded circuit diagram.\n"
                "Repeated several times is a tree like structure with circles\n"
                "intersecting every line.  You recognize it as a multi-\n"
                "controlled gate of some sort."
            ),
        )
    ],
    description="A forgotten, rusted serving tray.",
)

OVERGROWN_REEDS = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["reeds", "overgrown reeds"],
            (
                "Thick, overgrown reeds sway gently at the edge of the\n"
                "reflection pool. You notice several stalks bent in precise\n"
                "angles, some leaning west, others east, forming a subtle,\n"
                "almost invisible, directional pattern."
            ),
        )
    ],
)

DUSTY_BOOKSHELF = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["bookshelf", "shelf", "dusty bookshelf"],
            (
                "A bookshelf, partially toppled, with many books scattered\n"
                "on the floor. Most are water-damaged beyond recognition,\n"
                "but one, titled 'The Principles of Quantum Computing',\n"
                "is open to a chapter on 'Search Algorithms'."
            ),
        )
    ],
    description="A toppled and dusty bookshelf.",
)

FALLEN_CEILING_TILE = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["tile", "ceiling tile", "fallen tile"],
            (
                "A square ceiling tile lies broken on the floor. On its\n"
                "underside, what looks like maintenance instructions are\n"
                "scribbled. You can decipher 'Optimal path is derived\n"
                "from iterated amplitude amplification.' "
            ),
        )
    ],
)

BROKEN_WINDOW = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["window", "broken window"],
            (
                "A large window, its panes shattered. The jagged edges\n"
                "frame the outside world in a distorted view. A cold draft\n"
                "blows through, carrying with it a faint, repeating sequence\n"
                "of clicks and soft thuds, like a binary rhythm."
            ),
        )
    ],
)

FADED_EQUATIONS = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["equations", "faded equations", "scribbles"],
            (
                "The walls are covered in faded chalk equations, too complex\n"
                "to fully understand. One line reads 'U = 2|s><s> - I' and \n"
                "there seems to be a focus on a particular symbol |ω>.\n"
                "Circuit diagrams with a repeating structure cover the walls."
            ),
        )
    ],
)

DUSTY_CONSOLE = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["console", "dusty console", "machine"],
            (
                "A dust-covered electronic console, its screen dark. A thick wire\n"
                "connects to a dot-matrix printer, which is spooling out continous\n"
                "form paper.  On it, faded ink can barely be discerned.  It seems\n"
                "that the printer is writing out a log of some sort, counting out\n"
                "the iterations of a process up to the square root of a very large\n"
                "number."
            ),
        )
    ],
)

TANGLED_VINES = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["vines", "tangled vines"],
            (
                "Thick, thorny vines have taken over much of the rooftop\n"
                "garden. Among their chaotic sprawl, you notice that some\n"
                "vines have grown in surprisingly straight lines, almost\n"
                "forming a grid. One particular vine is noticeably straighter\n"
                "and thicker, pointing directly towards the forest."
            ),
        )
    ],
)

WEATHERED_BENCH = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["bench", "weathered bench"],
            (
                "A stone bench, heavily weathered by time and exposure.\n"
                "Scratched into its surface are representations of the\n"
                "Oracle monsters.  Next to it are etched the words:\n"
                "'Find the Signal'."
            ),
        )
    ],
    description="A decrepit stone bench on the terrace.",
)

SILVER_WATER = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["water", "silver water", "lake"],
            (
                "The water of Silver Lake is unusually clear and still.\n"
                "As you touch its placid surface, gentle waves spread out\n"
                "in a quadratically expanding pattern."
            ),
        )
    ],
)

ERODED_RAILING = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["railing", "eroded railing"],
            (
                "The metal railing of the bridge is heavily eroded by the elements."
            ),
        )
    ],
)

SEIZED_WHEEL = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["wheel", "water wheel", "seized wheel"],
            (
                "The old water wheel of the mill is entirely seized, covered\n"
                "in moss and rust. Its wooden paddles are broken, but you\n"
                "notice a series of small, almost imperceptible notches on\n"
                "the rim that indicate the direction of rotation."
            ),
        )
    ],
    description="The large, defunct water wheel of the mill.",
)

RUSTED_MACHINERY = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["machinery", "rusted machinery", "gears"],
            (
                "Signs that explain the mill's history and use of the\n"
                "equipment state that this mill was built in 1816 by one\n"
                "of the early settlers in the area and now houses a museum\n"
                "dedicated to the history of the area. Graffiti on one sign\n"
                "states 'We all rotate, round and round, closer to the end'."
            ),
        )
    ],
    description="Massive, rusted machinery in the grist mill.",
)

GIFT_SHOP = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["shelves", "gifts", "curios", "shop"],
            (
                "A variety of broken and decayed quantum-themed gifts line\n"
                "the shelves, including stuffed Schrödinger cats, periodic\n"
                "tables, and bloch sphere bouncy balls.  A shelf of fragrance\n"
                "diffusers seems strangely out of place."
            ),
        )
    ],
)


FOREST_FLOOR = Item(
    keyword_actions=[
        (
            EXAMINE,
            ["floor", "forest floor", "leaves"],
            (
                "The forest floor is covered in a thick carpet of fallen\n"
                "leaves and pine needles. Looking closely, you discern faint\n"
                "impressions in the soft earth, suggesting a repeated, short\n"
                "path that leads to a sudden, emphatic indentation."
            ),
        )
    ],
    description="The leaf-covered ground of the forest.",
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
        items=[CONSTRUCTION_SIGN, RECEPTION_DESK],
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
        items=[THEATRE_SCREEN, OVERTURNED_CHAIR],
        exits={Direction.WEST: "perimeter1", Direction.UP: "perimeter6"},
    ),
    Location(
        label="perimeter3",
        title="Atrium",
        description=(
            "Diffuse sunlight seeps in through an opening far above.  Several floors\n"
            "of broken windows surround the rectangular atrium, extending upwards.\n"
            "Vague pools of dissolved material and scattered glass shards are all\n"
            "that remain within this empty space. A faint scent of ozone hangs\n"
            "in the still air, and the air itself seems to shimmer slightly."
        ),
        encounters=[],
        items=[DISSOLVED_POOL, SHATTERED_GLASS],
        exits={Direction.SOUTH: "perimeter1", Direction.NORTH: "perimeter4"},
    ),
    Location(
        label="perimeter4",
        title="Black Hole Bistro",
        description=(
            "A sign hangs crookedly over the institute's cafeteria.\n"
            "Within, overturned chairs and tables fill the chaotically\n"
            "arranged place.  Strange, subtle fluctuations in the air\n"
            "suggest residual energy from experimental culinary ventures.\n"
            "A chilling cold spot persists near the main counter."
        ),
        encounters=[],
        items=[BLACK_HOLE_SIGN, BROKEN_COUNTER],
        exits={
            Direction.SOUTH: "perimeter3",
            Direction.NORTH: "perimeter5",
            Direction.UP: "perimeter9",
        },
    ),
    Location(
        label="perimeter5",
        title="Reflection Pool",
        description=(
            "A reflection pool outside the perimeter institute. The still\n"
            "water dimly reflects the shattered remains of the building.\n"
            "A gentle breeze rustles through overgrown reeds at the edge.\n"
            "Tiny ripples spread across the surface, seemingly from nothing,\n"
            "forming patterns that hint at hidden symmetry."
        ),
        encounters=[],
        items=[WORN_COMPASS, OVERGROWN_REEDS],
        exits={Direction.SOUTH: "perimeter4", Direction.NORTH: "perimeter20"},
    ),
    Location(
        label="perimeter6",
        title="Theatre Seating",
        description=(
            "You are in the upper seating area of the lecture hall. A thin\n"
            "layer of dust covers the tiered seats. The projector hums faintly\n"
            "below, casting distorted shadows on the screen. The acoustics\n"
            "here are strangely precise, amplifying even faint sounds,\n"
            "making distant echoes surprisingly clear."
        ),
        encounters=[],
        items=[FALLEN_CEILING_TILE],
        exits={Direction.DOWN: "perimeter2", Direction.NORTH: "perimeter7"},
    ),
    Location(
        label="perimeter7",
        title="Reading Room",
        description=(
            "A library within the Perimeter institute. Books containing\n"
            "quantapedia entries can be found here. Shelves are toppled,\n"
            "and scattered papers litter the floor. A faint scent of old\n"
            "paper and damp stone hangs in the air. One particular text\n"
            "is open to a page discussing 'iterative processes' and 'optimal paths',\n"
            "with a single, distinct diagram highlighted."
        ),
        encounters=[],
        items=[DUSTY_BOOKSHELF],
        exits={Direction.SOUTH: "perimeter6", Direction.NORTH: "perimeter8"},
    ),
    Location(
        label="perimeter8",
        title="Stairway",
        description=(
            "Stone steps spiral upwards, their surfaces worn smooth by countless\n"
            "footfalls. The air here is cool and still, carrying echoes from\n"
            "the floors above and below. A faint light filters down from above.\n"
            "A small, almost invisible '0' is etched into one of the lower steps,\n"
            "next to a faint arrow pointing west."
        ),
        encounters=[],
        items=[MOSS_COVERED_STONE],
        exits={
            Direction.UP: "perimeter11",
            Direction.SOUTH: "perimeter7",
            Direction.WEST: "perimeter9",
        },
    ),
    Location(
        label="perimeter9",
        title="Dining Area",
        description=(
            "This was once an elegant dining area, now just a larger,\n"
            "more open extension of the bistro downstairs. Broken plates\n"
            "and cutlery are strewn across the floor, glinting dully.\n"
            "A persistent draft blows through a broken window, carrying\n"
            "a whisper of distant, resonant tones, almost like a code."
        ),
        encounters=[],
        items=[BROKEN_WINDOW, RUSTED_TRAY],
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
            "correction can be seen past a large forest. The wind whips\n"
            "at your clothes, carrying the scent of pine and decay. You\n"
            "notice a pattern in the fallen leaves, strangely ordered,\n"
            "with distinct clusters and singular outliers."
        ),
        encounters=[],
        items=[WEATHERED_BENCH],
        exits={Direction.SOUTH: "perimeter9"},
    ),
    Location(
        label="perimeter11",
        title="Stairway",
        description=(
            "Another section of the spiraling stairway. The steps here are\n"
            "more damaged, some crumbling away. A sense of height pervades\n"
            "the space, and you can see a sliver of sky through the broken\n"
            "ceiling far above. A barely visible '1' is scratched into the\n"
            "wall beside a higher step, with an arrow pointing east."
        ),
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
        description=(
            "A long, desolate hallway stretches before you, lined with\n"
            "closed doors. The silence here is almost oppressive, broken\n"
            "only by the occasional creak of the decaying structure. A faint\n"
            "resonance seems to emanate from the west, a rhythmic, mechanical\n"
            "buzzing of an ancient device.\n"
        ),
        encounters=[],
        items=[SMUDGED_DIAGRAM],
        exits={
            Direction.SOUTH: "perimeter11",
            Direction.WEST: "perimeter13",
            Direction.EAST: "perimeter14",
        },
    ),
    Location(
        label="perimeter13",
        title="Theorist Office",
        description=(
            "This office once belonged to a theoretical physicist.\n"
            "Scattered chalk dust and equations scribbled on the walls\n"
            "are all that remain of their intricate work. A faint hum\n"
            "of residual quantum energy lingers in the air. One board\n"
            "has a series of binary strings, each with a single circled bit,\n"
            "as if a specific answer was being repeatedly isolated."
        ),
        encounters=[],
        items=[FADED_EQUATIONS],
        exits={Direction.EAST: "perimeter12"},
    ),
    Location(
        label="perimeter14",
        title="Experimentalist Office",
        description=(
            "The remnants of a laboratory fill this office. Broken glass\n"
            "and overturned equipment cover the floor. A blackboard lists\n"
            "failed experiments, one marked with a bold 'G' and arrows.\n"
            "A dot-matrix printer next to a dusty console regularly spits\n"
            "out faded type on spools of white paper.\n"
        ),
        encounters=[],
        items=[DUSTY_CONSOLE],
        exits={Direction.WEST: "perimeter12"},
    ),
    Location(
        label="perimeter15",
        title="Rooftop Garden",
        description=(
            "A once-beautiful rooftop garden is now a tangled mess of\n"
            "overgrown plants and shattered pottery. The wind is brisk\n"
            "here, carrying the scent of damp earth and distant decay.\n"
            "You can see the forest clearly from this height, noticing\n"
            "unusual clearings arranged in a linear fashion, leading towards\n"
            "a single, prominent point in the distance."
        ),
        encounters=[],
        items=[TANGLED_VINES],
        exits={Direction.DOWN: "perimeter11"},
    ),
    Location(
        label="perimeter20",
        title="By the shores of a Silver Lake",
        description=(
            "You stand on the edge of a shimmering lake, its surface calm\n"
            "and reflecting the broken sky. The water is surprisingly clear,\n"
            "and you can see glimpses of something metallic beneath the\n"
            "surface. The air here is unusually quiet, almost peaceful,\n"
            "save for the faint, rhythmic lapping of waves against the shore."
        ),
        encounters=[],
        items=[SILVER_WATER],
        exits={Direction.SOUTH: "perimeter5", Direction.NORTH: "perimeter21"},
    ),
    Location(
        label="perimeter21",
        title="Bridge over Silver Lake",
        description=(
            "A crumbling stone bridge spans the Silver Lake. Parts of the\n"
            "railing have fallen into the water below. A faint, distant drone\n"
            "can be heard, perhaps from some forgotten machinery. Looking\n"
            "down, you notice patterns in the eroded stone, resembling\n"
            "simple directional arrows, one consistently bolder than the others."
        ),
        encounters=[],
        items=[ERODED_RAILING],
        exits={Direction.SOUTH: "perimeter20", Direction.NORTH: "perimeter22"},
    ),
    Location(
        label="perimeter22",
        title="By an old mill",
        description=(
            "An ancient, dilapidated mill stands beside the lake, its water\n"
            "wheel long since seized. The air is damp and smells of moss and\n"
            "decaying wood. The drone you heard earlier seems to emanate\n"
            "from within the mill itself. A single, oddly clean cog lies\n"
            "on the ground, seemingly untouched by the decay, with a single\n"
            "tooth perfectly aligned to a nearby scratch mark."
        ),
        encounters=[],
        items=[SEIZED_WHEEL],
        exits={
            Direction.SOUTH: "perimeter21",
            Direction.EAST: "perimeter23",
            Direction.NORTH: "perimeter24",
        },
    ),
    Location(
        label="perimeter23",
        title="Grist Mill",
        description=(
            "Inside the old grist mill, the air is thick with dust and the\n"
            "ghosts of forgotten industry. Broken gears and rusted machinery\n"
            "line the sides of this place with explanatory signs denoting their\n"
            "historical origins.  Toppled shelves and discarded curios\n"
            "expose this place's prior function as a gift shop."
        ),
        encounters=[],
        items=[RUSTED_MACHINERY, GIFT_SHOP],
        exits={Direction.WEST: "perimeter22"},
    ),
    Location(
        label="perimeter24",
        title="On the edge of a twisty forest",
        description=(
            "You stand at the boundary of a dense, dark forest. The trees\n"
            "are unnaturally tall and twisted, their branches forming a\n"
            "tangled canopy overhead. A chill wind blows from within,\n"
            "carrying whispers that seem to beckon you deeper. Among the\n"
            "fallen leaves, a peculiar pattern of binary digits is imprinted,\n"
            "resembling a path marked with alternating directions."
        ),
        encounters=[],
        items=[CRUMPLED_PAPER, MOSS_COVERED_STONE],
        exits={Direction.SOUTH: "perimeter22", Direction.NORTH: "perimeter25"},
    ),
    Location(
        label="perimeter25",
        title="Maze of twisty little forest passages",
        description=(
            "You are deep within the twisty forest. The trees press in\n"
            "around you, making it difficult to discern any clear path.\n"
            "Each direction looks remarkably similar, and a strange sense\n"
            "of repetition hangs in the air. The rustling leaves sound\n"
            "like faint clicks and hums, as if a hidden mechanism is at work,\n"
            "iteratively searching for something."
        ),
        encounters=[],
        items=[FOREST_FLOOR],
        exits={Direction.SOUTH: "perimeter24"},
    ),
    Location(
        label="perimeter99",
        title="Into the Unknown",
        description=(
            "You have found a clearing in the forest, and beyond it,\n"
            "is a dark opening leading into the depths of the mountain.\n"
            "A cool wind filled with the tension of immense power flows\n"
            "from within.  Where it leads, you cannot be sure, but it is\n"
            "clear that you have passed beyond the classical realm now."
        ),
        encounters=[],
        items=[],
        exits={Direction.SOUTH: "perimeter25"},
    ),
]
