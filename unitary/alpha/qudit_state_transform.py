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
import itertools

import numpy as np
from typing import List


def _nearest_power_of_two_ceiling(qudit_dim: int) -> int:
    if qudit_dim == 0:
        return 0
    # Max index of the single qudit state.
    x = qudit_dim - 1
    # Number of (qu)bits needed to represent the max index.
    bits = 0
    while x:
        x = x >> 1
        bits += 1
    # Total number of states in the qubit representation i.e. Dimension of the single qudit
    # post-conversion.
    return 2**bits


def qudit_to_qubit_state(
    qudit_dimension: int,
    num_qudits: int,
    qudit_state_vector: np.ndarray,
    pad_value: np.complex_ = 0,
):
    """Converts a qudit-space quantum state vector to m-qubit-per-qudit column vector."""
    # Reshape the state vector to a `num_qudits` rank tensor.
    state_tensor = qudit_state_vector.reshape((qudit_dimension,) * num_qudits)
    # Number of extra elements needed in each dimension if represented using qubits.
    padding_amount = _nearest_power_of_two_ceiling(qudit_dimension) - qudit_dimension
    # Expand the number of elements in each dimension by the padding_amount. Fill
    # the new elements with the pad_value.
    padded_state_tensor = np.pad(
        state_tensor, pad_width=(0, padding_amount), constant_values=pad_value
    )
    # Return a flattened state vector view of the final tensor.
    return np.ravel(padded_state_tensor)


def qubit_to_qudit_state(
    qudit_dimension: int,
    num_qudits: int,
    qubit_state_vector: np.ndarray,
):
    """Converts a m-qubit-per-qudit column vector to a qudit-space quantum state vector."""
    mbit_dimension = _nearest_power_of_two_ceiling(qudit_dimension)
    # Reshape the state vector to a `num_qudits` rank tensor.
    state_tensor = qubit_state_vector.reshape((mbit_dimension,) * num_qudits)
    # Shrink the number of elements in each dimension up to the qudit_dimension, ignoring the rest.
    trimmed_state_tensor = state_tensor[(slice(qudit_dimension),) * num_qudits]
    # Return a flattened state vector view of the final tensor.
    return np.ravel(trimmed_state_tensor)


def qudit_to_qubit_unitary(
    qudit_dimension: int,
    num_qudits: int,
    qudit_unitary: np.ndarray,
    memoize: bool = False,
) -> np.ndarray:
    """Converts a qudit-space quantum unitary to m-qubit-per-qudit unitary."""
    dim_qubit_space = _nearest_power_of_two_ceiling(qudit_dimension) ** num_qudits

    if memoize:
        d_to_b_index_map = qubit_to_qudit_state(
            qudit_dimension,
            num_qudits,
            np.array([i + 1 for i in range(dim_qubit_space)]),
        )
        result = np.identity(dim_qubit_space, dtype=qudit_unitary.dtype)
        iter_range = range(qudit_dimension**num_qudits)
        for i, j in itertools.product(iter_range, iter_range):
            result[d_to_b_index_map[i] - 1][d_to_b_index_map[j] - 1] = qudit_unitary[i][
                j
            ]
        return result

    # Treat the unitary as a num_qudits^2 system's state vector and represent it using qubits (pad
    # with 0s).
    padded_unitary = qudit_to_qubit_state(
        qudit_dimension, num_qudits * 2, np.ravel(qudit_unitary)
    )
    # A qubit-based state vector with the extra padding bits having 1s and rest having 0s.
    pad_qubits_vector = qudit_to_qubit_state(
        qudit_dimension, num_qudits, np.zeros(qudit_dimension**num_qudits), 1
    )
    # Reshape the padded unitary to the final shape and add a diagonal matrix corresponding to the
    # pad_qubits_vector. This addition ensures that the invalid states with the "padding" bits map
    # to identity, preserving unitarity.
    return padded_unitary.reshape(dim_qubit_space, dim_qubit_space) + np.diag(
        pad_qubits_vector
    )


def qubit_to_qudit_unitary(
    qudit_dimension: int,
    num_qudits: int,
    qubit_unitary: np.ndarray,
):
    """Converts a m-qubit-per-qudit unitary to a qudit-space quantum unitary."""
    mbit_dimension = _nearest_power_of_two_ceiling(qudit_dimension)
    # Treat unitary as a `num_qudits*2` qudit system state vector.
    effective_num_qudits = num_qudits * 2
    # Reshape the state vector to a `num_qudits*2` rank tensor.
    unitary_tensor = qubit_unitary.reshape((mbit_dimension,) * effective_num_qudits)
    # Shrink the number of elements in each dimension up to the qudit_dimension, ignoring the rest.
    trimmed_unitary_tensor = unitary_tensor[
        (slice(qudit_dimension),) * effective_num_qudits
    ]
    # Return a flat unitary view of the final tensor.
    return trimmed_unitary_tensor.reshape(
        qudit_dimension**num_qudits, qudit_dimension**num_qudits
    )
