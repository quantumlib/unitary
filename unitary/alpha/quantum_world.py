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
import copy
import enum
from typing import Dict, List, Optional, Sequence, Union
import cirq

from unitary.alpha.quantum_object import QuantumObject


class QuantumWorld:
    def __init__(
        self, objects: Optional[List[QuantumObject]] = None, sampler=cirq.Simulator()
    ):
        self.objects: List[QuantumObject] = []
        if isinstance(objects, QuantumObject):
            objects = [objects]

        self.circuit = cirq.Circuit()
        self.effect_history = []
        self.used_object_keys = set()
        self.sampler = sampler
        self.ancilla_names = set()
        self.post_selection: Dict[QuantumObject, int] = {}

        if objects is not None:
            for obj in objects:
                self.add_object(obj)

    def add_object(self, obj: QuantumObject):
        """Adds a QuantumObject to the QuantumWorld.

        Raises:
            ValueError: if an object with the same name has
               already been added to the world.
        """
        if obj.name in self.used_object_keys:
            raise ValueError("QuantumObject {obj.name} already added to world.")
        self.used_object_keys.add(obj.name)
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

    def force_measurement(
        self, obj: QuantumObject, result: Union[enum.Enum, int]
    ) -> str:
        """Measures a QuantumObject with a defined outcome.

        This function will move the qubit to an ancilla and set
        a post-selection criteria on it in order to force it
        to be a particular result.  A new qubit set to the initial
        state of the result.
        """
        count = 0
        ancilla_name = f"ancilla_{obj.name}_{count}"
        while ancilla_name in self.used_object_keys:
            count += 1
            ancilla_name = f"ancilla_{obj.name}_{count}"
        new_obj = QuantumObject(ancilla_name, result)
        self.add_object(new_obj)
        self.ancilla_names.add(ancilla_name)
        self.circuit = self.circuit.transform_qubits(
            lambda q: q
            if q != obj.qubit and q != new_obj.qubit
            else (new_obj.qubit if q == obj.qubit else obj.qubit)
        )
        post_selection = result.value if isinstance(result, enum.Enum) else result
        self.post_selection[new_obj] = post_selection

    def peek(
        self,
        objects: Optional[Sequence[QuantumObject]] = None,
        count: int = 1,
        convert_to_enum: bool = True,
        _existing_list: List[List[Union[enum.Enum, int]]] = None,
        _num_reps: Optional[int] = None,
    ) -> List[List[Union[enum.Enum, int]]]:
        """Measures the state of the system 'non-destructively'.

        This function will measure the state of each object.
        It will _not_ modify the circuit of the QuantumWorld.

        Returns:
           A list of measurement results.  The length of the list will be
           equal to the count parameter.  Each element will be a list
           of measurement results for each object.
        """
        if _num_reps is None:
            num_reps = self._suggest_num_reps(count)
        else:
            if _num_reps > 1e6:
                raise RecursionError(
                    f"Count {count} reached without sufficient results. "
                    "Likely post-selection error"
                )
            num_reps = _num_reps

        measure_circuit = self.circuit.copy()
        if objects is None:
            objects = self.objects
        measure_set = set(objects + list(self.post_selection.keys()))
        measure_circuit.append(
            [cirq.measure(p.qubit, key=p.qubit.name) for p in measure_set]
        )
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
                    [
                        results.measurements[obj.name][rep]
                        for obj in objects
                        if obj.name not in self.ancilla_names
                    ]
                )
                if len(rtn_list) == count:
                    break
        if len(rtn_list) < count:
            # We post-selected too much, get more reps
            return self.peek(
                objects, count, convert_to_enum, rtn_list, _num_reps=num_reps * 10
            )

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
            self.force_measurement(objects[idx], result)

        return results[0]

    def get_histogram(self,
                      objects: Optional[Sequence[QuantumObject]] = None,
                      count: int = 100
    ) -> List[Dict[int, int]]:
        """Creates histogram based on measurements (peeks) carried out.

        Parameters:
            objects:    List of QuantumObjects
            count:      Number of measurements

        Returns:
            A list with one element for each object. Each element contains a dictionary with
            counts for each state of the given object.
        """
        if not objects:
            objects = self.objects
        peek_results = self.peek(objects=objects,
                                 convert_to_enum=False,
                                 count=count)
        histogram = []
        for obj in objects:
            histogram.append({state: 0 for state in range(obj.num_states)})
        for result in peek_results:
            for idx in range(len(objects)):
                histogram[idx][result[idx][0]] += 1
        return histogram

    def get_probabilities(self,
                          objects : Optional[Sequence[QuantumObject]] = None,
                          count: int = 100
    ) -> List[Dict[int, float]]:
        """Calculates the probabilities based on measurements (peeks) carried out.

        Parameters:
            objects:    List of QuantumObjects
            count:      Number of measurements

        Returns:
            A list with one element for each object. Each element contains a dictionary with
            the probability for each state of the given object.
        """
        histogram = self.get_histogram(objects=objects, count=count)
        probabilities = []
        for obj_hist in histogram:
            probabilities.append(
                {state: obj_hist[state]/count for state in range(len(obj_hist))} )
        return probabilities

    def get_binary_probabilities(self,
                                 objects : Optional[Sequence[QuantumObject]] = None,
                                 count: int = 100
    ) -> List[float]:
        """Calculates the probabilities based on measurements (peeks) carried out.

        Parameters:
            objects:    List of QuantumObjects
            count:      Number of measurements

        Returns:
            A list with one element for each object which contains
            the probability for state!=0.
        """
        full_probs = self.get_probabilities(objects=objects, count=count)
        binary_probs = []
        for one_probs in full_probs:
            binary_probs.append(1-one_probs[0])
        return binary_probs
