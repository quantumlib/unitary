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
from typing import Optional, Type, TYPE_CHECKING, Union
import enum

import cirq

from unitary.alpha.qubit_effects import Flip
from unitary.alpha.qudit_effects import Cycle

if TYPE_CHECKING:
    from unitary.alpha.quantum_world import QuantumWorld


class QuantumObject:
    """A Base class representing the state of a quantum object.

    Objects can be initialized by an integer or enum.
    The length of the enum will determine the 'qid_shape' of
    the object.  For instance, enums with two values will be
    qubits, enums with three values will be qutrits, etc.
    """

    def __init__(self, name: str, initial_state: Union[enum.Enum, int]):
        self.board: Optional["QuantumWorld"] = None
        if isinstance(initial_state, int):
            self.initial_state = initial_state
            self.enum_type: Type[Union[int, enum.Enum]] = int
            if initial_state < 2:
                self.num_states = 2
            else:
                self.num_states = initial_state + 1
        elif isinstance(initial_state, enum.Enum):
            self.enum_type = type(initial_state)
            self.num_states = len(self.enum_type)
            self.initial_state = initial_state.value
        else:
            raise ValueError("Unsupported initial state")
        self.name = name
        if self.num_states == 2:
            self.qubit: cirq.Qid = cirq.NamedQubit(name)
        else:
            self.qubit = cirq.NamedQid(name, dimension=self.num_states)

    def initial_effect(self) -> None:
        if self.num_states == 2:
            if self.initial_state == 1:
                Flip()(self)
        else:
            if self.initial_state > 0:
                Cycle(self.num_states, self.initial_state)(self)

        return None

    def __iadd__(self, other: Union[enum.Enum, int]):
        if isinstance(other, int):
            add_num = other
        elif isinstance(other, enum.Enum):
            add_num = other.value
        else:
            return NotImplemented

        if self.board is None:
            self.initial_state = (self.initial_state + add_num) % self.num_states
        else:
            if self.num_states == 2:
                if add_num == 1:
                    Flip()(self)
            else:
                if add_num > 0:
                    Cycle(self.num_states, add_num)(self)
        return self

    def __neg__(self):
        """Adds one to the state."""
        self += 1
