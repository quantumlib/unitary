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


class Piece(QuantumObject):
    def __init__(self, name: str, state: SquareState, type_: Type, color: Color):
        QuantumObject.__init__(self, name, state)
        self.type_ = type_
        self.color = color

    def symbol(self, lang: Language = Language.EN) -> str:
        if self.type_ == Type.EMPTY:
            return "."
        if lang == Language.EN:  # Return English symbols
            if self.color == Color.RED:
                return self.type_.value[0]
            elif self.color == Color.BLACK:
                return self.type_.value[1]
        elif lang == Language.ZH:  # Return Chinese symbols
            if self.color == Color.RED:
                return self.type_.value[2]
            elif self.color == Color.BLACK:
                return self.type_.value[3]
        return "Unexpected combinations"

    def __str__(self):
        return self.symbol()
