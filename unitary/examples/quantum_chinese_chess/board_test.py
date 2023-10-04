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
from unitary.examples.quantum_chinese_chess.enums import Language
from unitary.examples.quantum_chinese_chess.board import Board


def test_init_with_default_fen():
    board = Board()
    assert (
        board.to_str()
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

    print(board.to_str(Language.ZH))
    assert (
        board.to_str(Language.ZH)
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


def test_init_with_specified_fen():
    board = Board("4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c w---1 ")

    assert (
        board.to_str()
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

    assert (
        board.to_str(Language.ZH)
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
