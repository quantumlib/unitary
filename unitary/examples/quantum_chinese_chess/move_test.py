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
from unitary.examples.quantum_chinese_chess.move import (
    Move,
    get_move_from_string,
    parse_input_string,
)
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.enums import MoveType, MoveVariant
import pytest


def test_parse_input_string_success():
    assert parse_input_string("a1b1") == (["a1"], ["b1"])
    assert parse_input_string("a1b1^c2") == (["a1", "b1"], ["c2"])
    assert parse_input_string("a1^b1c2") == (["a1"], ["b1", "c2"])


def test_parse_input_string_fail():
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        parse_input_string("a1^b1")
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        parse_input_string("a^1b1c2")
    with pytest.raises(ValueError, match="Two sources should not be the same."):
        parse_input_string("a1a1^c2")
    with pytest.raises(ValueError, match="Two targets should not be the same."):
        parse_input_string("a1^c2c2")
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        parse_input_string("a1b")
    with pytest.raises(ValueError, match="Source and target should not be the same."):
        parse_input_string("a1a1")
    with pytest.raises(ValueError, match="Invalid location string."):
        parse_input_string("a1n1")


def test_get_move_from_string_fail():
    board = Board.from_fen()
    with pytest.raises(ValueError, match="Could not move empty piece."):
        get_move_from_string("a1b1", board)
    with pytest.raises(ValueError, match="Could not move the other player's piece."):
        get_move_from_string("a0b1", board)


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
    # TODO(): change to real senarios
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
    assert move1.to_str(3) == "a0c1^a6:MERGE_JUMP:CAPTURE:BLACK_ROOK->RED_PAWN"

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
    assert move2.to_str(3) == "a0^b3c1:SPLIT_JUMP:BASIC:BLACK_ROOK->NA_EMPTY"

    move3 = Move(
        "a0", "a6", board, move_type=MoveType.SLIDE, move_variant=MoveVariant.CAPTURE
    )
    assert move3.to_str(0) == ""
    assert move3.to_str(1) == "a0a6"
    assert move3.to_str(2) == "a0a6:SLIDE:CAPTURE"
    assert move3.to_str(3) == "a0a6:SLIDE:CAPTURE:BLACK_ROOK->RED_PAWN"
