# Copyright 2020 Google
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
import functools
import operator

from setuptools import find_packages, setup

__version__ = ''
exec(open('unitary/_version.py').read())
assert __version__, 'Version string cannot be empty'


def _parse_requirements(path: pathlib.Path):
    lines = [line.strip() for line in path.read_text().splitlines() if line]
    return [line for line in lines if not line.startswith('#')]


install_requires = _parse_requirements(pathlib.Path('requirements.txt'))
#extras_require_dir = [
#    'quantum_chess',
#]
#extras_require = {
#    r: _parse_requirements(pathlib.Path(f'recirq/{r}/extra-requirements.txt'))
#    for r in extras_require_dir
#}

# TODO(gh-231): remove and require users to install via extras_require.
install_requires = functools.reduce(operator.add, extras_require.values(), install_requires)

setup(name='recirq',
      version=__version__,
      url='http://github.com/quantumlib/unitary',
      author='Quantum AI team and collaborators',
      author_email='cirq@googlegroups.com',
      python_requires='>=3.6.0',
      install_requires=install_requires,
#      extras_require=extras_require,
      license='Apache 2',
      description="",
      long_description=open('README.md', encoding='utf-8').read(),
      packages=find_packages(),
      package_data={'unitary': [
      ]},
      )
