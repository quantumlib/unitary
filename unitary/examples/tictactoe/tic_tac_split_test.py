# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest

import cirq

import unitary.alpha as alpha
import unitary.examples.tictactoe as tictactoe

_E = tictactoe.TicTacSquare.EMPTY
_O = tictactoe.TicTacSquare.O
_X = tictactoe.TicTacSquare.X


@pytest.mark.parametrize(
    "mark, swap_state1, swap_state2",
    [(tictactoe.TicTacSquare.X, 0, 1), (tictactoe.TicTacSquare.O, 0, 2)],
)
def test_tic_tac_split_gate(
    mark: tictactoe.TicTacSquare, swap_state1: int, swap_state2: int
):
    q0 = cirq.NamedQid("a", dimension=3)
    q1 = cirq.NamedQid("b", dimension=3)

    sim = cirq.Simulator()
    for a in range(3):
        for b in range(3):
            c = cirq.Circuit()
            if a > 0:
                c.append(alpha.qudit_gates.QuditXGate(3, 0, a)(q0))
            if b > 0:
                c.append(alpha.qudit_gates.QuditXGate(3, 0, b)(q1))
            c.append(tictactoe.tic_tac_split.QuditSplitGate(mark)(q0, q1))
            c.append(tictactoe.tic_tac_split.QuditSplitGate(mark)(q0, q1))
            c.append(cirq.measure(q0, key="a"))
            c.append(cirq.measure(q1, key="b"))
            results = sim.run(c, repetitions=10)
            if (a == swap_state1 and b == swap_state2) or (
                a == swap_state2 and b == swap_state1
            ):
                # Swap the two states
                assert all(result == b for result in results.measurements["a"])
                assert all(result == a for result in results.measurements["b"])
            else:
                # Leave them alone
                assert all(result == a for result in results.measurements["a"])
                assert all(result == b for result in results.measurements["b"])


def test_invalid_mark_for_gate():
    with pytest.raises(ValueError, match="Not a valid square"):
        _ = tictactoe.tic_tac_split.QuditSplitGate(True)
    with pytest.raises(ValueError, match="Not a valid square"):
        _ = tictactoe.tic_tac_split.QuditSplitGate(0)


def test_diagram():
    q0 = cirq.NamedQid("a", dimension=3)
    q1 = cirq.NamedQid("b", dimension=3)
    c = cirq.Circuit(
        tictactoe.tic_tac_split.QuditSplitGate(tictactoe.TicTacSquare.X)(q0, q1)
    )
    assert (
        str(c)
        == """
a (d=3): ───×X───
            │
b (d=3): ───×X───
""".strip()
    )


