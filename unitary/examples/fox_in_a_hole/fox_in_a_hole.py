# Copyright 2022 Google
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

"""Classical and quantum Fox-in-a-hole game."""

import abc
import sys
import enum
import numpy as np

from unitary.alpha import (
    QuantumObject,
    QuantumWorld,
    Move,
    PhasedMove,
    Split,
    PhasedSplit,
)


class Game(abc.ABC):
    """Abstract ancestor class for Fox-in-a-hole game.

    Parameters:
    * hole_nr: integer - Number of holes
    * seed:    integer - Seed for random number generated (used for testing)
    """

    def __init__(self, hole_nr=5, seed=None):
        self.rng = np.random.default_rng(seed=seed)

        self.history = []

        self.all_hole_names = [str(i) for i in range(hole_nr)]

        self.hole_nr = hole_nr

        self.state = None
        self.initialize_state()

    @abc.abstractmethod
    def initialize_state(self):
        """Initializes the actual state."""

    @abc.abstractmethod
    def state_to_string(self) -> str:
        """Returns the string reprezentation of the state."""

    @abc.abstractmethod
    def check_guess(self, guess) -> bool:
        """Checks if user's guess is right and returns it as a boolean value."""

    @abc.abstractmethod
    def take_random_move(self) -> str:
        """Applies a random move on the current state. Gives back the move in string format."""

    def history_append_state(self):
        """Append the current state into the history."""
        self.history.append("State: {}".format(self.state_to_string()))

    def history_append_move(self, move_str):
        """Append the given move into the history."""
        self.history.append(move_str)

    def history_append_guess(self, guess):
        """Append the given guess into the history."""
        self.history.append("Guess: {}".format(guess))

    def run(self):
        """Handles the main game-loop of the Fox-in-a-hole game."""
        max_step_nr = 10
        step_nr = 0
        self.history_append_state()
        while step_nr < max_step_nr:
            while True:
                print("Where is the fox? (0-{} or q for quit)".format(self.hole_nr - 1))
                input_str = input()
                if input_str in ("q", "Q") or input_str in self.all_hole_names:
                    break
            if input_str in ("q", "Q"):
                print("\nQuitting.\n")
                break
            guess = int(input_str)
            self.history_append_guess(guess)
            result = self.check_guess(guess)
            self.history_append_state()
            if result:
                print("\nCongratulations! You won in {} step(s).\n".format(step_nr + 1))
                break
            move_str = self.take_random_move()
            self.history_append_move(move_str)
            self.history_append_state()
            step_nr += 1
        if step_nr == max_step_nr:
            print("\nIt seems you have lost :-(. Try again.\n")
        self.print_history()

    def print_history(self):
        """Prints out the history of states, guesses and moves."""
        print("History:")
        for hist_elem in self.history:
            print(hist_elem)


class ClassicalGame(Game):
    """Classical Fox-in-a-hole game."""

    def initialize_state(self):
        self.state = self.hole_nr * [0.0]
        index = self.rng.integers(low=0, high=self.hole_nr)
        self.state[index] = 1.0

    def state_to_string(self) -> str:
        return str(self.state)

    def check_guess(self, guess) -> bool:
        """Checks if user's guess is right and returns it as a boolean value."""
        return self.state[guess] == 1.0

    def take_random_move(self) -> str:
        """Applies a random move on the current state. Gives back the move in string format."""
        source = self.state.index(1.0)
        direction = self.rng.integers(low=0, high=2) * 2 - 1
        if source == 0 and direction == -1:
            direction = 1
        elif source == self.hole_nr - 1 and direction == 1:
            direction = -1
        self.state[source] = 0.0
        self.state[source + direction] = 1.0
        if direction == -1:
            dir_str = "left"
        else:
            dir_str = "right"
        move_str = f"Moving {dir_str} from position {source}."
        return move_str


class Hole(enum.Enum):
    """Enum for quantom object Hole."""

    EMPTY = 0
    FOX = 1


class QuantumGame(Game):
    """Fox-in-a-hole game with quantum effects.

    Structure of state:
    (QuantumWorld, [QuantumObject]) -> quantum world, list of holes
    """

    def __init__(self, hole_nr=5, iswap=False, seed=None):
        self.iswap = iswap
        super().__init__(hole_nr=hole_nr, seed=seed)

    def initialize_state(self):
        index = self.rng.integers(low=0, high=self.hole_nr)
        holes = []
        for i in range(self.hole_nr):
            hole = QuantumObject(
                f"Hole-{i}-{i}", Hole.FOX if i == index else Hole.EMPTY
            )
            holes.append(hole)
        self.state = (QuantumWorld(holes), holes)

    def state_to_string(self):
        return str(self.state[0].get_binary_probabilities(objects=self.state[1]))

    def check_guess(self, guess) -> bool:
        """Checks if user's guess is right and returns it as a boolean value.

        In the quantum version, quantum-measurement happens which might change the state.
        """
        measurement = self.state[0].pop([self.state[1][guess]])[0]
        return measurement == Hole.FOX

    def take_random_move(self) -> str:
        """Applies a random move on the current state. Gives back the move in string format."""
        probs = self.state[0].get_binary_probabilities(objects=self.state[1])
        non_empty_holes = []
        for i, prob in enumerate(probs):
            if prob > 0:
                non_empty_holes.append(i)
        index = self.rng.integers(low=0, high=len(non_empty_holes))
        source = non_empty_holes[index]
        direction = self.rng.integers(low=-1, high=2)  # -1: left; 0: both; 1:right

        if source == 0:
            direction = 1
        elif source == self.hole_nr - 1:
            direction = -1
        if direction in (-1, 1):  # Move left or right
            target = source + direction
            if self.iswap:
                PhasedMove()(self.state[1][source], self.state[1][target])
                swap_str = "iSWAP"
            else:
                Move()(self.state[1][source], self.state[1][target])
                swap_str = "SWAP"
            if direction == -1:
                dir_str = "left"
            else:
                dir_str = "right"
            move_str = f"Moving ({swap_str}-based) {dir_str} from position {source}."
        else:  # Move left & right (split)
            if self.iswap:
                PhasedSplit()(
                    self.state[1][source],
                    self.state[1][source - 1],
                    self.state[1][source + 1],
                )
                swap_str = "iSWAP"
            else:
                Split()(
                    self.state[1][source],
                    self.state[1][source - 1],
                    self.state[1][source + 1],
                )
                swap_str = "SWAP"
            move_str = (
                "Splitting ({}-based) from position {} to positions {} and {}.".format(
                    swap_str, source, source - 1, source + 1
                )
            )
        return move_str


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage:")
        print("python3 fox_in_a_hole.py [-q] [-i] [-h]")
        print("-h: This help.")
        print("-q: Use quantum version instead of classical version.")
        print("-i: Use iSWAP for moves in quantum version.")
        sys.exit(0)
    if "-q" in sys.argv:
        use_iswap = "-i" in sys.argv
        game = QuantumGame(iswap=use_iswap)
        print("Quantum Fox-in-a-hole game.")
    else:
        game = ClassicalGame()
        print("Classical Fox-in-a-hole game.")

    game.run()
