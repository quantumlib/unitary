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

import numpy as np
import cirq

from unitary.alpha import QuantumEffect, QuantumObject
from unitary.alpha.qudit_gates import QuditXGate, QuditISwapPowGate
from unitary.examples.tictactoe.enums import TicTacSquare, TicTacRules
from unitary.alpha.qudit_state_transform import qudit_to_qubit_unitary


class QuditSplitGate(cirq.Gate):
    """Performs a sqrt-swap gate between two qudits.

    This gate only swaps two states (either |01> and |10>
    or |02> and |20>), depending on whether initialized
    with either X or O.

    Args:
        square: use TicTacQuare.X to do a sqrtSWAP(01) and
            TicTacSquare.O to do a sqrtSWAP(02)
    """

    def __init__(self, square: TicTacSquare):
        self.square = square
        if self.square not in [TicTacSquare.O, TicTacSquare.X]:
            raise ValueError("Not a valid square: {self.square}")

    def _qid_shape_(self):
        return (4, 4)

    def _unitary_(self):
        arr = np.zeros((9, 9), dtype=np.complex64)
        for x in range(9):
            arr[x, x] = 1
        g = np.exp(1j * np.pi / 4)
        coeff = -1j * g * np.sin(np.pi / 4)
        diag = g * np.cos(np.pi / 4)
        if self.square == TicTacSquare.O:
            arr[2, 6] = coeff
            arr[6, 2] = coeff
            arr[6, 6] = diag
            arr[2, 2] = diag
        else:
            arr[1, 3] = coeff
            arr[3, 1] = coeff
            arr[3, 3] = diag
            arr[1, 1] = diag
        return qudit_to_qubit_unitary(3, 2, arr)

    def _circuit_diagram_info_(self, args):
        if not args.use_unicode_characters:
            wire_code = f"Swap{self.square.name}"
            return cirq.CircuitDiagramInfo(wire_symbols=(wire_code, wire_code))
        wire_code = f"×{self.square.name}"
        return cirq.CircuitDiagramInfo(wire_symbols=(wire_code, wire_code))


class TicTacSplit(QuantumEffect):
    """
    Flips a qubit from |0> to |1> then splits to another square.
    Depending on the ruleset, the split is done either using a standard
    sqrt-ISWAP gate, or using the custom QuditSplitGate.
    """

    def __init__(self, tic_tac_type: TicTacSquare, rules: TicTacRules):
        self.mark = tic_tac_type
        self.rules = rules

    def num_dimension(self) -> Optional[int]:
        return 4

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, square1: QuantumObject, square2: QuantumObject):
        yield QuditXGate(3, 0, self.mark.value)(square1.qubit)

        if self.rules == TicTacRules.QUANTUM_V3:
            yield QuditISwapPowGate(3, 0.5)(square1.qubit, square2.qubit)
        else:
            yield QuditSplitGate(self.mark)(square1.qubit, square2.qubit)
