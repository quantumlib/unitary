# Copyright 2024 The Unitary Authors
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
"""Simulation using a "Quokka" device."""

from typing import Any, Callable, Dict, Optional, Sequence

import cirq
import numpy as np
import json

_REQUEST_ENDPOINT = "http://{}.quokkacomputing.com/qsim/qasm"
_DEFAULT_QUOKKA_NAME = "quokka1"

JSON_TYPE = Dict[str, Any]
_RESULT_KEY = "result"
_ERROR_CODE_KEY = "error_code"
_RESULT_KEY = "result"
_SCRIPT_KEY = "script"
_REPETITION_KEY = "count"


class QuokkaSampler(cirq.Sampler):
    """Sampler for querying a Quokka quantum simulation device.

    See https://www.quokkacomputing.com/ for more information.a

    Args:
        name: name of your quokka device
        endpoint: HTTP url endpoint to post queries to.
        post_function: used only for testing to override default
            behavior to connect to internet URLs.
    """

    def __init__(
        self,
        name: str = _DEFAULT_QUOKKA_NAME,
        endpoint: Optional[str] = None,
        post_function: Optional[Callable[[JSON_TYPE], JSON_TYPE]] = None,
    ):
        self.quokka_name = name
        self.endpoint = endpoint
        self.post_function = post_function

        if self.endpoint is None:
            self.endpoint = _REQUEST_ENDPOINT.format(self.quokka_name)
        if self.post_function is None:
            self.post_function = self._post

    def _post(self, json_request: JSON_TYPE) -> JSON_TYPE:
        """Sends POST queries to quokka endpoint."""
        try:
            import requests
        except ImportError as e:
            print(
                "Please install requests library to use Quokka"
                "(e.g. pip install requests)"
            )
            raise e
        result = requests.post(self.endpoint, json=json_request)
        return json.loads(result.content)

    def run_sweep(
        self,
        program: "cirq.AbstractCircuit",
        params: "cirq.Sweepable",
        repetitions: int = 1,
    ) -> Sequence["cirq.Result"]:
        """Samples from the given Circuit.

        This allows for sweeping over different parameter values,
        unlike the `run` method.  The `params` argument will provide a
        mapping from `sympy.Symbol`s used within the circuit to a set of
        values.  Unlike the `run` method, which specifies a single
        mapping from symbol to value, this method allows a "sweep" of
        values.  This allows a user to specify execution of a family of
        related circuits efficiently.

        Args:
            program: The circuit to sample from.
            params: Parameters to run with the program.
            repetitions: The number of times to sample.

        Returns:
            Result list for this run; one for each possible parameter resolver.
        """
        rtn_results = []
        qubits = sorted(program.all_qubits())
        measure_keys = {}
        register_names = {}
        meas_i = 0

        # Find all measurements in the circuit and record keys
        # so that we can later translate between circuit and QASM registers.
        for op in program.all_operations():
            if isinstance(op.gate, cirq.MeasurementGate):
                key = cirq.measurement_key_name(op)
                if key in measure_keys:
                    print(
                        "Warning!  Keys can only be measured once in Quokka simulator"
                    )
                    print("Key {key} will only contain the last measured value")
                measure_keys[key] = op.qubits
                if cirq.QasmOutput.valid_id_re.match(key):
                    register_names[key] = f"m_{key}"
                else:
                    register_names[key] = f"m{meas_i}"
                    meas_i += 1

        # QASM 2.0 does not support parameter sweeps,
        # so resolve any symbolic functions to a concrete circuit.
        for param_resolver in cirq.to_resolvers(params):
            circuit = cirq.resolve_parameters(program, param_resolver)
            qasm = cirq.qasm(circuit)

            # Hack to change sqrt-X gates into rx 0.5 gates:
            # Since quokka does not support sx or sxdg gates
            qasm = qasm.replace("\nsx ", "\nrx(pi*0.5) ").replace(
                "\nsxdg ", "\nrx(pi*-0.5) "
            )

            # Send data to quokka endpoint
            data = {_SCRIPT_KEY: qasm, _REPETITION_KEY: repetitions}
            json_results = self.post_function(data)

            if _ERROR_CODE_KEY in json_results and json_results[_ERROR_CODE_KEY] != 0:
                raise RuntimeError(f"Quokka returned an error: {json_results}")

            if _RESULT_KEY not in json_results:
                raise RuntimeError(f"Quokka did not return any results: {json_results}")

            # Associate results from json response to measurement keys.
            result_measurements = {}
            for key in measure_keys:
                register_name = register_names[key]
                if register_name not in json_results[_RESULT_KEY]:
                    raise RuntimeError(
                        f"Quokka did not measure key {key}: {json_results}"
                    )
                result_measurements[key] = np.asarray(
                    json_results[_RESULT_KEY][register_name], dtype=np.dtype("int8")
                )

            # Append measurements to eventual result.
            rtn_results.append(
                cirq.ResultDict(
                    params=param_resolver,
                    measurements=result_measurements,
                )
            )
        return rtn_results
