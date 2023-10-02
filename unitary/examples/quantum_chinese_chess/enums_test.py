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
from unitary.examples.quantum_chinese_chess.enums import Type, Color, Language


def test_type_of():
    assert Type.type_of("p") == Type.PAWN
    assert Type.type_of("P") == Type.PAWN
    assert Type.type_of("k") == Type.KING
    assert Type.type_of("K") == Type.KING
    assert Type.type_of(".") == Type.EMPTY
    assert Type.type_of("b") == None


def test_symbol():
    assert Type.symbol(Type.CANNON, Color.RED) == "C"
    assert Type.symbol(Type.CANNON, Color.BLACK) == "c"
    assert Type.symbol(Type.CANNON, Color.RED, Language.ZH) == "炮"
    assert Type.symbol(Type.CANNON, Color.BLACK, Language.ZH) == "砲"

    assert Type.symbol(Type.HORSE, Color.RED) == "H"
    assert Type.symbol(Type.HORSE, Color.BLACK) == "h"
    assert Type.symbol(Type.HORSE, Color.RED, Language.ZH) == "马"
    assert Type.symbol(Type.HORSE, Color.BLACK, Language.ZH) == "馬"

    assert Type.symbol(Type.EMPTY, Color.RED) == "."
    assert Type.symbol(Type.EMPTY, Color.BLACK) == "."
    assert Type.symbol(Type.EMPTY, Color.RED, Language.ZH) == "."
    assert Type.symbol(Type.EMPTY, Color.BLACK, Language.ZH) == "."
