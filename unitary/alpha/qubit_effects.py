# Copyright 2022 Google
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
    """Flips a qubit in |0> to |1> and vice versa."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        for q in objects:
            yield cirq.X(q.qubit)


class Superposition(QuantumEffect):
    """Takes a qubit in a basis state into a superposition."""

    def num_dimension(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        for q in objects:
            yield cirq.H(q.qubit)


class Move(QuantumEffect):
    """Moves a qubit state into another quantum objects."""
    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 2

    def effect(self, *objects):
        yield cirq.SWAP(objects[0].qubit, objects[1].qubit)


class PhasedMove(QuantumEffect):
    """Moves a qubit state into another quantum objects with phase change."""
    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self):
        return 2

    def effect(self, *objects):
        yield cirq.ISWAP(objects[0].qubit, objects[1].qubit)


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
