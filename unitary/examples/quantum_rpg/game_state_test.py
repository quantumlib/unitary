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
import unitary.examples.quantum_rpg.qaracter as qaracter
import unitary.examples.quantum_rpg.game_state as game_state


def test_serialization() -> None:
    qar = qaracter.Qaracter(name="plato")
    qar.add_hp()
    qar.add_hp()
    qar.add_hp()
    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Phase(), 2)
    qar.add_quantum_effect(alpha.Superposition(), 3)
    qar2 = qaracter.Qaracter(name="aristotle")
    qar2.add_hp()
    qar2.add_quantum_effect(alpha.Flip(effect_fraction=0.25), 2)
    qar2.add_quantum_effect(alpha.Phase(effect_fraction=0.125), 1)

    state_dict = {"puzzle1": "complete", "puzzle2": "WIP"}
    label = "quantum_lab1"

    state = game_state.GameState(
        party=[qar, qar2], state_dict=state_dict, current_location_label=label
    )
    serialized_str = state.to_save_file()
    deserialized_state = game_state.GameState.from_save_file(serialized_str)

    assert deserialized_state.current_location_label == label
    assert deserialized_state.state_dict == state_dict
    assert len(deserialized_state.party) == 2

    deserialized_qar = deserialized_state.party[0]
    assert deserialized_qar.name == qar.name
    assert deserialized_qar.level == qar.level
    assert deserialized_qar.circuit == qar.circuit
    deserialized_qar2 = deserialized_state.party[1]
    assert deserialized_qar2.name == qar2.name
    assert deserialized_qar2.level == qar2.level
    assert deserialized_qar2.circuit == qar2.circuit


def test_bad_input():
    assert game_state.GameState.from_save_file("") is None
    assert game_state.GameState.from_save_file("ding;dong") is None
    assert game_state.GameState.from_save_file("ding;2;dong") is None


def test_quantopedia():
    state = game_state.GameState([])
    assert not state.has_quantopedia(8)
    assert not state.has_quantopedia(4)
    assert not state.has_quantopedia(2)
    assert not state.has_quantopedia(1)
    state.set_quantopedia(4)
    state.set_quantopedia(1)
    assert not state.has_quantopedia(8)
    assert state.has_quantopedia(4)
    assert not state.has_quantopedia(2)
    assert state.has_quantopedia(1)
