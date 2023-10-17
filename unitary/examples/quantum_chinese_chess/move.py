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
from unitary.examples.quantum_chinese_chess.board import Board
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


class Jump(QuantumEffect):
    """Jump from source_0 to target_0. The accepted move_variant includes
    - CLASSICAL (where all classical moves will be handled here)
    - CAPTURE
    - EXCLUDED
    - BASIC
    """

    def __init__(
        self,
        move_variant: MoveVariant,
    ):
        self.move_variant = move_variant

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        # TODO(): currently pawn capture is a same as jump capture, while in quantum chess it's different,
        # i.e. pawn would move only if the target is there, i.e. CNOT(t, s), and an entanglement could be
        # created. This could be a general game setting, i.e. we could allow players to choose if they
        # want the source piece to move (in case of capture) if the target piece is not there.
        source_0, target_0 = objects
        world = source_0.world
        if self.move_variant == MoveVariant.CAPTURE:
            # We peek and force measure source_0.
            source_is_occupied = world.pop([source_0])[0]
            # For move_variant==CAPTURE, we require source_0 to be occupied before further actions.
            # This is to prevent a piece of the board containing two types of different pieces.
            if not source_is_occupied:
                # If source_0 turns out to be not there, we clear set it to be EMPTY, and the jump
                # could not be made.
                source_0.reset()
                print("Jump move: source turns out to be empty.")
                return iter(())
            source_0.is_entangled = False
            # We replace the qubit of target_0 with a new ancilla, and set its classical properties to be EMPTY.
            world.unhook(target_0)
            target_0.reset()
        elif self.move_variant == MoveVariant.EXCLUDED:
            # We peek and force measure target_0.
            target_is_occupied = world.pop([target_0])[0]
            # For move_variant==EXCLUDED, we require target_0 to be empty before further actions.
            # This is to prevent a piece of the board containing two types of different pieces.
            if target_is_occupied:
                # If target_0 turns out to be there, we set it to be a classically OCCUPIED, and
                # the jump could not be made.
                print("Jump move: target turns out to be occupied.")
                target_0.is_entangled = False
                return iter(())
            # Otherwise we set target_0 to be classically EMPTY.
            target_0.reset()
        elif self.move_variant == MoveVariant.CLASSICAL:
            if target_0.type_ != Type.EMPTY:
                # For classical moves with target_0 occupied, we replace the qubit of target_0 with
                # a new ancilla, and set its classical properties to be EMPTY.
                world.unhook(target_0)
                target_0.reset()

        # Make the jump move.
        alpha.PhasedMove()(source_0, target_0)
        # Move the classical properties of the source piece to the target piece.
        target_0.reset(source_0)
        source_0.reset()
        return iter(())
