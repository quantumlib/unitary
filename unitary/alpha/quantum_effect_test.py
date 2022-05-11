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
import pytest

import cirq

import unitary.alpha as alpha

Q0 = cirq.NamedQubit("q0")
Q1 = cirq.NamedQubit("q1")


def test_quantum_if():
    board = alpha.QuantumWorld()
    piece = alpha.QuantumObject("q0", 1)
    piece2 = alpha.QuantumObject("q1", 0)
    board.add_piece(piece)
    board.add_piece(piece2)
    alpha.quantum_if(piece).then(alpha.Flip())(piece2)
    expected_circuit = cirq.Circuit()
    expected_circuit.append(cirq.X(Q0))
    expected_circuit.append(cirq.CNOT(Q0, Q1))
    assert board.circuit == expected_circuit


def test_anti_control():
    board = alpha.QuantumWorld()
    piece = alpha.QuantumObject("q0", 1)
    piece2 = alpha.QuantumObject("q1", 0)
    board.add_piece(piece)
    board.add_piece(piece2)
    alpha.quantum_if(piece).equals(0).then(alpha.Flip())(piece2)
    expected_circuit = cirq.Circuit()
    expected_circuit.append(cirq.X(Q0))
    expected_circuit.append(cirq.X(Q0))
    expected_circuit.append(cirq.CNOT(Q0, Q1))
    assert board.circuit == expected_circuit


def test_no_board():
    piece = alpha.QuantumObject("q0", 1)
    with pytest.raises(ValueError, match="must be on a board"):
        alpha.Flip()(piece)


def test_bad_length():
    board = alpha.QuantumWorld()
    piece = alpha.QuantumObject("q0", 1)
    board.add_piece(piece)
    with pytest.raises(ValueError, match="Not able to equate"):
        alpha.quantum_if(piece).equals(0, 1)

    with pytest.raises(ValueError, match="Cannot apply effect"):
        alpha.Split()(piece)


def test_no_qutrits():
    board = alpha.QuantumWorld()
    piece = alpha.QuantumObject("q0", 2)
    board.add_piece(piece)
    with pytest.raises(ValueError, match="Cannot apply effect to qids"):
        alpha.Flip()(piece)
