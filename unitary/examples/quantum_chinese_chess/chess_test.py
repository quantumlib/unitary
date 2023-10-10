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
        game.apply_move("a1b1")
    with pytest.raises(ValueError, match="Could not move the other player's piece."):
        game.apply_move("a0b1")


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
    # The move is blocked by classical path piece.
    with pytest.raises(ValueError, match="The path is blocked."):
        game.check_classical_rule("a0", "a4", ["a3"])

    # Cannon could jump across exactly one piece.
    game.check_classical_rule("b2", "b9", ["b7"])
    with pytest.raises(ValueError, match="Cannon cannot fire like this."):
        game.check_classical_rule("b2", "b9", ["b5", "b7"])
    # Cannon cannot fire to a piece with same color.
    game.board.board["b3"].reset(game.board.board["b2"])
    game.board.board["b2"].reset()
    with pytest.raises(
        ValueError, match="Cannon cannot fire to a piece with same color."
    ):
        game.check_classical_rule("b3", "e3", ["c3"])
    with pytest.raises(ValueError, match="Cannon cannot fire to an empty piece."):
        game.check_classical_rule("b3", "d3", ["c3"])

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
    game.board.board["g4"].reset(
        Piece("g4", SquareState.OCCUPIED, Type.ELEPHANT, Color.BLACK)
    )
    with pytest.raises(ValueError, match="ELEPHANT cannot cross the river"):
        game.check_classical_rule("g4", "i6", [])
    game.board.board["c5"].reset(
        Piece("c5", SquareState.OCCUPIED, Type.ELEPHANT, Color.RED)
    )
    with pytest.raises(ValueError, match="ELEPHANT cannot cross the river"):
        game.check_classical_rule("c5", "e3", [])

    # ADVISOR
    game.check_classical_rule("d9", "e8", [])
    with pytest.raises(ValueError, match="ADVISOR cannot move like this."):
        game.check_classical_rule("d9", "d8", [])
    with pytest.raises(ValueError, match="ADVISOR cannot leave the palace."):
        game.check_classical_rule("d0", "c1", [])
    with pytest.raises(ValueError, match="ADVISOR cannot leave the palace."):
        game.check_classical_rule("f9", "g8", [])

    # KING
    game.check_classical_rule("e9", "e8", [])
    with pytest.raises(ValueError, match="KING cannot move like this."):
        game.check_classical_rule("e9", "d8", [])
    game.board.board["c9"].reset()
    game.board.board["d9"].reset(game.board.board["e9"])
    game.board.board["e9"].reset()
    with pytest.raises(ValueError, match="KING cannot leave the palace."):
        game.check_classical_rule("d9", "c9", [])

    # CANNON
    game.check_classical_rule("b7", "b4", [])
    with pytest.raises(ValueError, match="CANNON cannot move like this."):
        game.check_classical_rule("b7", "a8", [])

    # PAWN
    game.check_classical_rule("a6", "a5", [])
    with pytest.raises(ValueError, match="PAWN cannot move like this."):
        game.check_classical_rule("a6", "a4", [])
    with pytest.raises(
        ValueError, match="PAWN can only go forward before crossing the river"
    ):
        game.check_classical_rule("a6", "b6", [])
    with pytest.raises(
        ValueError, match="PAWN can only go forward before crossing the river"
    ):
        game.check_classical_rule("g3", "h3", [])
    with pytest.raises(ValueError, match="PAWN can not move backward."):
        game.check_classical_rule("a6", "a7", [])
    with pytest.raises(ValueError, match="PAWN can not move backward."):
        game.check_classical_rule("g3", "g2", [])
    # After crossing the rive the pawn could move horizontally.
    game.board.board["c4"].reset(game.board.board["c6"])
    game.board.board["c6"].reset()
    game.check_classical_rule("c4", "b4", [])
    game.check_classical_rule("c4", "d4", [])


def test_classify_move():
    # classical basic
    # classical excluded
    # classical capture
    # jump basic
    # jump excluded
    # jump capture
    # slide basic
    # slide excluded
    # slide capture
    # split_jump basic
    # split_slide basic
    # merge_jump basic
    # merge_slide basic
    # cannon_fire capture
    pass
