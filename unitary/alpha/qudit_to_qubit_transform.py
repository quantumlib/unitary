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


def qudit_to_qubit_state(dim_single_qudit: int, num_qudits: int, qudit_state_vector: np.ndarray, pad_value: np.complex_ = 0):
    """This function converts a qudit-space quantum state vector to m-qubit-per-qudit column vector."""
    num_qubits_per_qudit = np.ceil(np.log(dim_single_qudit)/np.log(2))
    # Reshape the state vector to a `num_qudits` rank tensor.
    state_tensor = qudit_state_vector.reshape((dim_single_qudit,)*num_qudits)
    # Number of extra elements needed in each dimension if represented using qubits.
    padding_amount = int((2**num_qubits_per_qudit)-dim_single_qudit)
    # Expand the number of elements in each dimension by the padding_amount. Fill
    # the new elements with the pad_value.
    padded_state_tensor = np.pad(state_tensor,
                                 (0, padding_amount),
                                 constant_values=pad_value)
    # Return a flattened state vector view of the final tensor.
    return np.ravel(padded_state_tensor)


def qudit_to_qubit_unitary(dim_single_qudit: int, num_qudits: int, qudit_unitary: np.ndarray):
    """This function converts a qudit-space quantum state vector to m-qubit-per-qudit column vector."""
    num_qubits_per_qudit = np.ceil(np.log(dim_single_qudit)/np.log(2))
    num_qubits = num_qubits_per_qudit * num_qudits
    dim_qubit_space = int(2**num_qubits)

    # Treat the unitary as a num_qubits^2 system's state vector and represent it using qubits (pad with 0s).
    padded_unitary = qudit_to_qubit_state(dim_single_qudit, num_qudits**2, np.ravel(qudit_unitary))
    # A qubit-based state vector with the extra padding bits having 1s and rest having 0s.
    pad_qubits_vector = qudit_to_qubit_state(dim_single_qudit, num_qudits, np.zeros(dim_single_qudit**num_qudits), 1)
    # Reshape the padded unitary to the final shape and add a diagonal matrix corresponding to the pad_qubits_vector.
    # This addition ensures that the invalid states with the "padding" bits map to identity, preserving unitarity.
    return padded_unitary.reshape(dim_qubit_space, dim_qubit_space) + np.diag(pad_qubits_vector)
