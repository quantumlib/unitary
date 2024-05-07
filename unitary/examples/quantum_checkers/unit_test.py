import unittest
from quantum_checkers import Checkers

class TestIsAdjacent(unittest.TestCase):        
    def test_is_adjacent_true(self):
        game = Checkers(num_vertical=3, num_horizontal=3, num_vertical_pieces=1)
        for i in range(9):
            is_adjacent, id = game.is_adjacent(4, i)
            self.assertEqual(is_adjacent, True, "Should be True")
            self.assertEqual(id, None, f"{id} should be None")
    
    def test_is_adjacent_false(self):
        game = Checkers(num_vertical=5, num_horizontal=5, num_vertical_pieces=1)
        for i in range(9):
            is_adjacent, id = game.is_adjacent(24, i)
            self.assertEqual(is_adjacent, False, f"{i} is not adjacent to 24")
            self.assertEqual(id, None, f"{id} should be None")

    def test_is_adjacent_jump(self):
        game = Checkers(num_vertical=5, num_horizontal=5, num_vertical_pieces=1)
        is_adjacent, id = game.is_adjacent(0, 18)
        self.assertEqual(is_adjacent, False, f"0 is not adjacent to 18")
        self.assertEqual(id, None, f"{id} should be None")

        is_adjacent, id = game.is_adjacent(0, 12)
        self.assertEqual(is_adjacent, False, f"0 is not adjacent to 12")
        self.assertEqual(id, 6, f"{id} should be 6")

        is_adjacent, id = game.is_adjacent(12, 0)
        self.assertEqual(is_adjacent, False, f"12 is not adjacent to 0")
        self.assertEqual(id, 6, f"{id} should be 6")

        is_adjacent, id = game.is_adjacent(12, 24)
        self.assertEqual(is_adjacent, False, f"12 is not adjacent to 24")
        self.assertEqual(id, 18, f"{id} should be 18")

if __name__ == '__main__':
    unittest.main()
    