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
from typing import Optional, List, Tuple, Iterator
import cirq
from unitary import alpha
from unitary.alpha.quantum_effect import QuantumEffect
from unitary.examples.quantum_chinese_chess.board import *
from unitary.examples.quantum_chinese_chess.piece import Piece
from unitary.examples.quantum_chinese_chess.enums import MoveType, MoveVariant, Type


# TODO(): now the class is no longer the base class of all chess moves. Maybe convert this class
# to a helper class to save each move (with its pop results) in a string form into move history.
class Move(QuantumEffect):
    """The base class of all chess moves."""

    def __init__(
        self,
        source: str,
        target: str,
        board: Board,
        source2: Optional[str] = None,
        target2: Optional[str] = None,
        move_type: Optional[MoveType] = None,
        move_variant: Optional[MoveVariant] = None,
    ):
        self.source = source
        self.source2 = source2
        self.target = target
        self.target2 = target2
        self.move_type = move_type
        self.move_variant = move_variant
        self.board = board

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.source == other.source
                and self.source2 == other.source2
                and self.target == other.target
                and self.target2 == other.target2
                and self.move_type == other.move_type
                and self.move_variant == other.move_variant
            )
        return False

    def _verify_objects(self, *objects):
        # TODO(): add checks that apply to all move types
        return

    def effect(self, *objects):
        # TODO(): add effects according to move_type and move_variant
        return

    def is_split_move(self) -> bool:
        return self.target2 is not None

    def is_merge_move(self) -> bool:
        return self.source2 is not None

    def to_str(self, verbose_level: int = 1) -> str:
        """Constructs the string representation of the move.
        According to the value of verbose_level:
        - 1: only returns the move source(s) and target(s);
        - 2: additionally returns the move type and variant;
        - 3: additionally returns the source(s) and target(s) piece type and color.
        """
        if verbose_level < 1:
            return ""

        if self.is_split_move():
            move_str = [self.source + "^" + self.target + str(self.target2)]
        elif self.is_merge_move():
            move_str = [self.source + str(self.source2) + "^" + self.target]
        else:
            move_str = [self.source + self.target]

        if verbose_level > 1:
            move_str.append(self.move_type.name)
            move_str.append(self.move_variant.name)

        if verbose_level > 2:
            source = self.board.board[self.source]
            target = self.board.board[self.target]
            move_str.append(
                source.color.name
                + "_"
                + source.type_.name
                + "->"
                + target.color.name
                + "_"
                + target.type_.name
            )
        return ":".join(move_str)

    def __str__(self):
        return self.to_str()


class SplitJump(QuantumEffect):
    """SplitJump from source_0 to target_0 and target_1. The only accepted (default) move_variant is
    - BASIC.
    """

    def __init__(
        self,
    ):
        return

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, target_0, target_1 = objects
        # Make the split jump.
        source_0.is_entangled = True
        alpha.PhasedSplit()(source_0, target_0, target_1)
        # Pass the classical properties of the source piece to the target pieces.
        target_0.reset(source_0)
        target_1.reset(source_0)
        return iter(())


class MergeJump(QuantumEffect):
    """MergeJump from source_0 to source_1 to target_0. The only accepted (default) move_variant is
    - BASIC.
    """

    def __init__(
        self,
    ):
        return

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, source_1, target_0 = objects
        # Make the merge jump.
        alpha.PhasedMove(-0.5)(source_0, target_0)
        alpha.PhasedMove(-0.5)(source_0, target_0)
        alpha.PhasedMove(-0.5)(source_1, target_0)
        # Pass the classical properties of the source pieces to the target piece.
        target_0.reset(source_0)
        return iter(())
