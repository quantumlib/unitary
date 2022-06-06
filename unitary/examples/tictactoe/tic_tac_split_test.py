# Copyright 2022 Google
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
import pytest

import unitary.alpha as alpha
import unitary.examples.tictactoe as tictactoe


@pytest.mark.parametrize("mark", [tictactoe.TicTacSquare.X, tictactoe.TicTacSquare.O])
def test_tic_tact_split(mark: tictactoe.TicTacSquare):
    a = alpha.QuantumObject("a", tictactoe.TicTacSquare.EMPTY)
    b = alpha.QuantumObject("b", tictactoe.TicTacSquare.EMPTY)
    board = alpha.QuantumWorld([a, b])
    tictactoe.TicTacSplit(mark)(a, b)
    results = board.peek(count=1000)
    on_a = [tictactoe.TicTacSquare.EMPTY, mark]
    on_b = [mark, tictactoe.TicTacSquare.EMPTY]
    assert any(r == on_a for r in results)
    assert any(r == on_b for r in results)
    assert all(r == on_a or r == on_b for r in results)
