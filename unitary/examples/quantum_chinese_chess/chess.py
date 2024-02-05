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
    Color,
    MoveType,
    MoveVariant,
    TerminalType,
)
from unitary.examples.quantum_chinese_chess.move import (
    Jump,
    SplitJump,
    MergeJump,
    Slide,
    SplitSlide,
    MergeSlide,
    CannonFire,
)
import readline

# List of acceptable commands.
_HELP_TEXT = """
    Each location on the board is represented by two characters [abcdefghi][0-9], i.e. from a0 to i9. You may input (s=source, t=target)
    - s1t1 to do a slide move, e.g. "a1a4"; 
    - s1^t1t2 to do a split move, e.g. "a1^b1a2";
    - s1s2^t1 to do a merge move, e.g. "b1a2^a1";

    Other commands:
    - "peek": to peek (print a sample of) the current board state
    - "peek all": to print all possible board states with associated probabilities
    - "undo": to undo last move
    - "help": to see this message again
    - "exit": to quit the game
"""

_WELCOME_MESSAGE = """
        Welcome to Quantum Chinese Chess!
"""


class QuantumChineseChess:
    """A class that implements Quantum Chinese Chess using the unitary API."""

    def print_welcome(self) -> None:
        """Prints the welcome message. Gets board language and players' name."""
        print(_WELCOME_MESSAGE)
        print(_HELP_TEXT)
        # TODO(): add the whole set of Chinese interface support.
        lang = input(
            "Switch to Chinese board characters? (y/n) (default to be English)  "
        )
        if lang.lower() == "y":
            self.lang = Language.ZH
        else:
            self.lang = Language.EN
        terminal = input(
            "Are you running this game on Colab or Sublime Terminus? (y/n)  "
        )
        if terminal == "y":
            self.terminal = TerminalType.COLAB_OR_SUBLIME_TERMINUS
        else:
            self.terminal = TerminalType.MAC_OR_LINUX
        name_0 = input("Player 0's name (default to be Player_0):  ")
        self.players_name.append("Player_0" if len(name_0) == 0 else name_0)
        name_1 = input("Player 1's name (default to be Player_1):  ")
        self.players_name.append("Player_1" if len(name_1) == 0 else name_1)

    def __init__(self):
        self.players_name: List[str] = []
        self.print_welcome()
        self.board = Board.from_fen()
        self.board.set_language(self.lang)
        print(self.board.to_str(self.terminal))
        self.game_state = GameState.CONTINUES
        self.current_player = self.board.current_player
        self.debug_level = 3
        # This variable is used to save the classical properties of the whole board before each move is
        # made, so that if we later undo we could recover the earlier classical state.
        self.classical_properties_history: List[List[List[int]]] = []

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

    @classmethod
    def _is_in_palace(self, color: Color, x: int, y: int) -> bool:
        """Check if the given location is within palace. This check will be applied to all KING ans ADVISOR moves."""
        return (
            x <= ord("f")
            and x >= ord("d")
            and ((color == Color.RED and y <= 2) or (color == Color.BLACK and y >= 7))
        )

    def check_classical_rule(
        self, source: str, target: str, classical_path_pieces: List[str]
    ) -> None:
        """Check if the proposed move satisfies classical rules, and raises ValueError if not.

        Args:
            source: the name of the source piece
            target: the name of the target piece
            classical_path_pieces: the names of the path pieces from source to target (excluded)
        """
        source_piece = self.board.board[source]
        target_piece = self.board.board[target]
        # Check if the move is blocked by classical path piece.
        if len(classical_path_pieces) > 0 and source_piece.type_ != Type.CANNON:
            # The path is blocked by classical pieces.
            raise ValueError("The path is blocked.")

        # Check if the target has classical piece of the same color.
        if not target_piece.is_entangled and source_piece.color == target_piece.color:
            raise ValueError(
                "The target place has classical piece with the same color."
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
            if (source_piece.color == Color.RED and y1 > 4) or (
                source_piece.color == Color.BLACK and y1 < 5
            ):
                raise ValueError(
                    "ELEPHANT cannot cross the river (i.e. the middle line)."
                )
        elif source_piece.type_ == Type.ADVISOR:
            if not (abs(dx) == 1 and abs(dy) == 1):
                raise ValueError("ADVISOR cannot move like this.")
            if not self._is_in_palace(source_piece.color, x1, y1):
                raise ValueError("ADVISOR cannot leave the palace.")
        elif source_piece.type_ == Type.KING:
            if abs(dx) + abs(dy) != 1:
                raise ValueError("KING cannot move like this.")
            if not self._is_in_palace(source_piece.color, x1, y1):
                raise ValueError("KING cannot leave the palace.")
        elif source_piece.type_ == Type.CANNON:
            if dx != 0 and dy != 0:
                raise ValueError("CANNON cannot move like this.")
            if len(classical_path_pieces) > 0:
                if len(classical_path_pieces) > 1:
                    # Invalid cannon move, since there could only be at most one classical piece between
                    # the source (i.e. the cannon) and the target.
                    raise ValueError("CANNON cannot fire like this.")
                elif source_piece.color == target_piece.color:
                    raise ValueError("CANNON cannot fire to a piece with same color.")
                elif target_piece.color == Color.NA:
                    raise ValueError("CANNON cannot fire to an empty piece.")
        elif source_piece.type_ == Type.PAWN:
            if abs(dx) + abs(dy) != 1:
                raise ValueError("PAWN cannot move like this.")
            if source_piece.color == Color.RED:
                if dy == -1:
                    raise ValueError("PAWN can not move backward.")
                if y0 <= 4 and dy != 1:
                    raise ValueError(
                        "PAWN can only go forward before crossing the river (i.e. the middle line)."
                    )
            else:
                if dy == 1:
                    raise ValueError("PAWN can not move backward.")
                if y0 > 4 and dy != -1:
                    raise ValueError(
                        "PAWN can only go forward before crossing the river (i.e. the middle line)."
                    )

    def classify_move(
        self,
        sources: List[str],
        targets: List[str],
        classical_path_pieces_0: List[str],
        quantum_path_pieces_0: List[str],
        classical_path_pieces_1: List[str],
        quantum_path_pieces_1: List[str],
    ) -> Tuple[MoveType, MoveVariant]:
        """Determines and returns the MoveType and MoveVariant. This function assumes that check_classical_rule()
        has been called before this.

        Args:
            sources: the list of names of the source pieces
            targets: the list of names of the target pieces
            classical_path_pieces_0: the list of names of classical pieces from source_0 to target_0 (excluded)
            quantum_path_pieces_0: the list of names of quantum pieces from source_0 to target_0 (excluded)
            classical_path_pieces_1: the list of names of classical pieces from source_0 to target_1 (for split)
                                     or from source_1 to target_0 (for merge) (excluded)
            quantum_path_pieces_1: the list of names of quantum pieces from source_0 to target_1 (for split) or
                                     from source_1 to target_0 (for merge) (excluded)
        """
        move_type = MoveType.UNSPECIFIED
        move_variant = MoveVariant.UNSPECIFIED

        source = self.board.board[sources[0]]
        target = self.board.board[targets[0]]

        if len(sources) == 1 and len(targets) == 1:
            if len(quantum_path_pieces_0) == 0:
                if (
                    len(classical_path_pieces_0) == 0
                    and source.type_ == Type.CANNON
                    and target.color.value == 1 - source.color.value
                ):
                    # CANNON is special in that there has to be a platform between itself and the target
                    # to capture.
                    raise ValueError(
                        "CANNON could not fire/capture without a cannon platform."
                    )
                if not source.is_entangled and not target.is_entangled:
                    # This handles all classical cases, where no quantum piece is envolved.
                    # We don't need to further classify MoveVariant types since all classical cases
                    # will be handled in a similar way.
                    return MoveType.CLASSICAL, MoveVariant.CLASSICAL
                else:
                    # If any of the source or target is entangled, this move is a JUMP.
                    move_type = MoveType.JUMP
            else:
                # If there is any quantum path pieces, this move is a SLIDE.
                move_type = MoveType.SLIDE

            if (
                source.type_ == Type.CANNON
                and (
                    len(classical_path_pieces_0) == 1 or len(quantum_path_pieces_0) > 0
                )
                and target.color.value == 1 - source.color.value
            ):
                # By this time the classical cannon fire has been identified as CLASSICAL move,
                # so the current case has quantum piece(s) envolved.
                return MoveType.CANNON_FIRE, MoveVariant.CAPTURE

            # Determine MoveVariant.
            if target.color == Color.NA:
                # If the target piece is classical empty => BASIC.
                move_variant = MoveVariant.BASIC
            elif target.color == source.color:
                # If the target has the same color as the source => EXCLUDED.
                # TODO(): such move could be a merge. Take care of such cases later.
                move_variant = MoveVariant.EXCLUDED
            else:
                # If the target is on the opposite side => CAPTURE.
                move_variant = MoveVariant.CAPTURE

        elif len(sources) == 2:
            # Determine types for merge cases.
            source_1 = self.board.board[sources[1]]
            if not source.is_entangled or not source_1.is_entangled:
                raise ValueError(
                    "Both sources need to be in quantum state in order to merge."
                )
            # TODO(): Currently we don't support merge + excluded/capture, or cannon_merge_fire + capture. Maybe add support later.
            if len(classical_path_pieces_0) > 0 or len(classical_path_pieces_1) > 0:
                raise ValueError("Currently CANNON cannot merge while firing.")
            if target.type_ != Type.EMPTY:
                raise ValueError("Currently we could only merge into an empty piece.")
            if len(quantum_path_pieces_0) == 0 and len(quantum_path_pieces_1) == 0:
                # The move is MERGE_JUMP if there are no quantum pieces in either path.
                move_type = MoveType.MERGE_JUMP
            else:
                # The move is MERGE_SLIDE if there is quantum piece in any path.
                move_type = MoveType.MERGE_SLIDE
            # Currently we don't support EXCLUDE or CAPTURE typed merge moves.
            move_variant = MoveVariant.BASIC

        elif len(targets) == 2:
            # Determine types for split cases.
            target_1 = self.board.board[targets[1]]
            # TODO(): Currently we don't support split + excluded/capture, or cannon_split_fire + capture. Maybe add support later.
            if len(classical_path_pieces_0) > 0 or len(classical_path_pieces_1) > 0:
                raise ValueError("Currently CANNON cannot split while firing.")
            if target.type_ != Type.EMPTY or target_1.type_ != Type.EMPTY:
                raise ValueError("Currently we could only split into empty pieces.")
            if source.type_ == Type.KING:
                # TODO(): Currently we don't support KING split. Maybe add support later.
                raise ValueError("King split is not supported currently.")
            if len(quantum_path_pieces_0) == 0 and len(quantum_path_pieces_1) == 0:
                # The move is SPLIT_JUMP if there are no quantum pieces in either path.
                move_type = MoveType.SPLIT_JUMP
            else:
                # The move is SPLIT_SLIDE if there is quantum piece in any path.
                move_type = MoveType.SPLIT_SLIDE
            # Currently we don't support EXCLUDE or CAPTURE typed split moves.
            move_variant = MoveVariant.BASIC
        return move_type, move_variant

    def apply_move(self, str_to_parse: str) -> None:
        """Check if the input string is valid. If it is, determine the move type and variant and return the move."""
        sources, targets = self.parse_input_string(str_to_parse)

        # Additional checks based on the current board.
        for source in sources:
            if self.board.board[source].type_ == Type.EMPTY:
                raise ValueError("Could not move empty piece.")
            if self.board.board[source].color.value != self.board.current_player:
                raise ValueError("Could not move the other player's piece.")
        source_0 = self.board.board[sources[0]]
        target_0 = self.board.board[targets[0]]
        if len(sources) == 2:
            source_1 = self.board.board[sources[1]]
            if source_0.type_ != source_1.type_:
                raise ValueError("Two sources need to be the same type.")
        if len(targets) == 2:
            target_1 = self.board.board[targets[1]]
            # TODO(): handle the case where a piece is split into the current piece and another piece, in which case two targets are different.
            if target_0.type_ != target_1.type_:
                raise ValueError("Two targets need to be the same type.")
            if target_0.color != target_1.color:
                raise ValueError("Two targets need to be the same color.")

        # Check if the first path satisfies the classical rule.
        classical_pieces_0, quantum_pieces_0 = self.board.path_pieces(
            sources[0], targets[0]
        )
        self.check_classical_rule(sources[0], targets[0], classical_pieces_0)

        # Check if the second path (if exists) satisfies the classical rule.
        classical_pieces_1 = None
        quantum_pieces_1 = None

        if len(sources) == 2:
            classical_pieces_1, quantum_pieces_1 = self.board.path_pieces(
                sources[1], targets[0]
            )
            self.check_classical_rule(sources[1], targets[0], classical_pieces_1)
        elif len(targets) == 2:
            classical_pieces_1, quantum_pieces_1 = self.board.path_pieces(
                sources[0], targets[1]
            )
            self.check_classical_rule(sources[0], targets[1], classical_pieces_1)

        # Classify the move type and move variant.
        move_type, move_variant = self.classify_move(
            sources,
            targets,
            classical_pieces_0,
            quantum_pieces_0,
            classical_pieces_1,
            quantum_pieces_1,
        )

        if self.debug_level > 1:
            print(move_type, " ", move_variant)

        # Apply the move accoding to its type.
        # TODO(): using match...case... when python 3.11 satisfies the dependency.
        if move_type == MoveType.CLASSICAL:
            if source_0.type_ == Type.KING:
                # Update the locations of KING.
                self.board.king_locations[self.current_player] = targets[0]
                if self.debug_level > 1:
                    print(f"Updated king locations: {self.board.king_locations}.")
            if target_0.type_ == Type.KING:
                # King is captured, then the game is over.
                self.game_state = GameState(self.current_player)
            Jump(move_variant)(source_0, target_0)
        elif move_type == MoveType.JUMP:
            Jump(move_variant)(source_0, target_0)
        elif move_type == MoveType.SLIDE:
            Slide(quantum_pieces_0, move_variant)(source_0, target_0)
        elif move_type == MoveType.SPLIT_JUMP:
            SplitJump()(source_0, target_0, target_1)
        elif move_type == MoveType.SPLIT_SLIDE:
            SplitSlide(quantum_pieces_0, quantum_pieces_1)(source_0, target_0, target_1)
        elif move_type == MoveType.MERGE_JUMP:
            MergeJump()(source_0, source_1, target_0)
        elif move_type == MoveType.MERGE_SLIDE:
            MergeSlide(quantum_pieces_0, quantum_pieces_1)(source_0, source_1, target_0)
        elif move_type == MoveType.CANNON_FIRE:
            CannonFire(classical_pieces_0, quantum_pieces_0)(source_0, target_0)

    def next_move(self) -> Tuple[bool, str]:
        """Check if the player wants to exit or needs help message. Otherwise parse and apply the move.
        Returns True + output string if the move was made, otherwise returns False + output string.
        """
        input_str = input(
            f"\nIt is {self.players_name[self.current_player]}'s turn to move: "
        )
        output = ""
        if input_str.lower() == "help":
            output = _HELP_TEXT
        elif input_str.lower() == "exit":
            # The other player wins if the current player quits.
            self.game_state = GameState(1 - self.current_player)
            output = "Exiting."
        elif input_str.lower() == "peek":
            print(
                self.board.to_str(
                    self.terminal, None, self.board.board.peek(convert_to_enum=False)[0]
                )
            )
        elif input_str.lower() == "peek all":
            all_boards = self.board.board.get_correlated_histogram()
            sorted_boards = sorted(all_boards.items(), key=lambda x: x[1], reverse=True)
            for board, count in sorted_boards:
                print(
                    "\n ====== With probability ~ {:.1f} ======".format(count / 100.0)
                )
                print(self.board.to_str(self.terminal, None, list(board)))
        elif input_str.lower() == "undo":
            if self.undo():
                return True, "Undoing."
            return False, "Failed to undo."
        else:
            try:
                # The move is success if no ValueError is raised.
                self.apply_move(input_str.lower())
                return True, output
            except ValueError as e:
                output = f"Invalid move. {e}"
        return False, output

    def update_board_by_sampling(self) -> List[float]:
        """After quantum moves, there might be pieces that:
        - is actually empty, but their classical properties is not cleared; or
        - is actually classically occupied, but their is_entangled state is not updated.
        This method is called after each quantum move, and runs (100x) sampling of the board
        to identify and fix those cases.
        """
        probs = self.board.board.get_binary_probabilities()
        num_rows = 10
        num_cols = 9
        for row in range(num_rows):
            for col in "abcdefghi":
                piece = self.board.board[f"{col}{row}"]
                prob = probs[row * num_cols + ord(col) - ord("a")]
                # TODO(): This threshold does not actually work right now since we have 100 sampling.
                # Change it to be more meaningful values maybe when we do error mitigation.
                if prob < 1e-3:
                    piece.reset()
                    probs[row * num_cols + ord(col) - ord("a")] = 0
                elif prob > 1 - 1e-3:
                    piece.is_entangled = False
                    probs[row * num_cols + ord(col) - ord("a")] = 1
        return probs

    def game_over(self) -> None:
        """Checks if the game is over, and update self.game_state accordingly."""
        if self.game_state != GameState.CONTINUES:
            return
        if self.board.flying_general_check():
            # If two KINGs are directly facing each other (i.e. in the same column) without any pieces in between, then the game ends. The other player wins.
            self.game_state = GameState(1 - self.current_player)
        return
        # TODO(): add the following checks
        # - If player 0 made N repeatd back-and_forth moves in a row.

    def save_snapshot(self) -> None:
        """Saves the current length of the effect history, qubit_remapping_dict, and the current classical states of all pieces."""
        # Save the current length of the effect history and qubit_remapping_dict.
        self.board.board.save_snapshot()

        # Save the classical states of all pieces.
        snapshot = []
        for row in range(10):
            for col in "abcdefghi":
                piece = self.board.board[f"{col}{row}"]
                snapshot.append(
                    [piece.type_.value, piece.color.value, piece.is_entangled]
                )
        self.classical_properties_history.append(snapshot)

    def undo(self) -> bool:
        """Undo the last move, which includes reset quantum effects and classical properties, and remapping
        qubits.

        Returns True if the undo is success, and False otherwise.
        """
        world = self.board.board
        if (
            len(world.effect_history_length) <= 1
            or len(world.qubit_remapping_dict_length) <= 1
            or len(self.classical_properties_history) <= 1
        ):
            # length == 1 corresponds to the initial state, and no more undo could be made.
            return False

        # Recover the mapping of qubits to the last snapshot, remove any related post selection memory,
        # and recover the effects up to the last snapshot (which was saved after the last move finished).
        try:
            world.restore_last_snapshot()
        except ValueError as err:
            print(err)
            return False
        except Exception:
            print("Unexpected error during undo.")
            raise

        # Recover the classical properties of all pieces to the last snapshot.
        self.classical_properties_history.pop()
        snapshot = self.classical_properties_history[-1]
        index = 0
        for row in range(10):
            for col in "abcdefghi":
                piece = world[f"{col}{row}"]
                piece.type_ = Type(snapshot[index][0])
                piece.color = Color(snapshot[index][1])
                piece.is_entangled = snapshot[index][2]
                index += 1
        return True

    def play(self) -> None:
        """The loop where each player takes turn to play."""
        probs = None
        while True:
            move_success, output = self.next_move()
            if not move_success:
                # Continue if the player does not quit.
                if self.game_state == GameState.CONTINUES:
                    print(output)
                    print("\nPlease re-enter your move.")
                    continue
            print(output)
            if output != "Undoing.":
                # Check if the game is over.
                self.game_over()
                # Update any empty or occupied pieces' classical state.
                # TODO(): no need to do sampling if the last move was CLASSICAL.
                probs = self.update_board_by_sampling()
                # Save the current states.
                self.save_snapshot()
            else:
                probs = self.update_board_by_sampling()
            print(self.board.to_str(self.terminal, probs))
            if self.game_state == GameState.CONTINUES:
                # If the game continues, switch the player.
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


def main():
    game = QuantumChineseChess()
    game.play()


if __name__ == "__main__":
    main()
