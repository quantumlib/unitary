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
import numpy as np
from typing import List, Tuple
import unitary.alpha as alpha
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    Color,
    Type,
    Language,
)
from unitary.examples.quantum_chinese_chess.piece import Piece


# The default initial state of the game.
_INITIAL_FEN = "RHEAKAEHR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rheakaehr w---1"


class Board:
    """Board holds the assemble of all pieces. Each piece could be either in classical or quantum state."""

    def __init__(
        self, board: alpha.QuantumWorld, current_player: int, king_locations: List[str]
    ):
        self.board = board
        self.current_player = current_player
        # This saves the locations of KINGs in the order of [RED_KING_LOCATION, BLACK_KING_LOCATION].
        self.king_locations = king_locations
        self.lang = Language.EN  # The default language is English.

    def set_language(self, lang: Language):
        self.lang = lang

    @classmethod
    def from_fen(cls, fen: str = _INITIAL_FEN) -> "Board":
        """
        Translates FEN (Forsyth-Edwards Notation) symbols into the whole QuantumWorld board.
        FEN rule for Chinese Chess could be found at https://www.wxf-xiangqi.org/images/computer-xiangqi/fen-for-xiangqi-chinese-chess.pdf
        """
        chess_board = {}
        row_index = 9
        king_locations = []
        pieces, turns = fen.split(" ", 1)
        for row in pieces.split("/"):
            col = ord("a")
            for char in row:
                # Add empty board pieces.
                if "1" <= char <= "9":
                    for i in range(int(char)):
                        name = f"{chr(col)}{row_index}"
                        chess_board[name] = Piece(
                            name, SquareState.EMPTY, Type.EMPTY, Color.NA
                        )
                        col += 1
                # Add occupied board pieces.
                else:
                    name = f"{chr(col)}{row_index}"
                    piece_type = Type.type_of(char)
                    if piece_type == Type.KING:
                        king_locations.append(name)
                    color = Color.RED if char.isupper() else Color.BLACK
                    chess_board[name] = Piece(
                        name, SquareState.OCCUPIED, piece_type, color
                    )
                    col += 1
            row_index -= 1
        board = alpha.QuantumWorld(chess_board.values())
        # Here 0 means the player RED while 1 the player BLACK.
        current_player = 0 if "w" in turns else 1
        # TODO(): maybe add check to make sure the input fen itself is correct.
        if len(king_locations) != 2:
            raise ValueError(
                f"We expect two KINGs on the board, but got {len(king_locations)}."
            )
        return cls(board, current_player, king_locations)

    def __str__(self):
        num_rows = 10
        board_string = ["\n "]
        # Print the top line of col letters.
        for col in "abcdefghi":
            board_string.append(f" {col}")
        board_string.append("\n")
        for row in range(num_rows):
            # Print the row index on the left.
            board_string.append(f"{row} ")
            for col in "abcdefghi":
                piece = self.board[f"{col}{row}"]
                board_string += piece.symbol(self.lang)
                if self.lang == Language.EN:
                    board_string.append(" ")
            # Print the row index on the right.
            board_string.append(f" {row}\n")
        board_string.append(" ")
        # Print the bottom line of col letters.
        for col in "abcdefghi":
            board_string.append(f" {col}")
        board_string.append("\n")
        if self.lang == Language.EN:
            return "".join(board_string)
        # We need to turn letters into their full-width counterparts to align
        # a mix of letters + Chinese characters.
        chars = "".join(chr(c) for c in range(ord(" "), ord("z")))
        full_width_chars = "\N{IDEOGRAPHIC SPACE}" + "".join(
            chr(c)
            for c in range(
                ord("\N{FULLWIDTH EXCLAMATION MARK}"),
                ord("\N{FULLWIDTH LATIN SMALL LETTER Z}"),
            )
        )
        translation = str.maketrans(chars, full_width_chars)
        return (
            "".join(board_string)
            .replace(" ", "")
            .replace("abcdefghi", " abcdefghi")
            .translate(translation)
        )

    def path_pieces(self, source: str, target: str) -> Tuple[List[str], List[str]]:
        """Returns the nonempty classical and quantum pieces from source to target."""
        x0 = ord(source[0])
        x1 = ord(target[0])
        dx = x1 - x0
        y0 = int(source[1])
        y1 = int(target[1])
        dy = y1 - y0
        # In case of only moving one step, return empty path pieces.
        if abs(dx) + abs(dy) <= 1:
            return [], []
        # In case of advisor moving, return empty path pieces.
        # TODO(): maybe move this to the advisor move check.
        if abs(dx) == 1 and abs(dy) == 1:
            return [], []
        pieces = []
        classical_pieces = []
        quantum_pieces = []
        dx_sign = np.sign(dx)
        dy_sign = np.sign(dy)
        # In case of elephant move, there should only be one path piece.
        if abs(dx) == abs(dy):
            pieces.append(f"{chr(x0 + dx_sign)}{y0 + dy_sign}")
        elif dx == 0:
            for i in range(1, abs(dy)):
                pieces.append(f"{chr(x0)}{y0 + dy_sign * i}")
        elif dy == 0:
            for i in range(1, abs(dx)):
                pieces.append(f"{chr(x0 + dx_sign * i)}{y0}")
        # This covers four possible directions of horse move.
        elif abs(dx) == 2 and abs(dy) == 1:
            pieces.append(f"{chr(x0 + dx_sign)}{y0}")
        # This covers the other four possible directions of horse move.
        elif abs(dy) == 2 and abs(dx) == 1:
            pieces.append(f"{chr(x0)}{y0 + dy_sign}")
        else:
            raise ValueError("Unexpected input to path_pieces().")
        for piece in pieces:
            if self.board[piece].is_entangled:
                quantum_pieces.append(piece)
            elif self.board[piece].type_ != Type.EMPTY:
                classical_pieces.append(piece)
        return classical_pieces, quantum_pieces

    def flying_general_check(self) -> bool:
        """Check and return if the two KINGs are directly facing each other (i.e. in the same column) without any pieces in between."""
        king_0 = self.king_locations[0]
        king_1 = self.king_locations[1]
        if king_0[0] != king_1[0]:
            # If they are in different columns, the check fails. Game continues.
            return False
        classical_pieces, quantum_pieces = self.path_pieces(king_0, king_1)
        if len(classical_pieces) > 0:
            # If there are classical pieces between two KINGs, the check fails. Game continues.
            return False
        if len(quantum_pieces) == 0:
            # If there are no pieces between two KINGs, the check successes. Game ends.
            return True
        # TODO(): add check when there are quantum pieces in between.
