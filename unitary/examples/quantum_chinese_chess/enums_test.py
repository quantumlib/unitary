# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unitary.examples.quantum_chinese_chess.enums import Piece

def test_piece():
    assert Piece.type_of('s') == Piece.SOLDIER
    assert Piece.type_of('S') == Piece.SOLDIER
    assert Piece.type_of('g') == Piece.GENERAL
    assert Piece.type_of('G') == Piece.GENERAL
    assert Piece.type_of('.') == Piece.EMPTY
    assert Piece.type_of('b') == None

    assert Piece.CANNON.red_symbol() == 'C'
    assert Piece.CANNON.black_symbol() == 'c'
    assert Piece.HORSE.red_symbol() == 'H'
    assert Piece.HORSE.black_symbol() == 'h'

    assert Piece.type_of('r').red_symbol() == 'R'
    assert Piece.type_of('a').red_symbol() == 'A'

    assert Piece.type_of(Piece.ELEPHANT.red_symbol()) == Piece.ELEPHANT
    assert Piece.type_of(Piece.ELEPHANT.black_symbol()) == Piece.ELEPHANT
