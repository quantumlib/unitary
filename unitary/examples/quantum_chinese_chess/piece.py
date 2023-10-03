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
from colorama import Fore
from unitary.alpha import QuantumObject
from enums import (
    SquareState,
    Language,
    Color,
    Type,
)


class Piece(QuantumObject):
    def __init__(self, name: str, state: SquareState, type_: Type, color: Color):
        QuantumObject.__init__(self, name, state)
        self.type_ = type_
        self.color = color

    def symbol(self, print_color: bool = True, lang: Language = Language.EN) -> str:
        if not print_color:
            return Type.symbol(self.type_, self.color, lang)
        if self.color != Color.RED:
            return Fore.WHITE + Type.symbol(self.type_, self.color, lang)
        return Fore.RED + Type.symbol(self.type_, self.color, lang) + Fore.RESET

    def __str__(self):
        return self.symbol()
