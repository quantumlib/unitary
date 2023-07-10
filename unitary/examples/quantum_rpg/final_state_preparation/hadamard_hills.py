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
                "Look for the next section (Hadamard Hills) to open up soon!"
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
            "quantum realm."
        ),
        encounters=[],
        items=[CONSTRUCTION_SIGN],
        exits={Direction.SOUTH: "classical12"},
    ),
]
