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
from unitary.examples.quantum_chinese_chess.enums import Language


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
