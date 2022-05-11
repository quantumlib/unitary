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
import numpy as np
import cirq

import unitary.alpha.qudit_gates as qudit_gates


@pytest.mark.parametrize("num_gates", [1, 2, 3, 4, 5, 6])
def test_plus_one(num_gates: int):
    qutrit = cirq.NamedQid("a", dimension=3)
    c = cirq.Circuit()
    for i in range(num_gates):
        c.append(qudit_gates.QuditPlusGate(3)(qutrit))
    sim = cirq.Simulator()
    c.append(cirq.measure(qutrit, key="m"))
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == num_gates % 3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=num_gates)(qutrit))
    c.append(cirq.measure(qutrit, key="m"))
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == num_gates % 3)


@pytest.mark.parametrize(
    "q0, q1", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
)
def test_swap(q0: int, q1: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditSwapPowGate(3)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == q1)
    assert np.all(results.measurements["m1"] == q0)


@pytest.mark.parametrize(
    "q0, q1", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
)
def test_iswap(q0: int, q1: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditISwapPowGate(3)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == q1)
    assert np.all(results.measurements["m1"] == q0)


@pytest.mark.parametrize(
    "q0, q1", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
)
def test_sqrt_swap(q0: int, q1: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditSwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.any(results.measurements["m0"] == q0)
    assert np.any(results.measurements["m1"] == q0)
    assert np.any(results.measurements["m0"] == q1)
    assert np.any(results.measurements["m1"] == q1)
    assert np.all(
        (results.measurements["m0"] == q0) | (results.measurements["m0"] == q1)
    )
    assert np.all(
        (results.measurements["m1"] == q0) | (results.measurements["m1"] == q1)
    )
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditSwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(qudit_gates.QuditSwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == q1)
    assert np.all(results.measurements["m1"] == q0)


@pytest.mark.parametrize(
    "q0, q1", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
)
def test_sqrt_iswap(q0: int, q1: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditISwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.any(results.measurements["m0"] == q0)
    assert np.any(results.measurements["m1"] == q0)
    assert np.any(results.measurements["m0"] == q1)
    assert np.any(results.measurements["m1"] == q1)
    assert np.all(
        (results.measurements["m0"] == q0) | (results.measurements["m0"] == q1)
    )
    assert np.all(
        (results.measurements["m1"] == q0) | (results.measurements["m1"] == q1)
    )
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditPlusGate(3, addend=q1)(qutrit1))
    c.append(qudit_gates.QuditISwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(qudit_gates.QuditISwapPowGate(3, exponent=0.5)(qutrit0, qutrit1))
    c.append(cirq.measure(qutrit0, key="m0"))
    c.append(cirq.measure(qutrit1, key="m1"))
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == q1)
    assert np.all(results.measurements["m1"] == q0)
