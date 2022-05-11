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

import cirq

import unitary.alpha as alpha


def test_negation():
    piece = alpha.QuantumObject("t", 0)
    board = alpha.QuantumWorld(piece)
    assert board.peek() == [[0]]
    -piece
    assert board.peek() == [[1]]
    -piece
    assert board.peek() == [[0]]
    piece += 1
    assert board.peek() == [[1]]


def test_add_board_after_state_change():
    piece = alpha.QuantumObject("t", 0)
    piece += 1
    board = alpha.QuantumWorld(piece)
    assert board.peek() == [[1]]


def test_qutrit():
    piece = alpha.QuantumObject("t", 2)
    board = alpha.QuantumWorld(piece)
    assert board.peek() == [[2]]
    piece += 1
    assert board.peek() == [[0]]
    piece += 1
    assert board.peek() == [[1]]
    piece += 1
    assert board.peek() == [[2]]
    piece += 1
    assert board.peek() == [[0]]
    piece += 2
    assert board.peek() == [[2]]


def test_enum():
    class Color(enum.Enum):
        RED = 0
        YELLOW = 1
        GREEN = 2

    piece = alpha.QuantumObject("t", Color.YELLOW)
    board = alpha.QuantumWorld(piece)
    assert board.peek() == [[Color.YELLOW]]
    piece += Color.YELLOW
    assert board.peek() == [[Color.GREEN]]
    piece += Color.GREEN
    assert board.peek() == [[Color.YELLOW]]


def test_bag_args():
    with pytest.raises(ValueError, match="Unsupported initial state"):
        _ = alpha.QuantumObject("test", "bad arg")
    piece = alpha.QuantumObject("t", 0)
    with pytest.raises(TypeError, match="unsupported operand"):
        piece += "bad stuff"
