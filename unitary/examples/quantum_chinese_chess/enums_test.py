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
from unitary.examples.quantum_chinese_chess.enums import Type, Color, Language


def test_type_type_of():
    assert Type.type_of("s") == Type.SOLDIER
    assert Type.type_of("S") == Type.SOLDIER
    assert Type.type_of("g") == Type.GENERAL
    assert Type.type_of("G") == Type.GENERAL
    assert Type.type_of(".") == Type.EMPTY
    assert Type.type_of("b") == None
