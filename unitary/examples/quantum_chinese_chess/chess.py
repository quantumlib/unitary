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
from unitary.examples.quantum_chinese_chess.enums import Language
from unitary.examples.quantum_chinese_chess.move import Move, get_move_from_string

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


class QuantumChineseChess:
    """A class that implements Quantum Chinese Chess using the unitary API."""

    def __init__(self):
        self.players_name = []
        self.print_welcome()
        self.board = Board.from_fen()
        self.board.set_language(self.lang)
        print(self.board)
        self.player_quit = -1
        self.current_player = self.board.current_player
        self.debug_level = 3

    def game_over(self) -> int:
        """
        Checks if the game is over.
        Output:
            -1: game continues
             0: player 0 wins
             1: player 1 wins
             2: draw
        """
        # The other player wins if the current player quits.
        if self.player_quit > -1:
            return 1 - self.player_quit
        return -1
        # TODO(): add the following checks
        # - The current player wins if general is captured in the current move.
        # - The other player wins if the flying general rule is satisfied, i.e. there is no piece
        # (after measurement) between two generals.
        # - If player 0 made N repeatd back-and_forth moves in a row.

    def get_move(self) -> Move:
        input_str = input(
            f"\nIt is {self.players_name[self.current_player]}'s turn to move: "
        )
        if input_str.lower() == "help":
            print(_HELP_TEXT)
            raise ValueError("")
        if input_str.lower() == "exit":
            self.player_quit = self.current_player
            raise ValueError("Existing.")
        try:
            move = get_move_from_string(input_str.lower(), self.board)
            return move
        except ValueError as e:
            raise e

    def play(self) -> None:
        """The loop where each player takes turn to play."""
        while True:
            try:
                move = self.get_move()
                print(move.to_str(self.debug_level))
                # TODO(): apply the move.
                print(self.board)
            except ValueError as e:
                print(e)
                # Continue if the player does not quit.
                if self.player_quit == -1:
                    print("\nPlease re-enter your move.")
                    continue
            # Check if the game is over.
            game_over = self.game_over()
            # If the game continues, switch the player.
            if game_over == -1:
                self.current_player = 1 - self.current_player
                self.board.current_player = self.current_player
                continue
            elif game_over == 0:
                print(f"{self.players_name[0]} wins! Game is over.")
            elif game_over == 1:
                print(f"{self.players_name[1]} wins! Game is over.")
            elif game_over == 2:
                print("Draw! Game is over.")
            break

    def print_welcome(self) -> None:
        """
        Prints the welcome message. Gets board language and players' name.
        """
        welcome_message = """
        Welcome to Quantum Chinese Chess!
        """
        print(welcome_message)
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
