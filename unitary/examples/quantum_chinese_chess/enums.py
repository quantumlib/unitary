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
from typing import Optional


class Language(enum.Enum):
    EN = 0  # English
    ZH = 1  # Chinese


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


class Color(enum.Enum):
    NA = 0
    RED = 1
    BLACK = 2


class Type(enum.Enum):
    """The four values are symbols corresponding to
    English red
    English black
    Chinese red
    Chinese black
    """

    EMPTY = [".", ".", ".", "."]
    SOLDIER = ["s", "S", "兵", "卒"]
    CANNON = ["c", "C", "炮", "砲"]
    ROOK = ["r", "R", "车", "車"]
    HORSE = ["h", "H", "马", "馬"]
    ELEPHANT = ["e", "E", "象", "相"]
    ADVISOR = ["a", "A", "士", "仕"]
    GENERAL = ["g", "G", "将", "帥"]

    @staticmethod
    def type_of(c: str) -> Optional["Type"]:
        return {
            "s": Type.SOLDIER,
            "c": Type.CANNON,
            "r": Type.ROOK,
            "h": Type.HORSE,
            "e": Type.ELEPHANT,
            "a": Type.ADVISOR,
            "g": Type.GENERAL,
            ".": Type.EMPTY,
        }.get(c.lower(), None)
