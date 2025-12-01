# Author: Tom Haney
# GitHub username: TomStudies
# Date: 02Jun25
# Description: Code for testing the AnimalGame.py classes and methods. Attempted to be quite thorough, covering
# different kinds of moves which can and cannot be made.

import unittest
import AnimalGame

class UnitTests(unittest.TestCase):
    def setUp(self):
        # Makes an AnimalGame called game for use in testing
        self.game = AnimalGame.AnimalGame()

    def test_ag_init(self):
        # Tests to see if the init method works for AnimalGame
        default_board = [["H","W","E","C","E","W","H"],
                        [".",".",".",".",".",".","."],
                        [".",".",".",".",".",".","."],
                        [".",".",".",".",".",".","."],
                        [".",".",".",".",".",".","."],
                        [".",".",".",".",".",".","."],
                        ["h","w","e","c","e","w","h"]]
        default_state = "UNFINISHED"
        default_turn = "T"

        self.assertEqual(self.game.get_game_board(), default_board)
        self.assertEqual(self.game.get_game_state(), default_state)
        self.assertEqual(self.game.get_turn_tracker(), default_turn)

    def test_chinchilla_init(self):
        # Tests to see if the init method works for a Chinchilla
        test_chinchilla = AnimalGame.Chinchilla()
        self.assertEqual(test_chinchilla.get_char_version(), "H")
        self.assertEqual(test_chinchilla.get_direction(), "diagonal")
        self.assertEqual(test_chinchilla.get_distance(), 1)
        self.assertEqual(test_chinchilla.get_locomotion(), "sliding")

    def test_wombat_init(self):
        # Tests to see if the init method works for a Wombat
        test_wombat = AnimalGame.Wombat()
        self.assertEqual(test_wombat.get_char_version(), "W")
        self.assertEqual(test_wombat.get_direction(), "orthogonal")
        self.assertEqual(test_wombat.get_distance(), 4)
        self.assertEqual(test_wombat.get_locomotion(), "jumping")

    def test_emu_init(self):
        # Tests to see if the init method works for an Emu
        test_emu = AnimalGame.Emu()
        self.assertEqual(test_emu.get_char_version(), "E")
        self.assertEqual(test_emu.get_direction(), "orthogonal")
        self.assertEqual(test_emu.get_distance(), 3)
        self.assertEqual(test_emu.get_locomotion(), "sliding")

    def test_cuttlefish_init(self):
        # Tests to see if the init method works for a Cuttlefish
        test_cuttlefish = AnimalGame.Cuttlefish()
        self.assertEqual(test_cuttlefish.get_char_version(), "C")
        self.assertEqual(test_cuttlefish.get_direction(), "diagonal")
        self.assertEqual(test_cuttlefish.get_distance(), 2)
        self.assertEqual(test_cuttlefish.get_locomotion(), "jumping")

    def test_space_to_indices_normal(self):
        # Tests whether the space to indices method works for correctly entered spaces
        self.assertEqual(self.game._space_to_indices("a1"), (0,0))
        self.assertEqual(self.game._space_to_indices("G7"), (6,6))
        self.assertEqual(self.game._space_to_indices("c4"), (3,2))
        self.assertEqual(self.game._space_to_indices("B6"), (5,1))

    def test_space_to_indices_failures(self):
        # Tests whether the space to indices method correctly returns false for incorrect inputs
        self.assertFalse(self.game._space_to_indices("c17"))
        self.assertFalse(self.game._space_to_indices(12))
        self.assertFalse(self.game._space_to_indices("C"))
        self.assertFalse(self.game._space_to_indices(""))
        self.assertFalse(self.game._space_to_indices("The quick brown fox jumped over the lazy dog"))


    def test_check_for_win(self):
        # Tests for all 3 possible check for win results: no win yet, amethyst won, tangerine won
        self.game._check_for_win()
        self.assertEqual(self.game.get_game_state(), "UNFINISHED")

        self.game.set_game_board(   [["H","W","E",".","E","W","H"],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     ["h","w","e","c","e","w","h"]])
        self.game._check_for_win()
        self.assertEqual(self.game.get_game_state(), "AMETHYST_WON")

        self.game.set_game_board(   [["H","W","E","C","E","W","H"],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     [".",".",".",".",".",".","."],
                                     ["h","w","e",".","e","w","h"]])
        self.game._check_for_win()
        self.assertEqual(self.game.get_game_state(), "TANGERINE_WON")

    def test_update_turn_tracker(self):
        # Tests whether the turn tracker correctly starts with T and updates to the right characters
        self.assertEqual(self.game.get_turn_tracker(), "T")
        self.game.make_move("a1", "a2")
        self.assertEqual(self.game.get_turn_tracker(), "A")
        self.game.make_move("a7", "a6")
        self.assertEqual(self.game.get_turn_tracker(), "T")

    def test_make_move_game_already_won(self):
        # Tests whether the make_move method correctly returns False if the game was already won
        self.game.set_game_state("TANGERINE_WON")
        self.assertFalse(self.game.make_move("a1", "a2"))
        self.game.set_game_state("AMETHYST_WON")
        self.assertFalse(self.game.make_move("a1", "a2"))

    def test_make_move_going_nowhere(self):
        # Tests whether a move from and to the same space correctly returns False
        self.assertFalse(self.game.make_move("a1", "a1"))

    def test_make_move_from_out_of_bounds(self):
        # Tests whether a move from a space which is out of bounds correctly returns False
        self.assertFalse(self.game.make_move("a0", "a2"))
        self.assertFalse(self.game.make_move("H1", "G2"))

    def test_make_move_to_out_of_bounds(self):
        # Tests whether a move to a space which is out of bounds correctly returns False
        self.assertFalse(self.game.make_move("a1", "a0"))
        self.assertFalse(self.game.make_move("G1", "H1"))

    def test_make_move_from_empty_space(self):
        # Tests whether a move initiated from an empty space correctly returns False
        self.assertFalse(self.game.make_move("b4", "b6"))
        self.assertFalse(self.game.make_move("f2", "f3"))

    def test_make_move_tangerine_moving_amethyst(self):
        # Tests whether a tangerine attempt to move an amethyst piece correctly returns False
        self.assertFalse(self.game.make_move("a7", "a6"))

    def test_make_move_amethyst_moving_tangerine(self):
        # Tests whether an amethyst attempt to move a tangerine piece correctly returns False
        self.game.set_turn_tracker("A")
        self.assertFalse(self.game.make_move("a1", "a2"))

    def test_make_move_friendly_piece_at_destination(self):
        # Tests whether an attempt to move to a space with a friendly piece already there returns False
        self.game.set_game_board([[".", "W", "E", "C", "E", "W", "H"],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", "H", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  ["h", "w", "e", "c", "e", "w", "h"]])
        self.assertFalse(self.game.make_move("b1", "b5"))

        self.game.set_game_board([["H", "W", "E", "C", "E", "W", "H"],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "c"],
                                  ["h", "w", "e", ".", "e", "w", "h"]])
        self.assertFalse(self.game.make_move("g7", "g6"))

    def test_make_move_piece_along_sliding_route(self):
        # Tests whether an attempt to slide a piece through an obstruction correctly returns false
        self.game.set_game_board([[".", "W", "E", "C", "E", "W", "H"],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", "H", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  ["h", "w", "e", "c", "e", "w", "h"]])
        self.assertFalse(self.game.make_move("C1", "C4"))

        self.game.set_game_board([["H", "W", "E", "C", "E", "W", "H"],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", ".", ".", "."],
                                  [".", ".", ".", ".", "h", ".", "."],
                                  ["h", "w", "e", "c", "e", "w", "."]])
        self.assertFalse(self.game.make_move("E7", "E4"))

    def test_make_move_out_of_range(self):
        # Tests whether attempts to move a piece beyond its range correctly return False
        self.assertFalse(self.game.make_move("a1", "a3"))
        self.game.set_turn_tracker("A")
        self.assertFalse(self.game.make_move("D7", "D5"))

    def test_make_move_1_space_opposite(self):
        # Tests whether attempting to move a piece 1 space in the opposite direction of its normal motion works right
        self.assertTrue(self.game.make_move("a1", "a2"))
        self.assertTrue(self.game.make_move("b7", "a6"))
        self.assertTrue(self.game.make_move("c1", "d2"))
        self.assertTrue(self.game.make_move("d7", "d6"))

    def test_make_move_chinchilla(self):
        # Tests whether chinchillas can be moved correctly
        self.assertTrue(self.game.make_move("a1", "b2"))
        self.assertTrue(self.game.make_move("g7", "f6"))

    def test_make_move_wombat(self):
        # Tests whether wombats can be moved correctly
        self.assertTrue(self.game.make_move("b1", "B5"))
        self.assertTrue(self.game.make_move("f7", "f3"))

    def test_make_move_emu(self):
        # Tests whether emus can be moved correctly
        self.assertTrue(self.game.make_move("c1", "c4"))
        self.assertTrue(self.game.make_move("e7", "e5"))
        self.assertTrue(self.game.make_move("e1", "e2"))

    def test_make_move_cuttlefish(self):
        # Tests whether cuttlefish can be moved correctly
        self.assertTrue(self.game.make_move("D1", "B3"))
        self.assertTrue(self.game.make_move("D7", "F5"))

    def test_calculate_distance(self):
        # Tests whether the calculate distance method works correctly
        self.assertAlmostEqual(self.game._calculate_distance((0, 0), (2, 0)), 2)
        self.assertAlmostEqual(self.game._calculate_distance((6, 3), (4, 1)), 2)
        self.assertAlmostEqual(self.game._calculate_distance((0, 2), (4, 6)), 4)

if __name__ == "__main__":
    unittest.main()