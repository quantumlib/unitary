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
            move_str = [
                self.source_0.name + "^" + self.target_0.name + self.target_1.name
            ]
        elif self.is_merge_move():
            move_str = [
                self.source_0.name + self.source_1.name + "^" + self.target_0.name
            ]
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
            source_is_occupied = world.pop([source_0])[0]
            if not source_is_occupied:
                source_0.reset()
                print("Jump move: source turns out to be empty.")
                return iter(())
            # TODO(): Note: pop and force_measurement could cause other pieces to actually
            # turn back to classical piece or to empty, which is not checked/implemented currently.
            source_0.is_entangled = False
            # TODO(): we should implement and do unhook instead of force_measurement,
            # since there could be cases where target could be almost |1>.
            if target_0.is_entangled:
                world.force_measurement(target_0, 0)
            target_0.reset()
        elif self.move_variant == MoveVariant.EXCLUDED:
            target_is_occupied = world.pop([target_0])[0]
            if target_is_occupied:
                print("Jump move: target turns out to be occupied.")
                target_0.is_entangled = False
                return iter(())
            target_0.reset()
        yield alpha.PhasedMove().effect(source_0, target_0)
        target_0.reset(source_0)
        source_0.reset()
        return iter(())


class SplitJump(QuantumEffect):
    def __init__(
        self,
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
        source_0.is_entangled = True
        yield alpha.PhasedSplit().effect(source_0, target_0, target_1)
        # Pass the classical properties of the source piece to the target pieces.
        target_0.reset(source_0)
        target_1.reset(source_0)
        source_0.reset()
        return iter(())


class MergeJump(QuantumEffect):
    def __init__(
        self,
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
        return iter(())


class Slide(QuantumEffect):
    def __init__(
        self,
        # source_0: Piece,
        # target_0: Piece,
        quantum_path_pieces_0: List[str],
        # board: Board,
        move_variant: MoveVariant,
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
            target_is_occupied = world.pop([target_0])[0]
            if target_is_occupied:
                print("Slide move not applied: target turns out to be occupied.")
                target_0.is_entangled = False
                return iter(())
            # If the target is measured to be empty, then we reset its classical properties to be empty.
            target_0.reset()
        elif self.move_variant == MoveVariant.CAPTURE:
            could_capture = False
            if not source_0.is_entangled and len(quantum_path_pieces_0) == 1:
                if not world.pop(quantum_path_pieces_0)[0]:
                    quantum_path_pieces_0[0].reset()
                    could_capture = True
            else:
                source_0.is_entangled = True
                capture_ancilla = world._add_ancilla(f"{source_0.name}{target_0.name}")
                control_qubits = [source_0] + quantum_path_pieces_0
                yield alpha.quantum_if(*control_qubits).equals(
                    [1] + [0] * len(quantum_path_pieces_0)
                ).apply(alpha.Flip()).effect(capture_ancilla)
                could_capture = world.pop([capture_ancilla])[0]
            if not could_capture:
                # TODO(): in this case non of the path qubits are popped, i.e. the pieces are still entangled and the player
                # could try to do this move again. Is this desired?
                print(
                    "Slide move not applied: either the source turns out be empty, or the path turns out to be blocked."
                )
                return iter(())
            # Apply the capture.
            # TODO(): we should implement and do unhook instead of force_measurement,
            # since there are cases where target could be |1>.
            if target_0.is_entangled:
                world.force_measurement(target_0, 0)
            target_0.reset()
            alpha.PhasedMove()(source_0, target_0)
            # Move the classical properties of the source piece to the target piece.
            target_0.reset(source_0)
            source_0.reset()
            # Force measure the whole path to be empty.
            for path_piece in quantum_path_pieces_0:
                world.force_measurement(path_piece, 0)
                path_piece.reset()
        # For BASIC or EXCLUDED cases
        source_0.is_entangled = True
        alpha.quantum_if(*quantum_path_pieces_0).equals(
            [0] * len(quantum_path_pieces_0)
        ).apply(alpha.PhasedMove())(source_0, target_0)
        # Copy the classical properties of the source piece to the target piece.
        target_0.reset(source_0)
        return iter(())


class SplitSlide(QuantumEffect):
    def __init__(
        self,
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
        quantum_path_pieces_0 = [
            world[path] for path in self.quantum_path_pieces_0 if path != target_1.name
        ]
        quantum_path_pieces_1 = [
            world[path] for path in self.quantum_path_pieces_1 if path != target_0.name
        ]
        source_0.is_entangled = True
        if len(quantum_path_pieces_0) == 0 and len(self.quantum_path_pieces_1) == 0:
            # If both paths are empty, do split jump instead.
            # TODO(): maybe move the above checks (if any path piece is one of the target pieces)
            # into classify_move().
            SplitJump().effect(source_0, target_0, target_1)
            return iter(())
        # TODO(): save ancillas for some specific scenarios.
        path_0_clear_ancilla = world._add_ancilla(f"{source_0.name}{target_0.name}")
        yield alpha.quantum_if(*quantum_path_pieces_0).equals(
            [0] * len(quantum_path_pieces_0)
        ).apply(alpha.Flip()).effect(path_0_clear_ancilla)
        path_1_clear_ancilla = world._add_ancilla(f"{source_0.name}{target_1.name}")
        yield alpha.quantum_if(*quantum_path_pieces_1).equals(
            [0] * len(quantum_path_pieces_1)
        ).apply(alpha.Flip()).effect(path_1_clear_ancilla)

        # We do the normal split if both paths are clear.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 1]
        ).apply(alpha.PhasedMove(0.5)).effect(source_0, target_0)
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 1]
        ).apply(alpha.PhasedMove()).effect(source_0, target_1)

        # Else if only path 0 is clear, we ISWAP source_0 and target_0.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 0]
        ).apply(alpha.PhasedMove()).effect(source_0, target_0)

        # Else if only path 1 is clear, we ISWAP source_0 and target_1.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [0, 1]
        ).apply(alpha.PhasedMove()).effect(source_0, target_1)

        # TODO(): Do we need to zero-out, i.e. reverse those ancillas?
        # Move the classical properties of the source piece to the target pieces.
        target_0.reset(source_0)
        target_1.reset(source_0)
        source_0.reset()
        return iter(())


