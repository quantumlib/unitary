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
import enum

class SquareState(enum.Enum):
    EMPTY = 0
    OCCUPIED = 1


class MoveType(enum.Enum):
    NULL_TYPE = 0
    UNSPECIFIED_STANDARD = 1
    JUMP = 2
    SLIDE = 3
    SPLIT_JUMP = 4
    SPLIT_SLIDE = 5
    MERGE_JUMP = 6
    MERGE_SLIDE = 7
    HORSE_MOVE = 8
    HORSE_SPLIT_MOVE = 9
    HORSE_MERGE_MOVE = 10
    CANNON_FIRE = 11


class MoveVariant(enum.Enum):
    UNSPECIFIED = 0
    BASIC = 1
    EXCLUDED = 2
    CAPTURE = 3


class Piece(enum.Enum):
    EMPTY = 0
    SOLDIER = 1
    CANNON = 2
    ROOK = 3
    HORSE = 4
    ELEPHANT = 5
    ADVISOR = 6
    GENERAL = 7
