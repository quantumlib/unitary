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


class StopLight(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_flip(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Flip()(piece)
    assert board.circuit == cirq.Circuit(cirq.X(cirq.NamedQubit("t")))
    assert str(alpha.Flip()) == "Flip"


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_partial_flip(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Flip(effect_fraction=0.25)(piece)
    assert board.circuit == cirq.Circuit(cirq.X(cirq.NamedQubit("t")) ** 0.25)
    assert str(alpha.Flip(effect_fraction=0.25)) == "Flip(effect_fraction=0.25)"


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_partial_flip_multiple(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Flip(effect_fraction=0.5)(piece)
    alpha.Flip(effect_fraction=0.5)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [1] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_phase(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Phase()(piece)
    assert board.circuit == cirq.Circuit(cirq.Z(cirq.NamedQubit("t")))
    assert str(alpha.Phase()) == "Phase"


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_partial_phase(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Phase(effect_fraction=0.25)(piece)
    assert board.circuit == cirq.Circuit(cirq.Z(cirq.NamedQubit("t")) ** 0.25)
    assert str(alpha.Phase(effect_fraction=0.25)) == "Phase(effect_fraction=0.25)"


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_qubit_superposition(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", 0)
    board.add_object(piece)
    alpha.Superposition()(piece)
    assert board.circuit == cirq.Circuit(cirq.H(cirq.NamedQubit("t")))
    assert str(alpha.Superposition()) == "Superposition"


def test_qudit_superposition():
    board = alpha.QuantumWorld(sampler=cirq.Simulator(), compile_to_qubits=False)
    piece = alpha.QuantumObject("t", StopLight.GREEN)
    board.add_object(piece)
    alpha.Superposition()(piece)
    results = board.peek([piece], count=100)
    assert any(result == [StopLight.RED] for result in results)
    assert any(result == [StopLight.YELLOW] for result in results)
    assert any(result == [StopLight.GREEN] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
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
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_partial_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [1, 0] for result in results)
    alpha.Move(effect_fraction=0.5)(piece1, piece2)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.SWAP(a, b) ** 0.5)
    assert board.circuit == expected_circuit
    results = board.peek([piece1, piece2], count=100)
    assert any(result == [0, 1] for result in results)
    assert any(result == [1, 0] for result in results)
    assert all(result == [0, 1] or result == [1, 0] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_phased_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
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
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_partial_phased_move(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
    piece1 = alpha.QuantumObject("a", 1)
    piece2 = alpha.QuantumObject("b", 0)
    board.add_object(piece1)
    board.add_object(piece2)
    results = board.peek([piece1, piece2], count=100)
    assert all(result == [1, 0] for result in results)
    alpha.PhasedMove(effect_fraction=0.5)(piece1, piece2)
    expected_circuit = cirq.Circuit()
    a = cirq.NamedQubit("a")
    b = cirq.NamedQubit("b")
    expected_circuit.append(cirq.X(a))
    expected_circuit.append(cirq.ISWAP(a, b) ** 0.5)
    assert board.circuit == expected_circuit
    results = board.peek([piece1, piece2], count=100)
    assert any(result == [0, 1] for result in results)
    assert any(result == [1, 0] for result in results)
    assert all(result == [0, 1] or result == [1, 0] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_split(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
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
    expected_circuit.append(cirq.SWAP(a, b) ** 0.5)
    expected_circuit.append(cirq.SWAP(a, c) ** 0.5)
    expected_circuit.append(cirq.SWAP(a, c) ** 0.5)
    assert board.circuit == expected_circuit


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_phased_split(simulator, compile_to_qubits):
    board = alpha.QuantumWorld(sampler=simulator(), compile_to_qubits=compile_to_qubits)
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
    expected_circuit.append(cirq.ISWAP(a, b) ** 0.5)
    expected_circuit.append(cirq.ISWAP(a, c) ** 0.5)
    expected_circuit.append(cirq.ISWAP(a, c) ** 0.5)
    assert board.circuit == expected_circuit


def test_equalis():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(alpha.Flip(), alpha.Flip(), alpha.Flip(effect_fraction=1.0))
    eq.add_equality_group(alpha.Phase(), alpha.Phase(effect_fraction=1.0))
    eq.add_equality_group(alpha.Superposition(), alpha.Superposition())
    eq.add_equality_group(
        alpha.Flip(effect_fraction=0.25), alpha.Flip(effect_fraction=0.25)
    )
    eq.add_equality_group(
        alpha.Phase(effect_fraction=0.25), alpha.Phase(effect_fraction=0.25)
    )
    eq.add_equality_group(alpha.Split(), alpha.Split())
    eq.add_equality_group(alpha.Move(), alpha.Move())
    eq.add_equality_group(alpha.PhasedMove(), alpha.PhasedMove())
