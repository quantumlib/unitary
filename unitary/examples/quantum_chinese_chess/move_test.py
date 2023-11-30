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
from unitary.examples.quantum_chinese_chess.move import *
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
    get_board_probability_distribution,
    print_samples,
    set_board,
)


def test_move_eq():
    board = Board.from_fen()
    world = board.board
    move1 = Move(
        world["a1"],
        world["b2"],
        world["c1"],
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    move2 = Move(
        world["a1"],
        world["b2"],
        world["c1"],
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    move3 = Move(
        world["a1"],
        world["b2"],
        move_type=MoveType.JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    move4 = Move(
        world["a1"],
        world["b2"],
        world["c1"],
        move_type=MoveType.MERGE_SLIDE,
        move_variant=MoveVariant.CAPTURE,
    )

    assert move1 == move2
    assert move1 != move3
    assert move1 != move4


def test_move_type():
    # TODO(): change to real senarios
    board = Board.from_fen()
    world = board.board
    move1 = Move(
        world["a1"],
        world["b2"],
        world["c1"],
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move1.is_split_move() == False
    assert move1.is_merge_move()

    move2 = Move(
        world["a1"],
        world["b2"],
        target2=world["c1"],
        move_type=MoveType.SPLIT_JUMP,
        move_variant=MoveVariant.BASIC,
    )
    assert move2.is_split_move()
    assert move2.is_merge_move() == False

    move3 = Move(
        world["a1"],
        world["b2"],
        move_type=MoveType.SLIDE,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move3.is_split_move() == False
    assert move3.is_merge_move() == False


def test_to_str():
    # TODO(): change to real scenarios
    board = Board.from_fen()
    world = board.board
    move1 = Move(
        world["a0"],
        world["a6"],
        world["c1"],
        move_type=MoveType.MERGE_JUMP,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move1.to_str(0) == ""
    assert move1.to_str(1) == "a0c1^a6"
    assert move1.to_str(2) == "a0c1^a6:MERGE_JUMP:CAPTURE"
    assert move1.to_str(3) == "a0c1^a6:MERGE_JUMP:CAPTURE:RED_ROOK->BLACK_PAWN"

    move2 = Move(
        world["a0"],
        world["b3"],
        target2=world["c1"],
        move_type=MoveType.SPLIT_JUMP,
        move_variant=MoveVariant.BASIC,
    )
    assert move2.to_str(0) == ""
    assert move2.to_str(1) == "a0^b3c1"
    assert move2.to_str(2) == "a0^b3c1:SPLIT_JUMP:BASIC"
    assert move2.to_str(3) == "a0^b3c1:SPLIT_JUMP:BASIC:RED_ROOK->NA_EMPTY"

    move3 = Move(
        world["a0"],
        world["a6"],
        move_type=MoveType.SLIDE,
        move_variant=MoveVariant.CAPTURE,
    )
    assert move3.to_str(0) == ""
    assert move3.to_str(1) == "a0a6"
    assert move3.to_str(2) == "a0a6:SLIDE:CAPTURE"
    assert move3.to_str(3) == "a0a6:SLIDE:CAPTURE:RED_ROOK->BLACK_PAWN"


def test_jump_classical():
    """Target is empty."""
    board = set_board(["a1", "b1"])
    world = board.board
    # TODO(): try move all varaibles declarations of a1 = world["a1"] into a function.
    Jump(MoveVariant.CLASSICAL)(world["a1"], world["b2"])
    assert_samples_in(board, [locations_to_bitboard(["b2", "b1"])])

    # Target is occupied.
    Jump(MoveVariant.CLASSICAL)(world["b2"], world["b1"])
    assert_samples_in(board, [locations_to_bitboard(["b1"])])


def test_jump_capture_quantum_source():
    """Source is in quantum state."""
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a2", "b1"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3", "b1"]))
    Jump(MoveVariant.CAPTURE)(world["a2"], world["b1"])
    # pop() will break the superposition and only one of the following two states are possible.
    # We check the ancilla to learn if the jump was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    if source_is_occupied:
        assert_samples_in(board, [locations_to_bitboard(["b1"])])
    else:
        assert_samples_in(board, [locations_to_bitboard(["a3", "b1"])])


def test_jump_capture_quantum_target():
    """Target is in quantum state."""
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    Jump(MoveVariant.CAPTURE)(world["a1"], world["b2"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["b2", "b3"]))


def test_jump_capture_quantum_source_and_target():
    """Both source and target are in quantum state."""
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


def test_jump_excluded_quantum_target():
    """Target is in quantum state."""
    board = set_board(["a1", "b1"])
    world = board.board
    alpha.PhasedSplit()(world["b1"], world["b2"], world["b3"])
    Jump(MoveVariant.EXCLUDED)(world["a1"], world["b2"])
    # pop() will break the superposition and only one of the following two states are possible.
    # We check the ancilla to learn if the jump was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_b2_0"]]
    print(target_is_occupied)
    if target_is_occupied:
        assert_samples_in(board, [locations_to_bitboard(["a1", "b2"])])
    else:
        assert_samples_in(board, [locations_to_bitboard(["b2", "b3"])])


def test_jump_excluded_quantum_source_and_target():
    """Both source and target are in quantum state."""
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
    """Source is in quantum state."""
    board = set_board(["a1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    Jump(MoveVariant.BASIC)(world["a2"], world["d1"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["d1"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3"]))


def test_split_jump_classical_source():
    """Source is in classical state."""
    board = set_board(["a1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    board_probabilities = get_board_probability_distribution(board, 1000)
    assert len(board_probabilities) == 2
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a2"]))
    assert_fifty_fifty(board_probabilities, locations_to_bitboard(["a3"]))
    assert world["a2"].type_ == Type.ROOK
    assert world["a2"].color == Color.RED
    assert world["a2"].is_entangled == True
    assert world["a3"].type_ == Type.ROOK
    assert world["a3"].color == Color.RED
    assert world["a3"].is_entangled == True


def test_split_jump_quantum_source():
    """Source is in quantum state."""
    board = set_board(["a1"])
    world = board.board
    alpha.PhasedSplit()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["a3"], world["a4"], world["a5"])
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a2"]): 0.5,
            locations_to_bitboard(["a4"]): 0.25,
            locations_to_bitboard(["a5"]): 0.25,
        },
    )
    assert world["a4"].is_entangled == True
    assert world["a5"].is_entangled == True


def test_merge_jump_perfect_merge():
    """Two quantum pieces split from one source could be merge back to one."""
    board = set_board(["a1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    MergeJump()(world["a2"], world["a3"], world["a1"])
    assert_samples_in(board, {locations_to_bitboard(["a1"]): 1.0})


def test_merge_jump_imperfect_merge_scenario_1():
    """Imperfect merge scenario 1"""
    board = set_board(["a1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["a3"], world["a4"], world["a5"])
    # a2 has prob. 0.5 to be occupied, while a4 has prob. 0.25 to be occupied
    MergeJump()(world["a2"], world["a4"], world["a6"])
    # Accoding to matrix calculations, the ending coefficient of
    # a5 to be occupied: -1/2;
    # a6 to be occupied: 1/2 + i/2/sqrt(2)
    # a4 to be occupied: -i/2 -1/2/sqrt(2)
    # a2 to be occupied: 0
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a5"]): 1.0 / 4,
            locations_to_bitboard(["a6"]): 3.0 / 8,
            locations_to_bitboard(["a4"]): 3.0 / 8,
        },
    )


def test_merge_jump_imperfect_merge_scenario_2():
    """Imperfect merge scenario 2
    Two quantum pieces split from two sources could not be merge into to one.
    """
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    MergeJump()(world["a2"], world["b2"], world["c2"])
    # According to matrix calculations, the ending coefficient of
    # [a3, b3]: 1/2
    # [a3, c2]: i/2/sqrt(2)
    # [a3, b2]: -1/2/sqrt(2)
    # [b3, c2]: i/2/sqrt(2)
    # [b2, b3]: 1/2/sqrt(2)
    # [b2, c2]: 1/2
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a3", "b3"]): 1.0 / 4,
            locations_to_bitboard(["a3", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2"]): 1.0 / 8,
            locations_to_bitboard(["b3", "c2"]): 1.0 / 8,
            locations_to_bitboard(["b2", "b3"]): 1.0 / 8,
            locations_to_bitboard(["b2", "c2"]): 1.0 / 4,
        },
    )


def test_merge_jump_imperfect_merge_scenario_3():
    """Imperfect merge scenario 3.
    This is a simplied version of the scenario above, where we unhook a3 and b3.
    """
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    board.board.unhook(world["a3"])
    board.board.unhook(world["b3"])
    # Now the only quantum pieces in the board are a2 and b2.
    MergeJump()(world["a2"], world["b2"], world["c2"])
    # The expected distribution is same as above by summing over a3 and b3.
    assert_sample_distribution(
        board,
        {
            locations_to_bitboard([]): 1.0 / 4,
            locations_to_bitboard(["c2"]): 1.0 / 4,
            locations_to_bitboard(["b2"]): 1.0 / 4,
            locations_to_bitboard(["b2", "c2"]): 1.0 / 4,
        },
    )


def test_slide_basic_classical_source():
    """Source in classical state."""
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["b1"], world["b2"], world["b3"])

    Slide(["b2"], MoveVariant.BASIC)(world["a1"], world["c1"])

    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a1", "b2"]): 1.0 / 2,
            locations_to_bitboard(["b3", "c1"]): 1.0 / 2,  # success
        },
    )


