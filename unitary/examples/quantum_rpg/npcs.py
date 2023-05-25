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

import random

import unitary.alpha as alpha
from unitary.examples.quantum_rpg import qaracter


class Npc(qaracter.Qaracter):
    """Base class for non-player character `Qaracter` objects."""

    def is_npc(self):
        return True


class Observer(Npc):
    """Simple test NPC that measures a random qubit each turn."""

    def npc_action(self, battle) -> str:
        enemy_target = random.randint(0, len(battle.player_side) - 1)
        enemy_name = battle.player_side[enemy_target].name
        enemy_qubit = random.choice(battle.player_side[enemy_target].active_qubits())

        battle.player_side[enemy_target].sample(enemy_qubit, True)
        return f"Observer {self.name} measures {enemy_name} at qubit {enemy_qubit}"
