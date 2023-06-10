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
import unitary.examples.quantum_rpg.npcs as npcs


def test_battle():
    output = io.StringIO()
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    b = battle.Battle([c], [e], file=output)
    b.take_player_turn(user_input=["s", "1", "1"])
    b.take_npc_turn()
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
-----------------------------------------------
Aaronson Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Aaronson turn:
s
m
Sample result HealthPoint.HURT
Observer watcher measures Aaronson_1 as HURT.
""".strip()
    )


def test_bad_monster():
    output = io.StringIO()
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    b = battle.Battle([c], [e], file=output)
    b.take_player_turn(user_input=["s", "2", "1", "1"])
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
-----------------------------------------------
Aaronson Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Aaronson turn:
s
m
Invalid number selected.
Sample result HealthPoint.HURT
""".strip()
    )


def test_bad_qubit():
    output = io.StringIO()
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    b = battle.Battle([c], [e], file=output)
    b.take_player_turn(user_input=["s", "1", "2"])
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
-----------------------------------------------
Aaronson Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Aaronson turn:
s
m
watcher_2 is not an active qubit
""".strip()
    )


def test_battle_loop():
    output = io.StringIO()
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    b = battle.Battle([c], [e], file=output)
    assert b.loop(user_input=["s", "1", "1"]) == battle.BattleResult.PLAYERS_DOWN
    assert (
        output.getvalue().replace("\t", " ").strip()
        == r"""
-----------------------------------------------
Aaronson Analyst   watcher Observer
1QP (0|1> 0|0> 1?)   1QP (0|1> 0|0> 1?)
-----------------------------------------------
Aaronson turn:
s
m
Sample result HealthPoint.HURT
Observer watcher measures Aaronson_1 as HURT.
""".strip()
    )
