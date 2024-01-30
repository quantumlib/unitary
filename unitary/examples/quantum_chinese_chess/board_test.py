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
from unitary.examples.quantum_chinese_chess.test_utils import (
    locations_to_bitboard,
    assert_samples_in,
    assert_sample_distribution,
    get_board_probability_distribution,
    set_board,
)
from unitary import alpha
import re


def test_init_with_default_fen():
    board = Board.from_fen()
    assert (
        re.sub("\\033\[\d{1,2}m", "", board.to_str(None, False)).replace("\b", "")
        == """
    a   b   c   d   e   f   g   h   i   
0   R   H   E   A   K   A   E   H   R  0
1   ·   ·   ·   ·   ·   ·   ·   ·   ·  1
2   ·   C   ·   ·   ·   ·   ·   C   ·  2
3   P   ·   P   ·   P   ·   P   ·   P  3
4   ·   ·   ·   ·   ·   ·   ·   ·   ·  4
5   ·   ·   ·   ·   ·   ·   ·   ·   ·  5
6   p   ·   p   ·   p   ·   p   ·   p  6
7   ·   c   ·   ·   ·   ·   ·   c   ·  7
8   ·   ·   ·   ·   ·   ·   ·   ·   ·  8
9   r   h   e   a   k   a   e   h   r  9
    a   b   c   d   e   f   g   h   i   
"""
    )

    assert board.king_locations == ["e0", "e9"]


def test_init_with_specified_fen():
    board = Board.from_fen("4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c w---1 ")

    assert (
        re.sub("\\033\[\d{1,2}m", "", board.to_str(None, False)).replace("\b", "")
        == """
    a   b   c   d   e   f   g   h   i   
0   ·   ·   ·   ·   k   a   R   ·   ·  0
1   ·   ·   ·   ·   a   ·   ·   ·   ·  1
2   ·   ·   ·   h   R   ·   ·   ·   ·  2
3   ·   ·   ·   ·   ·   ·   ·   H   ·  3
4   ·   ·   ·   ·   ·   ·   ·   ·   ·  4
5   ·   ·   ·   ·   ·   ·   ·   ·   ·  5
6   ·   ·   ·   ·   ·   ·   ·   ·   ·  6
7   ·   ·   ·   ·   ·   ·   ·   ·   ·  7
8   ·   ·   ·   ·   A   p   ·   r   ·  8
9   ·   ·   ·   A   K   ·   ·   ·   c  9
    a   b   c   d   e   f   g   h   i   
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


def test_flying_general_check_classical_cases():
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


def test_flying_general_check_quantum_cases():
    # When there are quantum pieces in between.
    board = set_board(["a3", "a4", "e0", "e9"])
    board.king_locations = ["e0", "e9"]
    board.current_player = 0  # i.e. RED
    world = board.board
    alpha.PhasedSplit()(world["a3"], world["c3"], world["e3"])
    world["e3"].is_entangled = True
    alpha.PhasedSplit()(world["a4"], world["c4"], world["e4"])
    world["e4"].is_entangled = True

    result = board.flying_general_check()
    # We check the ancilla to learn whether the general/king flies or not.
    captured = world.post_selection[world["ancilla_ancilla_flying_general_check_0_0"]]
    if captured:
        assert result
        assert_samples_in(board, {locations_to_bitboard(["c3", "c4", "e0"]): 1.0})
    else:
        assert not result
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["e0", "e9", "e3", "e4"]): 1.0 / 3,
                locations_to_bitboard(["e0", "e9", "e3", "c4"]): 1.0 / 3,
                locations_to_bitboard(["e0", "e9", "c3", "e4"]): 1.0 / 3,
            },
        )


def test_flying_general_check_quantum_cases_not_captured():
    # When there are quantum pieces in between, but the capture cannot happen.
    board = set_board(["a3", "e0", "e9"])
    board.king_locations = ["e0", "e9"]
    board.current_player = 0  # i.e. RED
    world = board.board
    alpha.PhasedSplit()(world["a3"], world["e3"], world["e4"])
    world["e3"].is_entangled = True
    world["e4"].is_entangled = True

    result = board.flying_general_check()
    assert not result
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["e0", "e9", "e3"]): 1.0 / 2,
            locations_to_bitboard(["e0", "e9", "e4"]): 1.0 / 2,
        },
    )
