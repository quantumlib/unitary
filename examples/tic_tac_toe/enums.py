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

from typing import Union
import enum


class GameMoves(enum.Enum):
    """Possible inputs for the ASCII version of tic tac toe."""

    EXIT = "exit"
    MAP = "map"
    HELP = "help"


class TicTacSquare(enum.Enum):
    """Possible states of one tic tac toe square.

    For the quantum version of tic tac toe, these
    are represented as qutrits (qubits with three states).
    """

    EMPTY = 0
    X = 1
    O = 2

    @classmethod
    def from_result(cls, value: Union[enum.Enum, int]):
        if isinstance(value, enum.Enum):
            return cls(value.value)
        return cls(value)


class TicTacResult(enum.Enum):
    """End results of a tic tac toe game.

    Either one side has won or it is a draw.
    If the game has continued past the end state,
    it is possible both sides have completed a three-in-a-row.
    If the game is not complete, the result is UNFINISHED.
    """

    UNFINISHED = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3
    BOTH_WIN = 4


class TicTacRules(enum.Enum):
    """The different rulesets for Quantum TicTacToe.

    The quantum versions differ in the way split moves work, though in all
    cases a split move is implemented by 1) first flipping a square from empty
    to X or O (depending on the player), and then 2) performing a swap operation
    between the two involved squares. In QUANTUM_V2, this is a custom swap that
    takes XE -> XE + EX (and similarly for OE), but *not* XO -> XO + OX. In
    QUANTUM_V3, this latter type of swap *is* included.

    CLASSICAL        = No split moves, just classical TicTacToe.
    QUANTUM_V1       = Split moves only on two empty squares.
    QUANTUM_V2       = Split moves unrestricted, custom gate.
    QUANTUM_V3       = Split moves unrestircted, sqrt-ISWAP gate.
    """

    CLASSICAL = 0
    QUANTUM_V1 = 1
    QUANTUM_V2 = 2
    QUANTUM_V3 = 3
