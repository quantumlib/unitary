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
from unitary.examples.quantum_chinese_chess.enums import Piece, Language

def test_piece_type_of():
    assert Piece.type_of('s') == Piece.Type.SOLDIER
    assert Piece.type_of('S') == Piece.Type.SOLDIER
    assert Piece.type_of('g') == Piece.Type.GENERAL
    assert Piece.type_of('G') == Piece.Type.GENERAL
    assert Piece.type_of('.') == Piece.Type.EMPTY
    assert Piece.type_of('b') == None


def test_piece_symbol():
    p0 = Piece(Piece.Type.CANNON, Piece.Color.RED)
    assert p0.red_symbol() == 'C'
    assert p0.black_symbol() == 'c'
    assert p0.symbol() == 'C'
    assert p0.red_symbol(Language.ZH) == '炮'
    assert p0.black_symbol(Language.ZH) == '砲'
    assert p0.symbol(Language.ZH) == '炮'

    p1 = Piece(Piece.Type.HORSE, Piece.Color.BLACK)
    assert p1.red_symbol() == 'H'
    assert p1.black_symbol() == 'h'
    assert p1.symbol() == 'h'
    assert p1.red_symbol(Language.ZH) == '马'
    assert p1.black_symbol(Language.ZH) == '馬'
    assert p1.symbol(Language.ZH) == '馬'

    p2 = Piece(Piece.Type.EMPTY, Piece.Color.NA)
    assert p2.red_symbol() == '.'
    assert p2.black_symbol() == '.'
    assert p2.symbol() == '.'
    assert p2.red_symbol(Language.ZH) == '.'
    assert p2.black_symbol(Language.ZH) == '.'
    assert p2.symbol(Language.ZH) == '.'
