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
from unitary.examples.quantum_chinese_chess.move import Move
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.enums import MoveType, MoveVariant
import pytest
from string import ascii_lowercase, digits


def global_names():
    global board
    board = Board.from_fen()
    for col in ascii_lowercase[:9]:
        for row in digits:
            globals()[f"{col}{row}"] = board.board[f"{col}{row}"]


def test_move_eq():
    global_names()
    move1 = Move(a1, b2, board, MoveType.MERGE_JUMP, MoveVariant.CAPTURE, c1)
    move2 = Move(a1, b2, board, MoveType.MERGE_JUMP, MoveVariant.CAPTURE, c1)
    move3 = Move(a1, b2, board, MoveType.JUMP, MoveVariant.CAPTURE)
    move4 = Move(a1, b2, board, MoveType.MERGE_SLIDE, MoveVariant.CAPTURE, c1)

    assert move1 == move2
    assert move1 != move3
    assert move1 != move4


def test_move_type():
    # TODO(): change to real senarios
    move1 = Move(a1, b2, board, MoveType.MERGE_JUMP, MoveVariant.CAPTURE, c1)
    assert move1.is_split_move() == False
    assert move1.is_merge_move()

    move2 = Move(a1, b2, board, MoveType.SPLIT_JUMP, MoveVariant.BASIC, target_1=c1)
    assert move2.is_split_move()
    assert move2.is_merge_move() == False

    move3 = Move(a1, b2, board, MoveType.SLIDE, MoveVariant.CAPTURE)
    assert move3.is_split_move() == False
    assert move3.is_merge_move() == False


def test_to_str():
    # TODO(): change to real scenarios
    move1 = Move(a0, a6, board, MoveType.MERGE_JUMP, MoveVariant.CAPTURE, c1)
    assert move1.to_str(0) == ""
    assert move1.to_str(1) == "a0c1^a6"
    assert move1.to_str(2) == "a0c1^a6:MERGE_JUMP:CAPTURE"
    assert move1.to_str(3) == "a0c1^a6:MERGE_JUMP:CAPTURE:BLACK_ROOK->RED_PAWN"

    move2 = Move(a0, b3, board, MoveType.SPLIT_JUMP, MoveVariant.BASIC, target_1=c1)
    assert move2.to_str(0) == ""
    assert move2.to_str(1) == "a0^b3c1"
    assert move2.to_str(2) == "a0^b3c1:SPLIT_JUMP:BASIC"
    assert move2.to_str(3) == "a0^b3c1:SPLIT_JUMP:BASIC:BLACK_ROOK->NA_EMPTY"

    move3 = Move(a0, a6, board, MoveType.SLIDE, MoveVariant.CAPTURE)
    assert move3.to_str(0) == ""
    assert move3.to_str(1) == "a0a6"
    assert move3.to_str(2) == "a0a6:SLIDE:CAPTURE"
    assert move3.to_str(3) == "a0a6:SLIDE:CAPTURE:BLACK_ROOK->RED_PAWN"
