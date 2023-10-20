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
from unitary.examples.quantum_chinese_chess.move import Move, Jump
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.piece import Piece
import pytest
from unitary import alpha
from typing import List
from unitary.examples.quantum_chinese_chess.enums import (
    MoveType,
    MoveVariant,
    SquareState,
    Type,
    Color,
)
from unitary.examples.quantum_chinese_chess.test_utils import (
    locations_to_bitboard,
    assert_samples_in,
    assert_sample_distribution,
    assert_this_or_that,
    assert_prob_about,
    assert_fifty_fifty,
    sample_board,
    get_board_probability_distribution,
    print_samples,
    set_board,
)


def test_move_eq():
    board = Board.from_fen()
    move1 = Move(
        "a1",
        "b2",
        board,
        "c1",
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    move2 = Move(
        "a1",
        "b2",
        board,
        "c1",
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    move3 = Move(
        "a1", "b2", board, move_type=MoveType.JUMP, move_variant=MoveVariant.CAPTURE
    )
    move4 = Move(
        "a1",
        "b2",
        board,
        "c1",
        move_type=MoveType.MERGE_SLIDE,
        move_variant=MoveVariant.CAPTURE,
    )

    assert move1 == move2
    assert move1 != move3
    assert move1 != move4


def test_move_type():
    # TODO(): change to real senarios
    board = Board.from_fen()
    move1 = Move(
        "a1",
        "b2",
        board,
        "c1",
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move1.is_split_move() == False
    assert move1.is_merge_move()

    move2 = Move(
        "a1",
        "b2",
        board,
        target2="c1",
        move_type=MoveType.SPLIT_JUMP,
        move_variant=MoveVariant.BASIC,
    )
    assert move2.is_split_move()
    assert move2.is_merge_move() == False

    move3 = Move(
        "a1", "b2", board, move_type=MoveType.SLIDE, move_variant=MoveVariant.CAPTURE
    )
    assert move3.is_split_move() == False
    assert move3.is_merge_move() == False


def test_to_str():
    # TODO(): change to real scenarios
    board = Board.from_fen()
    move1 = Move(
        "a0",
        "a6",
        board,
        "c1",
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move1.to_str(0) == ""
    assert move1.to_str(1) == "a0c1^a6"
    assert move1.to_str(2) == "a0c1^a6:MERGE_JUMP:CAPTURE"
    assert move1.to_str(3) == "a0c1^a6:MERGE_JUMP:CAPTURE:RED_ROOK->BLACK_PAWN"

    move2 = Move(
        "a0",
        "b3",
        board,
        target2="c1",
        move_type=MoveType.SPLIT_JUMP,
        move_variant=MoveVariant.BASIC,
    )
    assert move2.to_str(0) == ""
    assert move2.to_str(1) == "a0^b3c1"
    assert move2.to_str(2) == "a0^b3c1:SPLIT_JUMP:BASIC"
    assert move2.to_str(3) == "a0^b3c1:SPLIT_JUMP:BASIC:RED_ROOK->NA_EMPTY"

    move3 = Move(
        "a0", "a6", board, move_type=MoveType.SLIDE, move_variant=MoveVariant.CAPTURE
    )
    assert move3.to_str(0) == ""
    assert move3.to_str(1) == "a0a6"
    assert move3.to_str(2) == "a0a6:SLIDE:CAPTURE"
    assert move3.to_str(3) == "a0a6:SLIDE:CAPTURE:RED_ROOK->BLACK_PAWN"


def test_jump_classical():
    # Target is empty.
    board = set_board(["a1", "b1"])
    world = board.board
    # TODO(): try move all varaibles declarations of a1 = world["a1"] into a function.
    Jump(MoveVariant.CLASSICAL)(world["a1"], world["b2"])
    assert_samples_in(board, [locations_to_bitboard(["b2", "b1"])])

    # Target is occupied.
    Jump(MoveVariant.CLASSICAL)(world["b2"], world["b1"])
    assert_samples_in(board, [locations_to_bitboard(["b1"])])


def test_jump_capture():
    # Source is in quantum state.
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a2", "b1"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b1"]))
    Jump(MoveVariant.CAPTURE)(world["a2"], world["b1"])
    # pop() will break the supersition and only one of the following two states are possible.
    # We check the ancilla to learn if the jump was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    if source_is_occupied:
        assert_samples_in(board, [locations_to_bitboard(["b1"])])
    else:
        assert_samples_in(board, [locations_to_bitboard(["a3", "b1"])])

    # Target is in quantum state.
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    Jump(MoveVariant.CAPTURE)(world["a1"], world["b2"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2", "b3"]))

    # Both source and target are in quantum state.
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a2", "b2"]): 1 / 4.0,
            locations_to_bitboard(["a2", "b3"]): 1 / 4.0,
            locations_to_bitboard(["a3", "b2"]): 1 / 4.0,
            locations_to_bitboard(["a3", "b3"]): 1 / 4.0,
        },
    )
    Jump(MoveVariant.CAPTURE)(world["a2"], world["b2"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    # We check the ancilla to learn if the jump was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    print(source_is_occupied)
    if source_is_occupied:
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2"]))
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2", "b3"]))
    else:
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b2"]))
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b3"]))


def test_jump_excluded():
    # Target is in quantum state.
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    Jump(MoveVariant.EXCLUDED)(world["a1"], world["b2"])
    # pop() will break the supersition and only one of the following two states are possible.
    # We check the ancilla to learn if the jump was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_b2_0"]]
    print(target_is_occupied)
    if target_is_occupied:
        assert_samples_in(board, [locations_to_bitboard(["a1", "b2"])])
    else:
        assert_samples_in(board, [locations_to_bitboard(["b2", "b3"])])

    # Both source and target are in quantum state.
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    Jump(MoveVariant.EXCLUDED)(world["a2"], world["b2"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    # We check the ancilla to learn if the jump was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_b2_0"]]
    print(target_is_occupied)
    if target_is_occupied:
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a2", "b2"]))
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b2"]))
    else:
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2", "b3"]))
        assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b3"]))


def test_jump_basic():
    # Source is in quantum state.
    board = set_board(["a1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    Jump(MoveVariant.BASIC)(world["a2"], world["d1"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["d1"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3"]))
