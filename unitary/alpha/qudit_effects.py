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

from unitary.alpha.qudit_gates import QuditPlusGate
from unitary.alpha.quantum_effect import QuantumEffect


class Cycle(QuantumEffect):
    """Flips a qubit in |0> to |1> and vice versa."""

    def __init__(self, dimenstion, num=1):
        self.dimension = dimenstion
        self.addend = num

    def effect(self, *objects):
        for q in objects:
            yield QuditPlusGate(self.dimension, addend=self.addend)(q.qubit)
