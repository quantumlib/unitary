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


class QuditPlusGate(cirq.Gate):
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
                g = np.exp(1j * np.pi * self.exponent / 2)
                coeff = -1j * g * np.sin(np.pi * self.exponent / 2)
                diag = g * np.cos(np.pi * self.exponent / 2)
                arr[x * self.dimension + y, y * self.dimension + x] = coeff
                arr[x * self.dimension + y, x * self.dimension + y] = diag
        return arr

    def _circuit_diagram_info_(self, args):
        if not args.use_unicode_characters:
            return protocols.CircuitDiagramInfo(
                wire_symbols=("Swap", "Swap"), exponent=self._diagram_exponent(args)
            )
        return protocols.CircuitDiagramInfo(
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
                coeff = 1j * np.sin(np.pi * self.exponent / 2)
                diag = np.cos(np.pi * self.exponent / 2)
                arr[x * self.dimension + y, y * self.dimension + x] = coeff
                arr[x * self.dimension + y, x * self.dimension + y] = diag

        return arr

    def _circuit_diagram_info_(self, args):
        return protocols.CircuitDiagramInfo(
            wire_symbols=("iSwap", "iSwap"), exponent=self._diagram_exponent(args)
        )
