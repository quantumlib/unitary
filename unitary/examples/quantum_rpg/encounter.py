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

import io
from typing import Optional, Sequence

import random

import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.qaracter as qaracter
from typing import Sequence


class Encounter:
    """Container class for specifying encounters.

    Useful in specifying an adventure in quantum RPG.
    """

    def __init__(
        self,
        enemies: Sequence[qaracter.Qaracter] = (),
        probability: float = 1.0,
        description: Optional[str] = None,
    ):
        self.enemies = enemies
        self.probability = probability
        self.description = description

    def will_trigger(self) -> bool:
        """Returns True if the encounter should be triggered.

        This is based on the probability of the encounter happening.
        """
        return random.random() < self.probability

    def initiate(
        self, players: Sequence[qaracter.Qaracter], file: Optional[io.IOBase] = None
    ) -> battle.Battle:
        if file:
            return battle.Battle(players, self.enemies, file)
        return battle.Battle(players, self.enemies)
