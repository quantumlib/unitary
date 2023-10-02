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
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    Language,
    Color,
    Type,
)
from unitary.examples.quantum_chinese_chess.piece import Piece
from unitary.alpha import QuantumWorld


def test_symbol():
    p0 = Piece("a0", SquareState.OCCUPIED, Type.CANNON, Color.RED)
    assert p0.symbol() == "c"
    assert p0.__str__() == "c"
    assert p0.symbol(Language.ZH) == "炮"

    p1 = Piece("b1", SquareState.OCCUPIED, Type.HORSE, Color.BLACK)
    assert p1.symbol() == "H"
    assert p1.__str__() == "H"
    assert p1.symbol(Language.ZH) == "馬"

    p2 = Piece("c2", SquareState.EMPTY, Type.EMPTY, Color.NA)
    assert p2.symbol() == "."
    assert p2.__str__() == "."
    assert p2.symbol(Language.ZH) == "."


def test_enum():
    p0 = Piece("a0", SquareState.OCCUPIED, Type.CANNON, Color.RED)
    p1 = Piece("b1", SquareState.OCCUPIED, Type.HORSE, Color.BLACK)
    p2 = Piece("c2", SquareState.EMPTY, Type.EMPTY, Color.NA)
    board = QuantumWorld([p0, p1, p2])
    assert board.peek() == [
        [SquareState.OCCUPIED, SquareState.OCCUPIED, SquareState.EMPTY]
    ]
