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
from typing import Optional, List, Tuple
from unitary.alpha.quantum_effect import QuantumEffect
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.enums import MoveType, MoveVariant, Type


def parse_input_string(str_to_parse: str) -> Tuple[List[str], List[str]]:
    """Check if the input string could be turned into a valid move.
    Returns the sources and targets if it is valid.
    The input needs to be:
        - s1t1 for slide/jump move; or
        - s1^t1t2 for split moves; or
        - s1s2^t1 for merge moves.
    Examples:
       'a1a2'
       'b1^a3c3'
       'a3b1^c3'
    """
    sources = None
    targets = None

    if "^" in str_to_parse:
        sources_str, targets_str = str_to_parse.split("^", maxsplit=1)
        # The only two allowed cases here are s1^t1t2 and s1s2^t1.
        if (
            str_to_parse.count("^") > 1
            or len(str_to_parse) != 7
            or len(sources_str) not in [2, 4]
        ):
            raise ValueError(f"Invalid sources/targets string {str_to_parse}.")
        sources = [sources_str[i : i + 2] for i in range(0, len(sources_str), 2)]
        targets = [targets_str[i : i + 2] for i in range(0, len(targets_str), 2)]
        if len(sources) == 2:
            if sources[0] == sources[1]:
                raise ValueError("Two sources should not be the same.")
        elif targets[0] == targets[1]:
            raise ValueError("Two targets should not be the same.")
    else:
        # The only allowed case here is s1t1.
        if len(str_to_parse) != 4:
            raise ValueError(f"Invalid sources/targets string {str_to_parse}.")
        sources = [str_to_parse[0:2]]
        targets = [str_to_parse[2:4]]
        if sources[0] == targets[0]:
            raise ValueError("Source and target should not be the same.")

    # Make sure all the locations are valid.
    for location in sources + targets:
        if location[0].lower() not in "abcdefghi" or not location[1].isdigit():
            raise ValueError(
                f"Invalid location string. Make sure they are from a0 to i9."
            )
    return sources, targets


def get_move_from_string(str_to_parse: str, board: Board) -> "Move":
    """Check if the input string is valid. If it is, determine the move type and variant and return the move."""
    try:
        sources, targets = parse_input_string(str_to_parse)
    except ValueError as e:
        raise e
    # Additional checks based on the current board.
    for source in sources:
        if board.board[source].type_ == Type.EMPTY:
            raise ValueError("Could not move empty piece.")
        if board.board[source].color.value != board.current_player:
            raise ValueError("Could not move the other player's piece.")
    # TODO(): add analysis to determine move type and variant.
    move_type = MoveType.UNSPECIFIED_STANDARD
    move_variant = MoveVariant.UNSPECIFIED
    return Move(
        sources[0],
        targets[0],
        board=board,
        move_type=move_type,
        move_variant=move_variant,
    )


class Move(QuantumEffect):
    """The base class of all chess moves."""

    def __init__(
        self,
        source: str,
        target: str,
        board: Board,
        source2: Optional[str] = None,
        target2: Optional[str] = None,
        move_type: Optional[MoveType] = None,
        move_variant: Optional[MoveVariant] = None,
    ):
        self.source = source
        self.source2 = source2
        self.target = target
        self.target2 = target2
        self.move_type = move_type
        self.move_variant = move_variant
        self.board = board

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.source == other.source
                and self.source2 == other.source2
                and self.target == other.target
                and self.target2 == other.target2
                and self.move_type == other.move_type
                and self.move_variant == other.move_variant
            )
        return False

    def _verify_objects(self, *objects):
        # TODO(): add checks that apply to all move types
        return

    def effect(self, *objects):
        # TODO(): add effects according to move_type and move_variant
        return

    def is_split_move(self) -> bool:
        return self.target2 is not None

    def is_merge_move(self) -> bool:
        return self.source2 is not None

    def to_str(self, verbose_level: int = 1) -> str:
        """
        Constructs the string representation of the move.
        According to the value of verbose_level:
        - 1: only returns the move source(s) and target(s);
        - 2: additionally returns the move type and variant;
        - 3: additionally returns the source(s) and target(s) piece type and color.
        """
        if verbose_level < 1:
            return ""

        if self.is_split_move():
            move_str = [self.source + "^" + self.target + str(self.target2)]
        elif self.is_merge_move():
            move_str = [self.source + str(self.source2) + "^" + self.target]
        else:
            move_str = [self.source + self.target]

        if verbose_level > 1:
            move_str.append(self.move_type.name)
            move_str.append(self.move_variant.name)

        if verbose_level > 2:
            source = self.board.board[self.source]
            target = self.board.board[self.target]
            move_str.append(
                source.color.name
                + "_"
                + source.type_.name
                + "->"
                + target.color.name
                + "_"
                + target.type_.name
            )
        return ":".join(move_str)

    def __str__(self):
        return self.to_str()
