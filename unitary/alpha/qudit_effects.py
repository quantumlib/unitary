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

from unitary.alpha.qudit_gates import QuditPlusGate, QuditXGate
from unitary.alpha.quantum_effect import QuantumEffect


class QuditCycle(QuantumEffect):
    """Cycles a qubit from |0> to |1>, |1> to |2>, etc.

    Essentially adds `addend` to the state, where `addend`
    is the parameter supplied at creation.
    """

    def __init__(self, dimenstion, num=1):
        self.dimension = dimenstion
        self.addend = num

    def effect(self, *objects):
        for q in objects:
            yield QuditPlusGate(self.dimension, addend=self.addend)(q.qubit)


class QuditFlip(QuantumEffect):
    """Flips two states of a qubit, leaving all other states unchanged.

    For instance, QuditFlip(3, 0, 1) is a qutrit effect
    that flips |0> to |1>, |1> to |0> and leaves
    |2> alone.  This is also sometimes referred to as the X_0_1 gate.
    """

    def __init__(self, dimenstion: int, state0: int, state1: int):
        self.dimension = dimenstion
        self.state0 = state0
        self.state1 = state1

    def effect(self, *objects):
        for q in objects:
            yield QuditXGate(self.dimension, self.state0, self.state1)(q.qubit)
