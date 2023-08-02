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

import os
import shutil
import time
from multiprocessing import Pool
from subprocess import run as _run, CalledProcessError

BASE_PACKAGES = [
    # for running the notebooks
    "jupyter",
    # assumed to be part of colab
    "seaborn~=0.11.1",
]


def _check_notebook(notebook_fn: str, notebook_id: str, stdout, stderr):
    """Helper function to actually do the work in `check_notebook`.

    `check_notebook` has all the context managers and exception handling,
    which would otherwise result in highly indented code.

    Args:
        notebook_fn: The notebook filename
        notebook_id: A unique string id for the notebook that does not include `/`
        stdout: A file-like object to redirect stdout
        stderr: A file-like object to redirect stderr
    """
    print(f"Starting {notebook_id}")

    def run(*args, **kwargs):
        return _run(*args, check=True, stdout=stdout, stderr=stderr, **kwargs)

    # 1. create venv
    venv_dir = os.path.abspath(f"./notebook_envs/{notebook_id}")
    run(["python", "-m", "venv", "--clear", venv_dir])

    # 2. basic colab-like environment
    pip = f"{venv_dir}/bin/pip"
    run([pip, "install"] + BASE_PACKAGES)

    # 3. execute
    jupyter = f"{venv_dir}/bin/jupyter"
    env = os.environ.copy()
    env["PATH"] = f'{venv_dir}/bin:{env["PATH"]}'
    run(
        [jupyter, "nbconvert", "--to", "html", "--execute", notebook_fn],
        cwd="../",
        env=env,
    )

    # 4. clean up
    shutil.rmtree(venv_dir)


def check_notebook(notebook_fn: str):
    """Check a notebook.

     1. Create a venv just for that notebook
     2. Verify the notebook executes without error (and that it installs its own dependencies!)
     3. Clean up venv dir

    A scratch directory dev_tools/notebook_envs will be created containing tvenv as well as
    stdout and stderr logs for each notebook. Each of these files and directories will be
    named according to the "notebook_id", which is `notebook_fn.replace('/', '-')`.

    The executed notebook will be rendered to html alongside its original .ipynb file for
    spot-checking.

    Args:
        notebook_fn: The filename of the notebook relative to the repo root.
    """
    notebook_id = notebook_fn.replace("/", "-")
    start = time.perf_counter()
    with open(f"./notebook_envs/{notebook_id}.stdout", "w") as stdout, open(
        f"./notebook_envs/{notebook_id}.stderr", "w"
    ) as stderr:
        try:
            _check_notebook(notebook_fn, notebook_id, stdout, stderr)
        except CalledProcessError:
            print("ERROR!", notebook_id)
    end = time.perf_counter()
    print(f"{notebook_id} {end - start:.1f}s")


NOTEBOOKS = [
    "docs/quantum_chess/concepts.ipynb",
    # 'docs/quantum_chess/quantum_chess_rest_api.ipynb', # runs a server, never finishes.
    # 'docs/quantum_chess/quantum_chess_client.ipynb',   # uses the server, requires modification.
]


def main():
    os.chdir(os.path.dirname(__file__))
    os.makedirs("./notebook_envs", exist_ok=True)
    with Pool(4) as pool:
        results = pool.map(check_notebook, NOTEBOOKS)
    print(results)


if __name__ == "__main__":
    main()
