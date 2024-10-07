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

from typing import Optional, Sequence

import random

from . import battle
from . import game_state
from . import qaracter
from . import xp_utils


class Encounter:
    """Container class for specifying encounters.

    Useful in specifying an adventure in quantum RPG.
    """

    def __init__(
        self,
        enemies: Sequence[qaracter.Qaracter] = (),
        probability: float = 1.0,
        description: Optional[str] = None,
        xp: Optional[xp_utils.EncounterXp] = None,
    ):
        self.enemies = list(enemies)
        self.probability = probability
        self.description = description
        self.xp = xp

    def will_trigger(self) -> bool:
        """Returns True if the encounter should be triggered.

        This is based on the probability of the encounter happening.
        """
        return random.random() < self.probability

    def copy(self) -> "Encounter":
        enemies_copy = [qar.copy() for qar in self.enemies]
        return Encounter(
            enemies=enemies_copy,
            probability=self.probability,
            description=self.description,
            xp=self.xp,
        )

    def initiate(self, state: game_state.GameState) -> battle.Battle:
        return battle.Battle(state, self.enemies, xp=self.xp)
