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
from typing import cast, List

import random

import unitary.alpha as alpha
import unitary.examples.quantum_rpg.enums as enums
import unitary.examples.quantum_rpg.qaracter as qaracter


def _enemy_qubits(party: List[qaracter.Qaracter]) -> List[alpha.QuantumObject]:
    """Determines valid enemy target qubits and returns them with the player."""
    enemy_qubits: List[alpha.QuantumObject] = []
    for player in party:
        for q in player.active_qubits():
            hp = player.get_hp(q)
            if hp is not None:
                enemy_qubits.append(hp)
    return enemy_qubits


def _sample_qubit(my_name: str, enemy_qubit: alpha.QuantumObject) -> str:
    if not enemy_qubit.world:
        return f"{enemy_qubit.name} is without a world!"
    enemy_name = enemy_qubit.name
    value = cast(qaracter.Qaracter, enemy_qubit.world).sample(enemy_name, True)
    return f"{my_name} measures {enemy_name} as {value.name}."


class Npc(qaracter.Qaracter):
    """Base class for non-player character `Qaracter` objects.

    Inheritors can overload either do_action or npc_action.

    For NPCs that target a single random qubit with an effect,
    one can overload act_on_enemy_qubit.

    For more general effects, npc_action can be overloaded.
    **kwargs can be used to add extra arguments for deterministic
    testing.
    """

    @property
    def display_name(self) -> str:
        return f"{self.__class__.__name__} {self.name}"

    def is_npc(self):
        return True

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        return ""

    def npc_action(self, battle, **kwargs) -> str:
        enemy_qubit = random.choice(_enemy_qubits(battle.player_side))
        action_choice = random.random()
        return self.act_on_enemy_qubit(enemy_qubit, action_choice, **kwargs)


#####################
#
#  Level 1 NPCs
#
#####################


class Observer(Npc):
    """Simple test NPC that measures a random qubit each turn."""

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        return _sample_qubit(self.display_name, enemy_qubit)


class BlueFoam(Npc):
    """Introductory NPC that starts in |0> state.

    Two actions:  can slime someone for a small X rotation,
    or measure a qubit.
    """

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        if action_choice > 0.2:
            slime = kwargs.get("slime") or random.randint(0, 250) / 1000.0
            alpha.Flip(effect_fraction=slime)(enemy_qubit)
            return f"{self.display_name} slimes {enemy_qubit.name} for {slime:0.3f}."
        else:
            return _sample_qubit(self.display_name, enemy_qubit)


class GreenFoam(Npc):
    """Introductory NPC that starts in |0> state.

    Two actions: can slime someone for a small Z rotation,
    or measure a qubit.
    """

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        if action_choice > 0.2:
            slime = kwargs.get("slime") or random.randint(0, 250) / 1000.0
            alpha.Phase(effect_fraction=slime)(enemy_qubit)
            return (
                f"{self.display_name} oozes {enemy_qubit.name} for {slime:0.3f} phase."
            )
        else:
            return _sample_qubit(self.display_name, enemy_qubit)


class RedFoam(Npc):
    """Introductory NPC that starts in |1> state.

    Two actions: can slime someone for a small X rotation,
    or measure a qubit.
    """

    def __init__(self, name):
        super().__init__(name)
        alpha.Flip()(self.get_hp(self.quantum_object_name(1)))

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        if action_choice > 0.2:
            slime = kwargs.get("slime") or random.randint(0, 350) / 1000.0
            alpha.Flip(effect_fraction=slime)(enemy_qubit)
            return f"{self.display_name} slimes {enemy_qubit.name} for {slime:0.3f}."
        else:
            return _sample_qubit(self.display_name, enemy_qubit)


class PurpleFoam(Npc):
    """Introductory NPC that starts in |+> state.

    Two actions: can slime someone for a small X rotation,
    or measure a qubit.
    """

    def __init__(self, name):
        super().__init__(name)
        alpha.Superposition()(self.get_hp(self.quantum_object_name(1)))

    def act_on_enemy_qubit(self, enemy_qubit, action_choice, **kwargs) -> str:
        if action_choice > 0.2:
            alpha.Superposition()(enemy_qubit)
            return f"{self.display_name} covers {enemy_qubit.name} with foam!"
        else:
            return _sample_qubit(self.display_name, enemy_qubit)
