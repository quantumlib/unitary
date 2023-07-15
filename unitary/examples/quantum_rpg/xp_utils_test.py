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
#
import io

import cirq

import unitary.alpha as alpha
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.xp_utils as xp_utils


def test_choose():
    enc = xp_utils.EncounterXp([[alpha.Superposition()]])
    assert all(enc.choose() == [alpha.Superposition()] for _ in range(10))

    enc = xp_utils.EncounterXp([[alpha.Superposition(), alpha.Flip()]])
    assert all(enc.choose() == [alpha.Superposition(), alpha.Flip()] for _ in range(10))

    enc = xp_utils.EncounterXp([[alpha.Superposition()], [alpha.Flip()]])
    choose_list = list(enc.choose() for _ in range(200))
    assert all(
        xp == [alpha.Superposition()] or xp == [alpha.Flip()] for xp in choose_list
    )
    assert any(xp == [alpha.Superposition()] for xp in choose_list)
    assert any(xp == [alpha.Flip()] for xp in choose_list)

    enc = xp_utils.EncounterXp([[alpha.Superposition()], [alpha.Flip()]], [1, 0])
    assert all(enc.choose() == [alpha.Superposition()] for xp in choose_list)


def test_award_xp():
    c = classes.Analyst("wizard")
    state = game_state.GameState(party=[c], user_input=["1", "1"], file=io.StringIO())
    enc = xp_utils.EncounterXp([[alpha.Superposition()]])
    xp_utils.award_xp(state, enc)
    assert c.circuit == cirq.Circuit(cirq.H(cirq.NamedQubit("wizard_1")))
    assert (
        state.file.getvalue()
        == """You have been awarded XP!
  Superposition

Choose the qaracter to add the Superposition to:
1) wizard
Current qaracter sheet:

Choose qubit 0 for Superposition:
1) wizard_1
"""
    )


def test_award_xp_multi_qubit_gate():
    c = classes.Analyst("wizard")
    c.add_hp()
    state = game_state.GameState(
        party=[c], user_input=["1", "1", "2"], file=io.StringIO()
    )
    enc = xp_utils.EncounterXp([[alpha.Move()]])
    xp_utils.award_xp(state, enc)
    assert c.circuit == cirq.Circuit(
        cirq.SWAP(cirq.NamedQubit("wizard_1"), cirq.NamedQubit("wizard_2"))
    )
    assert (
        state.file.getvalue()
        == """You have been awarded XP!
  Move

Choose the qaracter to add the Move to:
1) wizard
Current qaracter sheet:

Choose qubit 0 for Move:
1) wizard_1
2) wizard_2
Choose qubit 1 for Move:
1) wizard_1
2) wizard_2
"""
    )


def test_qaracter_not_high_enough():
    c = classes.Analyst("wizard")
    enc = xp_utils.EncounterXp([[alpha.Move()]])
    state = game_state.GameState(
        party=[c], user_input=["1", "1", "2"], file=io.StringIO()
    )
    xp_utils.award_xp(state, enc)
    assert c.circuit == cirq.Circuit()
    assert (
        state.file.getvalue()
        == """You have been awarded XP!
  Move

Qaracters are not high-enough level for Move!
"""
    )


def test_qaracter_levels():
    c = classes.Analyst("wizard")
    c.add_quantum_effect(alpha.Superposition(), 1)
    enc = xp_utils.EncounterXp([[alpha.Superposition()]])
    state = game_state.GameState(
        party=[c], user_input=["1", "1", "2"], file=io.StringIO()
    )
    xp_utils.award_xp(state, enc)
    assert (
        state.file.getvalue()
        == """You have been awarded XP!
  Superposition

Choose the qaracter to add the Superposition to:
1) wizard
Current qaracter sheet:
wizard_1: ───H───
Choose qubit 0 for Superposition:
1) wizard_1
wizard has advanced to the next level and gains a HP!
"""
    )