class MergeSlide(QuantumEffect):
    def __init__(
        self,
        quantum_path_pieces_0: List[str],
        quantum_path_pieces_1: List[str],
    ):
        self.quantum_path_pieces_0 = quantum_path_pieces_0
        self.quantum_path_pieces_1 = quantum_path_pieces_1

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, source_1, target_0 = objects
        world = source_0.world
        quantum_path_pieces_0 = [
            world[path] for path in self.quantum_path_pieces_0 if path != source_1.name
        ]
        quantum_path_pieces_1 = [
            world[path] for path in self.quantum_path_pieces_1 if path != source_0.name
        ]
        target_0.is_entangled = True
        if len(quantum_path_pieces_0) == 0 and len(self.quantum_path_pieces_1) == 0:
            # If both paths are empty, do split slide instead.
            # TODO(): maybe move the above checks (if any path piece is one of the source pieces)
            # into classify_move().
            MergeJump().effect(source_0, source_1, target_0)
            return iter(())
        # TODO(): save ancillas for some specific scenarios.
        path_0_clear_ancilla = world._add_ancilla(f"{source_0.name}{target_0.name}")
        yield alpha.quantum_if(*quantum_path_pieces_0).equals(
            [0] * len(quantum_path_pieces_0)
        ).apply(alpha.Flip()).effect(path_0_clear_ancilla)
        path_1_clear_ancilla = world._add_ancilla(f"{source_1.name}{target_0.name}")
        yield alpha.quantum_if(*quantum_path_pieces_1).equals(
            [0] * len(quantum_path_pieces_1)
        ).apply(alpha.Flip()).effect(path_1_clear_ancilla)

        # We do the normal merge if both paths are clear.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 1]
        ).apply(alpha.PhasedMove(-1.0)).effect(source_0, target_0)
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 1]
        ).apply(alpha.PhasedMove(-0.5)).effect(source_1, target_0)

        # Else if only path 0 is clear, we ISWAP source_0 and target_0.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [1, 0]
        ).apply(alpha.PhasedMove(-1.0)).effect(source_0, target_0)

        # Else if only path 1 is clear, we ISWAP source_1 and target_0.
        yield alpha.quantum_if(path_0_clear_ancilla, path_1_clear_ancilla).equals(
            [0, 1]
        ).apply(alpha.PhasedMove(-1.0)).effect(source_0, target_1)

        # TODO(): Do we need to zero-out, i.e. reverse those ancillas?
        # Move the classical properties of the source pieces to the target piece.
        target_0.reset(source_0)
        source_0.reset()
        source_1.reset()
        return iter(())


