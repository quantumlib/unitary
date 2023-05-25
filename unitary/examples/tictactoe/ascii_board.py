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

from unitary.examples.tictactoe.enums import TicTacSquare, TicTacResult, TicTacRules
from unitary.examples.tictactoe.tic_tac_toe import TicTacToe
import argparse, textwrap

help_str = """\
In classical TicTacToe, players alternate in putting their token (either an
X or an O) on the squares of a 3x3 board. Each of the 3x3 squares of the board
is labeled by its own letter as follows:

                                 |     |
                              a  |  b  |  c
                            _____|_____|_____
                                 |     |
                              d  |  e  |  f
                            _____|_____|_____
                                 |     |
                              g  |  h  |  i
                                 |     |

When it's your turn, to put your token on an empty square just input the
corresponding square's letter. That is, to put your token on the top-right
square, input 'c'.

In Quantum TicTacToe, you get access to so-called split moves, in which your
token can be put on two squares simultaneously. To input a quantum move,
enter the two letters of the involved squares. For example, a quantum move
putting your token in the top left and bottom right squares has input 'ai'.

Split moves can be made without restrictions using the default, fully quantum,
ruleset. If you'd like to allow split moves only on empty squares, choose the
minimal quantum ruleset. If you'd like no quantum moves at all, choose the
classical ruleset. Choose different rulesets can be done using the -r option,
see below.
"""


def _flip_turn(turn: TicTacSquare):
    return TicTacSquare.O if turn == TicTacSquare.X else TicTacSquare.X


class AsciiBoard:
    def __init__(self, rules: TicTacRules):
        self.board = TicTacToe(rules)

    def play(self):
        turn = TicTacSquare.X
        result = TicTacResult.UNFINISHED

        while result == TicTacResult.UNFINISHED:
            print(self.board.print())
            move = input(f"{turn.name} turn to move: ").lower()
            if move == "q":
                exit()

            try:
                result = self.board.move(move, turn)
            except Exception as e:
                print(e)
                continue

            turn = _flip_turn(turn)

        print(f"Result: {result.name}")
        print(self.board.print())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(help_str),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-r",
        dest="rules",
        default=3,
        type=int,
        choices=range(1, 4),
        help=textwrap.dedent(
            """
                            Set the ruleset:
                                1: Classical
                                2: Minimal Quantum
                                    Allow split moves, but only on empty squares
                                3: Fully Quantum (Default)
                                    Allow split moves, no restrictions"""
        ),
    )
    args = parser.parse_args()

    print(
        "Starting a new game of Quantum TicTacToe with "
        "ruleset '%s'" % TicTacRules(args.rules - 1)
    )
    print("Change the ruleset using the -r option. Or use -h for more help.")
    print("Input 'q' to exit.")

    # Start a new game with the chosen ruleset (defaults to FULLY_QUANTUM)
    AsciiBoard(TicTacRules(args.rules - 1)).play()
