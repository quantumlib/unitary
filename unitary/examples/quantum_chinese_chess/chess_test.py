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
import mock
import io
import sys
from unitary.examples.quantum_chinese_chess.chess import QuantumChineseChess
from unitary.examples.quantum_chinese_chess.enums import Language


def test_game_init():
    with mock.patch("builtins.input", side_effect=["y", "Bob", "Ben"]):
        game = QuantumChineseChess()
        assert game.lang == Language.ZH
        assert game.players_name == ["Bob", "Ben"]
        assert game.current_player == 0


def test_game_invalid_move():
    output = io.StringIO()
    sys.stdout = output
    with mock.patch("builtins.input", side_effect=["y", "Bob", "Ben", "a1n1", "exit"]):
        #        with pytest.raises(ValueError, match = "Invalid location string. Make sure they are from a0 to i9."):
        game = QuantumChineseChess()
        game.play()
        assert (
            "Invalid location string. Make sure they are from a0 to i9."
            in output.getvalue()
        )
    sys.stdout = sys.__stdout__
