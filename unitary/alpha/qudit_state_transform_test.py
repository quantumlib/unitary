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

import pytest
import numpy as np
from unitary.alpha import qudit_state_transform


@pytest.mark.parametrize("qudit_dim", range(10))
@pytest.mark.parametrize("num_qudits", range(4))
def test_qudit_state_and_unitary_transform_equivalence(qudit_dim, num_qudits):
    qudit_state_space = qudit_dim**num_qudits
    qudit_unitary_shape = (qudit_state_space, qudit_state_space)
    # Run each configuration with 3 random states and unitaries.
    for i in range(3):
        # Random complex state vector in the qudit space.
        random_state = np.random.rand(qudit_state_space) + 1j * np.random.rand(
            qudit_state_space
        )
        # Random complex unitary in the qudit space.
        random_unitary = np.random.rand(*qudit_unitary_shape) + 1j * np.random.rand(
            *qudit_unitary_shape
        )
        # Apply the unitary on the state vector.
        expected_product = np.matmul(random_unitary, random_state)
        # Qubit space representation of the qudit state vector.
        transformed_state = qudit_state_transform.qudit_to_qubit_state(
            qudit_dim, num_qudits, random_state
        )
        # Qubit space representation of the qudit unitary. Alternate between memoizing or not.
        transformed_unitary = qudit_state_transform.qudit_to_qubit_unitary(
            qudit_dim, num_qudits, random_unitary, memoize=(i % 2)
        )
        # Apply the transformed unitary on the transformed state vector.
        transformed_product = np.matmul(transformed_unitary, transformed_state)
        # Convert the transformed product back to the qudit space.
        product_in_qudit_space = qudit_state_transform.qubit_to_qudit_state(
            qudit_dim, num_qudits, transformed_product
        )
        # Assert that the transform back from qubit space is the inverse of the transform to qubit
        # space.
        np.testing.assert_allclose(
            qudit_state_transform.qubit_to_qudit_state(
                qudit_dim, num_qudits, transformed_state
            ),
            random_state,
        )
        np.testing.assert_allclose(
            qudit_state_transform.qubit_to_qudit_unitary(
                qudit_dim, num_qudits, transformed_unitary
            ),
            random_unitary,
        )
        # Assert that the operations in the qubit space are equivalent to the operations in the
        # qudit space.
        np.testing.assert_allclose(product_in_qudit_space, expected_product)


@pytest.mark.parametrize(
    "qudit_dim, num_qudits, qudit_representation, qubit_representation",
    [
        (
            3,
            2,
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 1]),
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
        ),
        (
            4,
            2,
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
        ),
        (
            3,
            2,
            np.array([1, 0, 0, 0, 0, 0, 0, 0, 1], dtype=np.complex128),
            np.array(
                [
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            ),
        ),
    ],
)
def test_specific_transformations_vectors(
    qudit_dim, num_qudits, qudit_representation, qubit_representation
):
    transformed_vector = qudit_state_transform.qudit_to_qubit_state(
        qudit_dim, num_qudits, qudit_representation
    )
    np.testing.assert_allclose(transformed_vector, qubit_representation)
    untransformed_vector = qudit_state_transform.qubit_to_qudit_state(
        qudit_dim, num_qudits, transformed_vector
    )
    np.testing.assert_allclose(untransformed_vector, qudit_representation)


a = complex(0.5, 0.5)
b = complex(0.5, -0.5)


@pytest.mark.parametrize(
    "qudit_dim, num_qudits, qudit_representation, qubit_representation",
    [
        # Qutrit square root of iSwap.
        (
            3,
            2,
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, a, 0, b, 0, 0, 0, 0, 0],
                    [0, 0, a, 0, 0, 0, b, 0, 0],
                    [0, b, 0, a, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, b, 0, 0, 0, a, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1],
                ]
            ),
            np.array(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, a, 0, 0, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, a, 0, 0, 0, 0, 0, b, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, b, 0, 0, a, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, b, 0, 0, 0, 0, 0, a, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                ]
            ),
        ),
    ],
)
def test_specific_transformations_unitaries(
    qudit_dim, num_qudits, qudit_representation, qubit_representation
):
    transformed_unitary = qudit_state_transform.qudit_to_qubit_unitary(
        qudit_dim, num_qudits, qudit_representation
    )
    np.testing.assert_allclose(transformed_unitary, qubit_representation)
    untransformed_unitary = qudit_state_transform.qubit_to_qudit_unitary(
        qudit_dim, num_qudits, transformed_unitary
    )
    np.testing.assert_allclose(untransformed_unitary, qudit_representation)
