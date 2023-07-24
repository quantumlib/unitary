# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import unitary.alpha as alpha
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.npcs as npcs
import unitary.examples.quantum_rpg.xp_utils as xp_utils


def test_trigger():
    e = encounter.Encounter([])
    assert all(e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 1)
    assert all(e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 0.0)
    assert all(not e.will_trigger() for _ in range(100))
    e = encounter.Encounter([], 0.5)
    assert not all(e.will_trigger() for _ in range(100))
    assert not all(not e.will_trigger() for _ in range(100))


def test_encounter():
    c = classes.Analyst("Aaronson")
    o = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["m", "1", "1"], file=io.StringIO()
    )
    e = encounter.Encounter([o])

    b = e.initiate(state)
    b.take_player_turn()
    b.take_npc_turn()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
h) Help.
watcher is DOWN!
""".strip()
    )


def test_copy():
    o = npcs.Observer("watcher")
    xp = xp_utils.EncounterXp([[alpha.Flip()]], weights=[1])
    e = encounter.Encounter([o], probability=0.75, description="Tester", xp=xp)
    e2 = e.copy()
    assert len(e.enemies) == len(e2.enemies)
    assert e.enemies[0] is not e2.enemies[0]
    qar = e.enemies[0]
    qar2 = e2.enemies[0]
    assert qar.circuit == qar2.circuit
    assert qar.name == qar2.name
    assert qar.level == qar2.level
    assert e.probability == e2.probability
    assert e.description == e2.description
    assert e.xp == e2.xp
