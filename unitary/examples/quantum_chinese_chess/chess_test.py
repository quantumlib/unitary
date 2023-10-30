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
import pytest
import io
import sys
from unitary.examples.quantum_chinese_chess.chess import QuantumChineseChess
from unitary.examples.quantum_chinese_chess.piece import Piece
from unitary.examples.quantum_chinese_chess.enums import (
    Language,
    Color,
    Type,
    SquareState,
    MoveType,
    MoveVariant,
)


def test_game_init(monkeypatch):
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    output = io.StringIO()
    sys.stdout = output
    game = QuantumChineseChess()
    assert game.lang == Language.ZH
    assert game.players_name == ["Bob", "Ben"]
    assert game.current_player == 0
    assert "Welcome" in output.getvalue()
    sys.stdout = sys.__stdout__


def test_parse_input_string_success(monkeypatch):
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    assert game.parse_input_string("a1b1") == (["a1"], ["b1"])
    assert game.parse_input_string("a1b1^c2") == (["a1", "b1"], ["c2"])
    assert game.parse_input_string("a1^b1c2") == (["a1"], ["b1", "c2"])


def test_parse_input_string_fail(monkeypatch):
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        game.parse_input_string("a1^b1")
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        game.parse_input_string("a^1b1c2")
    with pytest.raises(ValueError, match="Two sources should not be the same."):
        game.parse_input_string("a1a1^c2")
    with pytest.raises(ValueError, match="Two targets should not be the same."):
        game.parse_input_string("a1^c2c2")
    with pytest.raises(ValueError, match="Invalid sources/targets string "):
        game.parse_input_string("a1b")
    with pytest.raises(ValueError, match="Source and target should not be the same."):
        game.parse_input_string("a1a1")
    with pytest.raises(ValueError, match="Invalid location string."):
        game.parse_input_string("a1n1")


def test_apply_move_fail(monkeypatch):
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    with pytest.raises(ValueError, match="Could not move empty piece."):
        game.apply_move("a8b8")
    with pytest.raises(ValueError, match="Could not move the other player's piece."):
        game.apply_move("a9b8")
    with pytest.raises(ValueError, match="Two sources need to be the same type."):
        game.apply_move("a0a3^a4")
    with pytest.raises(ValueError, match="Two targets need to be the same type."):
        game.apply_move("b2^a2h2")
    with pytest.raises(ValueError, match="Two targets need to be the same color."):
        game.apply_move("b2^b7h2")


