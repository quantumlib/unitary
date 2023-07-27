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

from typing import Any, Callable, Dict

from unitary import alpha
from unitary.examples.quantum_rpg import qaracter


class Engineer(qaracter.Qaracter):
    """Example player class that can do an X gate.

    Engineeers can do an X gate at level 1 and a H gate at level 3.
    """

    def action_descriptions(self) -> Dict[str, str]:
        """Descriptions for each player action."""
        return {"x": "Attack with X gate",
                "h": "Attack with H gate"}

    def help(self) -> str:
        return (
            "The Engineer can 'attack' by applying an X gate to an enemy qubit.\n"
            "This flips a qubit from |0> to |1> and vice versa."
        )

    def actions(self) -> Dict[str, Callable]:
        """Callables for each player action."""
        actions = {
            "x": lambda monster, qubit: monster.add_quantum_effect(alpha.Flip(), qubit)
        }
        if self.level >= 3:
            actions["h"] = lambda monster, qubit: monster.add_quantum_effect(
                alpha.Superposition(), qubit
            )
        return actions


class Analyst(qaracter.Qaracter):
    """Example player class that can sample and measure.

    Analysts can sample ('s') or measure ('m').
    """

    def action_descriptions(self) -> Dict[str, str]:
        """Descriptions for each player action."""
        return {"s": "Sample enemy qubit", "m": "Measure enemy qubit"}

    def help(self) -> str:
        msg = "The analyst can measure enemy qubits.  This forces an enemy qubit\n"
        msg += "into the |0> state or |1> state with a probability based on its\n"
        msg += "amplitude. Try to measure the enemy qubits as |0> to defeat them.\n"
        if self.level >= 3:
            msg += "At level 3 and above, the analyst can sample enemy qubits.\n"
            msg += "This allows you to test the value of a qubit by choosing\n"
            msg += "(or sampling) from a qubit's probability distribution\n"
            msg += "without modifying the state of the qubit.\n"
        return msg

    def actions(self) -> Dict[str, Callable]:
        """Callables for each player action."""
        action_dict = {
            "m": lambda monster, qubit: monster.sample(
                monster.quantum_object_name(qubit), True
            ),
        }
        if self.level >= 3:
            action_dict[
                "s"
            ] = (
                lambda monster, qubit: f"Sample result {monster.sample(monster.quantum_object_name(qubit), False)}"
            )
        return action_dict
