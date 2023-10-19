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
from unitary.alpha import QuantumObject, QuantumWorld
from unitary.examples.quantum_chinese_chess.enums import SquareState, Type, Color
from unitary.examples.quantum_chinese_chess.board import Board
from unitary.examples.quantum_chinese_chess.piece import Piece
from unitary import alpha
from typing import List, Dict
from collections import defaultdict
from scipy.stats import chisquare


_EMPTY_FEN = "9/9/9/9/9/9/9/9/9/9 w---1"


def set_board(positions: List[str]) -> Board:
    """Returns a board with the specified positions filled with
    RED ROOKs.
    """
    board = Board.from_fen(_EMPTY_FEN)
    for position in positions:
        board.board[position].reset(
            Piece(position, SquareState.OCCUPIED, Type.ROOK, Color.RED)
        )
        alpha.Flip()(board.board[position])
    return board


def location_to_bit(location: str) -> int:
    """Transform location notation (e.g. "a3") into a bitboard bit number.
    The return value ranges from 0 to 89.
    """
    x = ord(location[0]) - ord("a")
    y = int(location[1])
    return y * 9 + x


def locations_to_bitboard(locations: List[str]) -> int:
    """Transform a list of locations into a 90-bit board bitstring.
    Each nonzero bit of the bitstring indicates that the corresponding
    piece is occupied.
    """
    bitboard = 0
    for location in locations:
        bitboard += 1 << location_to_bit(location)
    return bitboard


def nth_bit_of(n: int, bit_board: int) -> bool:
    """Returns the `n`-th (zero-based) bit of a 90-bit bitstring `bit_board`."""
    return (bit_board >> n) % 2 == 1


def bit_to_location(bit: int) -> str:
    """Transform a bitboard bit number into a location (e.g. "a3")."""
    y = bit // 9
    x = chr(bit % 9 + ord("a"))
    return f"{x}{y}"


def bitboard_to_locations(bitboard: int) -> List[str]:
    """Transform a 90-bit bitstring `bitboard` into a list of locations."""
    locations = []
    for n in range(90):
        if nth_bit_of(n, bitboard):
            locations.append(bit_to_location(n))
    return locations


def sample_board(board: Board, repetitions: int) -> List[int]:
    """Sample the given `board` by the given `repetitions`.
    Returns a list of 90-bit bitstring, each corresponding to one sample.
    """
    samples = board.board.peek(count=repetitions, convert_to_enum=False)
    # Convert peek results (in List[List[int]]) into List[int].
    samples = [
        int("0b" + "".join([str(i) for i in sample[::-1]]), base=2)
        for sample in samples
    ]
    return samples


def print_samples(samples: List[int]) -> None:
    """Aggregate all the samples and print the dictionary of {locations: count}."""
    sample_dict = {}
    for sample in samples:
        if sample not in sample_dict:
            sample_dict[sample] = 0
        sample_dict[sample] += 1
    print("Actual samples:")
    for key in sample_dict:
        print(f"{bitboard_to_locations(key)}: {sample_dict[key]}")


def get_board_probability_distribution(
    board: Board, repetitions: int = 1000
) -> Dict[int, float]:
    """Returns the probability distribution for each board found in the sample.
    The values are returned as a dict{bitboard(int): probability(float)}.
    """
    board_probabilities: Dict[int, float] = {}

    samples = sample_board(board, repetitions)
    for sample in samples:
        if sample not in board_probabilities:
            board_probabilities[sample] = 0.0
        board_probabilities[sample] += 1.0

    for board in board_probabilities:
        board_probabilities[board] /= repetitions

    return board_probabilities


def assert_samples_in(board: Board, probabilities: Dict[int, float]) -> None:
    """Samples the given `board` and asserts that all samples are within
    the given `probabilities` (i.e. a map from bitstring into its possibility),
    and that each possibility is represented at least once in the samples.
    """
    samples = sample_board(board, 500)
    assert len(samples) == 500
    all_in = all(sample in probabilities for sample in samples)
    assert all_in, print_samples(samples)
    # Make sure each possibility is represented at least once.
    for possibility in probabilities:
        any_in = any(sample == possibility for sample in samples)
        assert any_in, print_samples(samples)


def assert_sample_distribution(
    board: Board, probabilities: Dict[int, float], p_significant: float = 1e-6
) -> None:
    """Performs a chi-squared test that samples follow an expected distribution.
    `probabilities` is a map from bitboards to expected probability. An
    AssertionError is raised if any of the samples is not in the map, or if the
    expected versus observed samples fails the chi-squared test.
    """
    n_samples = 500
    assert abs(sum(probabilities.values()) - 1) < 1e-9
    samples = sample_board(board, n_samples)
    counts = defaultdict(int)
    for sample in samples:
        assert sample in probabilities, print_samples(samples)
        counts[sample] += 1
    observed = []
    expected = []
    for position, probability in probabilities.items():
        observed.append(counts[position])
        expected.append(n_samples * probability)
    p = chisquare(observed, expected).pvalue
    assert (
        p > p_significant
    ), f"Observed {observed} is far from expected {expected} (p = {p})"


def assert_this_or_that(samples: List[int], this: int, that: int) -> None:
    """Asserts all the samples are either equal to `this` or `that`,
    and that at least one of them exists in the samples.
    """
    assert any(sample == this for sample in samples), print_samples(samples)
    assert any(sample == that for sample in samples), print_samples(samples)
    assert all(sample == this or sample == that for sample in samples), print_samples(
        samples
    )


def assert_prob_about(
    probabilities: Dict[int, float], that: int, expected: float, atol: float = 0.05
) -> None:
    """Checks that the probability of `that` is within `atol` of the value of `expected`."""
    assert that in probabilities, print_samples(list(probabilities.keys()))
    assert probabilities[that] > expected - atol, print_samples(
        list(probabilities.keys())
    )
    assert probabilities[that] < expected + atol, print_samples(
        list(probabilities.keys())
    )


def assert_fifty_fifty(probabilities, that):
    """Checks that the probability of `that` is close to 50%."""
    assert_prob_about(probabilities, that, 0.5), print_samples(
        list(probabilities.keys())
    )
