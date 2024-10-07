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

import pytest

import cirq
from cirq.testing import random_circuit
from unitary.alpha import qudit_gates

from unitary.alpha.sparse_vector_simulator import (
    SparseSimulator,
    PostSelectOperation,
    InvalidPostSelectionError,
)


def test_simulation_fidelity():
    """Check that simulation results are roughly the same as a Cirq simulator."""
    circuit = random_circuit(
        qubits=10,
        n_moments=20,
        op_density=0.3,
        gate_domain={
            cirq.X: 1,
            cirq.H: 1,
            cirq.T: 1,
            cirq.Z: 1,
            cirq.Y: 1,
            cirq.SWAP**0.5: 2,
            cirq.ISWAP**0.5: 2,
            cirq.CNOT: 2,
            (cirq.SWAP**0.5).controlled(): 3,
            (cirq.ISWAP**0.5).controlled(): 3,
        },
    )
    circuit.append(cirq.measure(q) for q in circuit.all_qubits())
    test_sim = SparseSimulator()
    validation_sim = cirq.Simulator()
    repetitions = 10000
    test_data = test_sim.run(circuit, repetitions=repetitions).measurements
    validation_data = validation_sim.run(circuit, repetitions=repetitions).measurements
    for q in circuit.all_qubits():
        test_ones_fraction = test_data[q.name].sum() / repetitions
        validation_ones_fraction = validation_data[q.name].sum() / repetitions
        assert abs(test_ones_fraction - validation_ones_fraction) < 0.1


def test_simulation_fidelity_qudits_fails():
    """Check that SparseSimulator does not support Qudit operations yet.

    TODO(#78): Fix this.
    """
    qudit = cirq.NamedQid("a", 3)
    circuit = cirq.Circuit(qudit_gates.QuditXGate(3).on(qudit), cirq.measure(qudit))
    with pytest.raises(ValueError, match="size 2 is different from 3"):
        _ = SparseSimulator().run(circuit).measurements


def test_post_selection():
    """Test a circuit with PostSelectOperation."""
    sim = SparseSimulator()
    c1 = cirq.NamedQubit("c1")
    c2 = cirq.NamedQubit("c2")
    t = cirq.NamedQubit("t")
    repetitions = 10000
    circuit = cirq.Circuit(
        cirq.H(c1),
        cirq.H(c2),
        cirq.X(t).controlled_by(c1, c2),
        PostSelectOperation(t, 0),
        cirq.X(c1),
        cirq.measure(c1),
        cirq.measure(c2),
        cirq.measure(t),
    )
    data = sim.run(circuit, repetitions=repetitions).data
    assert sum(data.t == 0) == repetitions
    assert sum((data.c1 == 0) & (data.c2 == 1)) == 0
    assert 0.23 < sum((data.c1 == 1) & (data.c2 == 1)) / repetitions < 0.43
    assert 0.23 < sum((data.c1 == 1) & (data.c2 == 0)) / repetitions < 0.43
    assert 0.23 < sum((data.c1 == 0) & (data.c2 == 0)) / repetitions < 0.43


def test_impossible_post_selection():
    """Test post-selecting for a state with zero amplitude."""
    sim = SparseSimulator()
    qubit = cirq.NamedQubit("q")
    circuit = cirq.Circuit(PostSelectOperation(qubit, 1), cirq.measure(qubit))
    with pytest.raises(InvalidPostSelectionError):
        sim.run(circuit, repetitions=100)
