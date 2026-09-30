# Copyright 2020 The Unitary Authors
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

from collections import deque

import cirq
import cirq_google as cg
import pytest

import unitary.quantum_chess.initial_mapping_utils as imu

a0 = cirq.NamedQubit("a0")
a1 = cirq.NamedQubit("a1")
a2 = cirq.NamedQubit("a2")
a3 = cirq.NamedQubit("a3")
a4 = cirq.NamedQubit("a4")
a5 = cirq.NamedQubit("a5")
a6 = cirq.NamedQubit("a6")
a7 = cirq.NamedQubit("a7")

grid_qubits = dict(
    (f"{row}_{col}", cirq.GridQubit(row, col)) for row in range(10) for col in range(7)
)


def test_build_physical_qubits_graph():
    g = imu.build_physical_qubits_graph(cg.Sycamore23)
    expected = {
        grid_qubits["3_2"]: [grid_qubits["4_2"]],
        grid_qubits["4_1"]: [
            grid_qubits["4_2"],
            grid_qubits["5_1"],
        ],
        grid_qubits["4_2"]: [
            grid_qubits["3_2"],
            grid_qubits["4_3"],
            grid_qubits["5_2"],
            grid_qubits["4_1"],
        ],
        grid_qubits["4_3"]: [
            grid_qubits["4_2"],
            grid_qubits["5_3"],
        ],
        grid_qubits["5_0"]: [grid_qubits["5_1"]],
        grid_qubits["5_1"]: [
            grid_qubits["4_1"],
            grid_qubits["5_2"],
            grid_qubits["6_1"],
            grid_qubits["5_0"],
        ],
        grid_qubits["5_2"]: [
            grid_qubits["4_2"],
            grid_qubits["5_3"],
            grid_qubits["6_2"],
            grid_qubits["5_1"],
        ],
        grid_qubits["5_3"]: [
            grid_qubits["4_3"],
            grid_qubits["5_4"],
            grid_qubits["6_3"],
            grid_qubits["5_2"],
        ],
        grid_qubits["5_4"]: [
            grid_qubits["5_3"],
            grid_qubits["6_4"],
        ],
        grid_qubits["6_1"]: [
            grid_qubits["5_1"],
            grid_qubits["6_2"],
        ],
        grid_qubits["6_2"]: [
            grid_qubits["5_2"],
            grid_qubits["6_3"],
            grid_qubits["7_2"],
            grid_qubits["6_1"],
        ],
        grid_qubits["6_3"]: [
            grid_qubits["5_3"],
            grid_qubits["6_4"],
            grid_qubits["7_3"],
            grid_qubits["6_2"],
        ],
        grid_qubits["6_4"]: [
            grid_qubits["5_4"],
            grid_qubits["6_5"],
            grid_qubits["7_4"],
            grid_qubits["6_3"],
        ],
        grid_qubits["6_5"]: [
            grid_qubits["6_4"],
            grid_qubits["7_5"],
        ],
        grid_qubits["7_2"]: [
            grid_qubits["6_2"],
            grid_qubits["7_3"],
        ],
        grid_qubits["7_3"]: [
            grid_qubits["6_3"],
            grid_qubits["7_4"],
            grid_qubits["8_3"],
            grid_qubits["7_2"],
        ],
        grid_qubits["7_4"]: [
            grid_qubits["6_4"],
            grid_qubits["7_5"],
            grid_qubits["8_4"],
            grid_qubits["7_3"],
        ],
        grid_qubits["7_5"]: [
            grid_qubits["6_5"],
            grid_qubits["7_6"],
            grid_qubits["8_5"],
            grid_qubits["7_4"],
        ],
        grid_qubits["7_6"]: [grid_qubits["7_5"]],
        grid_qubits["8_3"]: [
            grid_qubits["7_3"],
            grid_qubits["8_4"],
        ],
        grid_qubits["8_4"]: [
            grid_qubits["7_4"],
            grid_qubits["8_5"],
            grid_qubits["9_4"],
            grid_qubits["8_3"],
        ],
        grid_qubits["8_5"]: [
            grid_qubits["7_5"],
            grid_qubits["8_4"],
        ],
        grid_qubits["9_4"]: [grid_qubits["8_4"]],
    }
    assert len(g) == len(expected)
    for q in expected:
        assert set(g[q]) == set(expected[q])


def test_get_least_connected_qubit():
    g = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1, 3],
        3: [2],
    }
    assert imu.get_least_connected_qubit(g, deque([0, 1, 2, 3])) == 3
    g = {
        0: [1],
        1: [0, 2],
        2: [1],
        3: [4],
        4: [3],
    }
    assert imu.get_least_connected_qubit(g, deque([0, 1, 2])) in {0, 2}
    assert imu.get_least_connected_qubit(g, deque([3, 4])) in {3, 4}


