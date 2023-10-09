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
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.enums import Language, GameState
from unitary.examples.quantum_chinese_chess.move import Move, apply_move

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
        """Checks if the game is over."""
        if self.game_state != GameState.CONTINUES:
            return
        return GameState.CONTINUES
        # TODO(): add the following checks
        # - The current player wins if general is captured in the current move.
        # - The other player wins if the flying general rule is satisfied, i.e. there is no piece
        # (after measurement) between two generals.
        # - If player 0 made N repeatd back-and_forth moves in a row.

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
                apply_move(input_str.lower(), self.board)
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
