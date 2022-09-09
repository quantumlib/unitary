"""Noiseless simulator using a sparse state vector.

Just enough features to support Unitary are implemented.

Supports standard unitary Cirq gates, plus a post-selection operator.

Does not work with 3+-state qudits. TODO: integrate with qutrit-to-qubit conversion
when that is available.
"""
import cirq
import numpy as np


# TODO: Is this a good number?
_EPSILON = 1e-14


class SparseSimulationState(cirq.SimulationState):
    """Implements sparse state vector evolution and sampling.

    Uses object arrays to represent states so that circuits with more than 64
    qubits work.
    """

    def __init__(self, qubits):
        super().__init__(qubits=qubits, state=None)
        self._states = np.array([0], dtype=object)
        self._amplitudes = np.array([1], dtype=np.complex128)

    def copy(self):
        raise NotImplementedError

    def _act_on_fallback_(self, action, qubits, allow_decompose):
        if action.gate is cirq.X:
            self._states ^= 1 << self.qubit_map[qubits[0]]
        else:
            # Create a matrix (partitioned_state) where each nonzero entry corresponds
            # to an element of the sparse state vector. The row indicates the value of
            # the qubits acted on by the unitary, the column indicates the value of the
            # remaining qubits, and the value there is the amplitude. Multiplying by
            # the gate unitary then gives the resulting state in the same format.
            # After filtering small entries it is then converted back to the lists
            # of states and amplitudes.
            #
            # The basic algorithm here is short and simple, but we go through a lot of
            # contortions to optimize it by using numpy operations instead of pure
            # Python ones (even at the cost of performing a much greater number of
            # mathematical operations).

            # The nth element of dst_rows tells which row of partitioned_state the
            # nth element of the state vector will go to.
            dst_rows = np.zeros(len(self._states), dtype=int)
            # reverse_affected maps row index of partitioned_state -> state with all
            # qubits not acted on by the unitary masked out.
            reverse_affected = np.zeros(1, dtype=object)
            mask = ~0
            for dst_bit, qubit in enumerate(qubits[::-1]):
                src_bit = self.qubit_map[qubit]
                bit = np.array((self._states >> src_bit) & 1, dtype=int)
                dst_rows |= bit << dst_bit
                reverse_affected = np.concatenate(
                    (reverse_affected, reverse_affected | 1 << src_bit)
                )
                mask ^= 1 << src_bit
            self._states &= mask
            # unique_affected is the set of states after masking out the qubits acted
            # on by the unitary.
            # The nth element of dst_colls which column of partitioned_state the nth
            # element of the state vector will go to.
            unique_unaffected, dst_cols = np.unique(self._states, return_inverse=True)
            partitioned_state = np.zeros(
                (1 << len(qubits), len(unique_unaffected)), dtype=np.complex128
            )
            partitioned_state[dst_rows, dst_cols] = self._amplitudes
            np.matmul(cirq.unitary(action), partitioned_state, out=partitioned_state)
            nz_rows, nz_cols = np.nonzero(abs(partitioned_state) > _EPSILON)
            self._states = reverse_affected[nz_rows] | unique_unaffected[nz_cols]
            self._amplitudes = partitioned_state[nz_rows, nz_cols]
        return True

    def _perform_measurement(self, qubits):
        raise NotImplementedError

    # abstract method of OperationTarget
    def sample(self, qubits, repetitions, prng):
        probs = abs(self._amplitudes) ** 2
        samples = prng.choice(self._states, size=repetitions, p=probs)
        out = np.empty((repetitions, len(qubits)), dtype=np.uint8)
        for j, q in enumerate(qubits):
            out[:, j] = (samples >> self.qubit_map[q]) & 1
        return out

    def post_select(self, qubit, value):
        assert value in (0, 1)
        mask = 1 << self.qubit_map[qubit]
        value *= mask
        nonzero_indices = np.nonzero(self._states & mask == value)
        self._states = self._states[nonzero_indices]
        self._amplitudes = self._amplitudes[nonzero_indices]
        self._amplitudes /= np.linalg.norm(self._amplitudes)


class SparseSimulator(cirq.SimulatesIntermediateStateVector):
    def __init__(self):
        super().__init__(split_untangled_states=False)

    # override
    def _can_be_in_run_prefix(self, val):
        return super()._can_be_in_run_prefix(val) or isinstance(
            val, PostSelectOperation
        )

    # abstract method of SimulatorBase
    def _create_partial_simulation_state(
        self, initial_state, qubits, logs=None, classical_data=None
    ):
        assert initial_state == 0
        return SparseSimulationState(qubits=qubits)

    # abstract method of SimulatorBase
    def _create_step_result(self, sim_state):
        return SparseSimulatorStep(sim_state=sim_state)


class PostSelectOperation(cirq.Operation):
    """Prunes states where self.qubit is not equal to self.value from the state vector.

    Must be used with SparseSimulator as the sampler.
    """

    def __init__(self, qubit, value):
        super().__init__()
        self.qubit = qubit
        self.value = value

    def _act_on_(self, simulation_state):
        simulation_state.post_select(self.qubit, self.value)
        return True

    @property
    def qubits(self):
        return (self.qubit,)

    def with_qubits(self, new_qubit):
        return PostSelectOperation(new_qubit, self.value)


class SparseSimulatorStep(cirq.StepResultBase):
    pass
