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

import cirq

from unitary.alpha.qudit_gates import QuditPlusGate, QuditXGate
from unitary.alpha.quantum_effect import QuantumEffect


class Cycle(QuantumEffect):
    """Cycles a qudit from |0> to |1>, |1> to |2>, etc.

    Essentially adds `addend` to the state, where `addend`
    is the parameter supplied at creation.
    """

    def __init__(self, num=1):
        self.addend = num

    def effect(self, *objects):
        for q in objects:
            if q.qubit.dimension == 2:
                if self.addend % 2:
                    yield cirq.X(q.qubit)
            else:
                yield QuditPlusGate(dimension=q.qubit.dimension, addend=self.addend)(
                    q.qubit
                )


class QuditCycle(Cycle):
    """Equivalent to Cycle.

    Exists only for backwards compatibiltity.
    Will be removed in 2024.
    """

    def __init__(self, dimension, num=1):
        super().__init__(num)


class Flip(QuantumEffect):
    """Flips two states of a qudit, leaving all other states unchanged.

    For instance, Flip(state0 = 0, state1 = 2) is a qutrit effect
    that flips |0> to |2>, |2> to |0> and leaves
    |1> alone.  This is also sometimes referred as the X_02 gate.

    For a partial flip, use the `effect_fraction` argument.
    Note that this is only applied so far on qubits and not yet for
    qudits.

    These effects will be cumulative.  For instance, two quarter
    flips (effect_fraction=0.25) will be equivalent to a half
    flip (effect_fraction=0.5).

    Note that most fractions will not produce the corresponding
    probabiltity distribution.  For instance, a effect_fraction
    of 0.25 will not produce a 25%/75% probability distribution
    of outcomes.

    Args:
        effect_fraction: Amount of flip effect to perform.
            This results in an exponentiation of the flip (X)
            effect.  A fraction of 1.0 corresponds to a full
            flip (this is the default).  A fraction of 0.5
            corresponds to a half flip (square root of NOT)
        state0: The source state to be flipped.  For instance,
            if state0=1, this will flip the |1> state to the
            state specified in state1.
        state1: The destination state to be flipped to.
    """

    def __init__(self, effect_fraction: float = 1.0, state0: int = 0, state1: int = 1):
        self.state0 = state0
        self.state1 = state1
        self.effect_fraction = effect_fraction

    def effect(self, *objects):
        for q in objects:
            if q.qubit.dimension == 2:
                yield cirq.X(q.qubit) ** self.effect_fraction
            else:
                yield QuditXGate(
                    dimension=q.qubit.dimension,
                    source_state=self.state0,
                    destination_state=self.state1,
                )(q.qubit)

    def __str__(self):
        if self.effect_fraction == 1:
            return "Flip"
        if self.state0 == 0 and self.state1 == 1:
            return f"Flip(effect_fraction={self.effect_fraction})"
        return (
            f"Flip(effect_fraction={self.effect_fraction}, "
            "state0={self.state0}, state1={self.state1})"
        )

    def __eq__(self, other):
        if isinstance(other, Flip):
            return self.effect_fraction == other.effect_fraction
        return NotImplemented


class QuditFlip(Flip):
    """Equivalent to Flip.

    Exists only for backwards compatibiltity.
    Will be removed in 2024.
    """

    def __init__(self, dimension: int, state0: int, state1: int):
        super().__init__(state0=state0, state1=state1)
