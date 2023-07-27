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

import unitary.alpha as alpha
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.enums as enums
import unitary.examples.quantum_rpg.game_state as game_state
import unitary.examples.quantum_rpg.npcs as npcs


def test_observer():
    qar = npcs.Observer(name="glasses")
    c = classes.Analyst("cat")
    state = game_state.GameState(party=[c])
    b = battle.Battle(state, [qar])
    assert qar.is_npc()
    assert qar.npc_action(b) == "Observer glasses measures cat_1 as HURT."


def test_blue_foam():
    qar = npcs.BlueFoam(name="bubbles")
    assert all(
        qar.sample("bubbles_1", False) == enums.HealthPoint.HURT for _ in range(100)
    )
    c = classes.Analyst("person")
    assert qar.is_npc()
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.1)
    assert msg == "BlueFoam bubbles measures person_1 as HURT."
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3, slime=0.25)
    assert msg == "BlueFoam bubbles slimes person_1 for 0.250."


def test_green_foam():
    qar = npcs.GreenFoam(name="bubbles")
    assert all(
        qar.sample("bubbles_1", False) == enums.HealthPoint.HURT for _ in range(100)
    )
    c = classes.Analyst("person")
    assert qar.is_npc()
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.1)
    assert msg == "GreenFoam bubbles measures person_1 as HURT."
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3)
    assert "GreenFoam bubbles oozes person_1 for " in msg
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3, slime=0.25)
    assert msg == "GreenFoam bubbles oozes person_1 for 0.250 phase."


def test_red_foam():
    qar = npcs.RedFoam(name="bubbles")
    assert all(
        qar.sample("bubbles_1", False) == enums.HealthPoint.HEALTHY for _ in range(100)
    )
    c = classes.Analyst("person")
    assert qar.is_npc()
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.1)
    assert msg == "RedFoam bubbles measures person_1 as HURT."
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3)
    assert "RedFoam bubbles slimes person_1 for " in msg
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3, slime=0.25)
    assert msg == "RedFoam bubbles slimes person_1 for 0.250."


def test_purple_foam():
    qar = npcs.PurpleFoam(name="bubbles")
    assert any(
        qar.sample("bubbles_1", False) == enums.HealthPoint.HEALTHY for _ in range(100)
    )
    assert any(
        qar.sample("bubbles_1", False) == enums.HealthPoint.HURT for _ in range(100)
    )
    c = classes.Analyst("person")
    assert qar.is_npc()
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.1)
    assert msg == "PurpleFoam bubbles measures person_1 as HURT."
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.3, slime=0.25)
    assert msg == "PurpleFoam bubbles covers person_1 with foam!"


def test_schrodinger_cat():
    num_qubits = 4
    qar = npcs.SchrodingerCat(name="nice_kitty", num_qubits=num_qubits)

    # Check that individual qubits seem random
    for q in range(1, num_qubits+1):
        assert any(
            qar.sample(f"nice_kitty_{q}", False) == enums.HealthPoint.HEALTHY
            for _ in range(100)
        )
        assert any(
            qar.sample(f"nice_kitty_{q}", False) == enums.HealthPoint.HURT
            for _ in range(100)
        )
    # measure one
    result = qar.sample(f"nice_kitty_{q}", True)
    # all qubits are the same
    for q in range(1, num_qubits+1):
        assert all(qar.sample(f"nice_kitty_{q}", False) == result for _ in range(100))
    c = classes.Analyst("person")
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.4)
    assert msg == "SchrodingerCat nice_kitty measures person_1 as HURT."
    msg = qar.act_on_enemy_qubit(c.get_hp("person_1"), 0.6, slime=0.25)
    assert msg == "SchrodingerCat nice_kitty scratches person_1 into a superposition!"
