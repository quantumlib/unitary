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

import unitary.alpha as alpha


class Light(enum.Enum):
    RED = 0
    GREEN = 1


class StopLight(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


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
    expected = "green (d=3): ────[+2]───\n\nyellow (d=3): ───[+1]───"
    assert str(board.circuit) == expected