def test_build_logical_qubits_graph():
    # One connected component.
    c = cirq.Circuit(
        cirq.ISWAP(a2, a0),
        cirq.ISWAP(a0, a1),
        cirq.ISWAP(a0, a2),
        cirq.ISWAP(a1, a2),
        cirq.ISWAP(a2, a3),
    )
    assert imu.build_logical_qubits_graph(c) == {
        a0: [(a2, 0), (a1, 1)],
        a1: [(a0, 1), (a2, 3)],
        a2: [(a0, 0), (a1, 3), (a3, 4)],
        a3: [(a2, 4)],
    }
    # Three connected components with one-qubit and two-qubit gates.
    c = cirq.Circuit(
        cirq.ISWAP(a2, a0),
        cirq.ISWAP(a0, a1),
        cirq.ISWAP(a0, a2),
        cirq.ISWAP(a1, a2),
        cirq.ISWAP(a2, a3),
        cirq.ISWAP(a4, a5),
        cirq.X(a6),
    )
    assert imu.build_logical_qubits_graph(c) == {
        a0: [(a2, 0), (a1, 1)],
        a1: [(a0, 1), (a2, 3)],
        a2: [(a0, 0), (a1, 3), (a3, 4)],
        a3: [(a2, 4), (a6, 6)],
        a4: [(a5, 0), (a6, 5)],
        a5: [(a4, 0)],
        a6: [(a4, 5), (a3, 6)],
    }
    # Three connected components with only one-qubit gates.
    c = cirq.Circuit(cirq.X(a1), cirq.X(a2), cirq.X(a3))
    assert imu.build_logical_qubits_graph(c) == {
        a1: [(a3, 2)],
        a2: [(a3, 1)],
        a3: [(a2, 1), (a1, 2)],
    }
    # Three connected components with a measurement gates.
    c = cirq.Circuit(cirq.X(a1), cirq.X(a2), cirq.X(a3), cirq.measure(a1))
    assert imu.build_logical_qubits_graph(c) == {
        a1: [(a3, 3)],
        a2: [(a3, 2)],
        a3: [(a2, 2), (a1, 3)],
    }
    # One connected component with an invalid gate.
    with pytest.raises(ValueError, match="Operation.*has more than 2 qubits!"):
        c = cirq.Circuit(cirq.X(a1), cirq.X(a2), cirq.CCNOT(a1, a2, a3))
        imu.build_logical_qubits_graph(c)


@pytest.mark.parametrize(
    "g",
    [
        {
            0: [1],
            1: [0, 2],
            2: [1, 3, 5],
            3: [2, 4, 6],
            4: [3, 5],
            5: [2],
            6: [3],
        },
        {
            0: [(1,)],
            1: [(0,), (2,)],
            2: [(1,), (3,), (5,)],
            3: [(2,), (4,), (6,)],
            4: [(3,), (5,)],
            5: [(2,)],
            6: [(3,)],
        },
    ],
)
def test_find_all_pairs_shortest_paths(g):
    expected = {
        (0, 0): 0,
        (0, 1): 1,
        (0, 2): 2,
        (0, 3): 3,
        (0, 4): 4,
        (0, 5): 3,
        (0, 6): 4,
        (1, 0): 1,
        (1, 1): 0,
        (1, 2): 1,
        (1, 3): 2,
        (1, 4): 3,
        (1, 5): 2,
        (1, 6): 3,
        (2, 0): 2,
        (2, 1): 1,
        (2, 2): 0,
        (2, 3): 1,
        (2, 4): 2,
        (2, 5): 1,
        (2, 6): 2,
        (3, 0): 3,
        (3, 1): 2,
        (3, 2): 1,
        (3, 3): 0,
        (3, 4): 1,
        (3, 5): 2,
        (3, 6): 1,
        (4, 0): 4,
        (4, 1): 3,
        (4, 2): 2,
        (4, 3): 1,
        (4, 4): 0,
        (4, 5): 1,
        (4, 6): 2,
        (5, 0): 3,
        (5, 1): 2,
        (5, 2): 1,
        (5, 3): 2,
        (5, 4): 3,
        (5, 5): 0,
        (5, 6): 3,
        (6, 0): 4,
        (6, 1): 3,
        (6, 2): 2,
        (6, 3): 1,
        (6, 4): 2,
        (6, 5): 3,
        (6, 6): 0,
    }
    result = imu.find_all_pairs_shortest_paths(g)
    assert len(result) == len(expected)
    for k in expected:
        assert result[k] == expected[k]


