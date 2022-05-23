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
    """Performs a X_0a gate.

    This swaps the |0〉state with the |a〉state,
    where a is the 'state' paramter that is passed in.

    For example, QuditXGate(dimension=3, state=1)
    is a X_01 gate that leaves the |2〉 state alone.
    """

    def __init__(self, dimension: int, state: int = 1):
        self.dimension = dimension
        self.state = state

    def _qid_shape_(self):
        return (self.dimension,)

    def _unitary_(self):
        arr = np.zeros((self.dimension, self.dimension))
        arr[0, self.state] = 1
        arr[self.state, 0] = 1
        for i in range(self.dimension):
            if i != 0 and i != self.state:
                arr[i, i] = 1
        return arr

    def _circuit_diagram_info_(self, args):
        return f"X(0_{self.state})"


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
