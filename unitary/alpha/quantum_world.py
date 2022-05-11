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
from typing import Dict, List, Optional, Sequence, Union
import cirq
import enum

from unitary.alpha.quantum_object import QuantumObject


class QuantumWorld:
    def __init__(
        self, pieces: Optional[List[QuantumObject]] = None, sampler=cirq.Simulator()
    ):
        self.pieces: List[QuantumObject] = []
        if isinstance(pieces, QuantumObject):
            pieces = [pieces]

        self.circuit = cirq.Circuit()
        if pieces is not None:
            for piece in pieces:
                self.add_piece(piece)
        self.sampler = sampler
        self.post_selection: Dict[QuantumObject, int] = {}

    def add_piece(self, piece: QuantumObject):
        self.pieces.append(piece)
        piece.board = self
        initial_piece = piece.initial_gate()
        if initial_piece is not None:
            self.circuit.append(initial_piece)

    def add(self, op: cirq.Operation):
        self.circuit.append(op)

    def peek(
        self,
        pieces: Optional[Sequence[QuantumObject]] = None,
        count: int = 1,
        convert_to_enum: bool = True,
    ) -> List[List[Union[enum.Enum, int]]]:
        measure_circuit = self.circuit.copy()
        if pieces is None:
            pieces = self.pieces
        measure_circuit.append(cirq.measure(*[p.qubit for p in pieces], key="m"))
        results = self.sampler.run(measure_circuit, repetitions=count)

        rtn_list = results.measurements["m"].tolist()
        if convert_to_enum:
            rtn_list = [
                [
                    pieces[piece_idx].enum_type(enum_int)
                    for piece_idx, enum_int in enumerate(result)
                ]
                for result in rtn_list
            ]

        return rtn_list

    def pop(
        self,
        pieces: Optional[Sequence[QuantumObject]] = None,
        convert_to_enum: bool = True,
    ) -> List[Union[enum.Enum, int]]:
        if pieces is None:
            pieces = self.pieces
        results = self.peek(pieces, convert_to_enum=convert_to_enum)
        for idx, result in enumerate(results):
            self.post_selection[pieces[idx]] = result

        return results[0]
