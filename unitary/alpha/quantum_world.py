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
import copy
import enum

from unitary.alpha.quantum_object import QuantumObject
from unitary.alpha.quantum_effect import QuantumEffect


class QuantumWorld:
    def __init__(
        self, objects: Optional[List[QuantumObject]] = None, sampler=cirq.Simulator()
    ):
        self.objects: List[QuantumObject] = []
        if isinstance(objects, QuantumObject):
            objects = [objects]

        self.circuit = cirq.Circuit()
        self.effect_history = []
        self.sampler = sampler
        self.post_selection: Dict[QuantumObject, int] = {}

        if objects is not None:
            for obj in objects:
                self.add_object(obj)

    def add_object(self, obj: QuantumObject):
        self.objects.append(obj)
        obj.board = self
        obj.initial_effect()

    def add_effect(self, op_list: List[cirq.Operation]):
        """Adds an operation to the current circuit."""
        self.effect_history.append(
            (self.circuit.copy(), copy.copy(self.post_selection))
        )
        for op in op_list:
            self.circuit.append(op)

    def undo_last_effect(self):
        """Restores the `QuantumWorld` to the state before the last effect.

        Note that pop() is considered to be an effect for the purposes
        of this call.
        """
        self.circuit, self.post_selection = self.effect_history.pop()

    def _suggest_num_reps(self, sample_size: int) -> int:
        """Guess the number of raw samples needed to get sample_size results.
        Assume that each post-selection is about 50/50.
        Noise and error mitigation will discard reps, so increase the total
        number of repetitions to compensate.
        """
        if len(self.post_selection) >= 1:
            sample_size <<= len(self.post_selection) + 1
        if sample_size < 100:
            sample_size = 100
        return sample_size

    def peek(
        self,
        objects: Optional[Sequence[QuantumObject]] = None,
        count: int = 1,
        convert_to_enum: bool = True,
        _existing_list: List[List[Union[enum.Enum, int]]] = None,
    ) -> List[List[Union[enum.Enum, int]]]:
        """Measures the state of the system 'non-destructively'.

        This function will measure the state of each object.
        It will _not_ modify the circuit of the QuantumWorld.

        Returns:
           A list of measurement results.  The length of the list will be
           equal to the count parameter.  Each element will be a list
           of measurement results for each object.
        """
        measure_circuit = self.circuit.copy()
        if objects is None:
            objects = self.objects
        measure_set = set(objects + list(self.post_selection.keys()))
        measure_circuit.append(
            [cirq.measure(p.qubit, key=p.qubit.name) for p in measure_set]
        )

        num_reps = self._suggest_num_reps(count)
        if _existing_list is not None:
            num_reps *= 4
        results = self.sampler.run(measure_circuit, repetitions=num_reps)

        # Perform post-selection
        rtn_list = _existing_list or []
        for rep in range(num_reps):
            post_selected = True
            for obj in self.post_selection.keys():
                result = results.measurements[obj.name][rep][0]
                if result != self.post_selection[obj]:
                    post_selected = False
                    break
            if post_selected:
                rtn_list.append(
                    [results.measurements[obj.name][rep] for obj in objects]
                )
                if len(rtn_list) == count:
                    break
        if len(rtn_list) < count:
            # We post-selected too much, get more reps
            return self.peek(objects, count, convert_to_enum, rtn_list)

        if convert_to_enum:
            rtn_list = [
                [
                    objects[idx].enum_type(enum_int)
                    for idx, enum_int in enumerate(result)
                ]
                for result in rtn_list
            ]

        return rtn_list

    def pop(
        self,
        objects: Optional[Sequence[QuantumObject]] = None,
        convert_to_enum: bool = True,
    ) -> List[Union[enum.Enum, int]]:
        self.effect_history.append(
            (self.circuit.copy(), copy.copy(self.post_selection))
        )
        if objects is None:
            objects = self.objects
        results = self.peek(objects, convert_to_enum=convert_to_enum)
        for idx, result in enumerate(results[0]):
            post_selection = result.value if isinstance(result, enum.Enum) else result
            self.post_selection[objects[idx]] = post_selection

        return results[0]
