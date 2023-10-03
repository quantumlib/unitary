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
import unitary.alpha as alpha
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    GameState,
    Color,
    Type
)
from unitary.examples.quantum_chinese_chess.piece import Piece


class Board:
    def __init__(self):
        self.load_fen("RHEAKAEHR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rheagaehr")
        self.king_locations = {"e0", "e9"}
        self.current_state = GameState.CONTINUE

    def load_fen(self):
        chess_board = {}
        row_index = 9
        for row in fen.split("/"):
            col = ord('a')
            for char in row:
                if "1" <= char <= "9":
                    for i in range(int(char)):
                        col += 1
                    name = chr(col) + "%i" % row_index
                    chess_board[name] = Piece(name, SquareState.EMPTY, Type.EMPTY, Color.NA)
                else:
                    name = chr(col) + "%i" % row_index
                    piece_type = Type.type_of(char)
                    color = Color.RED if char.isupper() else Color.BLACK
                    chess_board[name] = Piece(name, SquareState.OCCUPIED, piece_type, color)
                    col += 1
            row_index -= 1
        self.board = alpha.QuantumWorld(chess_board.values())

    def print(self):
        print("### board print to be implemented")

    def flying_general(self) -> bool:
        print("### flying general rule check to be implemented")
        return False
