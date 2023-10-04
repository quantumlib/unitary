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
    SquareState,
    Language,
    Color,
    Type,
)
from unitary.examples.quantum_chinese_chess.board import Board


def test_init(capsys):
    board = Board()
    board.print()
    output = capsys.readouterr()
    assert (
        output
        == """
          a b c d e f g h i\n0 r h e a k a e h r  0\n1 . . . . . . . . .  1\n2 . c . . . . . c .  2\n3 p . p . p . p . p  3\n4 . . . . . . . . .  4\n5 . . . . . . . . .  5\n6 P . P . P . P . P  6\n7 . C . . . . . C .  7\n8 . . . . . . . . .  8\n9 R H E A K A E H R  9\n  a b c d e f g h i\n
        """
    )

    board.print(Language.ZH)
    output = capsys.readouterr()
    assert (
        output
        == """
        """
    )
