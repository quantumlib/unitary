import random

import unitary.alpha as alpha
from unitary.examples.quantum_rpg import qaracter


class Npc(qaracter.Qaracter):
    """Base class for non-player character `Qaracter` objects.

    """

    def is_npc(self):
        return True


class Observer(Npc):
    """Simple test NPC that measures a random qubit each turn."""

    def npc_action(self, battle) -> str:
        enemy_target = random.randint(0, len(battle.player_side) - 1)
        enemy_name = battle.player_side[enemy_target].name
        enemy_qubit = random.choice(
            battle.player_side[enemy_target].active_qubits())

        battle.player_side[enemy_target].sample(enemy_qubit, True)
        return f'Observer {self.name} measures {enemy_name} at qubit {enemy_qubit}'
