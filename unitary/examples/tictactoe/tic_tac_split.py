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
from typing import Optional

from unitary.alpha import QuantumEffect, QuantumObject
from unitary.alpha.qudit_gates import QuditXGate, QuditSwapPowGate
from unitary.examples.tictactoe.enums import TicTacSquare


class TicTacSplit(QuantumEffect):
    """Flips a qubit from |0> to |1> then splits to another square."""

    def __init__(self, tic_tac_type: TicTacSquare):
        self.tic_tac_type = tic_tac_type.value

    def num_dimension(self) -> Optional[int]:
        return 3

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, square1: QuantumObject, square2: QuantumObject):
        yield QuditXGate(3, 0, self.tic_tac_type)(square1.qubit)
        yield QuditSwapPowGate(3, exponent=0.5)(square1.qubit, square2.qubit)
