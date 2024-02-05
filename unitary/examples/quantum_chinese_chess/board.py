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
    MoveVariant,
    TerminalType,
)
from unitary.examples.quantum_chinese_chess.piece import Piece
from unitary.examples.quantum_chinese_chess.move import Jump


# The default initial state of the game.
_INITIAL_FEN = "RHEAKAEHR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rheakaehr w---1"

# Constants for printing board
_RESET = "\033[0m"
_BOLD = "\033[01m"
# background
_BG_GREY = "\033[47m"
# foreground
_FG_BLACK = "\033[30m"
_FG_RED = "\033[31m"
_FG_LIGHT_RED = "\033[91m"
_FG_LIGHT_GREY = "\033[37m"
# full width chars
_FULL_SPACE = "\N{IDEOGRAPHIC SPACE}"
_FULL_A = ord("\N{FULLWIDTH LATIN SMALL LETTER A}")


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

    def set_language(self, lang: Language) -> None:
        self.lang = lang

    @classmethod
    def from_fen(cls, fen: str = _INITIAL_FEN) -> "Board":
        """
        Translates FEN (Forsyth-Edwards Notation) symbols into the whole QuantumWorld board.
        FEN rule for Chinese Chess could be found at https://www.wxf-xiangqi.org/images/computer-xiangqi/fen-for-xiangqi-chinese-chess.pdf
        """
        chess_board = {}
        row_index = 0
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
            row_index += 1
        board = alpha.QuantumWorld(chess_board.values())
        # Here 0 means the player RED while 1 the player BLACK.
        current_player = 0 if "w" in turns else 1
        # TODO(): maybe add check to make sure the input fen itself is correct.
        return cls(board, current_player, king_locations)

    # TODO(): print players' names in their corresponding side of the board.
    # TODO(): check if there is better way to automatic determine the current terminal
    # type, e.g. colab / sublime terminus vs glinux / mac terminal.
    # TODO(): right now all possibilities are printed in black, maybe update to print
    # in the same color as the corresponding pieces.
    # TODO(): in some scenarios the black entangled pieces seems too light/weak to see.
    def to_str(
        self,
        terminal: TerminalType,
        probabilities: List[float] = None,
        peek_result: List[int] = None,
    ) -> str:
        """
        Print the board into string.

        Args:
            terminal: type of the terminal that the game is currently running on;
            probabilities: the probabilities of each piece of the board, in length of 90;
            peek_result: for one peek of the board, provide a list of ints with length 90,
                         with int=1 indicating the piece is there (for this peek);
        """

        def add_piece_symbol(
            board_string: str,
            piece: Piece,
            peek_result: List[int],
            index: int,
            terminal: TerminalType,
        ):
            if peek_result is None and piece.is_entangled:
                if piece.color == Color.RED:
                    board_string += _FG_LIGHT_RED
                else:
                    # bold works on mac terminal and gLinux terminal,
                    # but not on sublime terminus
                    if terminal != TerminalType.COLAB_OR_SUBLIME_TERMINUS:
                        board_string += _BOLD
                    board_string += _FG_LIGHT_GREY
            else:
                if terminal != TerminalType.COLAB_OR_SUBLIME_TERMINUS:
                    board_string += _BOLD
                if piece.color == Color.RED:
                    board_string += _FG_RED
            if (
                peek_result is None
                or piece.type_ == Type.EMPTY
                or peek_result[index] == 1
            ):
                board_string += piece.symbol(self.lang)
            # If an entangled piece is peeked to be empty, we print empty.
            elif piece.is_entangled and peek_result[index] == 0:
                board_string += Type.symbol(Type.EMPTY, Color.NA, self.lang)
            board_string += _RESET

        num_rows = 10

        if self.lang == Language.EN:
            board_string = ["\n   "]
            # Print the top line of col letters.
            board_string += _BG_GREY
            board_string += _FG_BLACK
            for col in "abcdefghi":
                board_string.append(f" {col}  ")
            board_string += "\b" + _RESET + " \n"
            index = 0
            for row in range(num_rows):
                # Print the row index on the left.
                board_string.append(f"{row}   ")
                # Print each piece of this row, including empty piece.
                for col in "abcdefghi":
                    piece = self.board[f"{col}{row}"]
                    add_piece_symbol(board_string, piece, peek_result, index, terminal)
                    if col != "i":
                        board_string.append("   ")
                    board_string += _RESET
                    index += 1
                # Print the row index on the right.
                board_string += f"  {row}" + _RESET + "\n"
                # Print the sampled prob. of the pieces in the above row.
                if probabilities is not None:
                    board_string += "   "
                    board_string += _BG_GREY
                    board_string += _FG_BLACK
                    for i in range(row * 9, (row + 1) * 9):
                        # We only print non-zero probabilities
                        if probabilities[i] >= 1e-3:
                            board_string.append("{:.1f} ".format(probabilities[i]))
                        else:
                            board_string.append("    ")
                    board_string += "\b" + _RESET + " \n"
            board_string.append("   ")
            # Print the bottom line of col letters.
            board_string += _BG_GREY
            board_string += _FG_BLACK
            for col in "abcdefghi":
                board_string.append(f" {col}  ")
            board_string += "\b" + _RESET + " \n"
            return "".join(board_string)
        else:  # Print Chinese + full width characters
            board_string = ["\n" + _FULL_SPACE + " "]
            # Print the top line of col letters.
            board_string += _BG_GREY
            board_string += _FG_BLACK
            for col in range(_FULL_A, _FULL_A + 9):
                board_string.append(f"{chr(col)}")
                if col != _FULL_A + 8:
                    board_string += _FULL_SPACE * 2
            board_string += " \n" + _RESET
            index = 0
            for row in range(num_rows):
                # Print the row index on the left.
                board_string.append(f"{row}" + _FULL_SPACE)
                # Print each piece of this row, including empty piece.
                for col in "abcdefghi":
                    piece = self.board[f"{col}{row}"]
                    add_piece_symbol(board_string, piece, peek_result, index, terminal)
                    if col != "i":
                        board_string.append(_FULL_SPACE * 2)
                    index += 1
                # Print the row index on the right.
                board_string += _FULL_SPACE * 2 + f"{row}\n"
                # Print the sampled prob. of the pieces in the above row.
                if probabilities is not None:
                    board_string += _FULL_SPACE + " "
                    board_string += _BG_GREY
                    board_string += _FG_BLACK
                    for i in range(row * 9, (row + 1) * 9):
                        # We only print non-zero probabilities
                        if terminal != TerminalType.COLAB_OR_SUBLIME_TERMINUS:
                            # space + _FULL_SPACE works for mac terminal and gLinux terminal.
                            if probabilities[i] >= 1e-3:
                                board_string.append(
                                    "{:.1f} ".format(probabilities[i]) + _FULL_SPACE
                                )
                            else:
                                board_string.append("    " + _FULL_SPACE)
                        else:
                            if probabilities[i] >= 1e-3:
                                # space + space works for sublime terminus.
                                board_string.append("{:.1f}  ".format(probabilities[i]))
                            else:
                                board_string.append("     ")
                    board_string += "\b" + _RESET + _FULL_SPACE + "\n"
            # Print the bottom line of col letters.
            board_string.append(_FULL_SPACE + " ")
            board_string += _BG_GREY
            board_string += _FG_BLACK
            for col in range(_FULL_A, _FULL_A + 9):
                board_string.append(f"{chr(col)}")
                if col != _FULL_A + 8:
                    board_string += _FULL_SPACE * 2
            board_string += " " + _RESET + "\n"
            return "".join(board_string)

    def path_pieces(self, source: str, target: str) -> Tuple[List[str], List[str]]:
        """Returns the nonempty classical and quantum pieces from source to target (excluded)."""
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
        # This could be move of rook, king, pawn or cannon.
        elif dx == 0:
            for i in range(1, abs(dy)):
                pieces.append(f"{chr(x0)}{y0 + dy_sign * i}")
        # This could be move of rook, king, pawn or cannon.
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
            raise ValueError("The input move is illegal.")
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
        # When there are only quantum pieces in between, the check successes (and game ends)
        # if all of those pieces turn out to be empty.
        capture_ancilla = self.board._add_ancilla("flying_general_check")
        control_objects = [self.board[path] for path in quantum_pieces]
        conditions = [0] * len(control_objects)
        alpha.quantum_if(*control_objects).equals(*conditions).apply(alpha.Flip())(
            capture_ancilla
        )
        could_capture = self.board.pop([capture_ancilla])[0]
        if could_capture:
            # Force measure all path pieces to be empty.
            for path_piece in control_objects:
                self.board.force_measurement(path_piece, 0)
                path_piece.reset()

            # Let the general/king fly, i.e. the opposite king will capture the current king.
            current_king = self.board[self.king_locations[self.current_player]]
            oppsite_king = self.board[self.king_locations[1 - self.current_player]]
            Jump(MoveVariant.CLASSICAL)(oppsite_king, current_king)
            print("==== FLYING GENERAL ! ====")
            return True
        else:
            # Note: we are leaving the path pieces unchanged in entangled state.
            print("==== General not flies yet ! ====")
            return False

    def sample(self, repetitions: int) -> List[int]:
        """Sample the current board by the given `repetitions`.
        Returns a list of 90-bit bitstring, each corresponding to one sample.
        """
        samples = self.board.peek(count=repetitions, convert_to_enum=False)
        # Convert peek results (in List[List[int]]) into List[int].
        samples = [
            int("0b" + "".join([str(i) for i in sample[::-1]]), base=2)
            for sample in samples
        ]
        return samples
