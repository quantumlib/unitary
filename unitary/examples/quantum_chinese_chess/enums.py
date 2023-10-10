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
    """Currently we support the following two ways to print the board.
    TODO(): support Chinese langurage instructions.
    """

    EN = 0  # English
    ZH = 1  # Chinese


class SquareState(enum.Enum):
    """Defines two possible initial state of each piece of the board."""

    EMPTY = 0
    OCCUPIED = 1


class GameState(enum.Enum):
    """Defines all possible outcomes of the game, plus the continue state."""

    CONTINUES = -1
    RED_WINS = 0
    BLACK_WINS = 1
    DRAW = 2


# TODO(): consider if we could allow split/merge + excluded/capture,
# and cannon_split_fire/cannon_merge_fire + capture
class MoveType(enum.Enum):
    """Each valid move will be classfied into one of the following MoveTypes."""

    CLASSICAL = 0
    UNSPECIFIED_STANDARD = 1
    JUMP = 2
    SLIDE = 3
    SPLIT_JUMP = 4
    SPLIT_SLIDE = 5
    MERGE_JUMP = 6
    MERGE_SLIDE = 7
    CANNON_FIRE = 8


class MoveVariant(enum.Enum):
    """Each valid move will be classfied into one of the following MoveVariant, in addition to
    the MoveType above.
    """

    UNSPECIFIED = 0
    BASIC = 1
    EXCLUDED = 2
    CAPTURE = 3


class Color(enum.Enum):
    """Empty pieces are associated with Color=NA. Other pieces should be either RED or BLACK."""

    NA = -1
    RED = 0
    BLACK = 1


class Type(enum.Enum):
    """The names are from FEN for Xiangqi.
    The four values are symbols corresponding to
    - English red
    - English black
    - Chinese red
    - Chinese black
    """

    EMPTY = (".", ".", ".", ".")
    PAWN = ("P", "p", "兵", "卒")
    CANNON = ("C", "c", "炮", "砲")
    ROOK = ("R", "r", "车", "車")
    HORSE = ("H", "h", "马", "馬")
    ELEPHANT = ("E", "e", "象", "相")
    ADVISOR = ("A", "a", "士", "仕")
    KING = ("K", "k", "将", "帥")

    @staticmethod
    def type_of(c: str) -> Optional["Type"]:
        return {
            "p": Type.PAWN,
            "c": Type.CANNON,
            "r": Type.ROOK,
            "h": Type.HORSE,
            "e": Type.ELEPHANT,
            "a": Type.ADVISOR,
            "k": Type.KING,
            ".": Type.EMPTY,
        }.get(c.lower(), None)

    @staticmethod
    def symbol(type_: "Type", color: Color, lang: Language = Language.EN) -> str:
        """Returns symbol of the given piece according to its color and desired language."""
        if type_ == Type.EMPTY:
            return "."
        if lang == Language.EN:  # Return English symbols
            if color == Color.RED:
                return type_.value[0]
            elif color == Color.BLACK:
                return type_.value[1]
        elif lang == Language.ZH:  # Return Chinese symbols
            if color == Color.RED:
                return type_.value[2]
            elif color == Color.BLACK:
                return type_.value[3]
        raise ValueError("Unexpected combinations of language and color.")
