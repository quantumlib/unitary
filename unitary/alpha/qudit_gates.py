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

from typing import List, Dict, Optional, Tuple

import numpy as np
import cirq


class QuditXGate(cirq.Gate):
    """Performs a X_ab gate.

    This swaps the |a〉state with the |b〉state,
    where a is the 'source_state' parameter and b is the
    'destination_state' parameter that is passed in.
    All other states are left alone.

    For example, QuditXGate(dimension=3, source_state=0, destination_state=1)
    is a X_01 gate that leaves the |2〉state alone.
    """

    def __init__(
        self, dimension: int, source_state: int = 0, destination_state: int = 1
    ):
        self.dimension = dimension
        self.source_state = source_state
        self.destination_state = destination_state
        if self.source_state >= self.dimension:
            raise ValueError("Source state must be smaller than dimension.")
        if self.destination_state >= self.dimension:
            raise ValueError("Destination state must be smaller than dimension.")

    def _qid_shape_(self):
        return (self.dimension,)

    def _unitary_(self):
        arr = np.eye(self.dimension)
        if self.source_state != self.destination_state:
            arr[self.source_state, self.source_state] = 0
            arr[self.destination_state, self.destination_state] = 0
            arr[self.source_state, self.destination_state] = 1
            arr[self.destination_state, self.source_state] = 1
        return arr

    def _circuit_diagram_info_(self, args):
        return f"X({self.source_state}_{self.destination_state})"


class QuditRzGate(cirq.EigenGate):
    """Phase shifts a single state basis of the qudit.

    A generalization of the phase shift gate to qudits.
    https://en.wikipedia.org/wiki/Quantum_logic_gate#Phase_shift_gates

    Implements Z_d as defined in eqn (5) of https://arxiv.org/abs/2008.00959
    with the addition of a state parameter for convenience.
    For a qudit of dimensionality d, shifts the phase of |phased_state> by radians.

    Args:
        dimension: Dimension of the qudits. For instance, a dimension of 3
          would be a qutrit.
        radians: The phase shift applied to the |phased_state>, measured in
          radians.
        phased_state: Optional index of the state to be phase shifted. Defaults
          to phase shifting the state |dimension-1>.
    """

    _cached_eigencomponents: Dict[int, List[Tuple[float, np.ndarray]]] = {}

    def __init__(
        self, dimension: int, radians: float = np.pi, phased_state: Optional[int] = None
    ):
        super().__init__(exponent=radians / np.pi, global_shift=0)
        self.dimension = dimension
        if phased_state is not None:
            if phased_state >= dimension or phased_state < 0:
                raise ValueError(
                    f"state {phased_state} is not valid for a qudit of"
                    f" dimension {dimension}."
                )
            self.phased_state = phased_state
        else:
            self.phased_state = self.dimension - 1

    def _qid_shape_(self):
        return (self.dimension,)

    def _eigen_components(self) -> List[Tuple[float, np.ndarray]]:
        eigen_key = (self.dimension, self.phased_state)
        if eigen_key not in QuditRzGate._cached_eigencomponents:
            components = []
            for i in range(self.dimension):
                half_turns = 0
                m = np.zeros((self.dimension, self.dimension))
                m[i][i] = 1
                if i == self.phased_state:
                    half_turns = 1
                components.append((half_turns, m))
            QuditRzGate._cached_eigencomponents[eigen_key] = components
        return QuditRzGate._cached_eigencomponents[eigen_key]

    def _circuit_diagram_info_(self, args):
        return cirq.CircuitDiagramInfo(
            wire_symbols=("Z_d"), exponent=self._format_exponent_as_angle(args)
        )

    def _with_exponent(self, exponent: float) -> "QuditRzGate":
        return QuditRzGate(
                dimension=self.dimension,
                radians=exponent * np.pi,
                phased_state=self.phased_state)


class QuditPlusGate(cirq.Gate):
    """Cycles all the states by `addend` using a permutation gate.
    This gate adds a number to each state. For instance,`QuditPlusGate(dimension=3, addend=1)`
    will cycle state vector (a, b, c) to (c, a, b), and will cycle state |0> to |1>, |1> to |2>, |2> to |0>.
    """

    def __init__(self, dimension: int, addend: int = 1):
        self.dimension = dimension
        self.addend = addend

    def _qid_shape_(self):
        return (self.dimension,)

    def _unitary_(self):
        arr = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            arr[(i + self.addend) % self.dimension, i] = 1
        return arr

    def _circuit_diagram_info_(self, args):
        return f"[+{self.addend}]"


