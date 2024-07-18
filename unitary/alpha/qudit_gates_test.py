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
import pytest
import numpy as np
import cirq

import unitary.alpha.qudit_gates as qudit_gates


@pytest.mark.parametrize("state", [0, 1, 2])
def test_qutrit_x(state: int):
    qutrit = cirq.NamedQid("a", dimension=3)
    sim = cirq.Simulator()
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, state)(qutrit), cirq.measure(qutrit, key="m")
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == state)

    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, state)(qutrit),
        qudit_gates.QuditXGate(3, 0, state)(qutrit),
        cirq.measure(qutrit, key="m"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == 0)


@pytest.mark.parametrize("num_gates", [0, 1, 2, 3, 4, 5, 6])
def test_qutrit_plus_one(num_gates: int):
    qutrit = cirq.NamedQid("a", dimension=3)
    c = cirq.Circuit()
    for i in range(num_gates):
        c.append(qudit_gates.QuditPlusGate(3)(qutrit))
    c.append(cirq.measure(qutrit, key="m"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == num_gates % 3)


@pytest.mark.parametrize("num_gates", [0, 1, 2, 3, 4, 5, 6])
def test_qutrit_plus_addend(num_gates: int):
    qutrit = cirq.NamedQid("a", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=num_gates)(qutrit))
    c.append(cirq.measure(qutrit, key="m"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == num_gates % 3)


@pytest.mark.parametrize("control, dest", [(1, 1), (1, 2), (2, 1), (2, 2)])
def test_control_x(control: int, dest: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    sim = cirq.Simulator()

    # Control is zero and has no effect.
    c = cirq.Circuit(
        qudit_gates.QuditControlledXGate(3, control, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 0)
    assert np.all(results.measurements["m1"] == 0)

    # Control is activated and flips 2nd qutrit
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, control)(qutrit0),
        qudit_gates.QuditControlledXGate(3, control, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == control)
    assert np.all(results.measurements["m1"] == dest)

    # Control is activated and flips 2nd qutrit back to zero
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, control)(qutrit0),
        qudit_gates.QuditXGate(3, 0, dest)(qutrit1),
        qudit_gates.QuditControlledXGate(3, control, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == control)
    assert np.all(results.measurements["m1"] == 0)

    # Control is excited to a non-controlling state and has no effect.
    non_active = 3 - control
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, non_active)(qutrit0),
        qudit_gates.QuditControlledXGate(3, control, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == non_active)
    assert np.all(results.measurements["m1"] == 0)

    # 2nd qutrit is excited to a non-dest state and has no effect.
    non_active = 3 - dest
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, control)(qutrit0),
        qudit_gates.QuditXGate(3, 0, non_active)(qutrit1),
        qudit_gates.QuditControlledXGate(3, control, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == control)
    assert np.all(results.measurements["m1"] == non_active)


@pytest.mark.parametrize("dest", [1, 2])
def test_control_of_0_x(dest: int):
    qutrit0 = cirq.NamedQid("q0", dimension=3)
    qutrit1 = cirq.NamedQid("q1", dimension=3)
    sim = cirq.Simulator()

    # Control qutrit is in the zero state and flips 2nd qutrit
    c = cirq.Circuit(
        qudit_gates.QuditControlledXGate(3, 0, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 0)
    assert np.all(results.measurements["m1"] == dest)

    # Control qutrit is in the zero state and flips 2nd qutrit back to zero
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, dest)(qutrit1),
        qudit_gates.QuditControlledXGate(3, 0, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 0)
    assert np.all(results.measurements["m1"] == 0)

    # Control qutrit is in the one state and has no effect
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, 1)(qutrit0),
        qudit_gates.QuditControlledXGate(3, 0, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 1)
    assert np.all(results.measurements["m1"] == 0)

    # Control qutrit is in the two state and has no effect
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, 2)(qutrit0),
        qudit_gates.QuditControlledXGate(3, 0, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 2)
    assert np.all(results.measurements["m1"] == 0)

    # 2nd qutrit is in the non-dest state and has no effect
    non_active = 3 - dest
    c = cirq.Circuit(
        qudit_gates.QuditXGate(3, 0, non_active)(qutrit1),
        qudit_gates.QuditControlledXGate(3, 0, dest)(qutrit0, qutrit1),
        cirq.measure(qutrit0, key="m0"),
        cirq.measure(qutrit1, key="m1"),
    )
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m0"] == 0)
    assert np.all(results.measurements["m1"] == non_active)


