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
from typing import Tuple, List
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.enums import (
    Language,
    GameState,
    Type,
    MoveType,
    MoveVariant,
)
from unitary.examples.quantum_chinese_chess.move import Move

# List of accepable commands.
_HELP_TEXT = """
    Each location on the board is represented by two characters [abcdefghi][0-9], i.e. from a0 to i9. You may input (s=source, t=target)
    - s1t1 to do a slide move, e.g. "a1a4"; 
    - s1^t1t2 to do a split move, e.g. "a1^b1a2";
    - s1s2^t1 to do a merge move, e.g. "b1a2^a1";
    Other commands:
    - "exit" to quit
    - "help": to see this message again
"""

_WELCOME_MESSAGE = """
        Welcome to Quantum Chinese Chess!
"""


class QuantumChineseChess:
    """A class that implements Quantum Chinese Chess using the unitary API."""

    def __init__(self):
        self.players_name = []
        self.print_welcome()
        self.board = Board.from_fen()
        self.board.set_language(self.lang)
        print(self.board)
        self.game_state = GameState.CONTINUES
        self.current_player = self.board.current_player
        self.debug_level = 3

    def game_over(self) -> None:
        """Checks if the game is over, and update self.game_state accordingly."""
        if self.game_state != GameState.CONTINUES:
            return
        return
        # TODO(): add the following checks
        # - The current player wins if general is captured in the current move.
        # - The other player wins if the flying general rule is satisfied, i.e. there is no piece
        # (after measurement) between two generals.
        # - If player 0 made N repeatd back-and_forth moves in a row.

    @staticmethod
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

    def check_classical_rule(
        self, source: str, target: str, classical_path_pieces: List[str]
    ):
        source_piece = self.board.board[source]
        target_piece = self.board.board[target]
        # Check if the move is blocked by classical path piece.
        if len(classical_pieces) > 0:
            if sources.type_ != Type.CANNON:
                # The path is blocked by classical pieces.
                raise ValueError("Invalid move. The path is blocked.")
            elif len(classical_pieces) > 1:
                # Invalid cannon move, since there could only be at most one classical piece between
                # the source (i.e. the cannon) and the target.
                raise ValueError("Invalid move. Cannon cannot fire like this.")

        # Check if the target has classical piece of the same color.
        if (
            not target_piece.is_entanngled()
            and source_piece.color == target_piece.color
        ):
            raise ValueError(
                "Invalid move. The target place has classical piece with the same color."
            )

        # Check if the move violates any classical rule.
        x0 = ord(source[0])
        x1 = ord(target[0])
        dx = x1 - x0
        y0 = int(source[1])
        y1 = int(target[1])
        dy = y1 - y0

        if source_piece.type_ == Type.ROOK:
            if dx != 0 and dy != 0:
                raise ValueError("ROOK cannot move like this.")
        elif source_piece.type_ == Type.HORSE:
            if not ((abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)):
                raise ValueError("HORSE cannot move like this.")
        elif source_piece.type_ == Type.ELEPHANT:
            if not (abs(dx) == 2 and abs(dy) == 2):
                raise ValueError("ELEPHANT cannot move like this.")
            if (source_piece.color == color.RED and y1 < 5) or (
                source_piece.color == color.BLACK and y1 > 4
            ):
                raise ValueError(
                    "ELEPHANT cannot cross the river (i.e. the middle line)."
                )
        elif source_piece.type_ == Type.ADVISOR:
            if not (abs(dx) == 1 and abs(dy) == 1):
                raise ValueError("ADVISOR cannot move like this.")
            if (
                x1 > ord("f")
                or x1 < ord("d")
                or (source_piece.color == color.RED and y1 < 7)
                or (source_piece.color == color.BLACK and y1 > 2)
            ):
                raise ValueError("ADVISOR cannot leave the palace.")
        elif source_piece.type_ == Type.KING:
            if abs(dx) + abs(dy) != 1:
                raise ValueError("KING cannot move like this.")
            if (
                x1 > ord("f")
                or x1 < ord("d")
                or (source_piece.color == color.RED and y1 < 7)
                or (source_piece.color == color.BLACK and y1 > 2)
            ):
                raise ValueError("KING cannot leave the palace.")
        elif source_piece.type_ == Type.CANNON:
            if dx != 0 and dy != 0:
                raise ValueError("CANNON cannot move like this.")
        elif source_piece.type_ == Type.PAWN:
            if abs(dx) + abs(dy) != 1:
                raise ValueError("PAWN cannot move like this.")
            if source_piece.color == color.RED:
                if y0 > 4 and dy != -1:
                    raise ValueError(
                        "PAWN can only go forward before crossing the rive (i.e. the middle line)."
                    )
                if y0 <= 4 and dy == 1:
                    raise ValueError("PAWN can not move backward.")
            else:
                if y0 <= 4 and dy != 1:
                    raise ValueError(
                        "PAWN can only go forward before crossing the rive (i.e. the middle line)."
                    )
                if y0 > 4 and dy == -1:
                    raise ValueError("PAWN can not move backward.")

    def classify_move(
        self,
        sources: List[str],
        targets: List[str],
        classical_path_pieces_0: List[str],
        quantum_path_pieces_0: List[str],
        classical_path_pieces_1: List[str],
        quantum_path_pieces_1: List[str],
    ) -> Tuple[MoveType, MoveVariant]:
        """Determines the MoveType and MoveVariant."""
        move_type = MoveType.UNSPECIFIED_STANDARD
        move_variant = MoveVariant.UNSPECIFIED

        source = self.board.board[sources[0]]
        target = self.board.board[targets[0]]

        # Determine MoveType.
        if len(sources) == 1 and len(targets) == 1:
            if len(quantum_path_pieces_0) == 0:
                if not source.is_entangled() and not target.is_entangled():
                    move_type = MoveType.CLASSICAL
                else:
                    move_type = MoveType.JUMP
            else:
                move_type = MoveType.SLIDE
        elif len(sources) == 2:
            if len(quantum_path_pieces_0) == 0 and len(quantum_path_pieces_1) == 0:
                move_type = Type.MERGE_JUMP
            else:
                move_type = Type.MERGE_SLIDE
        elif len(targets) == 2:
            if len(quantum_path_pieces_0) == 0 and len(quantum_path_pieces_1) == 0:
                move_type = Type.SPLIT_JUMP
            else:
                move_type = Type.SPLIT_SLIDE

        # Determine MoveVariant.
        if target.color == Color.NA:
            move_variant = MoveVariant.BASIC
        elif target.color == source.color:
            move_variant = MoveVariant.EXCLUDED
        else:
            move_variant = MoveVariant.CAPTURE

    def apply_move(self, str_to_parse: str) -> None:
        """Check if the input string is valid. If it is, determine the move type and variant and return the move."""
        try:
            sources, targets = self.parse_input_string(str_to_parse)
        except ValueError as e:
            raise e

        # Additional checks based on the current board.
        for source in sources:
            if self.board.board[source].type_ == Type.EMPTY:
                raise ValueError("Could not move empty piece.")
            if self.board.board[source].color.value != self.board.current_player:
                raise ValueError("Could not move the other player's piece.")
        if len(sources) == 2:
            source_0 = self.board.board[sources[0]]
            source_1 = self.board.board[sources[1]]
            if source_0.type_ != source_1.type_:
                raise ValueError("Two sources need to be the same type.")
        if len(targets) == 2:
            target_0 = self.board.board[targets[0]]
            target_1 = self.board.board[targets[1]]
            if target_0.type_ != target_1.type_:
                raise ValueError("Two targets need to be the same type.")
            if target_0.color != target_1.color:
                raise ValueError("Two targets need to be the same color.")

        # Check if the first path satisfies the classical rule.
        classical_pieces_0, quantum_pieces_0 = board.path_pieces(sources[0], targets[0])
        try:
            check_classical_rule(sources[0], targets[0], classical_pieces_0)
        except ValueError as e:
            raise e

        # Check if the second path (if exists) satisfies the classical rule.
        classical_pieces_1 = None
        quantum_pieces_1 = None

        if len(sources) == 2:
            classical_pieces_1, quantum_pieces_1 = board.path_pieces(
                sources[1], targets[0]
            )
            try:
                check_classical_rule(sources[1], targets[0], classical_pieces_1)
            except ValueError as e:
                raise e
        elif len(targets) == 2:
            classical_pieces_1, quantum_pieces_1 = board.path_pieces(
                sources[0], targets[1]
            )
            try:
                check_classical_rule(sources[0], targets[1], classical_pieces_1)
            except ValueError as e:
                raise e

        try:
            move_type, move_variant = self.classify_move(
                sources,
                targets,
                classical_pieces_0,
                quantum_pieces_0,
                classical_pieces_1,
                quantum_pieces_1,
            )
        except ValueError as e:
            raise e

        # if len(sources) == 1 and len(targets) == 1:
        #     # Chances are normal/excluded/capture slide/jump or cannon fire.
        #     source = self.board.board[sources[0]]
        #     target = self.board.board[targets[0]]
        #     # Such move is jump, but needs further check.
        #     if len(quantum_pieces) == 0:
        #         # Classical case.
        #         if not source.is_entangled() and not target.type_ == Type.EMPTY:
        #             target.reset(source)
        #             source.reset()
        #             print("Classical jump.")
        #             return

    def next_move(self) -> bool:
        """Check if the player wants to exit or needs help message. Otherwise parse and apply the move.
        Returns True if the move was made, otherwise returns False.
        """
        input_str = input(
            f"\nIt is {self.players_name[self.current_player]}'s turn to move: "
        )
        if input_str.lower() == "help":
            print(_HELP_TEXT)
        elif input_str.lower() == "exit":
            # The other player wins if the current player quits.
            self.game_state = GameState(1 - self.current_player)
            print("Exiting.")
        else:
            try:
                # The move is success if no ValueError is raised.
                self.apply_move(input_str.lower())
                return True
            except ValueError as e:
                print(e)
        return False

    def play(self) -> None:
        """The loop where each player takes turn to play."""
        while True:
            move_success = self.next_move()
            print(self.board)
            if not move_success:
                # Continue if the player does not quit.
                if self.game_state == GameState.CONTINUES:
                    print("\nPlease re-enter your move.")
                    continue
            # Check if the game is over.
            self.game_over()
            # If the game continues, switch the player.
            if self.game_state == GameState.CONTINUES:
                self.current_player = 1 - self.current_player
                self.board.current_player = self.current_player
                continue
            elif self.game_state == GameState.RED_WINS:
                print(f"{self.players_name[0]} wins! Game is over.")
            elif self.game_state == GameState.BLACK_WINS:
                print(f"{self.players_name[1]} wins! Game is over.")
            elif self.game_state == GameState.DRAW:
                print("Draw! Game is over.")
            break

    def print_welcome(self) -> None:
        """Prints the welcome message. Gets board language and players' name."""
        print(_WELCOME_MESSAGE)
        print(_HELP_TEXT)
        # TODO(): add whole set of Chinese interface support.
        lang = input(
            "Switch to Chinese board characters? (y/n) (default to be English)  "
        )
        if lang.lower() == "y":
            self.lang = Language.ZH
        else:
            self.lang = Language.EN
        name_0 = input("Player 0's name (default to be Player_0):  ")
        self.players_name.append("Player_0" if len(name_0) == 0 else name_0)
        name_1 = input("Player 1's name (default to be Player_1):  ")
        self.players_name.append("Player_1" if len(name_1) == 0 else name_1)


def main():
    game = QuantumChineseChess()
    game.play()


if __name__ == "__main__":
    main()
