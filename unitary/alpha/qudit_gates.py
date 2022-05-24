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
import numpy as np
import cirq


class QuditXGate(cirq.Gate):
    """Performs a X_ab gate.

    This swaps the |a〉state with the |b〉state,
    where a is the 'source_state' parameter and b is the
    'destination_state' parameter that is passed in.
    All other states are left alone.

    For example, QuditXGate(dimension=3, state=1)
    is a X_01 gate that leaves the |2〉 state alone.
    """

    def __init__(
        self, dimension: int, source_state: int = 0, destination_state: int = 1
    ):
        self.dimension = dimension
        self.source_state = source_state
        self.destination_state = destination_state

    def _qid_shape_(self):
        return (self.dimension,)

    def _unitary_(self):
        arr = np.zeros((self.dimension, self.dimension))
        arr[self.source_state, self.destination_state] = 1
        arr[self.destination_state, self.source_state] = 1
        for i in range(self.dimension):
            if i != self.source_state and i != self.destination_state:
                arr[i, i] = 1
        return arr

    def _circuit_diagram_info_(self, args):
        return f"X({self.source_state}_{self.destination_state})"


class QuditPlusGate(cirq.Gate):
    """Cycles all the states using a permutation gate.

    This gate adds a number to each state.  For instance,
    `QuditPlusGate(dimension=3, addend=1)`
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

    This gate takes the dimension of the qudit (e.g. 3 for qutrits)
    as well as the control and destination gates to produce a
    controlled-X 2-qudit gate.

    Note that there are two parameters for this gate.  The first
    is the control state, which determines when the X gate on the
    second qudit is activated.  For instance, if this is set to 2,
    then the X gate will be activated when the first qudit is
    in the |2> state.

    The state parameter specifies the destination state of the
    second qudit.  For instance, if set to 1, it will perform a
    X_01 gate when activated by the control.
    """

    def __init__(self, dimension: int, control_state: int = 1, state: int = 1):
        self.dimension = dimension
        self.state = state
        self.control_state = control_state

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.zeros((size, size), dtype=np.complex64)
        control_block_offset = self.control_state * self.dimension
        arr[control_block_offset, control_block_offset + self.state] = 1
        arr[control_block_offset + self.state, control_block_offset] = 1
        for x in range(self.dimension):
            for y in range(self.dimension):
                if x != self.control_state or (y != self.state and y != 0):
                    arr[x * self.dimension + y, x * self.dimension + y] = 1
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

    def __init__(self, dimension: int, exponent: int = 1):
        self.dimension = dimension
        self.exponent = exponent

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.zeros((size, size), dtype=np.complex64)
        for x in range(self.dimension):
            for y in range(self.dimension):
                if x == y:
                    arr[x * self.dimension + y][x * self.dimension + y] = 1
                    continue
                g = np.exp(1j * np.pi * self.exponent / 2)
                coeff = -1j * g * np.sin(np.pi * self.exponent / 2)
                diag = g * np.cos(np.pi * self.exponent / 2)
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

    def __init__(self, dimension: int, exponent: int = 1):
        self.dimension = dimension
        self.exponent = exponent

    def _qid_shape_(self):
        return (self.dimension, self.dimension)

    def _unitary_(self):
        size = self.dimension * self.dimension
        arr = np.zeros((size, size), dtype=np.complex64)
        for x in range(self.dimension):
            for y in range(self.dimension):
                if x == y:
                    arr[x * self.dimension + y][x * self.dimension + y] = 1
                    continue
                coeff = 1j * np.sin(np.pi * self.exponent / 2)
                diag = np.cos(np.pi * self.exponent / 2)
                arr[x * self.dimension + y, y * self.dimension + x] = coeff
                arr[x * self.dimension + y, x * self.dimension + y] = diag

        return arr

    def _circuit_diagram_info_(self, args):
        return cirq.CircuitDiagramInfo(
            wire_symbols=("iSwap", "iSwap"), exponent=self._diagram_exponent(args)
        )
