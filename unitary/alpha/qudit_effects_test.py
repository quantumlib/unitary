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


class StopLight(enum.Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_qudit_cycle(compile_to_qubits):
    board = alpha.QuantumWorld(compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", StopLight.GREEN)
    board.add_object(piece)
    alpha.QuditCycle(3)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.RED] for result in results)
    alpha.QuditCycle(3)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.YELLOW] for result in results)
    alpha.QuditCycle(3)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.GREEN] for result in results)
    alpha.QuditCycle(3, num=2)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.YELLOW] for result in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_qudit_flip(compile_to_qubits):
    board = alpha.QuantumWorld(compile_to_qubits=compile_to_qubits)
    piece = alpha.QuantumObject("t", StopLight.GREEN)
    board.add_object(piece)
    alpha.QuditFlip(3, 0, 2)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.RED] for result in results)
    alpha.QuditFlip(3, 0, 2)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.GREEN] for result in results)
    alpha.QuditFlip(3, 0, 1)(piece)
    results = board.peek([piece], count=100)
    assert all(result == [StopLight.GREEN] for result in results)