@pytest.mark.parametrize("compile_to_qubits", [False, True])
@pytest.mark.parametrize(
    "mark, ruleset",
    [
        (tictactoe.TicTacSquare.X, tictactoe.TicTacRules.QUANTUM_V2),
        (tictactoe.TicTacSquare.X, tictactoe.TicTacRules.QUANTUM_V3),
        (tictactoe.TicTacSquare.O, tictactoe.TicTacRules.QUANTUM_V2),
        (tictactoe.TicTacSquare.O, tictactoe.TicTacRules.QUANTUM_V3),
    ],
)
def test_tic_tac_split(
    mark: tictactoe.TicTacSquare,
    ruleset: tictactoe.TicTacRules,
    compile_to_qubits: bool,
):
    a = alpha.QuantumObject("a", tictactoe.TicTacSquare.EMPTY)
    b = alpha.QuantumObject("b", tictactoe.TicTacSquare.EMPTY)
    board = alpha.QuantumWorld(
        [a, b], sampler=cirq.Simulator(), compile_to_qubits=compile_to_qubits
    )
    tictactoe.TicTacSplit(mark, ruleset)(a, b)
    results = board.peek(count=1000)
    on_a = [mark, tictactoe.TicTacSquare.EMPTY]
    on_b = [tictactoe.TicTacSquare.EMPTY, mark]
    assert any(r == on_a for r in results)
    assert any(r == on_b for r in results)
    assert all(r == on_a or r == on_b for r in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_tic_tac_split_entangled_v2(compile_to_qubits):
    a = alpha.QuantumObject("a", tictactoe.TicTacSquare.EMPTY)
    b = alpha.QuantumObject("b", tictactoe.TicTacSquare.EMPTY)
    c = alpha.QuantumObject("c", tictactoe.TicTacSquare.EMPTY)
    board = alpha.QuantumWorld(
        [a, b, c], sampler=cirq.Simulator(), compile_to_qubits=compile_to_qubits
    )
    ruleset = tictactoe.TicTacRules.QUANTUM_V2
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.X, ruleset)(a, b)
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.O, ruleset)(b, c)
    results = board.peek(count=1000)
    on_ab = [_X, _O, _E]
    on_ac = [_X, _E, _O]
    on_b = [_E, _X, _E]
    assert any(r == on_ab for r in results)
    assert any(r == on_ac for r in results)
    assert any(r == on_b for r in results)
    assert all(r == on_ab or r == on_ac or r == on_b for r in results)


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_tic_tac_split_entangled_v3(compile_to_qubits):
    a = alpha.QuantumObject("a", tictactoe.TicTacSquare.EMPTY)
    b = alpha.QuantumObject("b", tictactoe.TicTacSquare.EMPTY)
    c = alpha.QuantumObject("c", tictactoe.TicTacSquare.EMPTY)
    board = alpha.QuantumWorld(
        [a, b, c], sampler=cirq.Simulator(), compile_to_qubits=compile_to_qubits
    )
    ruleset = tictactoe.TicTacRules.QUANTUM_V3
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.X, ruleset)(a, b)
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.O, ruleset)(b, c)
    results = board.peek(count=1000)
    # This sequence of moves, for just three squares, should produce:
    # EEE -> XEE + EXE -> XEO + EXE -> XEO + XOE + EXE + EEX
    # The checks below check whether each of these last four samples occurs
    sample_1 = [_X, _O, _E]
    sample_2 = [_X, _E, _O]
    sample_3 = [_E, _X, _E]
    sample_4 = [_E, _E, _X]
    assert any(r == sample_1 for r in results)
    assert any(r == sample_2 for r in results)
    assert any(r == sample_3 for r in results)
    assert any(r == sample_4 for r in results)
    assert all(
        r == sample_1 or r == sample_2 or r == sample_3 or r == sample_4
        for r in results
    )


@pytest.mark.parametrize("compile_to_qubits", [False, True])
def test_tic_tac_split_entangled_v3_empty(compile_to_qubits):
    a = alpha.QuantumObject("a", tictactoe.TicTacSquare.EMPTY)
    b = alpha.QuantumObject("b", tictactoe.TicTacSquare.EMPTY)
    c = alpha.QuantumObject("c", tictactoe.TicTacSquare.EMPTY)
    board = alpha.QuantumWorld(
        [a, b, c], sampler=cirq.Simulator(), compile_to_qubits=compile_to_qubits
    )
    ruleset = tictactoe.TicTacRules.QUANTUM_V3
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.X, ruleset)(a, b)
    tictactoe.TicTacSplit(tictactoe.TicTacSquare.O, ruleset)(c, b)
    results = board.peek(count=1000)
    # This sequence of moves, for just three squares, should produce:
    # EEE -> XEE + EXE -> XEO + EXO -> XEO + XOE + EXO + EOX
    # The checks below check whether each of these last four samples occurs
    sample_1 = [_X, _O, _E]
    sample_2 = [_X, _E, _O]
    sample_3 = [_E, _X, _O]
    sample_4 = [_E, _O, _X]
    assert any(r == sample_1 for r in results)
    assert any(r == sample_2 for r in results)
    assert any(r == sample_3 for r in results)
    assert any(r == sample_4 for r in results)
    assert all(
        r == sample_1 or r == sample_2 or r == sample_3 or r == sample_4
        for r in results
    )
