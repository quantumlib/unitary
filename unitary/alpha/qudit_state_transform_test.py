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
        # Qubit space representation of the qudit unitary.
        transformed_unitary = qudit_state_transform.qudit_to_qubit_unitary(
            qudit_dim, num_qudits, random_unitary, memoize=True
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
