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
import io
import sys
from typing import Dict, List

from unitary.alpha import QuantumObject, QuantumWorld
from unitary.alpha.qudit_effects import QuditFlip
from unitary.examples.tictactoe.enums import TicTacSquare, TicTacResult, TicTacRules, GameMoves
from unitary.examples.tictactoe.tic_tac_split import TicTacSplit

_SQUARE_NAMES = "abcdefghi"
_MARK_SYMBOLS = {TicTacSquare.EMPTY: ".", TicTacSquare.X: "X", TicTacSquare.O: "O"}

# Possible ways to get three in a row (rows, columns, and diagonal) indices
_POSSIBLE_WINS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


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


def eval_board(result: List[TicTacSquare]) -> TicTacResult:
    x_wins = False
    o_wins = False
    still_empty = False
    for check in _POSSIBLE_WINS:
        if all(result[check[idx]] == TicTacSquare.X for idx in range(3)):
            x_wins = True
        if all(result[check[idx]] == TicTacSquare.O for idx in range(3)):
            o_wins = True
        if any(result[check[idx]] == TicTacSquare.EMPTY for idx in range(3)):
            still_empty = True
    if x_wins:
        if o_wins:
            return TicTacResult.BOTH_WIN
        else:
            return TicTacResult.X_WINS
    else:
        if o_wins:
            return TicTacResult.O_WINS
        else:
            if still_empty:
                return TicTacResult.UNFINISHED
            else:
                return TicTacResult.DRAW


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

    Set `run_on_hardware` to compile the board to qubits for running on
    actual hardware.
    """

    def __init__(
        self, rules: TicTacRules = TicTacRules.QUANTUM_V3, run_on_hardware: bool = False
    ):
        self.clear(run_on_hardware)
        self.rules = rules

    def clear(self, run_on_hardware: bool = False) -> None:
        """Clears the TicTacToe board.

        Sets all 9 squares to empty.
        """
        self.squares = {}
        self.last_result = [TicTacSquare.EMPTY] * 9
        self.empty_squares = set()
        for name in _SQUARE_NAMES:
            self.empty_squares.add(name)
            self.squares[name] = QuantumObject(name, TicTacSquare.EMPTY)
        self.board = QuantumWorld(
            list(self.squares.values()), compile_to_qubits=run_on_hardware
        )

    def result(self) -> TicTacResult:
        """Returns the result of the TicTacToe game.

        Returns EMPTY if no winner has been decided, X if
        three in a row.
        """
        return eval_board(self.last_result)

    def measure(self) -> None:
        """Measures all squares on the TicTacToe board.

        Once the board is measured, a new board is created
        that is initialized to the measured state.
        This should happen when no more squares are empty.
        """
        self.last_result = self.board.pop()
        for idx, name in enumerate(_SQUARE_NAMES):
            if self.last_result[idx] == TicTacSquare.EMPTY:
                self.empty_squares.add(name)
            self.squares[name] = QuantumObject(name, self.last_result[idx])
        self.board = QuantumWorld(list(self.squares.values()))

    def move(self, move: str, mark: TicTacSquare) -> TicTacResult:
        """Make a move on the TicTacToe board.

        Args:
            move: A move can be a one or two letter string.
                If the move is one letter, this places a mark
                on that square.  If the move is two letters, this
                performs a "split" move on the two squares.
            mark: Either TicTacSquare.X or TicTacSquare.O
        """
        if len(move) > 2 or len(move) == 0:
            raise ValueError(f"Your move ({move}) must be one or two letters.")
        if not all(m in _SQUARE_NAMES for m in move):
            raise ValueError(f"Your move ({move}) can only have these: {_SQUARE_NAMES}")
        if len(move) == 1:
            # Check if the square is empty
            if move not in self.empty_squares:
                raise ValueError(
                    f"You cannot put your token on non-empty square {move}"
                )
            # Flip the square to the correct value (mark.value)
            QuditFlip(3, 0, mark.value)(self.squares[move])
            # This square is now no longer empty
            self.empty_squares.discard(move)
        else:
            # Check if rules allow quantum moves
            if self.rules == TicTacRules.CLASSICAL:
                raise ValueError(
                    f"Quantum moves are not allowed in a classical TicTacToe"
                )

            # Check if either square is non-empty. Splitting on top of
            # non-empty squares is only allowed at full quantumness
            if (
                (move[0] not in self.empty_squares)
                or (move[1] not in self.empty_squares)
            ) and (self.rules == TicTacRules.QUANTUM_V1):
                raise ValueError(
                    f"This ruleset ({0}) does not allow splits on \
                              top of non-empty squares".format(
                        self.rules
                    )
                )

            # TicTacSplit first flips the first square before performing a split
            # If either of the two involved squares is empty, we want to do the
            # split on that square.
            if move[1] in self.empty_squares:
                TicTacSplit(mark, self.rules)(
                    self.squares[move[1]], self.squares[move[0]]
                )
            else:
                TicTacSplit(mark, self.rules)(
                    self.squares[move[0]], self.squares[move[1]]
                )

            # The involved squares are now no longer empty
            self.empty_squares.discard(move[0])
            self.empty_squares.discard(move[1])

        # If the board is full, we project everything
        if not self.empty_squares:
            self.measure()
        return self.result()

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

class Game:
    """
    A class that provides a command-line interface to play Quantum Tic Tac Toe.

    Initialize by providing an instance of a TicTacToe game, then call play()
    to run the game.

    Args:
        game: A TicTacToe instance for the game interface to wrap.
        file:  Optional IOBase file object to write output to.
            This enables the battle to write status to a file or string
            for testing.

    """
    def __init__(self, game: TicTacToe, file: io.IOBase = sys.stdout):
        self.game = game
        self.file = file
        self.player = "X"
        self.player_quit = False

    def player_move(self) -> None: 
        """
        Gets and handles the player's move.

        A move can be a one or two letter string within the set [abcdefghi],
        in which case this function hands the move off to the TicTacToe instance,
        or one of the GameMoves enums (GameMoves.MAP, GameMoves.EXIT, GameMoves.HELP),
        which prevent the game loop from alternating to the next player.

        Raises:
            ValueError if it is still the player's move.
        """
        move = input(f"Player {self.player} to move (\"help\" for help): ").upper()
        if move == GameMoves.MAP.name:
            print(self.print_board_map(), file=self.file)
            raise ValueError("Still your move.")
        if move == GameMoves.EXIT.name:
            self.player_quit = True
            raise ValueError("Goodbye!", file=self.file)
        if move == GameMoves.HELP.name:
            print(self.print_help())
            raise ValueError("Still your move.", file=self.file)
        else:
            mark = TicTacSquare.X if self.player == "X" else TicTacSquare.O
            self.game.move(move, mark)

    def play(self) -> None:
        """
        Run the game loop, requesting player moves, alternating players, until
        the TicTacToe instance reports that the game ends with a winner or a tie
        or one of the players has quit.
        """
        print("Welcome to quantum tic tac toe!", file=self.file)
        print("Here is the board:", file=self.file)
        print(self.print_board_map(), file=self.file)

        while self.game.result() == TicTacResult.UNFINISHED and not self.playerQuit: 
            try:
                self.player_move()
                self.player = "O" if self.player == "X" else "X"
                print(self.game.print(), file=self.file)
            except ValueError as e:
                print(e, file=self.file)
        print(self.game.result(), file=self.file)
    
    def print_help(self) -> None:
        """Print the available moves that player can take."""
        return """
    You can enter:
    - 1 character from [abcdefghi] to place a mark in the corresponding square (eg "a")
    - 2 characters from [abcdefghi] to place a split mark in corresponding squares (eg "bd")
    - "map": show board map
    - "exit" to quit
    """

    def print_board_map(self) -> None:
        """Print the mapping of letters to board spaces for player move reference."""
        return """
        a | b | c
        -----------
        d | e | f
        -----------
        g | h | i
        """

def main():
    game = Game(TicTacToe())
    game.play()
    
if __name__ == "__main__":
    main()