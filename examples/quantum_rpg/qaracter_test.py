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

from . import classes
from . import enums
from . import qaracter


def test_initialization() -> None:
    blank = qaracter.Qaracter(name="deutsch")
    assert blank.level == 1
    assert blank.name == "deutsch"
    assert not blank.is_npc()


def test_qubit_getters_and_effects() -> None:
    qar = qaracter.Qaracter(name="lovelace")
    obj_name = qar.quantum_object_name(1)
    qar_obj1 = qar.get_hp(obj_name)
    assert qar_obj1 is not None
    assert qar_obj1.name == obj_name
    assert qar.sample(obj_name, save_result=False) == enums.HealthPoint.HURT
    qar.add_quantum_effect(alpha.Flip(), 1)
    assert qar.sample(obj_name, save_result=False) == enums.HealthPoint.HEALTHY


def test_multi_qubit_effects() -> None:
    qar = qaracter.Qaracter(name="lovelace")
    qar.add_hp()
    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Move(), 1, 2)
    q1 = qar.quantum_object_name(1)
    q2 = qar.quantum_object_name(2)
    assert qar.sample(q1, save_result=False) == enums.HealthPoint.HURT
    assert qar.sample(q2, save_result=False) == enums.HealthPoint.HEALTHY


def test_copy() -> None:
    qar = qaracter.Qaracter(name="lovelace")
    qar.add_hp()
    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Move(), 1, 2)
    qar2 = qar.copy()
    assert qar.circuit == qar2.circuit
    assert qar.name == qar2.name
    assert qar.level == qar2.level
    # Assert the copy evolves separately
    qar2.add_hp()
    assert qar.level != qar2.level


def test_save_result() -> None:
    qar = qaracter.Qaracter(name="bohr")
    obj_name = qar.quantum_object_name(1)
    qar.add_quantum_effect(alpha.Superposition(), 1)

    # After being put in super position, the results should be 50-50
    x = qar.sample(obj_name, save_result=False)
    assert not all(qar.sample(obj_name, False) == x for _ in range(100))

    # After saving result (measuring), all results should be the same.
    x = qar.sample(obj_name, save_result=True)
    assert all(qar.sample(obj_name, False) == x for _ in range(100))


def test_active_qubits() -> None:
    qar = qaracter.Qaracter(name="hadamard")
    obj_name = qar.quantum_object_name(1)

    assert qar.active_qubits() == ["hadamard_1"]
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == "1QP (0|1> 0|0> 1?)"

    assert qar.sample(obj_name, save_result=True) == enums.HealthPoint.HURT
    assert qar.active_qubits() == []
    assert qar.is_down()
    assert not qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == "1QP (0|1> 1|0> 0?) *DOWN* "


def test_escaped() -> None:
    qar = qaracter.Qaracter(name="Châtelet")
    obj_name = qar.quantum_object_name(1)

    assert qar.active_qubits() == ["Châtelet_1"]
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == "1QP (0|1> 0|0> 1?)"

    qar.add_quantum_effect(alpha.Flip(), 1)

    assert qar.sample(obj_name, save_result=True) == enums.HealthPoint.HEALTHY
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == "1QP (1|1> 0|0> 0?) *ESCAPED* "


def test_odd_hp_qar() -> None:
    qar = qaracter.Qaracter(name="curie")
    qar.add_hp()
    qar.add_hp()

    assert qar.level == 3
    assert qar.active_qubits() == ["curie_1", "curie_2", "curie_3"]
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == "3QP (0|1> 0|0> 3?)"

    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Flip(), 3)
    assert (
        qar.sample(qar.quantum_object_name(1), save_result=True)
        == enums.HealthPoint.HEALTHY
    )
    assert (
        qar.sample(qar.quantum_object_name(2), save_result=True)
        == enums.HealthPoint.HURT
    )
    assert qar.active_qubits() == ["curie_3"]
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == "3QP (1|1> 1|0> 1?)"

    assert (
        qar.sample(qar.quantum_object_name(3), save_result=True)
        == enums.HealthPoint.HEALTHY
    )
    assert qar.active_qubits() == []
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == "3QP (2|1> 1|0> 0?) *ESCAPED* "


def test_even_hp_qar() -> None:
    """Even qubits with equal 0 and 1 should be considered escaped."""
    qar = qaracter.Qaracter(name="higgs")
    qar.add_hp()

    assert qar.level == 2
    assert qar.active_qubits() == ["higgs_1", "higgs_2"]
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == "2QP (0|1> 0|0> 2?)"

    qar.add_quantum_effect(alpha.Flip(), 2)
    assert (
        qar.sample(qar.quantum_object_name(1), save_result=True)
        == enums.HealthPoint.HURT
    )
    assert (
        qar.sample(qar.quantum_object_name(2), save_result=True)
        == enums.HealthPoint.HEALTHY
    )
    assert qar.active_qubits() == []
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()


def test_serialization() -> None:
    qar = classes.Engineer(name="curie")
    for _ in range(7):
        qar.add_hp()
    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Phase(), 2)
    qar.add_quantum_effect(alpha.Superposition(), 3)
    qar.add_quantum_effect(alpha.Flip(effect_fraction=0.25), 2)
    qar.add_quantum_effect(alpha.Phase(effect_fraction=0.125), 1)
    qar.add_quantum_effect(alpha.Split(), 1, 4, 5)
    qar.add_quantum_effect(alpha.PhasedSplit(), 3, 6, 7)
    serialized_str = qar.to_save_file()
    deserialized_qar = qaracter.Qaracter.from_save_file(serialized_str)
    assert type(deserialized_qar) == type(qar)
    assert deserialized_qar.name == qar.name
    assert deserialized_qar.level == qar.level
    assert deserialized_qar.circuit == qar.circuit
