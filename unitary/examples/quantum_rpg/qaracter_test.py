import unitary.alpha as alpha
import unitary.examples.quantum_rpg.qaracter as qaracter
import unitary.examples.quantum_rpg.enums as enums


def test_initialization() -> None:
    blank = qaracter.Qaracter(name='deutsch')
    assert blank.level == 1
    assert blank.name == 'deutsch'
    assert not blank.is_npc()


def test_qubit_getters_and_effects() -> None:
    qar = qaracter.Qaracter(name='lovelace')
    obj_name = qar.quantum_object_name(1)
    qar_obj1 = qar.get_hp(obj_name)
    assert qar_obj1.name == obj_name
    assert qar.sample(obj_name, save_result=False) == enums.HealthPoint.HURT
    qar.add_quantum_effect(alpha.Flip(), 1)
    assert qar.sample(obj_name, save_result=False) == enums.HealthPoint.HEALTHY


def test_save_result() -> None:
    qar = qaracter.Qaracter(name='bohr')
    obj_name = qar.quantum_object_name(1)
    qar.add_quantum_effect(alpha.Superposition(), 1)

    # After being put in super position, the results should be 50-50
    x = qar.sample(obj_name, save_result=False)
    assert not all(qar.sample(obj_name, False) == x for _ in range(100))

    # After saving result (measuring), all results should be the same.
    x = qar.sample(obj_name, save_result=True)
    assert all(qar.sample(obj_name, False) == x for _ in range(100))


def test_active_qubits() -> None:
    qar = qaracter.Qaracter(name='hadamard')
    obj_name = qar.quantum_object_name(1)

    assert qar.active_qubits() == ['hadamard_1']
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == '1QP (0|1> 0|0> 1?)'

    assert qar.sample(obj_name, save_result=True) == enums.HealthPoint.HURT
    assert qar.active_qubits() == []
    assert qar.is_down()
    assert not qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == '1QP (0|1> 1|0> 0?) *DOWN* '


def test_escaped() -> None:
    qar = qaracter.Qaracter(name='Châtelet')
    obj_name = qar.quantum_object_name(1)

    assert qar.active_qubits() == ['Châtelet_1']
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == '1QP (0|1> 0|0> 1?)'

    qar.add_quantum_effect(alpha.Flip(), 1)

    assert qar.sample(obj_name, save_result=True) == enums.HealthPoint.HEALTHY
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == '1QP (1|1> 0|0> 0?) *ESCAPED* '


def test_odd_hp_qar() -> None:
    qar = qaracter.Qaracter(name='curie')
    qar.add_hp()
    qar.add_hp()

    assert qar.level == 3
    assert qar.active_qubits() == ['curie_1', 'curie_2', 'curie_3']
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == '3QP (0|1> 0|0> 3?)'

    qar.add_quantum_effect(alpha.Flip(), 1)
    qar.add_quantum_effect(alpha.Flip(), 3)
    assert qar.sample(qar.quantum_object_name(1),
                      save_result=True) == enums.HealthPoint.HEALTHY
    assert qar.sample(qar.quantum_object_name(2),
                      save_result=True) == enums.HealthPoint.HURT
    assert qar.active_qubits() == ['curie_3']
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == '3QP (1|1> 1|0> 1?)'

    assert qar.sample(qar.quantum_object_name(3),
                      save_result=True) == enums.HealthPoint.HEALTHY
    assert qar.active_qubits() == []
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()
    assert qar.status_line() == '3QP (2|1> 1|0> 0?) *ESCAPED* '


def test_even_hp_qar() -> None:
    """Even qubits with equal 0 and 1 should be considered escaped."""
    qar = qaracter.Qaracter(name='higgs')
    qar.add_hp()

    assert qar.level == 2
    assert qar.active_qubits() == ['higgs_1', 'higgs_2']
    assert not qar.is_down()
    assert not qar.is_escaped()
    assert qar.is_active()
    assert qar.status_line() == '2QP (0|1> 0|0> 2?)'

    qar.add_quantum_effect(alpha.Flip(), 2)
    assert qar.sample(qar.quantum_object_name(1),
                      save_result=True) == enums.HealthPoint.HURT
    assert qar.sample(qar.quantum_object_name(2),
                      save_result=True) == enums.HealthPoint.HEALTHY
    assert qar.active_qubits() == []
    assert not qar.is_down()
    assert qar.is_escaped()
    assert not qar.is_active()
