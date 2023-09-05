# Unitary for Physicists

If you are already familiar with quantum computing terms, have used cirq, or come from a physics background,
the terms in the Unitary may feel a bit unfamiliar.  They are meant to connect quantum concepts to traditional
programming contructs, such as "if/then".  

The following is a table that connects physics terms to cirq and unitary terms.

| Physics    | Cirq |  Unitary |
| -------- | ------- | ----- |
| Qubit | cirq.Qid | alpha.QuantumObject |
| Qutrit | cirq.Qid | alpha.QuantumObject (using an enum with three values) |
| Quantum circuit | cirq.Circuit | alpha.QuantumWorld |
| Generic Unitary | cirq.Gate  | alpha.QuantumEffect |
| Gate applied to specified qubits | cirq.Operation | alpha.QuantumEffect(qubits) |
| X gate | cirq.X | alpha.Flip() |
| $\sqrt{X}$ or square root of NOT | cirq.X ** 0.5 | alpha.Flip(effect_fraction=0.5) |
| Z gate | cirq.Z | alpha.Phase() |
| Hadamard | cirq.H | alpha.Superposition() |
| Controlled-gate | gate.controlled_by() | alpha.quantum_if() |
| CNOT | cirq.CNOT(a,b) | alpha.quantum_if(a).then_apply(alpha.Flip())(b) |
| CZ | cirq.CZ(a,b) | alpha.quantum_if(a).then_apply(alpha.Phase())(b) |