class QuditControlledXGate(cirq.Gate):
    """A Qudit controlled-X gate.

    This gate takes the dimension of the qudit as well as the control and destination states to produce a
    controlled-X 2-qudit gate.

    Args:
        dimension: dimension of the qudits, for instance, a dimension of 3 would be a qutrit.
        control_state: the state of first qudit that when satisfied the X gate on the second qudit will be activated.
          For instance, if `control_state` is set to 2, then the X gate will be
          activated when the first qudit is in the |2> state.
        state: the destination state of the second qudit. For instance, if set to 1, it will perform a
          X_01 gate when activated by `control_state`.
    """

    def __init__(self, dimension: int, control_state: int = 1, state: int = 1):
        self.dimension = dimension
        self.state = state
        self.control_state = control_state

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.eye(size, dtype=np.complex64)
        control_block_offset = self.control_state * self.dimension
        arr[control_block_offset, control_block_offset] = 0
        arr[control_block_offset + self.state, control_block_offset + self.state] = 0
        arr[control_block_offset, control_block_offset + self.state] = 1
        arr[control_block_offset + self.state, control_block_offset] = 1
        return arr


class QuditSwapPowGate(cirq.Gate):
    """Performs a swap gate between two qudits.

    This is the equivalent of a SWAP gate for qubits.
    This gate will swap the states of two qudits.

    Args:
        dimension: dimension of the qudits, for instance,
          a dimension of 3 would be a qutrit.
        exponent: The amount to swap qubits.  For instance,
          an exponent of 1 would be a full swap and an
          exponent of 0.5 would be a square root of swap gate.

    """

    def __init__(self, dimension: int, exponent: float = 1):
        self.dimension = dimension
        self.exponent = exponent

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.zeros((size, size), dtype=np.complex64)
        g = np.exp(1j * np.pi * self.exponent / 2)
        coeff = -1j * g * np.sin(np.pi * self.exponent / 2)
        diag = g * np.cos(np.pi * self.exponent / 2)
        for x in range(self.dimension):
            for y in range(self.dimension):
                if x == y:
                    arr[x * self.dimension + y][x * self.dimension + y] = 1
                    continue
                arr[x * self.dimension + y, y * self.dimension + x] = coeff
                arr[x * self.dimension + y, x * self.dimension + y] = diag
        return arr

    def _circuit_diagram_info_(self, args):
        if not args.use_unicode_characters:
            return cirq.CircuitDiagramInfo(
                wire_symbols=("Swap", "Swap"), exponent=self._diagram_exponent(args)
            )
        return cirq.CircuitDiagramInfo(
            wire_symbols=("×", "×"), exponent=self._diagram_exponent(args)
        )


class QuditISwapPowGate(cirq.Gate):
    """Performs a swap gate between two qudits with a swap phase of i.

    This is the equivalent of a ISWAP gate for qubits.
    This gate will swap the states of two qudits with an
    additional phase of i per swap.

    Args:
        dimension: dimension of the qudits, for instance,
          a dimension of 3 would be a qutrit.
        exponent: The amount to swap qubits.  For instance,
          an exponent of 1 would be a full swap and an
          exponent of 0.5 would be a square root of iswap gate.
    """

    def __init__(self, dimension: int, exponent: float = 1):
        self.dimension = dimension
        self.exponent = exponent

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.zeros((size, size), dtype=np.complex64)
        coeff = 1j * np.sin(np.pi * self.exponent / 2)
        diag = np.cos(np.pi * self.exponent / 2)
        for x in range(self.dimension):
            for y in range(self.dimension):
                if x == y:
                    arr[x * self.dimension + y][x * self.dimension + y] = 1
                    continue
                arr[x * self.dimension + y, y * self.dimension + x] = coeff
                arr[x * self.dimension + y, x * self.dimension + y] = diag

        return arr

    def _circuit_diagram_info_(self, args):
        return cirq.CircuitDiagramInfo(
            wire_symbols=("iSwap", "iSwap"), exponent=self._diagram_exponent(args)
        )


class QuditHadamardGate(cirq.Gate):
    """Performs a Hadamard operation on the given qudit.
    This is the equivalent of a H gate for qubits. When applied to a given pure state,
    the state will be transformed to a (equal, in terms of absolute magnitude) superposition of
    all pure states.
    Args:
        dimension: dimension of the qudits, for instance,
          a dimension of 3 would be a qutrit.
    """

    def __init__(self, dimension: int):
        self.dimension = dimension

    def _qid_shape_(self):
        return (self.dimension,)

    def _unitary_(self):
        arr = (
            1.0
            / np.sqrt(self.dimension)
            * np.ones((self.dimension, self.dimension), dtype=np.complex64)
        )
        w = np.exp(1j * 2 * np.pi / self.dimension)
        # Note: this unitary matrice always has first row and first column elements equal to one,
        # so we only do calculation for rest of the elements.
        for i in range(1, self.dimension):
            for j in range(1, self.dimension):
                arr[i, j] *= w ** (i * j)
        return arr

    def _circuit_diagram_info_(self, args):
        return cirq.CircuitDiagramInfo(
            wire_symbols=("H", "H"), exponent=self._diagram_exponent(args)
        )
