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
from unitary.examples.quantum_chinese_chess.enums import SquareState
from unitary.examples.quantum_chinese_chess.board import Board
from string import ascii_lowercase, digits
from typing import List, Dict
from collections import defaultdict
from scipy.stats import chisquare

# Build quantum objects a0 to i9, and add them to a quantum world.
def init_board() -> QuantumWorld:
    board = {}
    for col in ascii_lowercase[:9]:
        for row in digits:
            board[col + row] = QuantumObject(col + row, SquareState.EMPTY)
    return QuantumWorld(list(board.values()))


def location_to_bit(location: str) -> int:
    """Transform location notation (e.g. "a3") into a bitboard bit number."""
    x = ord(location[0]) - ord("a")
    y = int(location[1])
    return y * 9 + x


def locations_to_bitboard(locations: List[str]) -> int:
    """Transform a list of locations into a 90-bit board bitstring."""
    bitboard = 0
    for location in locations:
        bitboard += 1 << location_to_bit(location)
    return bitboard


def nth_bit_of(n: int, bit_board: int) -> bool:
    """Returns the n-th bit of a 90-bit bitstring."""
    return (bit_board >> n) % 2 == 1


def bit_to_location(bit: int) -> str:
    """Transform a bitboard bit number into a location (e.g. "a3")."""
    y = bit // 9
    x = chr(bit % 9 + ord("a"))
    return f"{x}{y}"


def bitboard_to_locations(bitboard: int) -> List[str]:
    """Transform a 90-bit bitstring into a list of locations."""
    locations = []
    for n in range(90):
        if nth_bit_of(n, bitboard):
            locations.append(bit_to_location(n))
    return locations

def sample_board(board: Board, repetitions: int) -> List[int]:
    samples = board.board.peek(count = repetitions, convert_to_enum = False)
    # Convert peek results (in List[List[int]]) into bitstring.
    samples = [int("0b" + "".join([str(i) for i in sample[::-1]]), base=2) for sample in samples]
    return samples


def print_samples(samples):
    """Prints all the samples as lists of locations."""
    sample_dict = {}
    for sample in samples:
        if sample not in sample_dict:
            sample_dict[sample] = 0
        sample_dict[sample] += 1
    for key in sample_dict:
        print(f"{bitboard_to_locations(key)}: {sample_dict[key]}")


def get_board_probability_distribution(board: Board, repetitions: int = 1000) -> Dict[int, float]:
    """Returns the probability distribution for each board found in the sample.

    The values are returned as a dict{bitboard(int): probability(float)}.
    """
    board_probabilities: Dict[int, float] = {}

    samples = board.board.peek(count = repetitions, convert_to_enum = False)
    # Convert peek results (in List[List[int]]) into bitstring.
    samples = [int("0b" + "".join([str(i) for i in sample[::-1]]), base=2) for sample in samples]
    for sample in samples:
        if sample not in board_probabilities:
            board_probabilities[sample] = 0.0
        board_probabilities[sample] += 1.0

    for board in board_probabilities:
        board_probabilities[board] /= repetitions

    return board_probabilities


def assert_samples_in(board: Board, possibilities):
    samples = sample_board(board, 500)
    assert len(samples) == 500
    all_in = all(sample in possibilities for sample in samples)
    print(possibilities)
    print(set(samples))
    assert all_in, print_samples(samples)
    # Make sure each possibility is represented at least once.
    for possibility in possibilities:
        any_in = any(sample == possibility for sample in samples)
        assert any_in, print_samples(samples)


def assert_sample_distribution(board: Board, probability_map, p_significant=1e-6):
    """Performs a chi-squared test that samples follow an expected distribution.

    probability_map is a map from bitboards to expected probability. An
    assertion is raised if one of the samples is not in the map, or if the
    probability that the samples are at least as different from the expected
    ones as the observed sampless is less than p_significant.
    """
    assert abs(sum(probability_map.values()) - 1) < 1e-9
    samples = sample_board(board, 500)
    assert len(samples) == 500
    counts = defaultdict(int)
    for sample in samples:
        assert sample in probability_map, bitboard_to_locations(sample)
        counts[sample] += 1
    observed = []
    expected = []
    for position, probability in probability_map.items():
        observed.append(counts[position])
        expected.append(500 * probability)
    p = chisquare(observed, expected).pvalue
    assert (
        p > p_significant
    ), f"Observed {observed} far from expected {expected} (p = {p})"


def assert_this_or_that(samples, this, that):
    """Asserts all the samples are either equal to this or that,
    and that one of each exists in the samples.
    """
    assert any(sample == this for sample in samples), print_samples(samples)
    assert any(sample == that for sample in samples), print_samples(samples)
    assert all(sample == this or sample == that for sample in samples), print_samples(
        samples
    )


def assert_prob_about(probs, that, expected, atol=0.04):
    """Checks that the probability is within atol of the expected value."""
    assert probs[that] > expected - atol, print_samples([that])
    assert probs[that] < expected + atol, print_samples([that])


def assert_fifty_fifty(probs, that):
    """Checks that the probability is close to 50%."""
    assert_prob_about(probs, that, 0.5), print_samples([that])

