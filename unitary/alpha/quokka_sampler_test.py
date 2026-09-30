# Copyright 2024 The Unitary Authors
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

import pytest
import cirq
import sympy

import unitary.alpha.quokka_sampler as quokka_sampler

# Qubits for testing
_Q = cirq.LineQubit.range(10)


class FakeQuokkaEndpoint:
    def __init__(self, *responses: quokka_sampler.JSON_TYPE):
        self.responses = list(responses)
        self.requests = []

    def __call__(
        self, json_request: quokka_sampler.JSON_TYPE
    ) -> quokka_sampler.JSON_TYPE:
        self.requests.append(json_request)
        return self.responses.pop()


@pytest.mark.parametrize(
    "circuit,json_result",
    [
        (
            cirq.Circuit(cirq.X(_Q[0]), cirq.measure(_Q[0], key="mmm")),
            {"m_mmm": [[1], [1], [1], [1], [1]]},
        ),
        (
            cirq.Circuit(cirq.X(_Q[0]), cirq.measure(_Q[0])),
            {"m0": [[1], [1], [1], [1], [1]]},
        ),
        (
            cirq.Circuit(
                cirq.X(_Q[0]), cirq.X(_Q[1]), cirq.measure(_Q[0]), cirq.measure(_Q[1])
            ),
            {"m0": [[1], [1], [1], [1], [1]], "m1": [[1], [1], [1], [1], [1]]},
        ),
        (
            cirq.Circuit(
                cirq.X(_Q[0]),
                cirq.CNOT(_Q[0], _Q[1]),
                cirq.measure(_Q[0]),
                cirq.measure(_Q[1]),
            ),
            {"m0": [[1], [1], [1], [1], [1]], "m1": [[1], [1], [1], [1], [1]]},
        ),
        (
            cirq.Circuit(
                cirq.X(_Q[0]),
                cirq.CNOT(_Q[0], _Q[1]),
                cirq.measure(_Q[0], _Q[1], key="m2"),
            ),
            {"m_m2": [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]},
        ),
    ],
)
def test_quokka_deterministic_examples(circuit, json_result):
    sim = cirq.Simulator()
    expected_results = sim.run(circuit, repetitions=5)
    json_response = {"error": "no error", "error_code": 0, "result": json_result}
    quokka = quokka_sampler.QuokkaSampler(
        name="test_mctesterface", post=FakeQuokkaEndpoint(json_response)
    )
    quokka_results = quokka.run(circuit, repetitions=5)
    assert quokka_results == expected_results


def test_quokka_run_sweep():
    sim = cirq.Simulator()
    circuit = cirq.Circuit(
        cirq.X(_Q[0]),
        cirq.X(_Q[1]) ** sympy.Symbol("X_1"),
        cirq.measure(_Q[0], _Q[1], key="m2"),
    )
    sweep = cirq.Points("X_1", [0, 1])
    expected_results = sim.run_sweep(circuit, sweep, repetitions=5)
    json_response = {
        "error": "no error",
        "error_code": 0,
        "result": {"m_m2": [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]},
    }
    json_response2 = {
        "error": "no error",
        "error_code": 0,
        "result": {"m_m2": [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]},
    }
    quokka = quokka_sampler.QuokkaSampler(
        name="test_mctesterface", post=FakeQuokkaEndpoint(json_response, json_response2)
    )
    quokka_results = quokka.run_sweep(circuit, sweep, repetitions=5)
    assert quokka_results[0] == expected_results[0]
