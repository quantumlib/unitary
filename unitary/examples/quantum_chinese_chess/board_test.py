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
9 r h e a k a e h r  9
8 . . . . . . . . .  8
7 . c . . . . . c .  7
6 p . p . p . p . p  6
5 . . . . . . . . .  5
4 . . . . . . . . .  4
3 P . P . P . P . P  3
2 . C . . . . . C .  2
1 . . . . . . . . .  1
0 R H E A K A E H R  0
  a b c d e f g h i
"""
    )

    board.set_language(Language.ZH)
    assert (
        board.__str__()
        == """
　ａｂｃｄｅｆｇｈｉ
９車馬相仕帥仕相馬車９
８．．．．．．．．．８
７．砲．．．．．砲．７
６卒．卒．卒．卒．卒６
５．．．．．．．．．５
４．．．．．．．．．４
３兵．兵．兵．兵．兵３
２．炮．．．．．炮．２
１．．．．．．．．．１
０车马象士将士象马车０
　ａｂｃｄｅｆｇｈｉ
"""
    )

    assert board.king_locations == ["e0", "e9"]


def test_init_with_specified_fen():
    board = Board.from_fen("4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c w---1 ")

    assert (
        board.__str__()
        == """
  a b c d e f g h i
9 . . . A K . . . c  9
8 . . . . A p . r .  8
7 . . . . . . . . .  7
6 . . . . . . . . .  6
5 . . . . . . . . .  5
4 . . . . . . . . .  4
3 . . . . . . . H .  3
2 . . . h R . . . .  2
1 . . . . a . . . .  1
0 . . . . k a R . .  0
  a b c d e f g h i
"""
    )

    board.set_language(Language.ZH)
    assert (
        board.__str__()
        == """
　ａｂｃｄｅｆｇｈｉ
９．．．士将．．．砲９
８．．．．士卒．車．８
７．．．．．．．．．７
６．．．．．．．．．６
５．．．．．．．．．５
４．．．．．．．．．４
３．．．．．．．马．３
２．．．馬车．．．．２
１．．．．仕．．．．１
０．．．．帥仕车．．０
　ａｂｃｄｅｆｇｈｉ
"""
    )

    assert board.king_locations == ["e0", "e9"]


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
