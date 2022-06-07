# Copyright 2022 Google
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
import enum


class TicTacSquare(enum.Enum):
    EMPTY = 0
    X = 1
    O = 2


class TicTacResult(enum.Enum):
    UNFINISHED = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3
    BOTH_WIN = 4
