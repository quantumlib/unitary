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
from unitary.alpha import QuantumObject
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    Language,
    Color,
    Type,
)


class Piece:
    def __init__(self, type_: Type, color: Color):
        self.type_ = type_
        self.color = color
        self.is_entangled = False

    def symbol(self, lang: Language = Language.EN) -> str:
        return Type.symbol(self.type_, self.color, lang)

    def __str__(self):
        return self.symbol()

    def clear(self):
        self.type_ = Type.EMPTY
        self.color = Color.NA
        self.is_entangled = False


class QuantumPiece(Piece, QuantumObject):
    def __init__(self, name: str, state: SquareState, type_: Type, color: Color):
        QuantumObject.__init__(self, name, state)
        Piece.__init__(self, name, state, type_, color)
