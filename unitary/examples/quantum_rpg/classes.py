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

    def actions(self) -> Dict[str, Callable]:
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

    def actions(self) -> Dict[str, Callable]:
        return {
            "s": lambda monster, qubit: f"Sample result {monster.sample(monster.quantum_object_name(qubit), False)}",
            "m": lambda monster, qubit: monster.sample(
                monster.quantum_object_name(qubit), True
            ),
        }
