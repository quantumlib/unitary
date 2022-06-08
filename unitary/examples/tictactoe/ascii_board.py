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

from unitary.examples.tictactoe.enums import TicTacSquare, TicTacResult
from unitary.examples.tictactoe.tic_tac_toe import TicTacToe


def _flip_turn(turn: TicTacSquare):
    return TicTacSquare.O if turn == TicTacSquare.X else TicTacSquare.X


class AsciiBoard:
    def __init__(self):
        self.board = TicTacToe()

    def play(self):
        turn = TicTacSquare.X
        result = TicTacResult.UNFINISHED

        while result == TicTacResult.UNFINISHED:
            print(self.board.print())
            move = input(f"{turn.name} turn to move: ")
            result = self.board.move(move, turn)
            turn = _flip_turn(turn)

        print(f"Result: {result.name}")


if __name__ == "__main__":
    AsciiBoard().play()