def test_slide_basic_quantum_source():
    """Source in quantum state."""
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])

    Slide(["b2"], MoveVariant.EXCLUDED)(world["a2"], world["c1"])

    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a2", "b2"]): 1.0 / 4,
            locations_to_bitboard(["a3", "b2"]): 1.0 / 4,
            locations_to_bitboard(["c1", "b3"]): 1.0 / 4,  # success
            locations_to_bitboard(["a3", "b3"]): 1.0 / 4,
        },
    )


def test_slide_basic_quantum_source_with_path_qubits():
    """Source in quantum state + multiple path qubits."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    Slide(["b2", "c2"], MoveVariant.EXCLUDED)(world["a2"], world["d1"])

    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["a2", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a2", "b2", "c3"]): 1.0 / 8,
            locations_to_bitboard(["a2", "b3", "c2"]): 1.0 / 8,
            locations_to_bitboard(["d1", "b3", "c3"]): 1.0 / 8,  # success
            locations_to_bitboard(["a3", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2", "c3"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b3", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b3", "c3"]): 1.0 / 8,
        },
    )


def test_slide_excluded_classical_source():
    """Source in classical state."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    Slide(["b2"], MoveVariant.EXCLUDED)(world["a1"], world["c2"])

    # We check the ancilla to learn if the slide was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_c2_0"]]
    if target_is_occupied:
        # a1 is not moved, while both b2 and b3 are possible.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a1", "b2", "c2"]): 1.0 / 2,
                locations_to_bitboard(["a1", "b3", "c2"]): 1.0 / 2,
            },
        )
    else:
        # a1 could move to c2 if b2 is not there.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a1", "b2", "c3"]): 1.0 / 2,
                locations_to_bitboard(["b3", "c2", "c3"]): 1.0 / 2,  # success
            },
        )


