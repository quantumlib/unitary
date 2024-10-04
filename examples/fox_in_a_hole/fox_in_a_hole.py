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

"""Classical and quantum Fox-in-a-hole game."""

import abc
import argparse
import sys
import enum
from typing import Optional

import numpy as np

from unitary.alpha import (
    QuantumObject,
    QuantumWorld,
    Move,
    PhasedMove,
    Split,
    PhasedSplit,
    SparseSimulator,
)


class Game(abc.ABC):
    """Abstract ancestor class for Fox-in-a-hole game.

    This class does the mechanical operations of the
    Fox-in-a-hole game:  Keeping track of the history of
    moves, running the game by looping through guesses,
    and printing out the history.

    This class has two variants.  `ClassicalGame`
    demonstrates how to play the classical version of
    Fox-in-a-hole, often found in riddle and puzzle books.
    `QuantumGame` is a quantum variant, where, instead of
    moving from one hole to the next, the fox will move
    to a superposition of both adjacent holes by using a
    `Split` operator.

    This class has 4 abstract methods.  These methods will
    vary depending on whether the game is the classical or
    quantum variant:

    - initialize_state(): This function will initialize the game.
    - state_to_string(): This returns the state of the game as
        a string so it can be printed out.
    - check_guess(guess):  This checks whether the user's guess
        is correct.  In the classical version, this just checks
        whether the fox is in the hole. In the quantum version,
        this performs a measurement to determine if the fox is in
        this location.
    - take_random_move():  This function should move the fox.
        In the classical version, the fox moves to an adjacent hole.
        In the quantum version, the fox "splits" and moves to both
        adjacent holes.

    Args:
        number_of_holes:  The number of holes that the fox
            can hide in.
        seed: Seed for random number generator. (used for testing)
    """

    def __init__(self, number_of_holes: int = 5, seed: Optional[int] = None):
        # Initialize random number generate.
        self.rng = np.random.default_rng(seed=seed)

        # Initialize history and attributes of the object.
        self.history = []
        self.number_of_holes = number_of_holes

        # Initialize state of the game.
        self.state = None
        self.initialize_state()

    @abc.abstractmethod
    def initialize_state(self):
        """Initializes the actual state.

        This is an abstract method and will vary depending on
        whether the game is played classically or quantum.
        """

    @abc.abstractmethod
    def state_to_string(self) -> str:
        """Returns the string reprezentation of the state.

        This is an abstract method and will vary depending on
        whether the game is played classically or quantum.
        """

    @abc.abstractmethod
    def check_guess(self, guess: int) -> bool:
        """Checks if user's guess is right and returns it as a boolean value.

        This is an abstract method and will vary depending on
        whether the game is played classically or quantum.

        Args:
            guess: Which number hole that the user guessed.
        """

    @abc.abstractmethod
    def take_random_move(self) -> str:
        """Applies a random move on the current state.

        This is an abstract method and will vary depending on
        whether the game is played classically or quantum.

        Returns:  The move in string format.
        """

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
        self.history_append_state()

        # Ask for user guesses until the game ends
        for step_nr in range(max_step_nr):
            # Get the user guess for the fox's position.
            # Ask until the user inputs a valid result.
            guess = -1
            while guess < 0 or guess >= self.number_of_holes:
                print(f"Where is the fox? (0-{self.number_of_holes - 1} or q for quit)")
                input_str = input()
                if input_str in ("q", "Q"):
                    print("\nQuitting.\n")
                    self.print_history()
                try:
                    guess = int(input_str)
                except ValueError:
                    print("Invalid guess.")

            # Append guess to the history
            self.history_append_guess(guess)

            # Check whether the guess was correct.
            result = self.check_guess(guess)
            self.history_append_state()

            if result:
                print("\nCongratulations! You won in {} step(s).\n".format(step_nr + 1))
                self.print_history()
                return

            # Move the fox and keep track of history.
            move_str = self.take_random_move()
            self.history_append_move(move_str)
            self.history_append_state()

        print("\nIt seems you have lost :-(. Try again.\n")
        self.print_history()

    def print_history(self):
        """Prints out the history of states, guesses and moves."""
        print("History:")
        for hist_elem in self.history:
            print(hist_elem)


