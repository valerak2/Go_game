import datetime
import unittest
import numpy as np
import game_module.game
from game_module import logic_operations


class MyTestCase(unittest.TestCase):
    def test_valid_move(self):
        board = np.zeros((2, 2))
        board[0, 0] = 1
        self.assertFalse(logic_operations.is_valid_move(0, 0, board))  # add assertion here
        self.assertTrue(logic_operations.is_valid_move(1, 1, board))  # add assertion here

    def test_liberties(self):
        board = np.zeros((2, 2))

        board[1, 1] = 2
        board[0, 1] = 1
        board[1, 0] = 1
        board[0, 0] = 0

        other_color = "black"
        for group in list(logic_operations.get_stone_groups(board, other_color)):
            self.assertFalse(logic_operations.has_no_liberties(board, group))

        other_color = "white"
        for group in list(logic_operations.get_stone_groups(board, other_color)):
            self.assertTrue(logic_operations.has_no_liberties(board, group))

    def test_handicap(self):
        g = game_module.game.Game(size=4, handicap_point=3, clock=None, game_mode=None)
        g.black_turn = True
        try:
            for i in range(3):
                g.handicap_in_start_game()
                self.assertTrue(g.black_turn)
        except AttributeError:
            pass
        self.assertFalse(g.black_turn)


if __name__ == '__main__':
    unittest.main()
