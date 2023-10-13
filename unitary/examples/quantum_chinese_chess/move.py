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


def controlled_operation(gate, qubits, path_qubits, anti_qubits):
    """Apply gate on qubits, controlled by path_qubits and
    anti-controlled by anti_qubits.
    """
    for qubit in anti_qubits:
        yield cirq.X(qubit)
    yield gate.on(*qubits).controlled_by(*path_qubits, *anti_qubits)
    for qubit in anti_qubits:
        yield cirq.X(qubit)


class Move(QuantumEffect):
    """The base class of all chess moves."""

    def __init__(
        self,
        source_0: Piece,
        target_0: Piece,
        board: Board,
        move_type: MoveType,
        move_variant: MoveVariant,
        source_1: Piece = None,
        target_1: Piece = None,
    ):
        self.source_0 = source_0
        self.source_1 = source_1
        self.target_0 = target_0
        self.target_1 = target_1
        self.move_type = move_type
        self.move_variant = move_variant
        self.board = board

    def __eq__(self, other):
        return self.to_str(3) == other.to_str(3)

    def num_dimension(self) -> Optional[int]:
        return 2

    def _verify_objects(self, *objects):
        # TODO(): add checks that apply to all move types
        return

    def effect(self, *objects):
        # TODO(): add effects according to move_type and move_variant
        return

    def is_split_move(self) -> bool:
        return self.target_1 is not None

    def is_merge_move(self) -> bool:
        return self.source_1 is not None

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
            move_str = [self.source_0.name + "^" + self.target_0.name + self.target_1.name]
        elif self.is_merge_move():
            move_str = [self.source_0.name + self.source_1.name + "^" + self.target_0.name]
        else:
            move_str = [self.source_0.name + self.target_0.name]

        if verbose_level > 1:
            move_str.append(self.move_type.name)
            move_str.append(self.move_variant.name)

        if verbose_level > 2:
            move_str.append(
                self.source_0.color.name
                + "_"
                + self.source_0.type_.name
                + "->"
                + self.target_0.color.name
                + "_"
                + self.target_0.type_.name
            )
        return ":".join(move_str)

    def __str__(self):
        return self.to_str()


class Jump(QuantumEffect):
    def __init__(
        self,
        # source_0: Piece,
        # target_0: Piece,
        # board: Board,
        move_variant: MoveVariant,
    ):
        # super().__init__(source_0, target_0, board, move_type=MoveType.JUMP, move_variant=move_variant)
        self.move_variant = move_variant

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        # TODO(): currently pawn capture is a same as jump capture, while in quantum chess it's different,
        # i.e. pawn would only move if the source is there, i.e. CNOT(t, s), and an entanglement could be 
        # created. This could be a general game setting, i.e. we could allow players to choose if they 
        # want the source piece to move (in case of capture) if the target piece is not there.
        source_0, target_0 = objects
        world = source_0.world
        if self.move_variant == MoveVariant.CAPTURE:
            source_is_occupied = world.pop(source_0)
            if not source_is_occupied:
                source_0.reset()
                print("Jump move: source turns out to be empty.")
                return
            source_0.is_entangled = False
            # TODO(): we should implement and do unhook instead of force_measurement,
            # since there could be cases where target could be almost |1>.
            if target_0.is_entangled:
                world.force_measurement(target_0, 0)
            target_0.reset()
        elif self.move_variant == MoveVariant.EXCLUDED:
            target_is_occupied = world.pop(target_0)
            if target_is_occupied:
                print("Jump move: target turns out to be occupied.")
                target_0.is_entangled = False
                return
            target_0.reset()
        alpha.PhasedMove().effect(source_0, target_0)
        target_0.reset(source_0)
        source_0.reset()


class SplitJump(Move):
    def __init__(self,
        # source_0: Piece,
        # target_0: Piece,
        # target_1: Piece,
        # board: Board,
    ):
        # super().__init__(source_0, target_0, board, move_type=MoveType.SPLIT_JUMP, move_variant=MoveVariant.BASIC, target_1 = target_1)
        pass

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, target_0, target_1 = objects
        source_0.is_entangled() = True
        alpha.PhasedSplit().effect(source_0, target_0, target_1)
        # Pass the classical properties of the source piece to the target pieces.
        target_0.reset(source_0)
        target_1.reset(source_0)
        source_0.reset()


