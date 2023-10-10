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
#
from unitary.examples.quantum_chinese_chess.enums import (
    Language,
    Color,
    Type,
    SquareState,
)
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.piece import Piece


def test_init_with_default_fen():
    board = Board.from_fen()
    assert (
        board.__str__()
        == """
  a b c d e f g h i
0 r h e a k a e h r  0
1 . . . . . . . . .  1
2 . c . . . . . c .  2
3 p . p . p . p . p  3
4 . . . . . . . . .  4
5 . . . . . . . . .  5
6 P . P . P . P . P  6
7 . C . . . . . C .  7
8 . . . . . . . . .  8
9 R H E A K A E H R  9
  a b c d e f g h i
"""
    )

    board.set_language(Language.ZH)
    assert (
        board.__str__()
        == """
　ａｂｃｄｅｆｇｈｉ
０車馬相仕帥仕相馬車０
１．．．．．．．．．１
２．砲．．．．．砲．２
３卒．卒．卒．卒．卒３
４．．．．．．．．．４
５．．．．．．．．．５
６兵．兵．兵．兵．兵６
７．炮．．．．．炮．７
８．．．．．．．．．８
９车马象士将士象马车９
　ａｂｃｄｅｆｇｈｉ
"""
    )

    assert board.king_locations == ["e9", "e0"]


def test_init_with_specified_fen():
    board = Board.from_fen("4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c w---1 ")

    assert (
        board.__str__()
        == """
  a b c d e f g h i
0 . . . A K . . . c  0
1 . . . . A p . r .  1
2 . . . . . . . . .  2
3 . . . . . . . . .  3
4 . . . . . . . . .  4
5 . . . . . . . . .  5
6 . . . . . . . H .  6
7 . . . h R . . . .  7
8 . . . . a . . . .  8
9 . . . . k a R . .  9
  a b c d e f g h i
"""
    )

    board.set_language(Language.ZH)
    assert (
        board.__str__()
        == """
　ａｂｃｄｅｆｇｈｉ
０．．．士将．．．砲０
１．．．．士卒．車．１
２．．．．．．．．．２
３．．．．．．．．．３
４．．．．．．．．．４
５．．．．．．．．．５
６．．．．．．．马．６
７．．．馬车．．．．７
８．．．．仕．．．．８
９．．．．帥仕车．．９
　ａｂｃｄｅｆｇｈｉ
"""
    )

    assert board.king_locations == ["e9", "e0"]


def test_path_pieces():
    board = Board.from_fen()
    # In case of only moving one step, return empty path pieces.
    assert board.path_pieces("a0", "a1") == ([], [])

    # In case of advisor moving, return empty path pieces.
    assert board.path_pieces("d0", "e1") == ([], [])

    # In case of elephant move, there should be at most one path piece.
    assert board.path_pieces("c0", "e2") == ([], [])
    # Add one classical piece in the path.
    board.board["d1"].reset(Piece("d1", SquareState.OCCUPIED, Type.ROOK, Color.RED))
    assert board.path_pieces("c0", "e2") == (["d1"], [])
    # Add one quantum piece in the path.
    board.board["d1"].is_entangled = True
    assert board.path_pieces("c0", "e2") == ([], ["d1"])

    # Horizontal move
    board.board["c7"].reset(Piece("c7", SquareState.OCCUPIED, Type.ROOK, Color.RED))
    board.board["c7"].is_entangled = True
    assert board.path_pieces("a7", "i7") == (["b7", "h7"], ["c7"])

    # Vertical move
    assert board.path_pieces("c0", "c9") == (["c3", "c6"], ["c7"])

    # In case of horse move, there should be at most one path piece.
    assert board.path_pieces("b9", "a7") == ([], [])
    assert board.path_pieces("b9", "c7") == ([], [])
    # One classical piece in path.
    assert board.path_pieces("b9", "d8") == (["c9"], [])
    # One quantum piece in path.
    assert board.path_pieces("c8", "d6") == ([], ["c7"])


def test_flying_general_check():
    board = Board.from_fen()
    # If they are in different columns, the check fails.
    board.king_locations = ["d0", "e9"]
    assert board.flying_general_check() == False

    # If there are classical pieces between two KINGs, the check fails.
    board.king_locations = ["e0", "e9"]
    assert board.flying_general_check() == False

    # If there are no pieces between two KINGs, the check successes.
    board.board["e3"].reset()
    board.board["e6"].reset()
    assert board.flying_general_check() == True
