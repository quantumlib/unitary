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

from typing import Iterator, Optional, Sequence, Union, TYPE_CHECKING
import abc
import enum

import cirq

if TYPE_CHECKING:
    from unitary.alpha.quantum_object import QuantumObject


def _to_int(value: Union[enum.Enum, int]) -> int:
    return value.value if isinstance(value, enum.Enum) else value


class QuantumEffect(abc.ABC):
    @abc.abstractmethod
    def effect(self, *objects: "QuantumObject") -> Iterator[cirq.Operation]:
        """Apply the Quantum Effect to the QuantumObjects."""

    def num_dimension(self) -> Optional[int]:
        """Required Qid dimension.  If any allowed, return None."""
        return None

    def num_objects(self) -> Optional[int]:
        """Number of quantum objects allowed.

        If any allowed, return None.
        """
        return None

    def _verify_objects(self, *objects: "QuantumObject"):
        if self.num_objects() is not None and len(objects) != self.num_objects():
            raise ValueError(f"Cannot apply effect to {len(objects)} qubits.")

        required_dimension = self.num_dimension()
        for q in objects:
            if (required_dimension is not None) and (
                q.num_states != required_dimension
            ):
                raise ValueError(
                    f"Cannot apply effect to qids of dimension {q.num_states}."
                )
            if q.world is None:
                raise ValueError(
                    "Object must be added to a QuantumWorld to apply effects."
                )

    def __call__(self, *objects: "QuantumObject"):
        """Apply the Quantum Effect to the objects."""
        self._verify_objects(*objects)
        world = objects[0].world
        world.add_effect(list(self.effect(*objects)))

    def __str__(self):
        return self.__class__.__name__


class QuantumIf:
    """A `QuantumIf` effect allows quantum conditional effects.

    For conditional effects in a quantum world, a quantum if
    can be used, which produces a controlled operation.
    By using this in conjunction with a quantum object in
    superposition, this can produce an entangled state.

    Example usage:

    QuantumIf(qubit).equals(state).apply(effect)(on_qubits)

    Note that the parameters to `apply` must be a quantum
    effect.

    Multiple qubits can be set as the control by inputting
    a list of qubits.  However, the number of states (conditions)
    must equal the number of control qubits.
    """

    def effect(self, *objects: "QuantumObject") -> Iterator[cirq.Operation]:
        return iter(())

    def __call__(self, *objects: "QuantumObject"):
        return QuantumThen(*objects)


class QuantumThen(QuantumEffect):
    def __init__(self, *objects: "QuantumObject"):
        self.control_objects = list(objects)
        self.condition = [1] * len(self.control_objects)
        self.then_effect = None

    def equals(
        self, *conditions: Union[enum.Enum, int, Sequence[Union[enum.Enum, int]]]
    ) -> "QuantumThen":
        """Allows a quantum if condition for qubits to equal certain states.

        Adding an equals after a quantum if can produce an anti-control
        instead of a control if the condition is set to zero.
        """
        # TODO: add qutrit support
        if isinstance(conditions, (enum.Enum, int)):
            conditions = [conditions]
        if len(conditions) != len(self.control_objects):
            raise ValueError(
                f"Not able to equate {len(self.control_objects)} qubits with {len(conditions)} conditions"
            )
        self.condition = [_to_int(cond) for cond in conditions]
        return self

    def then(self, effect: "QuantumEffect"):
        """Use `apply(effect)` instead."""
        return self.apply(effect)

    def apply(self, effect: "QuantumEffect"):
        """Applies a QuantumEffect conditionally to the specified qubits."""
        self.then_effect = effect
        return self

    def effect(self, *objects: "QuantumObject"):
        """A Quantum if/then produces a controlled operation."""
        # For anti-controls, add an X before the controlled operation
        for idx, cond in enumerate(self.condition):
            if cond == 0 and self.control_objects[idx].num_states == 2:
                yield cirq.X(self.control_objects[idx].qubit)

        for op in self.then_effect.effect(*objects):
            yield op.controlled_by(*[q.qubit for q in self.control_objects])

        # For anti-controls, add an X after the controlled operation
        # to revert its state back to what it was.
        for idx, cond in enumerate(self.condition):
            if cond == 0 and self.control_objects[idx].num_states == 2:
                yield cirq.X(self.control_objects[idx].qubit)


quantum_if = QuantumIf()
