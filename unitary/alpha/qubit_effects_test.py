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
from unitary.alpha.sparse_vector_simulator import SparseSimulator


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_flip(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Flip()(piece)
    assert board.circuit == cirq.Circuit(cirq.X(cirq.NamedQubit("t")))


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_superposition(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Superposition()(piece)
    assert board.circuit == cirq.Circuit(cirq.H(cirq.NamedQubit("t")))


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [1, 0] for result in results)
    alpha.Move()(piece1, piece2)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.SWAP(a, b))
    assert board.circuit == expected_circuit
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [0, 1] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_phased_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [1, 0] for result in results)
    alpha.PhasedMove()(piece1, piece2)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.ISWAP(a, b))
    assert board.circuit == expected_circuit
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [0, 1] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_split(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    piece3 = alpha.QuantumObject("c", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    board.add_object(piece3)
    alpha.Split()(piece1, piece2, piece3)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    c = cirq.NamedQubit("c")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.SWAP(a, b)**0.5)
    expected_circuit.append(cirq.SWAP(a, c)**0.5)
    expected_circuit.append(cirq.SWAP(a, c)**0.5)
    assert board.circuit == expected_circuit


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, SparseSimulator])
def test_phased_split(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(),
                               compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    piece3 = alpha.QuantumObject("c", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    board.add_object(piece3)
    alpha.PhasedSplit()(piece1, piece2, piece3)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    c = cirq.NamedQubit("c")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.ISWAP(a, b)**0.5)
    expected_circuit.append(cirq.ISWAP(a, c)**0.5)
    expected_circuit.append(cirq.ISWAP(a, c)**0.5)
    assert board.circuit == expected_circuit
