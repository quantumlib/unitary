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
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.npcs as npcs


def test_battle():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["m", "1", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    b.take_player_turn()
    b.take_npc_turn()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
""".strip()
    )


def test_bad_monster():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["m", "2", "1", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    b.take_player_turn()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
Invalid number selected.
""".strip()
    )


def test_higher_level_players():
    """Tests printing all the class descriptions."""
    c = classes.Analyst("Aaronson")
    c.add_hp()
    c.add_hp()
    e = classes.Engineer("Preskill")
    e.add_hp()
    e.add_hp()
    w = npcs.Observer("watcher")
    w2 = npcs.Observer("watcher")
    state = game_state.GameState(
        [c, e], user_input=["m", "1", "1", "h", "2", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [w, w2])
    b.take_player_turn()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
3QP (0|1> 0|0> 3?)                      1QP (0|1> 0|0> 1?)
Preskill Engineer                       2) watcher Observer
3QP (0|1> 0|0> 3?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
s) Sample enemy qubit.
q) Read Quantopedia.
?) Help.
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
3QP (0|1> 0|0> 3?)                      1QP (0|1> 1|0> 0?) *DOWN* 
Preskill Engineer                       2) watcher Observer
3QP (0|1> 0|0> 3?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Preskill turn:
h) Attack with H gate.
x) Attack with X gate.
q) Read Quantopedia.
?) Help.
""".strip()
    )


def test_bad_qubit():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["s", "1", "2"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    b.take_player_turn()
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
""".strip()
    )


def test_battle_loop():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["m", "1", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    assert b.loop() == battle.BattleResult.PLAYERS_WON
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
""".strip()
    )


def test_battle_help():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["?", "m", "1", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    assert b.loop() == battle.BattleResult.PLAYERS_WON
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
The analyst can measure enemy qubits.  This forces an enemy qubit
into the |0> state or |1> state with a probability based on its
amplitude. Try to measure the enemy qubits as |0> to defeat them.
""".strip()
    )


def test_read_quantopedia_not_known():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["q", "m", "1", "1"], file=io.StringIO()
    )
    b = battle.Battle(state, [e])
    assert b.loop() == battle.BattleResult.PLAYERS_WON
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
You do not have information on Observer yet.
""".strip()
    )


def test_read_quantopedia():
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    state = game_state.GameState(
        party=[c], user_input=["q", "m", "1", "1"], file=io.StringIO()
    )
    state.set_quantopedia(1)
    b = battle.Battle(state, [e])
    assert b.loop() == battle.BattleResult.PLAYERS_WON
    assert (
        state.file.getvalue().replace("\t", " ").strip()
        == r"""
------------------------------------------------------------
Aaronson Analyst                        1) watcher Observer
1QP (0|1> 0|0> 1?)                      1QP (0|1> 0|0> 1?)
------------------------------------------------------------
Aaronson turn:
m) Measure enemy qubit.
q) Read Quantopedia.
?) Help.
Observers are known to frequent quantum events.
They will measure qubits in order to find out their values.
""".strip()
    )