def test_graph_center():
    g = {
        0: [1, 4],
        1: [0, 2, 4],
        2: [1, 4, 5],
        3: [4],
        4: [0, 1, 2, 3, 5],
        5: [2, 4],
    }
    assert imu.find_graph_center(g) == 4
    g = {
        0: [(1,), (4,)],
        1: [(0,), (2,), (4,)],
        2: [(1,), (4,), (5,)],
        3: [(4,)],
        4: [(0,), (1,), (2,), (3,), (5,)],
        5: [(2,), (4,)],
    }
    assert imu.find_graph_center(g) == 4


def test_traverse():
    g = {
        0: [(2, 0), (1, 1), (3, 6)],
        1: [(0, 1), (2, 3)],
        2: [(0, 0), (1, 3), (3, 5)],
        3: [(2, 5), (0, 6)],
    }
    assert imu.traverse(g, 0) == deque([0, 2, 1, 3])
    assert imu.traverse(g, 1) == deque([1, 0, 2, 3])
    assert imu.traverse(g, 2) == deque([2, 0, 1, 3])
    assert imu.traverse(g, 3) == deque([3, 2, 0, 1])


def test_find_reference_qubits():
    g = {
        a0: [(a2, 0), (a1, 1)],
        a1: [(a0, 1), (a2, 3)],
        a2: [(a0, 0), (a1, 3), (a3, 5)],
        a3: [(a2, 5)],
    }
    mapping = {
        a0: grid_qubits["0_5"],
    }
    assert set(imu.find_reference_qubits(mapping, g, a2)) == {
        grid_qubits["0_5"],
    }
    mapping = {
        a0: grid_qubits["0_5"],
        a2: grid_qubits["1_5"],
    }
    assert set(imu.find_reference_qubits(mapping, g, a1)) == {
        grid_qubits["0_5"],
        grid_qubits["1_5"],
    }


def test_find_candidate_qubits():
    g = imu.build_physical_qubits_graph(cg.Sycamore23)
    # First level has a free qubit.
    # The mapped variable contains "occupied" qubits.
    mapped = {
        grid_qubits["4_1"],
        grid_qubits["4_3"],
        grid_qubits["5_2"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["4_2"])) == {
        cirq.GridQubit(3, 2),
    }
    # Second level has free qubits.
    mapped = {
        grid_qubits["5_3"],
        grid_qubits["4_1"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["4_3"])) == {
        cirq.GridQubit(4, 2),
    }
    # Third level has free qubits.
    mapped = {
        grid_qubits["4_1"],
        grid_qubits["5_2"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["5_1"])) == {
        cirq.GridQubit(5, 0),
        cirq.GridQubit(6, 1),
    }
    # Fourth level has free qubits.
    mapped = {
        grid_qubits["5_4"],
        grid_qubits["7_4"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["6_4"])) == {
        cirq.GridQubit(6, 3),
        cirq.GridQubit(6, 5),
    }
    # Fifth level has free qubits.
    mapped = {
        grid_qubits["7_4"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["7_3"])) == {
        cirq.GridQubit(6, 3),
        cirq.GridQubit(8, 3),
        cirq.GridQubit(7, 2),
    }
    # Sixth level has free qubits.
    mapped = {
        grid_qubits["7_4"],
        grid_qubits["9_4"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["8_4"])) == {
        cirq.GridQubit(8, 3),
        cirq.GridQubit(8, 5),
    }
    # Seventh level has free qubits.
    mapped = {
        grid_qubits["7_4"],
        grid_qubits["8_5"],
        grid_qubits["8_3"],
    }
    assert set(imu.find_candidate_qubits(mapped, g, grid_qubits["8_4"])) == {
        cirq.GridQubit(9, 4),
    }


def test_find_shortest_path():
    g = {
        0: [1, 7],
        1: [0, 2, 7],
        2: [1, 3, 5, 8],
        3: [2, 4, 5],
        4: [3, 5],
        5: [2, 3, 4, 6],
        6: [5, 7],
        7: [0, 1, 6, 8],
        8: [2, 7],
    }
    assert imu.find_shortest_path(g, 0, 5) == 3
    assert imu.find_shortest_path(g, 1, 8) == 2
    assert imu.find_shortest_path(g, 4, 7) == 3


@pytest.mark.parametrize(
    "device",
    [
        cg.Sycamore23,
        cg.Sycamore,
    ],
)
def test_calculate_initial_mapping(device):
    c = cirq.Circuit(
        cirq.X(a1),
        cirq.X(a2),
        cirq.ISWAP(a0, a2) ** 0.5,
    )
    mapping = imu.calculate_initial_mapping(device, c)
    device.validate_circuit(c.transform_qubits(lambda q: mapping[q]))
