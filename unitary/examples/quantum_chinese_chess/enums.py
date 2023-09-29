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
    EN = 0 # English
    ZH = 1 # Chinese


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


class Piece:
    class Type(enum.Enum):
        EMPTY = '.'
        SOLDIER = 's'
        CANNON = 'c'
        ROOK = 'r'
        HORSE = 'h'
        ELEPHANT = 'e'
        ADVISOR = 'a'
        GENERAL = 'g'

    class Color(enum.Enum):
        NA = 0
        RED = 1
        BLACK = 2

    def __init__(self, type_: Type, color_: Color):
        self.type_ = type_
        self.color_ = color_

    def type_of(c: str) -> Optional["Type"]:
        return {
            's': Piece.Type.SOLDIER,
            'c': Piece.Type.CANNON,
            'r': Piece.Type.ROOK,
            'h': Piece.Type.HORSE,
            'e': Piece.Type.ELEPHANT,
            'a': Piece.Type.ADVISOR,
            'g': Piece.Type.GENERAL,
            '.': Piece.Type.EMPTY
            }.get(c.lower(), None)

    def red_symbol(self, lang: Language = Language.EN) -> str:
        if lang == Language.EN:  # Return English symbols
            return self.type_.value.upper()
        else:  # Return Chinese symbols
            return {
                Piece.Type.SOLDIER: '兵',
                Piece.Type.CANNON: '炮',
                Piece.Type.ROOK: '车',
                Piece.Type.HORSE: '马',
                Piece.Type.ELEPHANT: '象',
                Piece.Type.ADVISOR: '士',
                Piece.Type.GENERAL: '将',
                Piece.Type.EMPTY: '.'
            }.get(self.type_)

    def black_symbol(self, lang: Language = Language.EN) -> str:
        if lang == Language.EN:  # Return English symbols
            return self.type_.value
        else:  # Return Chinese symbols
            return {
                Piece.Type.SOLDIER: '卒',
                Piece.Type.CANNON: '砲',
                Piece.Type.ROOK: '車',
                Piece.Type.HORSE: '馬',
                Piece.Type.ELEPHANT: '相',
                Piece.Type.ADVISOR: '仕',
                Piece.Type.GENERAL: '帥',
                Piece.Type.EMPTY: '.'
            }.get(self.type_)

    def symbol(self, lang: Language = Language.EN) -> str:
        return {
            Piece.Color.RED: self.red_symbol(lang),
            Piece.Color.BLACK: self.black_symbol(lang),
            Piece.Color.NA: '.'
        }.get(self.color_)
