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
import enum

import pytest

import numpy as np

import cirq

import unitary.alpha as alpha
import unitary.alpha.qudit_gates as qudit_gates


class Light(enum.Enum):
    RED = 0
    GREEN = 1


class StopLight(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_duplicate_objects(compile_to_qubits):
    light = alpha.QuantumObject("test", Light.GREEN)
    board = alpha.QuantumWorld([light], compile_to_qubits=compile_to_qubits)
    with pytest.raises(ValueError, match="already added"):
        board.add_object(alpha.QuantumObject("test", Light.RED))


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_get_object_by_name(compile_to_qubits):
    light = alpha.QuantumObject("test", Light.GREEN)
    light2 = alpha.QuantumObject("test2", Light.RED)
    board = alpha.QuantumWorld([light, light2], compile_to_qubits=compile_to_qubits)
    assert board.get_object_by_name("test") == light
    assert board.get_object_by_name("test2") == light2
    assert board.get_object_by_name("test3") == None
    assert board["test"] == light
    assert board["test2"] == light2
    with pytest.raises(KeyError):
        _ = board["test3"]


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_one_qubit(simulator, compile_to_qubits):
    light = alpha.QuantumObject("test", Light.GREEN)
    board = alpha.QuantumWorld(
        [light], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[Light.GREEN]]
    assert board.peek([light], count=2) == [[Light.GREEN], [Light.GREEN]]
    assert board.peek(["test"], count=2) == [[Light.GREEN], [Light.GREEN]]
    light = alpha.QuantumObject("test", 1)
    board = alpha.QuantumWorld([light], compile_to_qubits=compile_to_qubits)
    assert board.peek() == [[1]]
    assert board.peek([light], count=2) == [[1], [1]]
    assert board.peek(["test"], count=2) == [[1], [1]]
    assert board.pop() == [1]


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_two_qubits(simulator, compile_to_qubits):
    light = alpha.QuantumObject("green", Light.GREEN)
    light2 = alpha.QuantumObject("red", Light.RED)
    board = alpha.QuantumWorld(
        [light, light2], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek() == [[Light.GREEN, Light.RED]]
    assert board.peek(convert_to_enum=False) == [[1, 0]]
    assert board.peek([light], count=2) == [[Light.GREEN], [Light.GREEN]]
    assert board.peek([light2], count=2) == [[Light.RED], [Light.RED]]
    assert board.peek(["green"], count=2) == [[Light.GREEN], [Light.GREEN]]
    assert board.peek(["red"], count=2) == [[Light.RED], [Light.RED]]
    assert board.peek(count=3) == [
        [Light.GREEN, Light.RED],
        [Light.GREEN, Light.RED],
        [Light.GREEN, Light.RED],
    ]


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_two_qutrits(compile_to_qubits):
    light = alpha.QuantumObject("yellow", StopLight.YELLOW)
    light2 = alpha.QuantumObject("green", StopLight.GREEN)
    board = alpha.QuantumWorld([light, light2], compile_to_qubits=compile_to_qubits)
    assert board.peek(convert_to_enum=False) == [[1, 2]]
    assert board.peek() == [[StopLight.YELLOW, StopLight.GREEN]]
    assert board.peek([light], count=2) == [[StopLight.YELLOW], [StopLight.YELLOW]]
    assert board.peek([light2], count=2) == [[StopLight.GREEN], [StopLight.GREEN]]
    assert board.peek(count=3) == [
        [StopLight.YELLOW, StopLight.GREEN],
        [StopLight.YELLOW, StopLight.GREEN],
        [StopLight.YELLOW, StopLight.GREEN],
    ]
    if board.compile_to_qubits:
        g0 = cirq.NamedQubit("ancilla_green_0")
        g1 = cirq.NamedQubit("ancilla_green_1")
        y0 = cirq.NamedQubit("ancilla_yellow_0")
        y1 = cirq.NamedQubit("ancilla_yellow_1")
        # Flip the 0 and 2 states from identity for Green.
        g_x02 = cirq.MatrixGate(
            np.array(
                [[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]], dtype=float
            )
        ).on(g0, g1)
        # Flip the 0 and 1 states from identity for Yellow.
        y_x01 = cirq.MatrixGate(
            np.array(
                [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float
            )
        ).on(y0, y1)
        circuit = cirq.Circuit(g_x02, y_x01)
        expected = str(circuit)
    else:
        expected = "green (d=3): ────X(0_2)───\n\nyellow (d=3): ───X(0_1)───"
    assert str(board.circuit) == expected
    assert board.pop() == [StopLight.YELLOW, StopLight.GREEN]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_qubit_and_qutrit(simulator, compile_to_qubits):
    light = alpha.QuantumObject("yellow", Light.GREEN)
    light2 = alpha.QuantumObject("green", StopLight.GREEN)
    board = alpha.QuantumWorld(
        [light, light2], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    assert board.peek(convert_to_enum=False) == [[1, 2]]
    assert board.peek() == [[Light.GREEN, StopLight.GREEN]]
    assert board.peek([light], count=2) == [[Light.GREEN], [Light.GREEN]]
    assert board.peek([light2], count=2) == [[StopLight.GREEN], [StopLight.GREEN]]
    assert board.peek(count=3) == [
        [Light.GREEN, StopLight.GREEN],
        [Light.GREEN, StopLight.GREEN],
        [Light.GREEN, StopLight.GREEN],
    ]
    # Only the qutrit gets compiled to ancillas.
    assert len(board.ancilla_names) == (2 if compile_to_qubits else 0)
    assert board.pop() == [Light.GREEN, StopLight.GREEN]


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_pop(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    board = alpha.QuantumWorld(
        [light, light2, light3],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    alpha.Split()(light, light2, light3)
    results = board.peek([light2, light3], count=200, convert_to_enum=False)
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == 0 for result in results)
    assert not all(result[0] == 1 for result in results)
    popped = board.pop([light2])[0]
    popped2 = board.pop(["l2"])[0]
    assert popped == popped2
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] == popped for result in results)
    assert all(result[1] != popped for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_unhook(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    board = alpha.QuantumWorld(
        [light, light2, light3],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    alpha.Split()(light, light2, light3)
    board.unhook(light2)
    results = board.peek([light2, light3], count=200, convert_to_enum=False)
    print(results)
    assert all(result[0] == 0 for result in results)
    assert not all(result[1] == 0 for result in results)
    assert not all(result[1] == 1 for result in results)


# TODO: Consider moving to qudit_effects.py if this can be broadly useful.
class QuditSwapEffect(alpha.QuantumEffect):
    def __init__(self, dimension):
        self.dimension = dimension

    def effect(self, object1, object2):
        yield qudit_gates.QuditSwapPowGate(self.dimension)(object1.qubit, object2.qubit)


# TODO: Consider moving to qudit_effects.py if this can be broadly useful.
class QuditSplitEffect(alpha.QuantumEffect):
    def __init__(self, dimension):
        self.dimension = dimension

    def effect(self, object1, object2, object3):
        yield qudit_gates.QuditSwapPowGate(self.dimension, 0.5)(
            object1.qubit, object2.qubit
        )
        yield qudit_gates.QuditSwapPowGate(self.dimension, 1)(
            object1.qubit, object3.qubit
        )


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_pop_qudit(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", StopLight.GREEN)
    light2 = alpha.QuantumObject("l2", StopLight.RED)
    light3 = alpha.QuantumObject("l3", StopLight.RED)
    board = alpha.QuantumWorld(
        [light, light2, light3],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    QuditSplitEffect(3)(light, light2, light3)
    results = board.peek([light2, light3], count=200)
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == 0 for result in results)
    assert not all(result[0] == 1 for result in results)
    popped = board.pop([light2])[0]
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] == popped for result in results)
    assert all(result[1] != popped for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_pop_and_reuse(simulator, compile_to_qubits):
    """Tests reusing a popped qubit."""
    light = alpha.QuantumObject("l1", Light.GREEN)
    board = alpha.QuantumWorld(
        [light], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    popped = board.pop([light])[0]
    assert popped == Light.GREEN
    alpha.Flip()(light)
    popped = board.pop([light])[0]
    assert popped == Light.RED


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_pop_and_reuse_qudit(simulator, compile_to_qubits):
    """Tests reusing a popped qudit."""
    light = alpha.QuantumObject("l1", StopLight.GREEN)
    board = alpha.QuantumWorld(
        [light], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    popped = board.pop([light])[0]
    assert popped == StopLight.GREEN
    alpha.QuditFlip(3, StopLight.RED.value, StopLight.GREEN.value)(light)
    popped = board.pop([light])[0]
    assert popped == StopLight.RED


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_undo(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", Light.GREEN)
    board = alpha.QuantumWorld(
        [light], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.Flip()(light)
    results = board.peek([light], count=200)
    assert all(result[0] == Light.RED for result in results)
    board.undo_last_effect()
    results = board.peek([light], count=200)
    assert all(result[0] == Light.GREEN for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_copy(simulator, compile_to_qubits):
    light1 = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    board = alpha.QuantumWorld(
        [light1, light2], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.Flip()(light1)
    alpha.Flip()(light2)
    assert board.pop([light1])[0] == Light.RED
    assert board.pop([light2])[0] == Light.GREEN

    board2 = board.copy()

    # Assert the board and the copy are equivalent
    # (but are two distinct objects)
    assert board.get_object_by_name("l1") is light1
    assert board.get_object_by_name("l2") is light2
    light1_copy = board2.get_object_by_name("l1")
    light2_copy = board2.get_object_by_name("l2")
    assert light1_copy is not light1
    assert light2_copy is not light2
    assert board.peek([light1])[0] == [Light.RED]
    assert board.peek([light2])[0] == [Light.GREEN]
    assert board2.peek([light1])[0] == [Light.RED]
    assert board2.peek([light2])[0] == [Light.GREEN]
    assert board.circuit == board2.circuit
    assert board.circuit is not board2.circuit
    assert board.effect_history == board2.effect_history
    assert board.effect_history is not board2.effect_history
    assert board.ancilla_names == board2.ancilla_names
    assert board.ancilla_names is not board2.ancilla_names
    assert len(board2.post_selection) == 2

    # Assert that they now evolve independently
    board2.undo_last_effect()
    board2.undo_last_effect()
    assert len(board.post_selection) == 2
    assert len(board2.post_selection) == 1
    alpha.Flip()(light1_copy)
    alpha.Flip()(light2_copy)
    assert board.peek([light1])[0] == [Light.RED]
    assert board.peek([light2])[0] == [Light.GREEN]
    assert board2.peek([light1])[0] == [Light.GREEN]
    assert board2.peek([light2])[0] == [Light.RED]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_undo_qudit(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", StopLight.GREEN)
    board = alpha.QuantumWorld(
        [light], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.QuditFlip(3, StopLight.RED.value, StopLight.GREEN.value)(light)
    results = board.peek([light], count=200)
    assert all(result[0] == StopLight.RED for result in results)
    board.undo_last_effect()
    results = board.peek([light], count=200)
    assert all(result[0] == StopLight.GREEN for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_undo_no_effects(compile_to_qubits):
    board = alpha.QuantumWorld([], compile_to_qubits=compile_to_qubits)
    with pytest.raises(IndexError, match="No effects"):
        board.undo_last_effect()


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_undo_post_select(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    board = alpha.QuantumWorld(
        [light, light2, light3],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    alpha.Split()(light, light2, light3)

    # After split, should be fifty-fifty
    results = board.peek([light2, light3], count=200)
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == Light.RED for result in results)
    assert not all(result[0] == Light.GREEN for result in results)

    # After pop, should be consistently one value
    popped = board.pop([light2])[0]
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] == popped for result in results)
    assert all(result[1] != popped for result in results)

    # After undo, should be fifty-fifty
    board.undo_last_effect()
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == Light.RED for result in results)
    assert not all(result[0] == Light.GREEN for result in results)


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_undo_post_select_qudits(simulator, compile_to_qubits):
    light = alpha.QuantumObject("l1", StopLight.GREEN)
    light2 = alpha.QuantumObject("l2", StopLight.RED)
    light3 = alpha.QuantumObject("l3", StopLight.RED)
    board = alpha.QuantumWorld(
        [light, light2, light3],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    QuditSplitEffect(3)(light, light2, light3)

    # After split, should be fifty-fifty
    results = board.peek([light2, light3], count=200)
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == StopLight.RED for result in results)
    assert not all(result[0] == StopLight.GREEN for result in results)

    # After pop, should be consistently one value
    popped = board.pop([light2])[0]
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] == popped for result in results)
    assert all(result[1] != popped for result in results)

    # After undo, should be fifty-fifty
    board.undo_last_effect()
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == StopLight.RED for result in results)
    assert not all(result[0] == StopLight.GREEN for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_pop_not_enough_reps(simulator, compile_to_qubits):
    """Tests forcing a measurement of a rare outcome,
    so that peek needs to be called recursively to get more
    occurances.
    """
    lights = [alpha.QuantumObject("l" + str(i), Light.RED) for i in range(15)]
    board = alpha.QuantumWorld(
        lights, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.Flip()(lights[0])
    alpha.Split()(lights[0], lights[1], lights[2])
    alpha.Split()(lights[2], lights[3], lights[4])
    alpha.Split()(lights[4], lights[5], lights[6])
    alpha.Split()(lights[6], lights[7], lights[8])
    alpha.Split()(lights[8], lights[9], lights[10])
    alpha.Split()(lights[10], lights[11], lights[12])
    alpha.Split()(lights[12], lights[13], lights[14])

    results = board.peek([lights[14]], count=20000)
    assert any(result[0] == Light.GREEN for result in results)
    assert not all(result[0] == Light.GREEN for result in results)
    board.force_measurement(lights[14], Light.GREEN)

    results = board.peek([lights[14]], count=200)
    assert len(results) == 200
    assert all(result[0] == Light.GREEN for result in results)
    results = board.peek(count=200)
    assert all(len(result) == 15 for result in results)
    assert all(result == [Light.RED] * 14 + [Light.GREEN] for result in results)


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_pop_not_enough_reps_qudits(simulator, compile_to_qubits):
    """Tests forcing a measurement of a rare outcome,
    so that peek needs to be called recursively to get more
    occurances.
    """
    lights = [alpha.QuantumObject("l" + str(i), StopLight.RED) for i in range(9)]
    board = alpha.QuantumWorld(
        lights, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.QuditFlip(3, StopLight.RED.value, StopLight.GREEN.value)(lights[0])
    QuditSplitEffect(3)(lights[0], lights[1], lights[2])
    QuditSplitEffect(3)(lights[2], lights[3], lights[4])
    QuditSplitEffect(3)(lights[4], lights[5], lights[6])
    QuditSplitEffect(3)(lights[6], lights[7], lights[8])

    results = board.peek([lights[8]], count=2000)
    assert any(result[0] == StopLight.GREEN for result in results)
    assert not all(result[0] == StopLight.GREEN for result in results)
    board.force_measurement(lights[8], StopLight.GREEN)

    results = board.peek([lights[8]], count=200)
    assert len(results) == 200
    assert all(result[0] == StopLight.GREEN for result in results)
    results = board.peek(count=200)
    assert all(len(result) == 9 for result in results)
    assert all(result == [StopLight.RED] * 8 + [StopLight.GREEN] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_pop_qubits_twice(simulator, compile_to_qubits):
    """Tests popping qubits twice, so that 2 ancillas are created
    for each qubit."""
    lights = [alpha.QuantumObject("l" + str(i), Light.RED) for i in range(3)]
    board = alpha.QuantumWorld(
        lights, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.Flip()(lights[0])
    alpha.Split()(lights[0], lights[1], lights[2])
    result = board.pop()
    green_on_1 = [Light.RED, Light.GREEN, Light.RED]
    green_on_2 = [Light.RED, Light.RED, Light.GREEN]
    assert (result == green_on_1) or (result == green_on_2)
    alpha.Move()(lights[1], lights[2])
    result2 = board.pop()
    peek_results = board.peek(count=200)
    if result == green_on_1:
        assert result2 == green_on_2
    else:
        assert result2 == green_on_1
    assert all(peek_result == result2 for peek_result in peek_results)


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_pop_qudits_twice(simulator, compile_to_qubits):
    """Tests popping qudits twice, so that 2 ancillas are created
    for each qudit."""
    lights = [alpha.QuantumObject("l" + str(i), StopLight.RED) for i in range(3)]
    board = alpha.QuantumWorld(
        lights, sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    alpha.QuditFlip(3, StopLight.RED.value, StopLight.GREEN.value)(lights[0])
    QuditSplitEffect(3)(lights[0], lights[1], lights[2])
    result = board.pop()
    green_on_1 = [StopLight.RED, StopLight.GREEN, StopLight.RED]
    green_on_2 = [StopLight.RED, StopLight.RED, StopLight.GREEN]
    assert (result == green_on_1) or (result == green_on_2)
    QuditSwapEffect(3)(lights[1], lights[2])
    result2 = board.pop()
    peek_results = board.peek(count=200)
    if result == green_on_1:
        assert result2 == green_on_2
    else:
        assert result2 == green_on_1
    assert all(peek_result == result2 for peek_result in peek_results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_combine_overlapping_worlds(compile_to_qubits):
    l1 = alpha.QuantumObject("l1", Light.GREEN)
    world1 = alpha.QuantumWorld([l1], compile_to_qubits=compile_to_qubits)
    l2 = alpha.QuantumObject("l1", StopLight.YELLOW)
    world2 = alpha.QuantumWorld([l2], compile_to_qubits=compile_to_qubits)
    with pytest.raises(ValueError, match="overlapping"):
        world1.combine_with(world2)
    with pytest.raises(ValueError, match="overlapping"):
        world2.combine_with(world1)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_combine_incompatibly_sparse_worlds(compile_to_qubits):
    l1 = alpha.QuantumObject("l1", Light.GREEN)
    world1 = alpha.QuantumWorld(
        [l1], sampler=cirq.Simulator(), compile_to_qubits=compile_to_qubits
    )
    l2 = alpha.QuantumObject("l2", StopLight.YELLOW)
    world2 = alpha.QuantumWorld(
        [l2], sampler=alpha.SparseSimulator(), compile_to_qubits=compile_to_qubits
    )
    with pytest.raises(ValueError, match="sparse"):
        world1.combine_with(world2)
    with pytest.raises(ValueError, match="sparse"):
        world2.combine_with(world1)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_combine_worlds(compile_to_qubits):
    l1 = alpha.QuantumObject("l1", Light.GREEN)
    l2 = alpha.QuantumObject("l2", Light.RED)
    l3 = alpha.QuantumObject("l3", Light.RED)
    world1 = alpha.QuantumWorld([l1, l2, l3], compile_to_qubits=compile_to_qubits)

    # Split and pop to test post-selection after combining
    alpha.Split()(l1, l2, l3)
    result = world1.pop()

    l4 = alpha.QuantumObject("stop_light", StopLight.YELLOW)
    world2 = alpha.QuantumWorld([l4], compile_to_qubits=compile_to_qubits)
    world2.combine_with(world1)

    results = world2.peek(count=100)
    expected = [StopLight.YELLOW] + result
    print(results)
    print(expected)
    assert all(actual == expected for actual in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize("simulator", [cirq.Simulator, alpha.SparseSimulator])
def test_get_histogram_and_get_probabilities_one_binary_qobject(
    simulator, compile_to_qubits
):
    l1 = alpha.QuantumObject("l1", Light.GREEN)
    world = alpha.QuantumWorld(
        [l1], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    histogram = world.get_histogram()
    assert histogram == [{0: 0, 1: 100}]
    histogram = world.get_correlated_histogram()
    assert histogram == {(1,): 100}
    probs = world.get_probabilities()
    assert probs == [{0: 0.0, 1: 1.0}]
    bin_probs = world.get_binary_probabilities()
    assert bin_probs == [1.0]
    alpha.Flip()(l1)
    histogram = world.get_histogram()
    assert histogram == [{0: 100, 1: 0}]
    histogram = world.get_correlated_histogram()
    assert histogram == {(0,): 100}
    probs = world.get_probabilities()
    assert probs == [{0: 1.0, 1: 0.0}]
    bin_probs = world.get_binary_probabilities()
    assert bin_probs == [0.0]
    alpha.Superposition()(l1)
    histogram = world.get_histogram()
    assert len(histogram) == 1
    assert len(histogram[0]) == 2
    assert histogram[0][0] > 10
    assert histogram[0][1] > 10
    histogram = world.get_correlated_histogram()
    assert len(histogram) == 2
    assert histogram[(0,)] > 10
    assert histogram[(1,)] > 10
    probs = world.get_probabilities()
    assert len(probs) == 1
    assert len(probs[0]) == 2
    assert probs[0][0] > 0.1
    assert probs[0][1] > 0.1
    bin_probs = world.get_binary_probabilities()
    assert 0.1 <= bin_probs[0] <= 1.0


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_get_histogram_and_get_probabilities_one_trinary_qobject(
    simulator, compile_to_qubits
):
    l1 = alpha.QuantumObject("l1", StopLight.YELLOW)
    world = alpha.QuantumWorld(
        [l1], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    histogram = world.get_histogram()
    assert histogram == [{0: 0, 1: 100, 2: 0}]
    histogram = world.get_correlated_histogram()
    assert histogram == {(1,): 100}
    probs = world.get_probabilities()
    assert probs == [{0: 0.0, 1: 1.0, 2: 0.0}]
    bin_probs = world.get_binary_probabilities()
    assert bin_probs == [1.0]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_get_histogram_and_get_probabilities_two_qobjects(simulator, compile_to_qubits):
    l1 = alpha.QuantumObject("l1", Light.GREEN)
    l2 = alpha.QuantumObject("l2", StopLight.YELLOW)
    world = alpha.QuantumWorld(
        [l1, l2], sampler=simulator(), compile_to_qubits=compile_to_qubits
    )
    histogram = world.get_histogram()
    assert histogram == [{0: 0, 1: 100}, {0: 0, 1: 100, 2: 0}]
    histogram = world.get_correlated_histogram()
    assert histogram == {(1, 1): 100}
    probs = world.get_probabilities()
    assert probs == [{0: 0.0, 1: 1.0}, {0: 0.0, 1: 1.0, 2: 0.0}]
    bin_probs = world.get_binary_probabilities()
    assert bin_probs == [1.0, 1.0]
    histogram = world.get_histogram(objects=[l2], count=1000)
    assert histogram == [{0: 0, 1: 1000, 2: 0}]
    histogram = world.get_correlated_histogram(objects=[l2], count=1000)
    assert histogram == {(1,): 1000}
    probs = world.get_probabilities(objects=[l2], count=1000)
    assert probs == [{0: 0.0, 1: 1.0, 2: 0.0}]
    bin_probs = world.get_binary_probabilities(objects=[l2], count=1000)
    assert bin_probs == [1.0]


@pytest.mark.parametrize(
    ("simulator", "compile_to_qubits"),
    [
        (cirq.Simulator, False),
        (cirq.Simulator, True),
        # Cannot use SparseSimulator without `compile_to_qubits` due to issue #78.
        (alpha.SparseSimulator, True),
    ],
)
def test_get_correlated_histogram_with_entangled_qobjects(simulator, compile_to_qubits):
    light1 = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    light4 = alpha.QuantumObject("l4", Light.GREEN)
    light5 = alpha.QuantumObject("l5", Light.RED)

    world = alpha.QuantumWorld(
        [light1, light2, light3, light4, light5],
        sampler=simulator(),
        compile_to_qubits=compile_to_qubits,
    )
    alpha.Split()(light1, light2, light3)
    alpha.quantum_if(light2).equals(1).apply(alpha.Move())(light4, light5)

    # histogram = world.get_histogram()
    # assert histogram == [{0: 0, 1: 100}, {0: 0, 1: 100, 2: 0}]
    histogram = world.get_correlated_histogram()
    assert histogram.keys() == [(0, 0, 1, 1, 0), (0, 1, 0, 0, 1)]
