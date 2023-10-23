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
import copy
import enum
from typing import cast, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union
import cirq

from unitary.alpha.quantum_object import QuantumObject
from unitary.alpha.sparse_vector_simulator import PostSelectOperation, SparseSimulator
from unitary.alpha.qudit_state_transform import qudit_to_qubit_unitary, num_bits


class QuantumWorld:
    """A collection of `QuantumObject`s with effects.

    This object represents an entire state of a quantum game.
    This includes all the `QuantumObjects` as well as the effects
    that have been applied to them.  It also includes all
    criteria of measurement so that repetitions of the circuit
    will be the same even if some of the quantum objects have
    already been meaaured,

    This object also has a history so that effects can be undone.

    This object should be initialized with a sampler that determines
    how to evaluate the quantum game state.  If not specified, this
    defaults to the built-in cirq Simulator.

    Setting the `compile_to_qubits` option results in an internal state
    representation of ancilla qubits for every qudit in the world. That
    also results in the effects being applied to the corresponding qubits
    instead of the original qudits.
    """

    def __init__(
        self,
        objects: Optional[List[QuantumObject]] = None,
        sampler=cirq.Simulator(),
        compile_to_qubits: bool = False,
    ):
        self.clear()
        self.sampler = sampler
        self.use_sparse = isinstance(sampler, SparseSimulator)
        self.compile_to_qubits = compile_to_qubits

        if isinstance(objects, QuantumObject):
            objects = [objects]
        if objects is not None:
            for obj in objects:
                self.add_object(obj)

    def clear(self) -> None:
        """Removes all objects and effects from this QuantumWorld.

        This will reset the QuantumWorld to an empty state.
        """
        self.circuit = cirq.Circuit()
        self.effect_history: List[Tuple[cirq.Circuit, Dict[QuantumObject, int]]] = []
        self.object_name_dict: Dict[str, QuantumObject] = {}
        self.ancilla_names: Set[str] = set()
        # When `compile_to_qubits` is True, this tracks the mapping of the
        # original qudits to the compiled qubits.
        self.compiled_qubits: Dict[cirq.Qid, List[cirq.Qid]] = {}
        self.post_selection: Dict[QuantumObject, int] = {}

    def copy(self) -> "QuantumWorld":
        new_objects = []
        new_post_selection: Dict[QuantumObject, int] = {}
        for obj in self.object_name_dict.values():
            new_obj = copy.copy(obj)
            new_objects.append(new_obj)
            if obj in self.post_selection:
                new_post_selection[new_obj] = self.post_selection[obj]
        new_world = self.__class__(
            objects=new_objects,
            sampler=self.sampler,
            compile_to_qubits=self.compile_to_qubits,
        )
        new_world.circuit = self.circuit.copy()
        new_world.ancilla_names = self.ancilla_names.copy()
        new_world.effect_history = [
            (circuit.copy(), copy.copy(post_selection))
            for circuit, post_selection in self.effect_history
        ]
        new_world.post_selection = new_post_selection
        return new_world

    def add_object(self, obj: QuantumObject):
        """Adds a QuantumObject to the QuantumWorld.

        Raises:
            ValueError: if an object with the same name has
               already been added to the world.
        """
        if obj.name in self.object_name_dict:
            raise ValueError("QuantumObject {obj.name} already added to world.")
        self.object_name_dict[obj.name] = obj
        obj.world = self
        if self.compile_to_qubits:
            qudit_dim = obj.qubit.dimension
            if qudit_dim == 2:
                self.compiled_qubits[obj.qubit] = [obj.qubit]
            else:
                self.compiled_qubits[obj.qubit] = []
                for qubit_num in range(num_bits(qudit_dim)):
                    new_obj = self._add_ancilla(obj.qubit.name)
                    self.compiled_qubits[obj.qubit].append(new_obj.qubit)
        obj.initial_effect()

    @property
    def objects(self) -> List[QuantumObject]:
        return list(self.object_name_dict.values())

    @property
    def public_objects(self) -> List[QuantumObject]:
        """All non-ancilla objects in the world."""
        return [
            obj
            for obj in self.object_name_dict.values()
            if obj.name not in self.ancilla_names
        ]

    def get_object_by_name(self, name: str) -> Optional[QuantumObject]:
        """Returns the object with the given name.

        If the object with that name does not exist in this QuantumWorld,
        the function returns None.
        """
        return self.object_name_dict.get(name)

    def combine_with(self, other_world: "QuantumWorld"):
        """Combines all the objects from the specified world into this one.

        This will add all the objects as well as all the effects into the
        current world.  The passed in world then becomes unusable.

        Note that the effect history is cleared when this function is called,
        so previous effects cannot be undone.
        """
        my_keys = set(self.object_name_dict.keys())
        other_keys = set(other_world.object_name_dict.keys())
        if my_keys.intersection(other_keys):
            raise ValueError("Cannot combine two worlds with overlapping object keys")
        if self.use_sparse != other_world.use_sparse:
            raise ValueError("Cannot combine sparse simulator world with non-sparse")
        self.object_name_dict.update(other_world.object_name_dict)
        self.ancilla_names.update(other_world.ancilla_names)
        self.compiled_qubits.update(other_world.compiled_qubits)
        self.post_selection.update(other_world.post_selection)
        self.circuit = self.circuit.zip(other_world.circuit)
        # Clear effect history, since undoing would undo the combined worlds
        self.effect_history.clear()
        # Clear the other world so that objects cannot be used from that world.
        other_world.clear()

    def _add_ancilla(
        self, namespace: str, value: Union[enum.Enum, int] = 0
    ) -> QuantumObject:
        """Adds an ancilla qudit object with a unique name.

        Args:
            namespace: Custom string to be added in the name
            value: The value for the ancilla qudit

        Returns:
            The added ancilla object.
        """
        count = 0
        ancilla_name = f"ancilla_{namespace}_{count}"
        while ancilla_name in self.object_name_dict:
            count += 1
            ancilla_name = f"ancilla_{namespace}_{count}"
        new_obj = QuantumObject(ancilla_name, value)
        self.add_object(new_obj)
        self.ancilla_names.add(ancilla_name)
        return new_obj

    def _append_op(self, op: cirq.Operation):
        """Add the operation in a way designed to speed execution.

        For the sparse simulator post-selections should be as early as possible to cut
        down the state size. Also X's since they don't increase the size.
        """

        if (
            not self.use_sparse
            or isinstance(op, PostSelectOperation)
            or op.gate is cirq.X
        ):
            strategy = cirq.InsertStrategy.EARLIEST
        else:
            strategy = cirq.InsertStrategy.NEW

        if self.compile_to_qubits:
            op = self._compile_op(op)

        self.circuit.append(op, strategy=strategy)

    def _compile_op(self, op: cirq.Operation) -> Union[cirq.Operation, cirq.OP_TREE]:
        """Compiles the operation down to qubits, if needed."""
        qid_shape = cirq.qid_shape(op)
        if len(set(qid_shape)) > 1:
            # TODO(#77): Add support for arbitrary Qid shapes to
            #  `qudit_state_transform`.
            raise ValueError(
                f"Found operation shape {qid_shape}. Compiling operations with"
                " a mix of different dimensioned qudits is not supported yet."
            )
        qudit_dim = qid_shape[0]
        if qudit_dim == 2:
            return op
        num_qudits = len(qid_shape)
        compiled_qubits = []
        for qudit in op.qubits:
            compiled_qubits.extend(self.compiled_qubits[qudit])

        if isinstance(op, PostSelectOperation):
            # Spread the post-selected value across the compiled qubits using the
            # big endian convention.
            value_bits = cirq.big_endian_int_to_bits(
                op.value, bit_count=len(compiled_qubits)
            )
            return [
                PostSelectOperation(qubit, value)
                for qubit, value in zip(compiled_qubits, value_bits)
            ]

        # Compile the input unitary to a target qubit-based unitary.
        compiled_unitary = qudit_to_qubit_unitary(
            qudit_dimension=qudit_dim,
            num_qudits=num_qudits,
            qudit_unitary=cirq.unitary(op),
        )
        return cirq.MatrixGate(
            matrix=compiled_unitary, qid_shape=(2,) * len(compiled_qubits)
        ).on(*compiled_qubits)

    def add_effect(self, op_list: List[cirq.Operation]):
        """Adds an operation to the current circuit."""
        self.effect_history.append(
            (self.circuit.copy(), copy.copy(self.post_selection))
        )
        for op in op_list:
            self._append_op(op)

    def undo_last_effect(self):
        """Restores the `QuantumWorld` to the state before the last effect.

        Note that pop() is considered to be an effect for the purposes
        of this call.

        Raises:
            IndexError if there are no effects in the history.
        """
        if not self.effect_history:
            raise IndexError("No effects to undo")
        self.circuit, self.post_selection = self.effect_history.pop()

    def _suggest_num_reps(self, sample_size: int) -> int:
        """Guess the number of raw samples needed to get sample_size results.
        Assume that each post-selection is about 50/50.
        Noise and error mitigation will discard reps, so increase the total
        number of repetitions to compensate.
        """
        if self.use_sparse:
            return sample_size
        if len(self.post_selection) >= 1:
            sample_size <<= len(self.post_selection) + 1
        if sample_size < 100:
            sample_size = 100
        return sample_size

    def _interpret_result(self, result: Union[int, Iterable[int]]) -> int:
        """Canonicalize an entry from the measurement results array to int.

        When `compile_to_qubit` is set, the results are expected to be a
        sequence of bits that are the binary representation of the measurement
        of the original key. Returns the `int` represented by the bits.

        If the input is a single-element Iterable, returns the first element.
        """
        if self.compile_to_qubits:
            # For a compiled qudit, the results will be a bit array
            # representing an integer outcome.
            return cirq.big_endian_bits_to_int(result)
        if isinstance(result, Iterable):
            # If it is a single-element iterable, return the first element.
            result_list = list(result)
            if len(result_list) != 1:
                raise ValueError(
                    f"Cannot interpret a multivalued iterable {result} as a "
                    "single result for a non-compiled world."
                )
            return result_list[0]
        return result

    def force_measurement(
        self, obj: QuantumObject, result: Union[enum.Enum, int]
    ) -> None:
        """Measures a QuantumObject with a defined outcome.

        This function will move the qubit to an ancilla and set
        a post-selection criteria on it in order to force it
        to be a particular result.  A new qubit set to the initial
        state of the result.
        """
        new_obj = self._add_ancilla(namespace=obj.name, value=result)
        # Swap the input and ancilla qubits using a remapping dict.
        qubit_remapping_dict = {obj.qubit: new_obj.qubit, new_obj.qubit: obj.qubit}
        if self.compile_to_qubits:
            # Swap the compiled qubits.
            obj_qubits = self.compiled_qubits.get(obj.qubit, [obj.qubit])
            new_obj_qubits = self.compiled_qubits.get(new_obj.qubit, [new_obj.qubit])
            qubit_remapping_dict.update(
                {*zip(obj_qubits, new_obj_qubits), *zip(new_obj_qubits, obj_qubits)}
            )

        self.circuit = self.circuit.transform_qubits(
            lambda q: qubit_remapping_dict.get(q, q)
        )
        post_selection = result.value if isinstance(result, enum.Enum) else result
        self.post_selection[new_obj] = post_selection
        if self.use_sparse:
            self._append_op(PostSelectOperation(new_obj.qubit, post_selection))

    def peek(
        self,
        objects: Optional[Sequence[Union[QuantumObject, str]]] = None,
        count: int = 1,
        convert_to_enum: bool = True,
        _existing_list: Optional[List[List[Union[enum.Enum, int]]]] = None,
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
            quantum_objects = self.public_objects
        else:
            quantum_objects = [
                self[obj_or_str] if isinstance(obj_or_str, str) else obj_or_str
                for obj_or_str in objects
            ]
        measure_set = set(quantum_objects)
        measure_set.update(self.post_selection.keys())
        measure_circuit.append(
            [
                cirq.measure(
                    self.compiled_qubits.get(p.qubit, p.qubit), key=p.qubit.name
                )
                for p in measure_set
            ]
        )
        results = self.sampler.run(measure_circuit, repetitions=num_reps)

        # Perform post-selection
        rtn_list = _existing_list or []
        for rep in range(num_reps):
            post_selected = True
            for obj in self.post_selection.keys():
                result = self._interpret_result(results.measurements[obj.name][rep])
                if result != self.post_selection[obj]:
                    post_selected = False
                    break
            if post_selected:
                rtn_list.append(
                    [
                        self._interpret_result(results.measurements[obj.name][rep])
                        for obj in quantum_objects
                    ]
                )
                if len(rtn_list) == count:
                    break
        if len(rtn_list) < count:
            # We post-selected too much, get more reps
            return self.peek(
                quantum_objects,
                count,
                convert_to_enum,
                rtn_list,
                _num_reps=num_reps * 10,
            )

        if convert_to_enum:
            rtn_list = [
                [quantum_objects[idx].enum_type(meas) for idx, meas in enumerate(res)]
                for res in rtn_list
            ]

        return rtn_list

    def pop(
        self,
        objects: Optional[Sequence[Union[QuantumObject, str]]] = None,
        convert_to_enum: bool = True,
    ) -> List[Union[enum.Enum, int]]:
        self.effect_history.append(
            (self.circuit.copy(), copy.copy(self.post_selection))
        )
        if objects is None:
            quantum_objects = self.public_objects
        else:
            quantum_objects = [
                self[obj_or_str] if isinstance(obj_or_str, str) else obj_or_str
                for obj_or_str in objects
            ]
        results = self.peek(quantum_objects, convert_to_enum=convert_to_enum)
        for idx, result in enumerate(results[0]):
            self.force_measurement(quantum_objects[idx], result)

        return results[0]

    def get_histogram(
        self, objects: Optional[Sequence[QuantumObject]] = None, count: int = 100
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
            objects = self.public_objects
        peek_results = self.peek(objects=objects, convert_to_enum=False, count=count)
        histogram = []
        for obj in objects:
            histogram.append({state: 0 for state in range(obj.num_states)})
        for result in peek_results:
            for idx in range(len(objects)):
                histogram[idx][cast(int, result[idx])] += 1
        return histogram

    def get_probabilities(
        self, objects: Optional[Sequence[QuantumObject]] = None, count: int = 100
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
                {state: obj_hist[state] / count for state in range(len(obj_hist))}
            )
        return probabilities

    def get_binary_probabilities(
        self, objects: Optional[Sequence[QuantumObject]] = None, count: int = 100
    ) -> List[float]:
        """Calculates the total probabilities for all non-zero states
        based on measurements (peeks) carried out.

        Parameters:
            objects:    List of QuantumObjects
            count:      Number of measurements

        Returns:
            A list with one element for each object which contains
            the probability for the event state!=0. Which is the same as
            1.0-Probability(state==0).
        """
        full_probs = self.get_probabilities(objects=objects, count=count)
        binary_probs = []
        for one_probs in full_probs:
            binary_probs.append(1 - one_probs[0])
        return binary_probs

    def __getitem__(self, name: str) -> QuantumObject:
        quantum_object = self.object_name_dict.get(name, None)
        if not quantum_object:
            raise KeyError(f"{name} did not exist in this world.")
        return quantum_object