def test_slide_excluded_classical_source():
    """Source in quantum state."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    Slide(["b2"], MoveVariant.EXCLUDED)(world["a2"], world["c2"])

    # We check the ancilla to learn if the slide was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_c2_0"]]
    if target_is_occupied:
        # a2 is not moved, while both b2 and b3 are possible.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a3", "b2", "c2"]): 1.0 / 4,
                locations_to_bitboard(["a3", "b3", "c2"]): 1.0 / 4,
                locations_to_bitboard(["a2", "b2", "c2"]): 1.0 / 4,
                locations_to_bitboard(["a2", "b3", "c2"]): 1.0 / 4,
            },
        )
    else:
        # a2 could move to c2 if b2 is not there.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a2", "b2", "c3"]): 1.0 / 4,
                locations_to_bitboard(["a3", "b2", "c3"]): 1.0 / 4,
                locations_to_bitboard(["b3", "c2", "c3"]): 1.0 / 4,  # success
                locations_to_bitboard(["a3", "b3", "c3"]): 1.0 / 4,
            },
        )


def test_slide_excluded_quantum_source_with_path_qubits():
    """Source in quantum state + multiple path qubits."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    Slide(["b2", "c2"], MoveVariant.EXCLUDED)(world["a2"], world["d2"])

    # We check the ancilla to learn if the slide was applied or not.
    target_is_occupied = world.post_selection[world["ancilla_d2_0"]]
    if target_is_occupied:
        # a2 is not moved, while all path qubits combinations are possible.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a2", "b2", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a2", "b2", "c3", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a2", "b3", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a2", "b3", "c3", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c3", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c3", "d2"]): 1.0 / 8,
            },
        )
    else:
        # a2 could move to d2 if both b2 and c2 are not there.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a2", "b2", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a2", "b2", "c3", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c3", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a2", "b3", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["d2", "b3", "c3", "d3"]): 1.0 / 8,  # success
                locations_to_bitboard(["a3", "b3", "c3", "d3"]): 1.0 / 8,
            },
        )


