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
Observer watcher measures Aaronson at qubit Aaronson_1
""".strip()
    )


def test_bad_monster():
    output = io.StringIO()
    c = classes.Analyst("Aaronson")
    e = npcs.Observer("watcher")
    b = battle.Battle([c], [e], file=output)
    b.take_player_turn(user_input=["s", "2", "1"])
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
2 is not a valid monster
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
Observer watcher measures Aaronson at qubit Aaronson_1
""".strip()
    )