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
