# Copyright 2022 Google
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
from typing import Dict, List

from unitary.alpha import QuantumObject, QuantumWorld
from unitary.alpha.qudit_effects import QuditFlip
from unitary.examples.tictactoe.enums import TicTacSquare
from unitary.examples.tictactoe.tic_tac_split import TicTacSplit


_SQUARE_NAMES = "abcdefghi"
_MARK_SYMBOLS = {TicTacSquare.EMPTY: ".", TicTacSquare.X: "X", TicTacSquare.O: "O"}


def _histogram(results: List[List[TicTacSquare]]) -> List[Dict[TicTacSquare, int]]:
    """Turns a list of whole board measurements into a histogram.

    Returns:
        A 9 element list (one for each square) that contains a dictionary with
        counts for EMPTY, X, and O.
    """
    hist = []
    for idx in range(9):
        hist.append({TicTacSquare.EMPTY: 0, TicTacSquare.X: 0, TicTacSquare.O: 0})
    for r in results:
        for idx in range(9):
            hist[idx][r[idx]] += 1
    return hist


def _result_to_str(result: List[TicTacSquare]) -> str:
    """Transforms a result list of measurements into a 9 letter string."""
    return "".join([_MARK_SYMBOLS[square] for square in result])


class TicTacToe:
    """A class that implements Quantum TicTacToe using the unitary API.

    The TicTacToe board can be initialized with `TicTacToe()`.
    Moves can be done by using `move()`.  Moves can be one or two
    letters, where a two letter move indicates a "split" move.
    Letters are 'a' through 'i', in the following format:


       a | b | c
      -----------
       d | e | f
      -----------
       g | h | i

    Results can be viewed by using `print()` to see the board in a
    human-friendly text format or by using `sample()` to get one
    or more samples (measurements) of the board.
    """

    def __init__(self):
        self.clear()

    def clear(self) -> None:
        """Clears the TicTacToe board.

        Sets all 9 squares to empty.
        """
        self.squares = {}
        self.empty_squares = set()
        for name in _SQUARE_NAMES:
            self.empty_squares.add(name)
            self.squares[name] = QuantumObject(name, TicTacSquare.EMPTY)
        self.board = QuantumWorld(list(self.squares.values()))

    def move(self, move: str, mark: TicTacSquare) -> None:
        """Make a move on the TicTacToe board.

        Args:
            move: A move can be a one or two letter string.
                If the move is one letter, this places a mark
                on that square.  If the move is two letters, this
                performs a "split" move on the two squares.
            mark: Either TicTacSquare.X or TicTacSquare.O
        """
        if len(move) > 2 or len(move) == 0:
            raise ValueError(f"Move {move} must be one or two letters.")
        if not all(m in _SQUARE_NAMES for m in move):
            raise ValueError(
                f"Move {move} must be one of these squares: {_SQUARE_NAMES}"
            )
        if len(move) == 1:
            QuditFlip(3, 0, mark.value)(self.squares[move])
            self.empty_squares.remove(move)
        else:
            TicTacSplit(mark)(self.squares[move[0]], self.squares[move[1]])
            self.empty_squares.remove(move[0])
            self.empty_squares.remove(move[1])

    def sample(self, count: int = 1) -> List[str]:
        """Samples the quantum TicTacToe board.

        This will return a 9 letter string containing
        '.', 'X', or 'O' for each square.  For instance,

           | X |
        -----------
         X | O |
        -----------
           | O | O

        would return '.X.XO..OO'.
        """
        return [_result_to_str(result) for result in self.board.peek(count=count)]

    def print(self) -> str:
        """Returns the TicTacToe board in ASCII form."""
        results = self.board.peek(count=100)
        hist = _histogram(results)
        output = "\n"
        for row in range(3):
            for mark in TicTacSquare:
                output += " "
                for col in range(3):
                    idx = row * 3 + col
                    output += f" {_MARK_SYMBOLS[mark]} {hist[idx][mark]:3}"
                    if col != 2:
                        output += " |"
                output += "\n"
            if idx in [2, 5, 8] and row != 2:
                output += "--------------------------\n"
        return output
