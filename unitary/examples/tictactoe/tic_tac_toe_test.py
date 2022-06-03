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

import unitary.examples.tictactoe as tictactoe


def test_sample():
    board = tictactoe.TicTacToe()
    board.move("a", tictactoe.TicTacSquare.X)
    board.move("e", tictactoe.TicTacSquare.O)
    results = board.sample(count=100)
    assert len(results) == 100
    assert all(result == "X...O...." for result in results)
    board.move("h", tictactoe.TicTacSquare.O)
    board.move("i", tictactoe.TicTacSquare.X)
    results = board.sample(count=200)
    assert len(results) == 200
    assert all(result == "X...O..OX" for result in results)


def test_split():
    board = tictactoe.TicTacToe()
    board.move("ab", tictactoe.TicTacSquare.X)
    results = board.sample(count=1000)
    assert len(results) == 1000
    in_a = "X........"
    in_b = ".X......."
    assert any(result == in_a for result in results)
    assert any(result == in_b for result in results)
    assert all(result == in_a or result == in_b for result in results)


def test_print():
    board = tictactoe.TicTacToe()
    board.move("a", tictactoe.TicTacSquare.X)
    board.move("e", tictactoe.TicTacSquare.O)
    output = board.print()

    assert (
        output
        == """
  .   0 | . 100 | . 100
  X 100 | X   0 | X   0
  O   0 | O   0 | O   0
--------------------------
  . 100 | .   0 | . 100
  X   0 | X   0 | X   0
  O   0 | O 100 | O   0
--------------------------
  . 100 | . 100 | . 100
  X   0 | X   0 | X   0
  O   0 | O   0 | O   0
"""
    )