class ClassicalGame(Game):
    """Classical Fox-in-a-hole game.

    In this version, we play the classical version of
    Fox-in-a-Hole.

    Each hole is either 0.0 (Fox not there) or 1.0 (Fox is there).

    """

    def initialize_state(self):
        # All holes start as empty
        self.state = [0.0] * self.number_of_holes

        # Pick a random hole index and put the fox in it
        index = self.rng.integers(low=0, high=self.number_of_holes)
        self.state[index] = 1.0

    def state_to_string(self) -> str:
        return str(self.state)

    def check_guess(self, guess) -> bool:
        """Checks if user's guess is right and returns it as a boolean value."""
        return self.state[guess] == 1.0

    def take_random_move(self) -> str:
        """Applies a random move on the current state.

        Moves the fox in a random direction (either forward or backwards).
        If the fox is on one end of the track (position 0 or self.number_of_holes -1),
        it only has one choice.

        Returns: The move in string format."""

        # Get where the fox started
        source = self.state.index(1.0)

        # If the fox is on the end, it has one choice.
        # Otherwise, it can move either direction.
        if source == 0:
            direction = 1
        elif source == self.number_of_holes - 1:
            direction = -1
        else:
            direction = self.rng.choice([1, -1])

        # Move fox.
        self.state[source] = 0.0
        self.state[source + direction] = 1.0

        dir_str = "left" if direction == -1 else "right"
        return f"Moving {dir_str} from position {source}."


class Hole(enum.Enum):
    """Enum for quantom object Hole."""

    EMPTY = 0
    FOX = 1


class QuantumGame(Game):
    """Fox-in-a-hole game with quantum effects.

    Structure of state:
    (QuantumWorld, [QuantumObject]) -> quantum world, list of holes
    """

    def __init__(self, number_of_holes: int = 5, iswap: bool = False, qprob:float = 0.5, seed: Optional[int] = None):
        if iswap:
            self.move_operation = PhasedMove()
            self.split_operation = PhasedSplit()
            self.swap_str = "iSWAP"
        else:
            self.move_operation = Move()
            self.split_operation = Split()
            self.swap_str = "SWAP"

        self.iswap = iswap
        self.qprob = qprob
        super().__init__(number_of_holes=number_of_holes, seed=seed)

    def initialize_state(self):
        index = self.rng.integers(low=0, high=self.number_of_holes)
        holes = []
        for i in range(self.number_of_holes):
            hole = QuantumObject(f"Hole-{i}", Hole.FOX if i == index else Hole.EMPTY)
            holes.append(hole)
        self.state = (QuantumWorld(holes, sampler=SparseSimulator()), holes)

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
        non_empty_holes = [i for i, p in enumerate(probs) if p > 0]
        index = self.rng.integers(low=0, high=len(non_empty_holes))
        source = non_empty_holes[index]

        # Choose whether to move in one direction or both directions.
        if self.rng.random() < self.qprob:
            direction = 0  # Left & right at the same time
        else:
            direction = self.rng.choice([1, -1])  # -1: left; 1:right

        # If the fox is on the edge, it only has one choice
        if source == 0:
            direction = 1
        elif source == self.number_of_holes - 1:
            direction = -1

        if direction in (-1, 1):
            # Move left or right using a (Phased)Move operation
            target = source + direction
            self.move_operation(self.state[1][source], self.state[1][target])
            dir_str = "left" if direction == -1 else "right"
            return f"Moving ({self.swap_str}-based) {dir_str} from position {source}."
        else:
            # Move left & right (split) using a (Phased) operation
            self.split_operation(
                self.state[1][source],
                self.state[1][source - 1],
                self.state[1][source + 1],
            )
            return (
                f"Splitting ({self.swap_str}-based) from position {source} "
                f"to positions {source-1} and {source+1}."
            )


if __name__ == "__main__":
    # Create command-line arguments for Fox-in-a-hole

    parser = argparse.ArgumentParser(description="Fox-in-a-hole game.")

    parser.add_argument(
        "-q",
        dest="is_quantum",
        action="store_const",
        const=True,
        default=False,
        help="Use quantum version instead of classical version.",
    )
    parser.add_argument(
        "-i",
        dest="use_iswap",
        action="store_const",
        const=True,
        default=False,
        help="Use iSWAP for moves in quantum case.",
    )
    parser.add_argument(
        "-qprob",
        metavar="p",
        type=float,
        dest="qprob",
        help="Probability p of quantum move: 0.0<=p<=1.0. Default: 0.5.",
    )
    args = parser.parse_args()

    # Set defaults for arguments when not specified

    if args.qprob is not None and not 0.0 < args.qprob <= 1.0:
        print("The probability p of a quantum move has to be: 0.0<p<=1.0.")
        sys.exit()

    # Initialize game object

    print(f"---------------------------------")
    if args.is_quantum or (args.qprob is not None and args.qprob > 0.0):
        game: Game = QuantumGame(qprob=args.qprob, iswap=args.use_iswap)
        print(f"Quantum Fox-in-a-hole game.")
        print(f"Probability of quantum move: {game.qprob}.")
        if args.use_iswap:
            print(f"Using iSWAP for moves.")
        else:
            print(f"Using SWAP for moves.")
    else:
        game = ClassicalGame()
        print("Classical Fox-in-a-hole game.")
    print(f"---------------------------------")

    # Run Fox-in-a-hole
    game.run()
