# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import Tuple
import unitary.quantum_chess.enums as enums
import unitary.quantum_chess.move as move


@dataclass(frozen=True, eq=True)
class CacheKey:
    move_type: enums.MoveType
    repetitions: int


def cache_key_from_move(m: move.Move, repetitions: int) -> CacheKey:
    return CacheKey(m.move_type or enums.MoveType.NULL_TYPE, repetitions)


@dataclass(frozen=True)
class ProbabilityHistory:
    """Stores square occupancy histogram for a point in the move history.

    Args:
        repetitions: number of samples used to generate probabilities
        probabilities: maps square -> probability of being occupied
        full_squares: (derived from self.probabilities) full squares bitboard
        empty_squares: (derived from self.probabilities) empty squares bitboard
    """

    repetitions: int
    probabilities: Tuple[float, ...]  # for each square
    full_squares: int  # bitboard derived from square_probabilities
    empty_squares: int  # bitboard derived from square_probabilities