def test_game_invalid_move(monkeypatch):
    output = io.StringIO()
    sys.stdout = output
    inputs = iter(["y", "Bob", "Ben", "a1n1", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    game.play()
    assert (
        "Invalid location string. Make sure they are from a0 to i9."
        in output.getvalue()
    )
    sys.stdout = sys.__stdout__


def test_check_classical_rule(monkeypatch):
    output = io.StringIO()
    sys.stdout = output
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    board = game.board.board
    # The move is blocked by classical path piece.
    with pytest.raises(ValueError, match="The path is blocked."):
        game.check_classical_rule("a0", "a4", ["a3"])

    # Target should not be a classical piece of the same color.
    with pytest.raises(
        ValueError, match="The target place has classical piece with the same color."
    ):
        game.check_classical_rule("a0", "a3", [])

    # ROOK
    game.check_classical_rule("a0", "a2", [])
    with pytest.raises(ValueError, match="ROOK cannot move like this."):
        game.check_classical_rule("a0", "b1", [])

    # HORSE
    game.check_classical_rule("b0", "c2", [])
    with pytest.raises(ValueError, match="HORSE cannot move like this."):
        game.check_classical_rule("b0", "c1", [])

    # ELEPHANT
    game.check_classical_rule("c0", "e2", [])
    with pytest.raises(ValueError, match="ELEPHANT cannot move like this."):
        game.check_classical_rule("c0", "e1", [])
    board["g5"].reset(Piece("g5", SquareState.OCCUPIED, Type.ELEPHANT, Color.BLACK))
    with pytest.raises(ValueError, match="ELEPHANT cannot cross the river"):
        game.check_classical_rule("g5", "i3", [])
    board["c4"].reset(Piece("c4", SquareState.OCCUPIED, Type.ELEPHANT, Color.RED))
    with pytest.raises(ValueError, match="ELEPHANT cannot cross the river"):
        game.check_classical_rule("c4", "e6", [])

    # ADVISOR
    game.check_classical_rule("d9", "e8", [])
    with pytest.raises(ValueError, match="ADVISOR cannot move like this."):
        game.check_classical_rule("d9", "d8", [])
    with pytest.raises(ValueError, match="ADVISOR cannot leave the palace."):
        game.check_classical_rule("d9", "c8", [])
    with pytest.raises(ValueError, match="ADVISOR cannot leave the palace."):
        game.check_classical_rule("f0", "g1", [])

    # KING
    game.check_classical_rule("e9", "e8", [])
    with pytest.raises(ValueError, match="KING cannot move like this."):
        game.check_classical_rule("e9", "d8", [])
    board["c0"].reset()
    board["d0"].reset(board["e0"])
    board["e0"].reset()
    with pytest.raises(ValueError, match="KING cannot leave the palace."):
        game.check_classical_rule("d0", "c0", [])

    # CANNON
    game.check_classical_rule("b7", "b4", [])
    with pytest.raises(ValueError, match="CANNON cannot move like this."):
        game.check_classical_rule("b7", "a8", [])
    # Cannon could jump across exactly one piece.
    game.check_classical_rule("b2", "b9", ["b7"])
    with pytest.raises(ValueError, match="CANNON cannot fire like this."):
        game.check_classical_rule("b2", "b9", ["b5", "b7"])
    # Cannon cannot fire to a piece with same color.
    board["b3"].reset(board["b2"])
    board["b2"].reset()
    board["e3"].is_entangled = True
    with pytest.raises(
        ValueError, match="CANNON cannot fire to a piece with same color."
    ):
        game.check_classical_rule("b3", "e3", ["c3"])
    with pytest.raises(ValueError, match="CANNON cannot fire to an empty piece."):
        game.check_classical_rule("b3", "d3", ["c3"])

    # PAWN
    game.check_classical_rule("a3", "a4", [])
    with pytest.raises(ValueError, match="PAWN cannot move like this."):
        game.check_classical_rule("a3", "a5", [])
    with pytest.raises(
        ValueError, match="PAWN can only go forward before crossing the river"
    ):
        game.check_classical_rule("e3", "f3", [])
    with pytest.raises(
        ValueError, match="PAWN can only go forward before crossing the river"
    ):
        game.check_classical_rule("g6", "h6", [])
    with pytest.raises(ValueError, match="PAWN can not move backward."):
        game.check_classical_rule("a3", "a2", [])
    with pytest.raises(ValueError, match="PAWN can not move backward."):
        game.check_classical_rule("g6", "g7", [])
    # After crossing the rive the pawn could move horizontally.
    board["c4"].reset(board["c6"])
    board["c6"].reset()
    game.check_classical_rule("c4", "b4", [])
    game.check_classical_rule("c4", "d4", [])


def test_classify_move_fail(monkeypatch):
    output = io.StringIO()
    sys.stdout = output
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    board = game.board.board
    with pytest.raises(
        ValueError, match="CANNON could not fire/capture without a cannon platform."
    ):
        game.classify_move(["b7"], ["b2"], [], [], [], [])

    with pytest.raises(
        ValueError, match="Both sources need to be in quantum state in order to merge."
    ):
        game.classify_move(["b2", "h2"], ["e2"], [], [], [], [])

    board["c0"].reset(board["b7"])
    board["c0"].is_entangled = True
    board["b7"].reset()
    board["g0"].reset(board["h7"])
    board["g0"].is_entangled = True
    board["h7"].reset()
    with pytest.raises(ValueError, match="Currently CANNON cannot merge while firing."):
        game.classify_move(["c0", "g0"], ["e0"], ["d0"], [], ["f0"], [])

    board["b3"].reset(board["b2"])
    board["b3"].is_entangled = True
    board["b2"].reset()
    board["d3"].reset(board["h2"])
    board["d3"].is_entangled = True
    board["h2"].reset()
    with pytest.raises(
        ValueError, match="Currently we could only merge into an empty piece."
    ):
        game.classify_move(["b3", "d3"], ["c3"], [], [], [], [])

    with pytest.raises(ValueError, match="Currently CANNON cannot split while firing."):
        game.classify_move(["g0"], ["e0", "i0"], ["f0"], [], ["h0"], [])

    board["d0"].is_entangled = True
    with pytest.raises(
        ValueError, match="Currently we could only split into empty pieces."
    ):
        game.classify_move(["d3"], ["d0", "d4"], [], [], [], [])

    board["d0"].reset()
    board["f0"].reset()
    with pytest.raises(ValueError, match="King split is not supported currently."):
        game.classify_move(["e0"], ["d0", "f0"], [], [], [], [])


def test_classify_move_success(monkeypatch):
    output = io.StringIO()
    sys.stdout = output
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    board = game.board.board
    # classical
    assert game.classify_move(["h9"], ["g7"], [], [], [], []) == (
        MoveType.CLASSICAL,
        MoveVariant.CLASSICAL,
    )
    assert game.classify_move(["b2"], ["b9"], ["b7"], [], [], []) == (
        MoveType.CLASSICAL,
        MoveVariant.CLASSICAL,
    )

    # jump basic
    board["c9"].is_entangled = True
    assert game.classify_move(["c9"], ["e7"], [], [], [], []) == (
        MoveType.JUMP,
        MoveVariant.BASIC,
    )
    board["b2"].is_entangled = True
    assert game.classify_move(["b2"], ["e2"], [], [], [], []) == (
        MoveType.JUMP,
        MoveVariant.BASIC,
    )

    # jump excluded
    board["a3"].is_entangled = True
    assert game.classify_move(["a0"], ["a3"], [], [], [], []) == (
        MoveType.JUMP,
        MoveVariant.EXCLUDED,
    )

    # jump capture
    board["g4"].reset(board["g6"])
    board["g4"].is_entangled = True
    board["g6"].reset()
    assert game.classify_move(["g4"], ["g3"], [], [], [], []) == (
        MoveType.JUMP,
        MoveVariant.CAPTURE,
    )

    # slide basic
    assert game.classify_move(["a0"], ["a4"], [], ["a3"], [], []) == (
        MoveType.SLIDE,
        MoveVariant.BASIC,
    )

    # slide excluded
    board["i7"].reset(board["h7"])
    board["i7"].is_entangled = True
    board["h7"].reset()
    board["i6"].is_entangled = True
    assert game.classify_move(["i9"], ["i6"], [], ["i7"], [], []) == (
        MoveType.SLIDE,
        MoveVariant.EXCLUDED,
    )

    # slide capture
    assert game.classify_move(["a0"], ["a6"], [], ["a3"], [], []) == (
        MoveType.SLIDE,
        MoveVariant.CAPTURE,
    )

    # split_jump basic
    assert game.classify_move(["g4"], ["f4", "h4"], [], [], [], []) == (
        MoveType.SPLIT_JUMP,
        MoveVariant.BASIC,
    )

    # split_slide basic
    board["d3"].reset(board["h2"])
    board["h2"].reset()
    board["c3"].is_entangled = True
    board["e3"].is_entangled = True
    assert game.classify_move(["d3"], ["b3", "f3"], [], ["c3"], [], ["e3"]) == (
        MoveType.SPLIT_SLIDE,
        MoveVariant.BASIC,
    )

    # merge_jump basic
    board["b7"].is_entangled = True
    assert game.classify_move(["b7", "i7"], ["e7"], [], [], [], []) == (
        MoveType.MERGE_JUMP,
        MoveVariant.BASIC,
    )

    # merge_slide basic
    assert game.classify_move(["b7", "i7"], ["a7"], [], [], [], ["b7"]) == (
        MoveType.MERGE_SLIDE,
        MoveVariant.BASIC,
    )

    # cannon_fire capture
    assert game.classify_move(["i7"], ["i3"], [], ["i6"], [], []) == (
        MoveType.CANNON_FIRE,
        MoveVariant.CAPTURE,
    )
    board["i6"].is_entangled = False
    assert game.classify_move(["i7"], ["i3"], ["i6"], [], [], []) == (
        MoveType.CANNON_FIRE,
        MoveVariant.CAPTURE,
    )


def test_update_board_by_sampling(monkeypatch):
    output = io.StringIO()
    sys.stdout = output
    inputs = iter(["y", "Bob", "Ben"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    game = QuantumChineseChess()
    board = game.board.board

    board.unhook(board["a0"])
    board["a0"].type_ = Type.ROOK
    board["a0"].color = Color.RED
    board["a0"].is_entangled = True

    # Verify that the method would set a0 to classically empty.
    game.update_board_by_sampling()
    assert board["a0"].type_ == Type.EMPTY
    assert board["a0"].color == Color.NA
    assert board["a0"].is_entangled == False

    board["a1"].is_entangled = True
    # Verify that the method would set a1 to classically occupied.
    game.update_board_by_sampling()
    assert board["a1"].is_entangled == False