class MergeJump(Move):
    def __init__(self,
        # source_0: Piece,
        # source_1: Piece,
        # target_0: Piece,
        # board: Board,
    ):
        # super().__init__(source_0, target_0, board, move_type=MoveType.MERGE_JUMP, move_variant=MoveVariant.BASIC, source_1)
        pass

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, source_1, target_0 = objects
        yield cirq.ISWAP(source_0, target_0) ** -0.5
        yield cirq.ISWAP(source_0, target_0) ** -0.5
        yield cirq.ISWAP(source_1, target_0) ** -0.5
        # Pass the classical properties of the source pieces to the target piece.
        target_0.reset(source_0)
        # TODO(): double check if we should do the following reset().
        source_1.reset()
        source_0.reset()


class Slide(Move):
    def __init__(self,
        # source_0: Piece,
        # target_0: Piece,
        quantum_path_pieces_0: List[str],
        # board: Board,
        move_variant:MoveVariant
    ):
        # super().__init__(source_0, target_0, board, move_type=MoveType.SLIDE, move_variant=move_variant)
        self.quantum_path_pieces_0 = quantum_path_pieces_0
        self.move_variant = move_variant

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, target_0 = objects
        world = source_0.world
        quantum_path_pieces_0 = [world[path] for path in self.quantum_path_pieces_0]
        if self.move_variant == MoveVariant.EXCLUDED:
            target_is_occupied = world.pop(target_0)
            if target_is_occupied:
                print("Slide move not applied: target turns out to be occupied.")
                target_0.is_entangled = False
                return
            # If the target is measured to be empty, then we reset its classical properties to be empty.
            target_0.reset()
        elif self.move_variant == MoveVariant.CAPTURE:
            could_capture = False
            if not source_0.is_entangled and len(quantum_path_pieces_0) == 1:
                if not world.pop(quantum_path_pieces_0[0]):
                    quantum_path_pieces_0[0].reset()
                    could_capture = True
            else:
                source_0.is_entangled = True
                capture_ancilla = world._add_ancilla(f"{source_0.name}{target_0.name}")
                alpha.quantum_if([source_0] + quantum_path_pieces_0).equals([1] + [0] * len(quantum_path_pieces_0)).apply(alpha.Flip()).effect(capture_ancilla)
                could_capture = world.pop(capture_ancilla)
            if not could_capture:
                # TODO(): in this case non of the path qubits are popped, i.e. the pieces are still entangled and the player
                # could try to do this move again. Is this desired?
                print("Slide move not applied: either the source turns out be empty, or the path turns out to be blocked.")
                return
            # Apply the capture.
            # TODO(): we should implement and do unhook instead of force_measurement,
            # since there are cases where target could be |1>.
            if target_0.is_entangled:
                world.force_measurement(target_0, 0)
            target_0.reset()
            alpha.PhasedMove().effect(source_0, target_0)
            # Pass the classical properties of source piece to the target piece.
            target_0.reset(source_0)
            source_0.reset()
            # Force measure the whole path to be empty.
            for path_piece in quantum_path_pieces_0:
                world.force_measurement(path_piece, 0)
                path_piece.reset()
        # For BASIC or EXCLUDED cases
        source_0.is_entangled = True
        alpha.quantum_if(quantum_path_pieces_0).equals([0] * len(quantum_path_pieces_0)).apply(alpha.PhasedMove()).effect(source_0, target_0)
        # Copy the classical properties of the source piece to the target piece.
        target_0.reset(source_0)


class SplitSlide(Move):
    def __init__(self,
        # source_0: Piece,
        # target_0: Piece,
        # target_1: Piece,
        quantum_path_pieces_0: List[str],
        quantum_path_pieces_1: List[str],
        # board: Board,
    ):
        # super().__init__(source_0, target_0, board, move_type=MoveType.SPLIT_SLIDE, move_variant=MoveVariant.BASIC, target_1=target_1)
        self.quantum_path_pieces_0 = quantum_path_pieces_0
        self.quantum_path_pieces_1 = quantum_path_pieces_1

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, target_0, target_1 = objects
        world = source_0.world
        quantum_path_pieces_0 = [world[path] for path in self.quantum_path_pieces_0 if path != target_1.name]
        quantum_path_pieces_1 = [world[path] for path in self.quantum_path_pieces_1 if path != target_0.name]
        if len(quantum_path_pieces_0) ==0 and len(self.quantum_path_pieces_1) == 0:
            # If both paths are empty, do split jump instead.
            # TODO(): maybe move the above checks (if any path piece is one of the target pieces) and
            # into classify_move().
            SplitJump().effect(source_0, target_0, target_1)
            return

