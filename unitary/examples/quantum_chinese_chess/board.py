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
    Type,
    Language,
)
from unitary.examples.quantum_chinese_chess.piece import Piece

class Board:
    def __init__(self):
        self.load_fen()
        self.king_locations = {"e0", "e9"}
        self.current_state = GameState.CONTINUE

    def load_fen(
        self, fen: str = "RHEAKAEHR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rheakaehr"
    ):
        chess_board = {}
        row_index = 9
        for row in fen.split("/"):
            col = ord("a")
            for char in row:
                # Add empty board pieces.
                if "1" <= char <= "9":
                    for i in range(int(char)):
                        name = chr(col) + "%i" % row_index
                        chess_board[name] = Piece(
                            name, SquareState.EMPTY, Type.EMPTY, Color.NA
                        )
                        col += 1
                # Add occupied board pieces.
                else:
                    name = chr(col) + "%i" % row_index
                    piece_type = Type.type_of(char)
                    color = Color.RED if char.isupper() else Color.BLACK
                    chess_board[name] = Piece(
                        name, SquareState.OCCUPIED, piece_type, color
                    )
                    col += 1
            row_index -= 1
        self.board = alpha.QuantumWorld(chess_board.values())

    def print(self, lang: Language = Language.EN):
        num_rows = 10
        board_string = ""
        board_string += " "
        # Print the top line of col letters.
        for col in "abcdefghi":
            board_string += " %c" % col
        board_string += "\n"
        for row in range(num_rows):
            # Print the row index on the left.
            board_string += "%d " % row
            for col in "abcdefghi":
                piece = self.board[col + "%d" % row]
                board_string += piece.symbol(True, lang)
                if lang == Language.EN or piece.type_ == Type.EMPTY:
                    board_string += " "
            # Print the row index on the right.
            board_string += " %d\n" % row
        board_string += " "
        # Print the bottom line of col letters.
        for col in "abcdefghi":
            board_string += " %c" % col
        print(board_string)

    def flying_general(self) -> bool:
        print("### flying general rule check to be implemented")
        return False


board = Board()
board.print()

board.print(Language.ZH)