@pytest.mark.parametrize(
    "gate",
    [
        qudit_gates.QuditPlusGate(3, addend=1),
        qudit_gates.QuditPlusGate(3, addend=2),
        qudit_gates.QuditPlusGate(3, addend=3),
        qudit_gates.QuditPlusGate(4, addend=1),
        qudit_gates.QuditPlusGate(4, addend=2),
        qudit_gates.QuditPlusGate(4, addend=3),
        qudit_gates.QuditXGate(3, 0, 1),
        qudit_gates.QuditXGate(3, 0, 2),
        qudit_gates.QuditControlledXGate(3),
        qudit_gates.QuditControlledXGate(3, 0, 2),
        qudit_gates.QuditSwapPowGate(3),
        qudit_gates.QuditISwapPowGate(3),
        qudit_gates.QuditSwapPowGate(3, exponent=0.5),
        qudit_gates.QuditISwapPowGate(3, exponent=0.5),
        qudit_gates.QuditHadamardGate(2),
        qudit_gates.QuditHadamardGate(3),
        qudit_gates.QuditHadamardGate(4),
    ],
)
def test_gates_are_unitary(gate: cirq.Gate):
    m = cirq.unitary(gate)
    np.set_printoptions(linewidth=200)
    assert np.allclose(np.eye(len(m)), m.dot(m.T.conj()), atol=1e-6)


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


@pytest.mark.parametrize("dimension, phase_rads", [(2, np.pi), (3, 1), (4, np.pi * 2)])
def test_rz_unitary(dimension: float, phase_rads: float):
    rz = qudit_gates.QuditRzGate(dimension=dimension, radians=phase_rads)
    expected_unitary = np.identity(n=dimension, dtype=np.complex64)

    # 1j = e ^ ( j * ( pi / 2 )), so we multiply phase_rads by 2 / pi.
    expected_unitary[dimension - 1][dimension - 1] = 1j ** (phase_rads * 2 / np.pi)

    assert np.isclose(phase_rads / np.pi, rz._exponent)
    rz_unitary = cirq.unitary(rz)
    assert np.allclose(cirq.unitary(rz), expected_unitary)
    assert np.allclose(np.eye(len(rz_unitary)), rz_unitary.dot(rz_unitary.T.conj()))


@pytest.mark.parametrize(
    "phase_1, phase_2, addend, expected_state",
    [
        (0, 0, 1, 2),
        (np.pi * 2 / 3, np.pi * 4 / 3, 0, 2),
        (np.pi * 4 / 3, np.pi * 2 / 3, 0, 1),
    ],
)
def test_X_HZH_qudit_identity(
    phase_1: float, phase_2: float, addend: int, expected_state: int
):
    # For d=3, there are three identities: one for each swap.
    # HH is equivalent to swapping |1> with |2>
    # Applying a 1/3 turn to |1> and a 2/3 turn to |2> results in swapping
    # |0> and |2>
    # Applying a 2/3 turn to |1> and a 1/3 turn to |2> results in swapping
    # |0> and |1>
    qutrit = cirq.NamedQid("q0", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=addend)(qutrit))
    c.append(qudit_gates.QuditHadamardGate(dimension=3)(qutrit))
    c.append(
        qudit_gates.QuditRzGate(dimension=3, radians=phase_1, phased_state=1)(qutrit)
    )
    c.append(
        qudit_gates.QuditRzGate(dimension=3, radians=phase_2, phased_state=2)(qutrit)
    )
    c.append(qudit_gates.QuditHadamardGate(dimension=3)(qutrit))
    c.append(cirq.measure(qutrit, key="m"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == expected_state)


@pytest.mark.parametrize(
    "phase_1, phase_2, addend, expected_state",
    [
        (0, 0, 1, 2),
        (np.pi * 2 / 3, np.pi * 4 / 3, 0, 2),
        (np.pi * 4 / 3, np.pi * 2 / 3, 0, 1),
    ],
)
def test_X_HZH_qudit_identity(
    phase_1: float, phase_2: float, addend: int, expected_state: int
):
    # For d=3, there are three identities: one for each swap.
    # HH is equivalent to swapping |1> with |2>
    # Applying a 1/3 turn to |1> and a 2/3 turn to |2> results in swapping
    # |0> and |2>
    # Applying a 2/3 turn to |1> and a 1/3 turn to |2> results in swapping
    # |0> and |1>
    qutrit = cirq.NamedQid("q0", dimension=3)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(3, addend=addend)(qutrit))
    c.append(qudit_gates.QuditHadamardGate(dimension=3)(qutrit))
    c.append(
        qudit_gates.QuditRzGate(dimension=3, radians=phase_1, phased_state=1)(qutrit)
    )
    c.append(
        qudit_gates.QuditRzGate(dimension=3, radians=phase_2, phased_state=2)(qutrit)
    )
    c.append(qudit_gates.QuditHadamardGate(dimension=3)(qutrit))
    c.append(cirq.measure(qutrit, key="m"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    assert np.all(results.measurements["m"] == expected_state)


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


@pytest.mark.parametrize(
    "d, q0", [(2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)]
)
def test_hadamard(d: int, q0: int):
    qutrit0 = cirq.NamedQid("q0", dimension=d)
    c = cirq.Circuit()
    c.append(qudit_gates.QuditPlusGate(d, addend=q0)(qutrit0))
    c.append(qudit_gates.QuditHadamardGate(d)(qutrit0))
    c.append(cirq.measure(qutrit0, key="m0"))
    sim = cirq.Simulator()
    results = sim.run(c, repetitions=1000)
    for each_possible_outcome in range(d):
        assert np.any(results.measurements["m0"] == each_possible_outcome)
