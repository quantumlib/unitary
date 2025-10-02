from unitary.alpha import QuantumEffect
from enums import CheckersRules, CheckersSquare
from typing import Optional
from unitary.alpha.qudit_gates import QuditXGate, QuditISwapPowGate
import cirq
import numpy as np


class QuditSplitGate(cirq.Gate):
    """Performs a sqrt-swap gate between two qudits.

    This gate only swaps two states (either |01> and |10>
    or |02> and |20>), depending on whether initialized
    with either X or O.

    Args:
        square: use TicTacQuare.X to do a sqrtSWAP(01) and
            TicTacSquare.O to do a sqrtSWAP(02)
    """

    def __init__(self, square: CheckersSquare):
        self.square = square
        if self.square not in [CheckersSquare.WHITE, CheckersSquare.BLACK]:
            raise ValueError("Not a valid square: {self.square}")

    def _qid_shape_(self):
        return (3, 3)

    def _unitary_(self):
        arr = np.zeros((9, 9), dtype=np.complex64)
        for x in range(9):
            arr[x, x] = 1
        g = np.exp(1j * np.pi / 4)
        coeff = -1j * g * np.sin(np.pi / 4)
        diag = g * np.cos(np.pi / 4)
        if self.square == CheckersSquare.WHITE:  # Maybe should be black?
            arr[2, 6] = coeff
            arr[6, 2] = coeff
            arr[6, 6] = diag
            arr[2, 2] = diag
        else:
            arr[1, 3] = coeff
            arr[3, 1] = coeff
            arr[3, 3] = diag
            arr[1, 1] = diag
        return arr

    def _circuit_diagram_info_(self, args):
        if not args.use_unicode_characters:
            wire_code = f"Swap{self.square.name}"
            return cirq.CircuitDiagramInfo(wire_symbols=(wire_code, wire_code))
        wire_code = f"×{self.square.name}"
        return cirq.CircuitDiagramInfo(wire_symbols=(wire_code, wire_code))


class CheckersSplit(QuantumEffect):
    """
    Flips a qubit from |0> to |1> then splits to another square.
    Depending on the ruleset, the split is done either using a standard
    sqrt-ISWAP gate
    """

    def __init__(self, checkers_type: CheckersSquare, rules: CheckersRules):
        self.mark = checkers_type
        self.rules = rules

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 3

    def effect(self, *objects):
        source = objects[0]
        target1 = objects[1]
        target2 = objects[2]
        # yield QuditXGate(5, 0, self.mark.value)(square1.qubit)
        yield QuditISwapPowGate(2, 1)(source.qubit, target1.qubit)
        yield QuditISwapPowGate(2, 0.5)(target1.qubit, target2.qubit)
        # yield QuditISwapPowGate(5, 0.5)(square1.qubit, square2.qubit)


class CheckersClassicMove(QuantumEffect):
    """
    Flips a qubit from |0> to |1> then splits to another square.
    Depending on the ruleset, the split is done either using a standard
    sqrt-ISWAP gate
    """

    def __init__(self, checkers_type: CheckersSquare, rules: CheckersRules):
        self.mark = checkers_type
        self.rules = rules

    def num_dimension(self) -> Optional[int]:
        return 2

    def num_objects(self) -> Optional[int]:
        return 2

    def effect(self, *objects):
        source = objects[0]
        target = objects[1]
        yield QuditISwapPowGate(2, 1)(source.qubit, target.qubit)
