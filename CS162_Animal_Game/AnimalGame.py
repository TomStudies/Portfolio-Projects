# Author: Tom Haney
# GitHub username: TomStudies
# Date: 27May25
# Description: Code which simulates a board game containing various animals. The game is somewhat like chess, with the
#   end goal being to capture the opponent's cuttlefish. There are two sides, one tangerine and one amethyst.
#   See the README for a full description of the game's mechanics.

import math # Used for isclose(), sqrt()

class Piece:
    """
    Contains the private members and getters that each different type of game piece will have.

    Note that in my implementation, the game piece classes act more like dictionaries than anything, simply references
    for the AnimalGame code to determine what action to take.
    """
    def __init__(self, char_version, direction, distance, locomotion):
        # Initiate each private data member to its corresponding value
        self._char_version = char_version
        self._direction = direction
        self._distance = distance
        self._locomotion = locomotion

    # Below getters fairly self-explanatory, no need for docstrings I feel
    def get_char_version(self):
        return self._char_version

    def get_direction(self):
        return self._direction

    def get_distance(self):
        return self._distance

    def get_locomotion(self):
        return self._locomotion

class Chinchilla(Piece):
    # Represents the characteristics of a Chinchilla piece (get methods for these attributes in Piece class)
    def __init__(self):
        super().__init__("H", "diagonal", 1, "sliding")

class Wombat(Piece):
    # Represents the characteristics of a Wombat piece (get methods for these attributes in Piece class)
    def __init__(self):
        super().__init__("W", "orthogonal", 4, "jumping")

class Emu(Piece):
    # Represents the characteristics of an Emu piece (get methods for these attributes in Piece class)
    def __init__(self):
        super().__init__("E", "orthogonal", 3, "sliding")

class Cuttlefish(Piece):
    # Represents the characteristics of a Cuttlefish piece (get methods for these attributes in Piece class)
    def __init__(self):
        super().__init__("C", "diagonal", 2, "jumping")

