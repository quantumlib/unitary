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

from typing import List, Optional, Sequence

import io
import random
import sys

import unitary.alpha as alpha
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.input_helpers as input_helpers
import unitary.examples.quantum_rpg.qaracter as qaracter


class EncounterXp:
    """What experience (XP) is possible from an encounter."""

    def __init__(
        self,
        xp_choices: Sequence[Sequence[alpha.QuantumEffect]],
        weights: Optional[Sequence[float]] = None,
    ):
        self.xp_choices = list(xp_choices)
        if not weights:
            self.weights = [1.0] * len(self.xp_choices)
        else:
            self.weights = list(weights)
        if len(self.weights) != len(self.xp_choices):
            raise ValueError(
                "Weighted probabilities must match the length of the gate XP"
            )

    def choose(self) -> List[alpha.QuantumEffect]:
        """Choose an XP possibility from the list of possible XP choices."""
        return list(random.choices(self.xp_choices, weights=self.weights)[0])


def is_ready_for_next_level(qar: qaracter.Qaracter) -> bool:
    """Checks if a qaracter is ready to advance to the next level.

    Once the number of operations on each qubit exceeds your level,
    you will gain another level (and HP).
    """
    current_level = qar.level
    for idx in range(current_level):
        hp = qar.get_hp(qar.quantum_object_name(idx + 1))
        if not hp:
            continue
        if (
            len(list(qar.circuit.findall_operations(lambda op: hp.qubit in op.qubits)))
            <= current_level
        ):
            return False
    return True


def award_xp(
    state: game_state.GameState,
    xp: Optional[EncounterXp],
):
    """Prompt user to choose a qaracter to award XP to."""
    if not xp:
        return
    print("You have been awarded XP!", file=state.file)
    effect_list = xp.choose()
    for effect in effect_list:
        print(f"  {effect}", file=state.file)
    print("", file=state.file)
    for effect in effect_list:
        num_qubits = effect.num_objects() or 1
        eligible_party = [
            qar for qar in state.party if len(qar.active_qubits()) >= num_qubits
        ]
        if not eligible_party:
            print(f"Qaracters are not high-enough level for {effect}!", file=state.file)
            continue
        print(f"Choose the qaracter to add the {effect} to:", file=state.file)
        for idx, qar in enumerate(eligible_party):
            print(f"{idx+1}) {qar.name}", file=state.file)
        qar_choice = input_helpers.get_user_input_number(
            state.get_user_input, ">", len(eligible_party)
        )
        qar = eligible_party[qar_choice - 1]
        print("Current qaracter sheet:", file=state.file)
        print(qar.circuit, file=state.file)
        qubit_list = list(qar.active_qubits())
        qubit_choices = []
        for qubit_num in range(num_qubits):
            print(f"Choose qubit {qubit_num} for {effect}:", file=state.file)
            for idx, q in enumerate(qubit_list):
                print(f"{idx+1}) {q}", file=state.file)
            choice = input_helpers.get_user_input_number(
                state.get_user_input, ">", len(qubit_list)
            )
            qubit_choices.append(qar.get_hp(qubit_list[choice - 1]))
        effect(*qubit_choices)
        if is_ready_for_next_level(qar):
            print(
                f"{qar.name} has advanced to the next level and gains a HP!",
                file=state.file,
            )
            qar.add_hp()
