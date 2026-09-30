# Copyright 2026 The Unitary Authors
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

import pathlib
import subprocess
import sys


SCRIPT = pathlib.Path(__file__).with_name("write-ci-requirements.py")


def _write_requirements(tmp_path, version):
    output = tmp_path / "ci-requirements.txt"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            f"--out-fn={output}",
            f"--relative-cirq-version={version}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return output.read_text()


def test_current_cirq_ci_pins_legacy_setuptools(tmp_path):
    requirements = _write_requirements(tmp_path, "current")

    assert "cirq-core==0.15.0" in requirements
    assert "cirq-google==0.15.0" in requirements
    assert "setuptools<82" in requirements


def test_next_cirq_ci_does_not_constrain_setuptools(tmp_path):
    requirements = _write_requirements(tmp_path, "next")

    assert "cirq-core>=1.0.0" in requirements
    assert "cirq-google>=1.0.0" in requirements
    assert "\nsetuptools\n" in requirements
    assert "setuptools<82" not in requirements
