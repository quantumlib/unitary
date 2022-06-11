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
import pytest

import unitary.examples.tictactoe as tictactoe

_E = tictactoe.TicTacSquare.EMPTY
_O = tictactoe.TicTacSquare.O
_X = tictactoe.TicTacSquare.X


@pytest.mark.parametrize(
    "result,expected",
    [
        ([_E, _E, _E, _E, _E, _E, _E, _E, _E], tictactoe.TicTacResult.UNFINISHED),
        ([_E, _E, _X, _X, _E, _E, _O, _E, _E], tictactoe.TicTacResult.UNFINISHED),
        ([_E, _E, _X, _X, _E, _X, _O, _E, _X], tictactoe.TicTacResult.X_WINS),
        ([_E, _X, _E, _X, _X, _O, _O, _X, _E], tictactoe.TicTacResult.X_WINS),
        ([_X, _E, _E, _X, _O, _O, _X, _E, _E], tictactoe.TicTacResult.X_WINS),
        ([_X, _X, _X, _X, _O, _O, _E, _E, _E], tictactoe.TicTacResult.X_WINS),
        ([_E, _E, _E, _X, _X, _X, _E, _O, _E], tictactoe.TicTacResult.X_WINS),
        ([_E, _E, _E, _E, _E, _E, _X, _X, _X], tictactoe.TicTacResult.X_WINS),
        ([_X, _E, _E, _E, _X, _E, _E, _E, _X], tictactoe.TicTacResult.X_WINS),
        ([_E, _E, _X, _E, _X, _E, _X, _E, _E], tictactoe.TicTacResult.X_WINS),
        ([_O, _E, _E, _E, _O, _E, _E, _E, _O], tictactoe.TicTacResult.O_WINS),
        ([_E, _E, _O, _E, _O, _E, _O, _E, _E], tictactoe.TicTacResult.O_WINS),
        ([_O, _O, _O, _E, _E, _E, _E, _E, _E], tictactoe.TicTacResult.O_WINS),
        ([_E, _E, _E, _O, _O, _O, _E, _E, _E], tictactoe.TicTacResult.O_WINS),
        ([_E, _E, _E, _E, _E, _E, _O, _O, _O], tictactoe.TicTacResult.O_WINS),
        ([_O, _E, _E, _O, _E, _E, _O, _E, _E], tictactoe.TicTacResult.O_WINS),
        ([_E, _O, _E, _E, _O, _E, _E, _O, _E], tictactoe.TicTacResult.O_WINS),
        ([_E, _E, _O, _E, _E, _O, _E, _E, _O], tictactoe.TicTacResult.O_WINS),
        ([_E, _E, _O, _E, _E, _O, _E, _E, _O], tictactoe.TicTacResult.O_WINS),
        ([_X, _E, _O, _X, _E, _O, _X, _E, _O], tictactoe.TicTacResult.BOTH_WIN),
        ([_X, _X, _X, _O, _O, _O, _E, _E, _E], tictactoe.TicTacResult.BOTH_WIN),
        ([_E, _E, _E, _O, _O, _O, _X, _X, _X], tictactoe.TicTacResult.BOTH_WIN),
        ([_X, _O, _O, _O, _X, _X, _O, _X, _O], tictactoe.TicTacResult.DRAW),
        ([_X, _O, _X, _X, _O, _X, _O, _X, _O], tictactoe.TicTacResult.DRAW),
    ],
)
def test_eval_board(result, expected):
    assert tictactoe.tic_tac_toe.eval_board(result) == expected


def test_measure():
    board = tictactoe.TicTacToe()
    board.move("ab", tictactoe.TicTacSquare.X)
    board.move("cd", tictactoe.TicTacSquare.O)
    board.move("ef", tictactoe.TicTacSquare.X)
    board.move("gh", tictactoe.TicTacSquare.O)
    results = board.sample(count=1000)
    assert len(results) == 1000
    assert all(result.count("X") == 2 for result in results)
    assert all(result.count("O") == 2 for result in results)
    assert all(result.count(".") == 5 for result in results)

    # There should be 16 different possibilities depending on the splits.
    result_set = set()
    result_set.update(results)
    assert len(result_set) == 16

    # This should trigger a measurement
    board.move("i", tictactoe.TicTacSquare.X)
    results = board.sample(count=1000)
    assert len(results) == 1000
    assert all(result.count("X") == 3 for result in results)
    assert all(result.count("O") == 2 for result in results)
    assert all(result.count(".") == 4 for result in results)
    assert all(result == results[0] for result in results)

    result_set = set()
    result_set.update(results)
    assert len(result_set) == 1

    # Now try an operation after measurement
    if results[0][0] == ".":
        board.move("a", tictactoe.TicTacSquare.O)
        expected = "OX" + results[0][2:]
    else:
        board.move("b", tictactoe.TicTacSquare.O)
        expected = "XO" + results[0][2:]
    results = board.sample(count=1000)
    assert len(results) == 1000
    assert all(result == expected for result in results)


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


def test_rulesets():
    # Try to make a quantum move with classical rules
    board = tictactoe.TicTacToe(tictactoe.TicTacRules.CLASSICAL)
    with pytest.raises(ValueError):
        board.move("ab", tictactoe.TicTacSquare.X)

    # Try to make a split move on non-empty squares at minimal quantum
    board = tictactoe.TicTacToe(tictactoe.TicTacRules.MINIMAL_QUANTUM)
    board.move("a", tictactoe.TicTacSquare.X)
    with pytest.raises(ValueError):
        board.move("ab", tictactoe.TicTacSquare.O)


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
