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
from typing import Optional
from unitary.alpha import QuantumObject
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    Language,
    Color,
    Type,
)


class Piece(QuantumObject):
    """Each Piece stands for a position in the board, it could hold different types/colors
    of chess pieces either in quantum state or classical state. It could also be classically
    EMPTY.
    """

    def __init__(self, name: str, state: SquareState, type_: Type, color: Color):
        QuantumObject.__init__(self, name, state)
        self.type_ = type_
        self.color = color
        # TODO(): maybe modify QuantumObject to allow it to:
        # - not create qubit at initialization;
        # - add qubit and set it to the current classical state when needed.
        self.is_entangled = False

    def symbol(self, lang: Language = Language.EN) -> str:
        """Returns the symbol of this piece according to its type, color and language."""
        return Type.symbol(self.type_, self.color, lang)

    def __str__(self):
        return self.symbol()

    def reset(self, piece: "Piece" = None) -> None:
        """Modifies the classical attributes of the piece.
        If `piece` is provided, then its type_, color, and is_entangled is copied,
        otherwise set the current piece to be a classically empty piece.
        """
        if piece is not None:
            self.type_ = piece.type_
            self.color = piece.color
            self.is_entangled = piece.is_entangled
        else:
            self.type_ = Type.EMPTY
            self.color = Color.NA
            self.is_entangled = False
