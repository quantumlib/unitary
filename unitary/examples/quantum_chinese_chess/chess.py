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
from unitary.examples.quantum_chinese_chess.enums import Language, GameState, Type
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
        # TODO(): add analysis to determine move type and variant.

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