class AnimalGame:
    """
    Class containing the logic of the Animal Game. Will reference objects of the classes Emu, Cuttlefish, Wombat,
    and Chinchilla for game piece behavior, but otherwise contains all logic within itself.

    Contains logic for the rules as described in the README, as well as extra functionality for printing the game
    board to the console and asking for console inputs to determine game moves (as an alternative to entering game
    moves as lines of code per the README description.)
    """
    def __init__(self):
        """
        Initializes the Animal Game. Sets up the game board, sets the game state to UNFINISHED, sets the turn
        to be Tangerine's (T).

        Interacts with the get_game_mode() method to check the game mode set (could just access the data member
        directly but this seems against the spirit of private data members)
        Interacts with the _display_game_board() private method to display the initial state to the console
        """
        self._game_board = [["H","W","E","C","E","W","H"],
                            [".",".",".",".",".",".","."],
                            [".",".",".",".",".",".","."],
                            [".",".",".",".",".",".","."],
                            [".",".",".",".",".",".","."],
                            [".",".",".",".",".",".","."],
                            ["h","w","e","c","e","w","h"]]
        self._game_state = "UNFINISHED"
        self._turn_tracker = "T"

        self._pieces = [Chinchilla(), Wombat(), Emu(), Cuttlefish()]
        self._display_game_board()

    def get_game_state(self):
        # Return the state of the game - used to determine if someone won
        return self._game_state

    def get_game_board(self):
        # Return the current state of the game board (for use in testing)
        return self._game_board

    def get_turn_tracker(self):
        # Return the current state of the turn tracker (for use in testing)
        return self._turn_tracker

    def set_game_board(self, new_board):
        # Set the game board (for use in testing)
        self._game_board = new_board

    def set_game_state(self, new_state):
        # Set the game state (for use in testing)
        self._game_state = new_state

    def set_turn_tracker(self, new_tracker):
        # Set the turn tracker (for use in testing)
        self._turn_tracker = new_tracker

    def make_move(self, moved_from, moved_to):
        """
        Contains the logic for a player to make a move from one space to another.

        First, _game_state is checked to make sure nobody won yet.

        Next, the strings representing the spaces are converted to a tuple of two indices via the private
        _space_to_indices method (unless either is outside the range of spaces on the board, in which case
        false will be returned.)

        Those two tuples are passed to the _calculate_distance private method to determine the distance between
        the two spaces.

        Whatever piece is located at the moved_from space is cross-checked with the behavior
        of that piece (an instance of the class) and the move is executed accordingly. Then, _display_game_board()
        is called.

        Next, the _check_for_win() method is called to see if a win happened and update the game state accordingly.

        At the end of this method, the turn_tracker is updated if the move was successful and true is returned.
        :param moved_from: A string representing the space a piece should be moved from (e.g. "c4")
        :param moved_to: A string representing the space a piece should be moved to (e.g. "b6")
        :return: False if an attempted move is illegal, True if an attempted move is allowed.
        """

        # Check and see if game was already won (return False if it was)
        if self.get_game_state() == "TANGERINE_WON" or self.get_game_state() == "AMETHYST_WON":
            print("The game is already won!")
            return False

        # Turn the string spaces into tuples of indices
        from_indices = self._space_to_indices(moved_from)
        to_indices = self._space_to_indices(moved_to)

        # If the string spaces were invalid, return False
        if from_indices is False or to_indices is False:
            print("Invalid spaces selected!")
            return False

        # Calculate the x and y deltas, for use in figuring out intended direction of movement
        x_delta = from_indices[1] - to_indices[1]
        y_delta = from_indices[0] - to_indices[0]

        # Make sure the move is actually going somewhere
        if x_delta == 0 and y_delta == 0:
            print("Cannot make a move which goes nowhere!")
            return False

        # Determine the intended direction of movement
        intended_direction = "diagonal"
        if x_delta == 0 or y_delta == 0:
            intended_direction = "orthogonal"

        # Figure out what piece the player intended to move
        piece_to_move = self._game_board[from_indices[0]][from_indices[1]]

        # If the piece is invalid, return False
        if piece_to_move == ".":
            print("Attempted to move from a space containing no piece!")
            return False

        # If the player intended to move a piece from the other team, return False
        if (self._turn_tracker == "T" and piece_to_move in ["h", "w", "e", "c"] or
            self._turn_tracker == "A" and piece_to_move in ["H", "W", "E", "C"]):
            print("Cannot move a piece from the other player!")
            return False

        # Initialize movable_distance, direction, locomotion to nonsensical values
        movable_distance = -1
        direction = "vertical"
        locomotion = "flying"

        # Update movable_distance, direction, locomotion based on what piece is being moved
        for piece in self._pieces:
            if piece_to_move.capitalize() == piece.get_char_version():
                movable_distance = piece.get_distance()
                direction = piece.get_direction()
                locomotion = piece.get_locomotion()
                break
        if movable_distance < 0:
            print("Something seriously wrong if you see this text")
            return False

        # Regardless of whether jumping or sliding piece, check for obstructions at destination
        intended_destination = self._game_board[to_indices[0]][to_indices[1]]
        if (self._turn_tracker == "T" and intended_destination in ["H", "W", "E", "C"] or
            self._turn_tracker == "A" and intended_destination in ["h", "w", "e", "c"]):
            print("One of the player's own pieces is at the intended destination!")
            return False

        # Calculate the distance the player intends to move
        intended_distance = self._calculate_distance(from_indices, to_indices)

        if math.isclose(intended_distance, 1):

            if (intended_direction == "diagonal" and direction == "orthogonal" or
                intended_direction == "orthogonal" and direction == "diagonal" or locomotion == "sliding"):
                # If moving 1 space in the opposite direction of normal motion, or sliding, execute
                self._game_board[from_indices[0]][from_indices[1]] = "."
                self._game_board[to_indices[0]][to_indices[1]] = piece_to_move
                self._update_turn_tracker()
                self._display_game_board()
                self._check_for_win()
                return True

            else:
                # If attempting to move 1 space in the same direction as normal motion, don't execute
                print("Cannot move this piece 1 space in its direction of normal movement!")
                return False

        elif locomotion == "jumping" and math.isclose(intended_distance, movable_distance):

            if (intended_direction == "diagonal" and direction == "diagonal" or
                intended_direction == "orthogonal" and direction == "orthogonal"):
                # If attempting to move the correct number of spaces in the correct direction, execute
                self._game_board[from_indices[0]][from_indices[1]] = "."
                self._game_board[to_indices[0]][to_indices[1]] = piece_to_move
                self._update_turn_tracker()
                self._display_game_board()
                self._check_for_win()
                return True

            else:
                print("This piece cannot move that number of spaces in that direction!")
                return False
        elif locomotion == "sliding" and intended_distance <= movable_distance:

            # If the piece is a sliding piece and can move more than 1 space, check for obstructions along the way
            # Note that this is only possible for Emus, which move orthogonally
            if x_delta == 0 and from_indices[0] < to_indices[0]:
                # Moving downwards
                for y_index in range(from_indices[0] + 1, to_indices[0]):
                    if self._game_board[y_index][to_indices[1]].capitalize() in ["H", "W", "E", "C"]:
                        print("The move is obstructed!")
                        return False
            elif x_delta == 0 and from_indices[0] > to_indices[0]:
                # Moving upwards
                for y_index in range(to_indices[0] + 1, from_indices[0]):
                    if self._game_board[y_index][to_indices[1]].capitalize() in ["H", "W", "E", "C"]:
                        print("The move is obstructed!")
                        return False
            elif y_delta == 0 and from_indices[1] < to_indices[1]:
                # Moving right
                for x_index in range(from_indices[1] + 1, to_indices[1]):
                    if self._game_board[to_indices[0]][x_index].capitalize() in ["H", "W", "E", "C"]:
                        print("The move is obstructed!")
                        return False
            elif y_delta == 0 and from_indices[1] > to_indices[1]:
                # Moving left
                for x_index in range(to_indices[1] + 1, from_indices[1]):
                    if self._game_board[to_indices[0]][x_index].capitalize() in ["H", "W", "E", "C"]:
                        print("The move is obstructed!")
                        return False

            self._game_board[from_indices[0]][from_indices[1]] = "."
            self._game_board[to_indices[0]][to_indices[1]] = piece_to_move
            self._update_turn_tracker()
            self._display_game_board()
            self._check_for_win()
            return True

        else:
            print("Intended move is out of range!")
            return False

    def _space_to_indices(self, space_string):
        """
        Creates a tuple based on a string representing a space on the game board. The first character is converted
        to lower-case, then checked against a dictionary with their associated indexes. The second character simply
        is converted to an integer and has 1 subtracted from it.
        :param space_string: A string representing a space on the game board (e.g. "a3")
        :return: A tuple representing the indices of the game board that space represents. e.g. (0, 2), or False if
        the string is out of the range of the board.
        """
        if isinstance(space_string, str) and len(space_string) == 2:
            row_index = -1
            column_index = -1
            letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
            if space_string[0].capitalize() in letter_to_index.keys():
                column_index = letter_to_index[space_string[0].capitalize()]
            else:
                return False
            if int(space_string[1]) in range(1, 8):
                row_index = int(space_string[1]) - 1
            else:
                return False
            index_tuple = (row_index, column_index)
            return index_tuple
        else:
            return False

    def _calculate_distance(self, from_tuple, to_tuple):
        """
        Calculates the distance intended to be moved on the board. This is the larger value when the horizontal delta
            and the vertical delta are compared (can only move orthogonally or diagonally)
        :param from_tuple: A tuple with two values representing the "from" space
        :param to_tuple: A tuple with two values representing the "to" space
        :return: Distance value
        """
        y_delta = abs(from_tuple[0] - to_tuple[0])
        x_delta = abs(from_tuple[1] - to_tuple[1])
        if x_delta >= y_delta:
            return x_delta
        else:
            return y_delta

    def _check_for_win(self):
        """
        Starts with two flags set to false. Iterates through the game board and searches for each cuttlefish, setting
        the flags to true as each cuttlefish is found. If at the end one is not found, the _game_state member is
        updated accordingly.
        """
        tangerine_fish = False
        amethyst_fish = False
        for row in self._game_board:
            for character in row:
                if character == "C":
                    tangerine_fish = True
                elif character == "c":
                    amethyst_fish = True
        if tangerine_fish is False:
            self._game_state = "AMETHYST_WON"
        if amethyst_fish is False:
            self._game_state = "TANGERINE_WON"

    def _display_game_board(self):
        """
        Prints the game board to the console, with whitespace underneath. Can be used to track game state.
        :return: None
        """
        print("    A B C D E F G")
        print()
        row_counter = 1
        for row in self._game_board:
            print(row_counter, end="   ")
            row_counter += 1
            for character in row:
                print(character, end=" ")
            print()
        print()

    def _update_turn_tracker(self):
        """
        Updates the turn tracker (if "T" switches it to "A" and vice versa)
        :return: none
        """
        if self._turn_tracker == "T":
            self._turn_tracker = "A"
        else:
            self._turn_tracker = "T"

"""
Testing Zone
def main():
    game = AnimalGame()
    move_result = game.make_move("a1", "a2")

    move_result = game.make_move("b7", "b3")

    move_result = game.make_move("a2", "b3")

    move_result = game.make_move("c7", "b6")

    move_result = game.make_move("b3", "a4")

    move_result = game.make_move("b6", "d6")

    move_result = game.make_move("e1", "e4")

    move_result = game.make_move("e7", "e4")

    move_result = game.make_move("f1", "f5")

    move_result = game.make_move("f1", "f5")

    move_result = game.make_move("e4", "f5")

    move_result = game.make_move("a4", "b5")

    move_result = game.make_move("d7", "b5")

    move_result = game.make_move("d1", "d2")

    move_result = game.make_move("f7", "b7")

    move_result = game.make_move("b1", "b5")

    move_result = game.make_move("a7", "a6")
    state = game.get_game_state()
    print(state)

if __name__ == "__main__":
    main()
"""