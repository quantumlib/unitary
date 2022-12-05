import unitary.examples.quantum_rpg.classes as classes

def test_engineer():
    qar = classes.Engineer(name='d')
    assert not qar.is_npc()
    assert set(qar.actions().keys()) == {'x'}
    qar.add_hp()
    assert set(qar.actions().keys()) == {'x'}
    qar.add_hp()
    assert set(qar.actions().keys()) == {'x', 'h'}

def test_analyst():
    qar = classes.Analyst(name='a')
    assert not qar.is_npc()
    assert set(qar.actions().keys()) == {'s', 'm'}
    qar.add_hp()
    qar.add_hp()
    assert set(qar.actions().keys()) == {'s', 'm'}
