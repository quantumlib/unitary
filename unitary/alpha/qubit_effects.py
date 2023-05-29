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
#
from typing import Iterator, Optional, Sequence, Union
import abc
import enum

import cirq

from unitary.alpha.quantum_effect import QuantumEffect


class Flip(QuantumEffect):
    """Flips a qubit in |0> to |1> and vice versa.

    For a partial flip, use the `effect_fraction` argument.

    These effects will be cumulative.  For instance, two quarter
    flips (effect_fraction=0.25) will be equivalent to a half
    flip (effect_fraction=0.5).

    Note that most fractions will not produce the corresponding
    probabiltity distribution.  For instance, a effect_fraction
    of 0.25 will not produce a 25%/75% probability distribution
    of outcomes.

    Args:
        effect_fraction: Amount of flip effect to perform.
            This results in an exponentiation of the flip (X)
            effect.  A fraction of 1.0 corresponds to a full
            flip (this is the default).  A fraction of 0.5
            corresponds to a half flip (square root of NOT)
            and a fraction of 0.0 has no effect.
    """

    def __init__(self, effect_fraction: float = 1.0):
        self.effect_fraction = effect_fraction

    def num_dimension(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        for q in objects:
            yield cirq.X(q.qubit) ** self.effect_fraction

    def __str__(self):
        if self.effect_fraction == 1:
            return "Flip"
        return f"Flip(effect_fraction={self.effect_fraction})"

    def __eq__(self, other):
        if isinstance(other, Flip):
            return self.effect_fraction == other.effect_fraction
        return NotImplemented


class Phase(QuantumEffect):
    """Phases a qubit from |+> to |-> and vice versa.

    This effect 'spins' the qubit and brings it in or out phase
    when compared to other qubits.   This has little effect
    on the |0> and |1> states, but can change the phase (complex sign)
    of states in superpositions.

    A full phase is the same as a 180° rotation around the Z axis, or a Z gate.
    For a partial phase, use the `effect_fraction` argument.

    These effects will be cumulative.  For instance, two quarter
    phases (effect_fraction=0.25) will be equivalent to a half
    phases (effect_fraction=0.5).

    Args:
        effect_fraction: Amount of phase effect to perform.
            This results in an exponentiation of the flip (Z)
            effect.  A fraction of 1.0 corresponds to a full
            phase flip (this is the default).  A fraction of 0.5
            corresponds to a half flip (square root of Z)
            and a fraction of 0.0 has no effect.
    """

    def __init__(self, effect_fraction: float = 1.0):
        self.effect_fraction = effect_fraction

    def num_dimension(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        for q in objects:
            yield cirq.Z(q.qubit) ** self.effect_fraction

    def __str__(self):
        if self.effect_fraction == 1:
            return "Phase"
        return f"Phase(effect_fraction={self.effect_fraction})"

    def __eq__(self, other):
        if isinstance(other, Phase):
            return self.effect_fraction == other.effect_fraction
        return NotImplemented


class Superposition(QuantumEffect):
    """Takes a qubit in a basis state into a superposition."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        for q in objects:
            yield cirq.H(q.qubit)

    def __eq__(self, other):
        return isinstance(other, Superposition) or NotImplemented


class Move(QuantumEffect):
    """Moves a qubit state into another quantum objects."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 2

    def effect(self, *objects):
        yield cirq.SWAP(objects[0].qubit, objects[1].qubit)

    def __eq__(self, other):
        return isinstance(other, Move) or NotImplemented


class PhasedMove(QuantumEffect):
    """Moves a qubit state into another quantum objects with phase change."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 2

    def effect(self, *objects):
        yield cirq.ISWAP(objects[0].qubit, objects[1].qubit)

    def __eq__(self, other):
        return isinstance(other, PhasedMove) or NotImplemented


class Split(QuantumEffect):
    """Splits a qubit state into two different quantum objects."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 3

    def effect(self, *objects):
        yield cirq.SWAP(objects[0].qubit, objects[1].qubit) ** 0.5
        yield cirq.SWAP(objects[0].qubit, objects[2].qubit) ** 0.5
        yield cirq.SWAP(objects[0].qubit, objects[2].qubit) ** 0.5

    def __eq__(self, other):
        return isinstance(other, Split) or NotImplemented

    def __eq__(self, other):
        return isinstance(other, Split) or NotImplemented


class PhasedSplit(QuantumEffect):
    """Splits a qubit state into two different quantum objects with a phase."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 3

    def effect(self, *objects):
        yield cirq.ISWAP(objects[0].qubit, objects[1].qubit) ** 0.5
        yield cirq.ISWAP(objects[0].qubit, objects[2].qubit) ** 0.5
        yield cirq.ISWAP(objects[0].qubit, objects[2].qubit) ** 0.5

    def __eq__(self, other):
        return isinstance(other, PhasedSplit) or NotImplemented
