import unitary.alpha as alpha
import unitary.examples.quantum_rpg.battle as battle
import unitary.examples.quantum_rpg.classes as classes
import unitary.examples.quantum_rpg.npcs as npcs


def test_observer():
    qar = npcs.Observer(name="glasses")
    c = classes.Analyst("cat")
    b = battle.Battle([c], [qar])
    assert qar.is_npc()
    assert qar.npc_action(b) == "Observer glasses measures cat at qubit cat_1"
