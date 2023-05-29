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
    output = io.StringIO()
    c = classes.Analyst("wizard")
    enc = xp_utils.EncounterXp([[alpha.Superposition()]])
    xp_utils.award_xp([c], enc, ["1", "1"], output)
    assert c.circuit == cirq.Circuit(cirq.H(cirq.NamedQubit("wizard_1")))
    assert (
        output.getvalue()
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
    output = io.StringIO()
    c = classes.Analyst("wizard")
    c.add_hp()
    enc = xp_utils.EncounterXp([[alpha.Move()]])
    xp_utils.award_xp([c], enc, ["1", "1", "2"], output)
    assert c.circuit == cirq.Circuit(
        cirq.SWAP(cirq.NamedQubit("wizard_1"), cirq.NamedQubit("wizard_2"))
    )
    assert (
        output.getvalue()
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
