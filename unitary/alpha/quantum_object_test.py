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

import enum
import pytest

import cirq

import unitary.alpha as alpha


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_negation(simulator, compile_to_qubits):
    piece = alpha.QuantumObject("t", 0)
    board = alpha.QuantumWorld(
        piece, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[0]]
    -piece  # pylint: disable=pointless-statement
    assert board.peek() == [[1]]
    -piece  # pylint: disable=pointless-statement
    assert board.peek() == [[0]]
    piece += 1
    assert board.peek() == [[1]]


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_add_world_after_state_change(simulator, compile_to_qubits):
    piece = alpha.QuantumObject("t", 0)
    piece += 1
    board = alpha.QuantumWorld(
        piece, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[1]]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_qutrit(simulator, compile_to_qubits):
    piece = alpha.QuantumObject("t", 2)
    board = alpha.QuantumWorld(
        piece, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[2]]
    piece += 1
    assert board.peek() == [[0]]
    piece += 1
    assert board.peek() == [[1]]
    piece += 1
    assert board.peek() == [[2]]
    piece += 1
    assert board.peek() == [[0]]
    piece += 2
    assert board.peek() == [[2]]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_enum(simulator, compile_to_qubits):
    class Color(enum.Enum):
        RED = 0
        YELLOW = 1
        GREEN = 2

    piece = alpha.QuantumObject("t", Color.YELLOW)
    board = alpha.QuantumWorld(
        piece, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[Color.YELLOW]]
    piece += Color.YELLOW
    assert board.peek() == [[Color.GREEN]]
    piece += Color.GREEN
    assert board.peek() == [[Color.YELLOW]]


def test_bag_args():
    with pytest.raises(ValueError, match="Unsupported initial state"):
        _ = alpha.QuantumObject("test", "bad arg")
    piece = alpha.QuantumObject("t", 0)
    with pytest.raises(TypeError, match="unsupported operand"):
        piece += "bad stuff"
