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

"""Tests for ClassicalGame and QuantumGame classes."""

import pytest

import unitary.examples.fox_in_a_hole.fox_in_a_hole as fh

def test_classical_game():
    """Simple tests for ClassicalGame."""
    test_game = fh.ClassicalGame(seed=42)
    assert test_game.hole_nr == 5
    assert len(test_game.history) == 0
    assert test_game.state == [1.0,0.0,0.0,0.0,0.0]
    for i in range(5):
        guess = test_game.check_guess(i)
        assert guess == (i==0)
        hist_len=len(test_game.history)
        test_game.history_append_guess(i)
        assert len(test_game.history) == hist_len+1
    hist_len=len(test_game.history)
    test_game.history_append_move("abc")
    assert len(test_game.history) == hist_len+1
    assert test_game.history[-1] == "abc"
    hist_len=len(test_game.history)
    test_game.history_append_state()
    assert len(test_game.history) == hist_len+1

    test_game = fh.ClassicalGame(seed=42)
    test_game.take_random_move()
    assert test_game.state == [0.0,1.0,0.0,0.0,0.0]
    test_game.take_random_move()
    assert test_game.state == [0.0,0.0,1.0,0.0,0.0]
    test_game.take_random_move()
    assert test_game.state == [0.0,1.0,0.0,0.0,0.0]
    for i in range(5):
        guess = test_game.check_guess(i)
        assert guess == (i==1)

def test_quantum_game():
    """Simple tests for QuantumGame."""
    test_game = fh.QuantumGame(seed=42)
    assert test_game.hole_nr == 5
    assert len(test_game.history) == 0
    probs = test_game.state[0].get_binary_probabilities(objects=test_game.state[1])
    assert probs == [1.0,0.0,0.0,0.0,0.0]
    for i in range(5):
        guess = test_game.check_guess(i)
        assert guess == (i==0)
        hist_len=len(test_game.history)
        test_game.history_append_guess(i)
        assert len(test_game.history) == hist_len+1
    hist_len=len(test_game.history)
    test_game.history_append_move("abc")
    assert len(test_game.history) == hist_len+1
    assert test_game.history[-1] == "abc"
    hist_len=len(test_game.history)
    test_game.history_append_state()
    assert len(test_game.history) == hist_len+1

    test_game = fh.QuantumGame(seed=42)
    probs = test_game.state[0].get_binary_probabilities(objects=test_game.state[1])
    assert probs == [1.0,0.0,0.0,0.0,0.0]
    test_game.take_random_move()
    probs = test_game.state[0].get_binary_probabilities(objects=test_game.state[1])
    assert probs == [0.0,1.0,0.0,0.0,0.0]
    test_game.take_random_move()
    probs = test_game.state[0].get_binary_probabilities(objects=test_game.state[1])
    assert probs[0]>0.0
    assert probs[1]==0.0
    assert probs[2]>0.0
    assert probs[3]==0.0
    assert probs[4]==0.0
    guess = test_game.check_guess(0)
    probs = test_game.state[0].get_binary_probabilities(objects=test_game.state[1])
    assert probs[1]==0.0
    assert probs[3]==0.0
    assert probs[4]==0.0
    assert (guess and probs[0]==1.0 and probs[2]==0.0) or \
           (not guess and probs[0]==0.0 and probs[2]==1.0)