class CannonFire(QuantumEffect):
    def __init__(
        self,
        classical_path_pieces_0: List[str],
        quantum_path_pieces_0: List[str],
    ):
        self.classical_path_pieces_0 = classical_path_pieces_0
        self.quantum_path_pieces_0 = quantum_path_pieces_0

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, *objects) -> Iterator[cirq.Operation]:
        source_0, target_0 = objects
        world = source_0.world
        quantum_path_pieces_0 = [world[path] for path in self.quantum_path_pieces_0]
        # Source has to be there to fire.
        print(world.get_binary_probabilities())
        if not world.pop([source_0])[0]:
            source_0.reset()
            print("Cannonn fire not applied: source turns out to be empty.")
            return iter(())
        # Target has to be there to fire.
        if not world.pop([target_0])[0]:
            target_0.reset()
            print("Cannonn fire not applied: target turns out to be empty.")
            return iter(())
        print(world.get_binary_probabilities())
        if len(self.classical_path_pieces_0) == 1:
            # In the case where there already is a cannon platform, the cannon could
            # fire and capture only if quantum_path_pieces_0 are all empty.
            could_capture = False
            if not source_0.is_entangled and len(quantum_path_pieces_0) == 1:
                # Consider this special case to save an ancilla.
                if not world.pop(quantum_path_pieces_0)[0]:
                    quantum_path_pieces_0[0].reset()
                    could_capture = True
            else:
                source_0.is_entangled = True
                capture_ancilla = world._add_ancilla(f"{source_0.name}{target_0.name}")
                # yield alpha.quantum_if(*control_qubits).equals(
                #     [1] + [0] * len(quantum_path_pieces_0)
                # ).apply(alpha.Flip()).effect(capture_ancilla)

                # Note: test not use yield and effect
                control_objects = [source_0] + quantum_path_pieces_0
                alpha.quantum_if(*control_objects).equals(
                    [1] + [0] * len(quantum_path_pieces_0)
                ).apply(alpha.Flip())(capture_ancilla)
                could_capture = world.pop([capture_ancilla])[0]
            if not could_capture:
                # TODO(): in this case non of the path qubits are popped, i.e. the pieces are still entangled and the player
                # could try to do this move again. Is this desired?
                print(
                    "Cannon fire not applied: the source turns out to be empty or the path turns out to be blocked."
                )
                return iter(())
            # Apply the capture.
            # MUST TODO
            # TODO(): we should implement and do unhook instead of force_measurement,
            # since there are cases where target could be |1>.
            # if target_0.is_entangled:
            #     world.force_measurement(target_0, 0)
            world.unhook(target_0)
            target_0.reset()
            alpha.PhasedMove()(source_0, target_0)
            # Move the classical properties of the source piece to the target piece.
            target_0.reset(source_0)
            source_0.reset()
            # Force measure all quantum_path_pieces_0 to be empty.
            for path_piece in quantum_path_pieces_0:
                world.force_measurement(path_piece, 0)
                path_piece.reset()
            return iter(())
        else:
            # In the case where there are no classical path piece but only quantum
            # path piece(s), the cannon could fire and capture only if there is exactly
            # one quantum path piece occupied.
            could_capture = False
            source_0.is_entangled = True
            # TODO(): think a more efficient way of implementing this case.
            for index, expect_occupied_path_piece in enumerate(quantum_path_pieces_0):
                capture_ancilla = world._add_ancilla(
                    f"{expect_occupied_path_piece.name}"
                )
                expected_empty_pieces = [
                    piece
                    for piece in quantum_path_pieces_0
                    if piece.name != expect_occupied_path_piece.name
                ]
                control_qubits = [
                    source_0,
                    expect_occupied_path_piece,
                ] + expected_empty_pieces
                yield alpha.quantum_if(*control_qubits).equals(
                    [1, 1] + [0] * len(expected_empty_pieces)
                ).apply(alpha.Flip()).effect(capture_ancilla)
                could_capture = world.pop([capture_ancilla])[0]
                if could_capture:
                    # Apply the capture.
                    # TODO(): we should implement and do unhook instead of force_measurement,
                    # since there are cases where target could be |1>.
                    if target_0.is_entangled:
                        world.force_measurement(target_0, 0)
                    target_0.reset()
                    yield alpha.PhasedMove().effect(source_0, target_0)
                    # Move the classical properties of the source piece to the target piece.
                    target_0.reset(source_0)
                    source_0.reset()
                    # Force measure all expected_empty_pieces to be empty.
                    for empty_path_piece in expected_empty_pieces:
                        world.force_measurement(empty_path_piece, 0)
                        empty_path_piece.reset()
                    # Force measure the current expect_occupied_path_piece to be occupied.
                    world.force_measurement(expect_occupied_path_piece, 0)
                    expect_occupied_path_piece.is_entangled = False
                    return iter(())
            print(
                "Cannon fire not applied: either the source turns out be empty, or there turns out to be (!=1) occupied path pieces."
            )
            return iter(())
