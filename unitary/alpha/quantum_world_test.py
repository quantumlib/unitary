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
import enum
import pytest

import unitary.alpha as alpha


class Light(enum.Enum):
    RED = 0
    GREEN = 1


class StopLight(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


def test_duplicate_objects():
    light = alpha.QuantumObject("test", Light.GREEN)
    board = alpha.QuantumWorld([light])
    with pytest.raises(ValueError, match="already added"):
        board.add_object(alpha.QuantumObject("test", Light.RED))


def test_one_qubit():
    light = alpha.QuantumObject("test", Light.GREEN)
    board = alpha.QuantumWorld([light])
    assert board.peek() == [[Light.GREEN]]
    assert board.peek([light], count=2) == [[Light.GREEN], [Light.GREEN]]
    light = alpha.QuantumObject("test", 1)
    board = alpha.QuantumWorld([light])
    assert board.peek() == [[1]]
    assert board.peek([light], count=2) == [[1], [1]]
    assert board.pop() == [1]


def test_two_qubits():
    light = alpha.QuantumObject("green", Light.GREEN)
    light2 = alpha.QuantumObject("red", Light.RED)
    board = alpha.QuantumWorld([light, light2])
    assert board.peek() == [[Light.GREEN, Light.RED]]
    assert board.peek(convert_to_enum=False) == [[1, 0]]
    assert board.peek([light], count=2) == [[Light.GREEN], [Light.GREEN]]
    assert board.peek([light2], count=2) == [[Light.RED], [Light.RED]]
    assert board.peek(count=3) == [
        [Light.GREEN, Light.RED],
        [Light.GREEN, Light.RED],
        [Light.GREEN, Light.RED],
    ]


def test_two_qutrits():
    light = alpha.QuantumObject("yellow", StopLight.YELLOW)
    light2 = alpha.QuantumObject("green", StopLight.GREEN)
    board = alpha.QuantumWorld([light, light2])
    assert board.peek(convert_to_enum=False) == [[1, 2]]
    assert board.peek() == [[StopLight.YELLOW, StopLight.GREEN]]
    assert board.peek([light], count=2) == [[StopLight.YELLOW], [StopLight.YELLOW]]
    assert board.peek([light2], count=2) == [[StopLight.GREEN], [StopLight.GREEN]]
    assert board.peek(count=3) == [
        [StopLight.YELLOW, StopLight.GREEN],
        [StopLight.YELLOW, StopLight.GREEN],
        [StopLight.YELLOW, StopLight.GREEN],
    ]
    expected = "green (d=3): ────X(0_2)───\n\nyellow (d=3): ───X(0_1)───"
    assert str(board.circuit) == expected


def test_pop():
    light = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    board = alpha.QuantumWorld([light, light2, light3])
    alpha.Split()(light, light2, light3)
    results = board.peek([light2, light3], count=200)
    assert all(result[0] != result[1] for result in results)
    assert not all(result[0] == 0 for result in results)
    assert not all(result[0] == 1 for result in results)
    popped = board.pop([light2])[0]
    results = board.peek([light2, light3], count=200)
    assert len(results) == 200
    assert all(result[0] == popped for result in results)
    assert all(result[1] != popped for result in results)


def test_pop_and_reuse():
    """Tests reusing a popped qubit."""
    light = alpha.QuantumObject("l1", Light.GREEN)
    board = alpha.QuantumWorld([light])
    popped = board.pop([light])[0]
    assert popped == Light.GREEN
    alpha.Flip()(light)
    popped = board.pop([light])[0]
    assert popped == Light.RED


def test_undo():
    light = alpha.QuantumObject("l1", Light.GREEN)
    board = alpha.QuantumWorld([light])
    alpha.Flip()(light)
    results = board.peek([light], count=200)
    assert all(result[0] == Light.RED for result in results)
    board.undo_last_effect()
    results = board.peek([light], count=200)
    assert all(result[0] == Light.GREEN for result in results)


def test_undo_post_select():
    light = alpha.QuantumObject("l1", Light.GREEN)
    light2 = alpha.QuantumObject("l2", Light.RED)
    light3 = alpha.QuantumObject("l3", Light.RED)
    board = alpha.QuantumWorld([light, light2, light3])
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


def test_pop_not_enough_reps():
    """Tests forcing a measurement of a rare outcome,
    so that peek needs to be called recursively to get more
    occurances.
    """
    lights = [alpha.QuantumObject("l" + str(i), Light.RED) for i in range(15)]
    board = alpha.QuantumWorld(lights)
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


def test_pop_qubits_twice():
    """Tests popping qubits twice, so that 2 ancillas are created
    for each qubit."""
    lights = [alpha.QuantumObject("l" + str(i), Light.RED) for i in range(3)]
    board = alpha.QuantumWorld(lights)
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
