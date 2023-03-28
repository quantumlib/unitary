import unitary.alpha as alpha
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.enums as enums
import unitary.examples.quantum_rpg.qaracter as qaracter


def test_engineer():
    qar = classes.Engineer(name="d")
    assert not qar.is_npc()
    assert set(qar.actions().keys()) == {"x"}
    qar.add_hp()
    assert set(qar.actions().keys()) == {"x"}
    qar.add_hp()
    assert set(qar.actions().keys()) == {"x", "h"}


def test_engineer_effects():
    qar = classes.Engineer(name="d")
    qar.add_hp()
    qar.add_hp()
    test_monster = qaracter.Qaracter("t")

    # Test X
    qar.actions()["x"](test_monster, 1)
    q = test_monster.quantum_object_name(1)
    for _ in range(100):
        assert test_monster.sample(q, False) == enums.HealthPoint.HEALTHY

    # Test H
    qar.actions()["h"](test_monster, 1)
    results = [test_monster.sample(q, False) for _ in range(100)]
    assert any(results[i] == enums.HealthPoint.HEALTHY for i in range(100))
    assert any(results[i] == enums.HealthPoint.HURT for i in range(100))


def test_analyst_effects():
    qar = classes.Analyst(name="a")
    test_monster = qaracter.Qaracter("t")

    # Test sample
    res = qar.actions()["s"](test_monster, 1)
    assert res == "Sample result HealthPoint.HURT"

    # Test measurement
    # First Hadamard to put into superposition
    # Then test measurement destroys that superposition.
    test_monster.add_quantum_effect(alpha.Superposition(), 1)
    q = test_monster.quantum_object_name(1)
    results = [test_monster.sample(q, False) for _ in range(100)]
    assert not all(results[0] == results[i] for i in range(100))
    qar.actions()["m"](test_monster, 1)
    results = [test_monster.sample(q, False) for _ in range(100)]
    assert all(results[0] == results[i] for i in range(100))


def test_analyst():
    qar = classes.Analyst(name="a")
    assert not qar.is_npc()
    assert set(qar.actions().keys()) == {"s", "m"}
    qar.add_hp()
    qar.add_hp()
    assert set(qar.actions().keys()) == {"s", "m"}