def test_slide_capture_classical_source_one_path_qubit():
    """Source is in classical state + only one path qubit."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    Slide(["b2"], MoveVariant.CAPTURE)(world["a1"], world["c2"])

    # We check the ancilla to learn if the slide was applied or not.
    path_is_blocked = world.post_selection[world["ancilla_b2_0"]]
    if path_is_blocked:
        # a1 is not moved, while both c2 and c3 are possible.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a1", "b2", "c2"]): 1.0 / 2,
                locations_to_bitboard(["a1", "b2", "c3"]): 1.0 / 2,
            },
        )
    else:
        # a1 moves to c2.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["b3", "c2"]): 1.0 / 2,  # slided and captured
                locations_to_bitboard(["b3", "c2", "c3"]): 1.0
                / 2,  # slided but not captured
            },
        )


def test_slide_capture_quantum_source_multiple_path_qubits():
    """Source in quantum state + multiple path qubits."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    Slide(["b2", "c2"], MoveVariant.CAPTURE)(world["a2"], world["d2"])

    # We check the ancilla to learn if the jump was applied or not.
    # Note: at first there is a ancilla named ancilla_a2d2_0 created.
    # then another ancilla ancilla_ancilla_a2d2_0_0 is created during the
    # force measurement of ancilla_a2d2_0.
    captured = world.post_selection[world["ancilla_ancilla_a2d2_0_0"]]
    if captured:
        # a2 is moved to d2, and the path is clear.
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["b3", "c3", "d2"]): 1.0
                / 2,  # slided and captured
                locations_to_bitboard(["b3", "c3", "d2", "d3"]): 1.0
                / 2,  # slided but not captured
            },
        )
    else:
        # The slide is not made, either because source is not there, or the path is blocked.
        assert_sample_distribution(
            board,
            {
                # cases with blocked path
                locations_to_bitboard(["a2", "b2", "c2", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a2", "b2", "c2", "d3"]): 1.0 / 14,
                locations_to_bitboard(["a2", "b2", "c3", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a2", "b2", "c3", "d3"]): 1.0 / 14,
                locations_to_bitboard(["a2", "b3", "c2", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a2", "b3", "c2", "d3"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b2", "c2", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b2", "c2", "d3"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b2", "c3", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b2", "c3", "d3"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b3", "c2", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b3", "c2", "d3"]): 1.0 / 14,
                # cases where the source is not there
                locations_to_bitboard(["a3", "b3", "c3", "d2"]): 1.0 / 14,
                locations_to_bitboard(["a3", "b3", "c3", "d3"]): 1.0 / 14,
            },
        )


def test_split_slide_classical_source_one_path_clear():
    """Source is in classical state + one path is clear."""
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["b1"], world["b2"], world["b3"])

    SplitSlide(["b2"], [])(world["a1"], world["c1"], world["c2"])

    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["b2", "c2"]): 1.0 / 2,
            locations_to_bitboard(["b3", "c1"]): 1.0 / 4,
            locations_to_bitboard(["b3", "c2"]): 1.0 / 4,
        },
    )


def test_split_slide_quantum_source_multiple_path_qubits():
    """Source in quantum state + multiple path qubits."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    SplitSlide(["b2", "c2"], ["d2"])(world["a2"], world["e1"], world["e2"])

    assert_sample_distribution(
        board,
        {
            # both paths blocked
            locations_to_bitboard(["a2", "b2", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b3", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b2", "c3", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b2", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b3", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b2", "c3", "d2"]): 1.0 / 16,
            # path 0 is clear
            locations_to_bitboard(["a3", "b3", "c3", "d2"]): 1.0 / 16,
            locations_to_bitboard(["e1", "b3", "c3", "d2"]): 1.0 / 16,  # slide to e1
            # path 1 is clear
            locations_to_bitboard(["e2", "b2", "c2", "d3"]): 1.0 / 16,  # slide to e2
            locations_to_bitboard(["e2", "b3", "c2", "d3"]): 1.0 / 16,  # slide to e2
            locations_to_bitboard(["e2", "b2", "c3", "d3"]): 1.0 / 16,  # slide to e2
            locations_to_bitboard(["a3", "b2", "c2", "d3"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b3", "c2", "d3"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b2", "c3", "d3"]): 1.0 / 16,
            # both paths are clear
            locations_to_bitboard(["e1", "b3", "c3", "d3"]): 1.0 / 32,  # slide to e1
            locations_to_bitboard(["e2", "b3", "c3", "d3"]): 1.0 / 32,  # slide to e2
            locations_to_bitboard(["a3", "b3", "c3", "d3"]): 1.0 / 16,
        },
    )


def test_split_slide_quantum_source_overlapped_paths():
    """Source in quantum state + overlapped paths."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    SplitSlide(["b2", "c2"], ["b2"])(world["a2"], world["d1"], world["e1"])

    assert_sample_distribution(
        board,
        {
            # both paths blocked
            locations_to_bitboard(["a2", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a2", "b2", "c3"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2", "c3"]): 1.0 / 8,
            # path 1 is clear
            locations_to_bitboard(["e1", "b3", "c2"]): 1.0 / 8,  # slide to e1
            locations_to_bitboard(["a3", "b3", "c2"]): 1.0 / 8,
            # both paths are clear
            locations_to_bitboard(["e1", "b3", "c3"]): 1.0 / 16,  # slide to e1
            locations_to_bitboard(["d1", "b3", "c3"]): 1.0 / 16,  # slide to d1
            locations_to_bitboard(["a3", "b3", "c3"]): 1.0 / 8,
        },
    )


def test_merge_slide_one_path_clear():
    """One path is clear."""
    board = set_board(["a1", "b1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])

    MergeSlide(["b2"], [])(world["a2"], world["a3"], world["c1"])

    assert_sample_distribution(
        board,
        {
            locations_to_bitboard(["b2", "c1"]): 1.0 / 4,
            locations_to_bitboard(["b2", "a2"]): 1.0 / 4,
            locations_to_bitboard(["b3", "c1"]): 1.0 / 2,
        },
    )


def test_merge_slide_multiple_path_qubits():
    """Multiple path qubits."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    MergeSlide(["b2", "c2"], ["d2"])(world["a2"], world["a3"], world["e1"])

    assert_sample_distribution(
        board,
        {
            # both paths blocked
            locations_to_bitboard(["a2", "b2", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b3", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b2", "c3", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b2", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b3", "c2", "d2"]): 1.0 / 16,
            locations_to_bitboard(["a3", "b2", "c3", "d2"]): 1.0 / 16,
            # path 0 is clear
            locations_to_bitboard(["a3", "b3", "c3", "d2"]): 1.0 / 16,
            locations_to_bitboard(["e1", "b3", "c3", "d2"]): 1.0 / 16,  # success
            # path 1 is clear
            locations_to_bitboard(["a2", "b2", "c2", "d3"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b3", "c2", "d3"]): 1.0 / 16,
            locations_to_bitboard(["a2", "b2", "c3", "d3"]): 1.0 / 16,
            locations_to_bitboard(["e1", "b2", "c2", "d3"]): 1.0 / 16,  # success
            locations_to_bitboard(["e1", "b3", "c2", "d3"]): 1.0 / 16,  # success
            locations_to_bitboard(["e1", "b2", "c3", "d3"]): 1.0 / 16,  # success
            # both paths are clear
            locations_to_bitboard(["e1", "b3", "c3", "d3"]): 1.0 / 8,  # success
        },
    )


def test_merge_slide_overlapped_paths():
    """Overlapped paths."""
    board = set_board(["a1", "b1", "c1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])

    MergeSlide(["b2", "c2"], ["b2"])(world["a2"], world["a3"], world["d1"])

    assert_sample_distribution(
        board,
        {
            # both paths blocked
            locations_to_bitboard(["a2", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2", "c2"]): 1.0 / 8,
            locations_to_bitboard(["a2", "b2", "c3"]): 1.0 / 8,
            locations_to_bitboard(["a3", "b2", "c3"]): 1.0 / 8,
            # path 1 is clear
            locations_to_bitboard(["d1", "b3", "c2"]): 1.0 / 8,  # success
            locations_to_bitboard(["a2", "b3", "c2"]): 1.0 / 8,
            # both paths are clear
            locations_to_bitboard(["d1", "b3", "c3"]): 1.0 / 4,  # success
        },
    )


def test_cannon_fire_classical_source_target():
    """There are one classical piece and one quantum piece in path + both source and target are classical."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["c1"], world["c2"], world["c3"])

    CannonFire(["b1"], ["c2"])(world["a1"], world["d1"])

    # We check the ancilla to learn if the fire was applied or not.
    path_is_blocked = world.post_selection[world["ancilla_c2_0"]]

    if not path_is_blocked:
        assert_samples_in(board, {locations_to_bitboard(["b1", "c3", "d1"]): 1.0})
    else:
        assert_samples_in(board, {locations_to_bitboard(["a1", "b1", "c2", "d1"]): 1.0})


def test_cannon_fire_quantum_source_target():
    # There are one classical piece and one quantum piece in path + both source and target are quantum.
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    CannonFire(["b1"], ["c2"])(world["a2"], world["d2"])

    # We check the ancilla to learn if the fire was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    if not source_is_occupied:
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a3", "b1", "c2", "d2"]): 1.0 / 4,
                locations_to_bitboard(["a3", "b1", "c2", "d3"]): 1.0 / 4,
                locations_to_bitboard(["a3", "b1", "c3", "d2"]): 1.0 / 4,
                locations_to_bitboard(["a3", "b1", "c3", "d3"]): 1.0 / 4,
            },
        )
    else:
        target_is_occupied = world.post_selection[world["ancilla_d2_0"]]
        if not target_is_occupied:
            assert_sample_distribution(
                board,
                {
                    locations_to_bitboard(["a2", "b1", "c2", "d3"]): 1.0 / 2,
                    locations_to_bitboard(["a2", "b1", "c3", "d3"]): 1.0 / 2,
                },
            )
        else:
            path_is_blocked = world.post_selection[world["ancilla_c2_0"]]
            if path_is_blocked:
                assert_samples_in(
                    board, {locations_to_bitboard(["a2", "b1", "c2", "d2"]): 1.0}
                )
            else:
                # successful fire
                assert_samples_in(
                    board, {locations_to_bitboard(["b1", "c3", "d2"]): 1.0}
                )


def test_cannon_fire_multiple_quantum_pieces():
    """There are one classical piece and multiple quantum pieces in path."""
    board = set_board(["a1", "b1", "c1", "d1", "e1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])
    SplitJump()(world["e1"], world["e2"], world["e3"])

    CannonFire(["b1"], ["c2", "d2"])(world["a2"], world["e2"])

    # We check the ancilla to learn if the fire was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    if not source_is_occupied:
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a3", "b1", "c2", "d2", "e2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c2", "d2", "e3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c2", "d3", "e2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c2", "d3", "e3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c3", "d2", "e2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c3", "d2", "e3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c3", "d3", "e2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b1", "c3", "d3", "e3"]): 1.0 / 8,
            },
        )
    else:
        target_is_occupied = world.post_selection[world["ancilla_e2_0"]]
        if not target_is_occupied:
            assert_sample_distribution(
                board,
                {
                    locations_to_bitboard(["a2", "b1", "c2", "d2", "e3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b1", "c2", "d3", "e3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b1", "c3", "d2", "e3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b1", "c3", "d3", "e3"]): 1.0 / 4,
                },
            )
        else:
            captured = world.post_selection[world["ancilla_ancilla_a2e2_0_0"]]
            if not captured:
                assert_sample_distribution(
                    board,
                    {
                        locations_to_bitboard(["a2", "b1", "c2", "d2", "e2"]): 1.0 / 3,
                        locations_to_bitboard(["a2", "b1", "c2", "d3", "e2"]): 1.0 / 3,
                        locations_to_bitboard(["a2", "b1", "c3", "d2", "e2"]): 1.0 / 3,
                    },
                )
            else:
                # successful fire
                assert_samples_in(
                    board, {locations_to_bitboard(["b1", "c3", "d3", "e2"]): 1.0}
                )


def test_cannon_fire_no_classical_piece_in_path():
    """There is no classical piece in path."""
    board = set_board(["a1", "b1", "c1", "d1"])
    world = board.board
    SplitJump()(world["a1"], world["a2"], world["a3"])
    SplitJump()(world["b1"], world["b2"], world["b3"])
    SplitJump()(world["c1"], world["c2"], world["c3"])
    SplitJump()(world["d1"], world["d2"], world["d3"])

    CannonFire([], ["b2", "c2"])(world["a2"], world["d2"])

    # We check the ancilla to learn if the fire was applied or not.
    source_is_occupied = world.post_selection[world["ancilla_a2_0"]]
    if not source_is_occupied:
        assert_sample_distribution(
            board,
            {
                locations_to_bitboard(["a3", "b2", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c3", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b2", "c3", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c2", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c2", "d3"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c3", "d2"]): 1.0 / 8,
                locations_to_bitboard(["a3", "b3", "c3", "d3"]): 1.0 / 8,
            },
        )
    else:
        target_is_occupied = world.post_selection[world["ancilla_d2_0"]]
        if not target_is_occupied:
            assert_sample_distribution(
                board,
                {
                    locations_to_bitboard(["a2", "b2", "c2", "d3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b2", "c3", "d3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b3", "c2", "d3"]): 1.0 / 4,
                    locations_to_bitboard(["a2", "b3", "c3", "d3"]): 1.0 / 4,
                },
            )
        else:
            only_b2_is_occupied_in_path = world.post_selection[
                world["ancilla_ancilla_b2_0_0"]
            ]
            if only_b2_is_occupied_in_path:
                # successful fire
                assert_samples_in(
                    board, {locations_to_bitboard(["b2", "c3", "d2"]): 1.0}
                )
            else:
                only_c2_is_occupied_in_path = world.post_selection[
                    world["ancilla_ancilla_c2_0_0"]
                ]
                if only_c2_is_occupied_in_path:
                    # successful fire
                    assert_samples_in(
                        board, {locations_to_bitboard(["b3", "c2", "d2"]): 1.0}
                    )
                else:
                    assert_sample_distribution(
                        board,
                        {
                            locations_to_bitboard(["a2", "b2", "c2", "d2"]): 1.0 / 2,
                            locations_to_bitboard(["a2", "b3", "c3", "d2"]): 1.0 / 2,
                        },
                    )
