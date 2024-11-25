# Author: Alon Shkedy
# Date: 3/10/2021
# Description: A Janggi game that has pieces that represent a general, guard horse, elephant, chariot,
#              cannon, and soldiers that move in different ways and can capture other pieces on a 10x9 board


class Piece:
    """
    Represents a general, guard, horse, elephant, chariot, cannon, and soldiers that move in different ways and can
    capture other pieces on the 10x9 board
    """

    def __init__(self, color, row, column):
        """Initializes the class Piece"""
        self._color = color
        self._row = row
        self._column = column
        self._type = "Piece"

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """The base move function"""
        return True

    def get_color(self):
        """Gets the color of the piece"""
        return self._color

    def get_row(self):
        """Gets the row where the piece is located"""
        return self._row

    def get_column(self):
        """Gets the column where the piece is located"""
        return self._column

    def set_row(self, row):
        """Sets the row where the piece is located"""
        self._row = row

    def set_column(self, column):
        """Sets the column where the piece is located"""
        self._column = column

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        return False

    def get_type(self):
        """Gets the type of piece"""
        return self._type


class General(Piece):
    """
    Represents a general that can move one step along the marked lines of the palace and cannot leave the palace
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class General"""
        Piece.__init__(self, color, row, column)
        self._type = "General"

    def general_in_check(self, board, row, column):
        """Determines if the general is moving itself into check"""
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the General"""
        board = game.get_board()
        if board[move_from_row][move_from_column] is None:
            return False
        if abs(move_to_row - move_from_row) > 1:
            return False
        if abs(move_to_column - move_from_column) > 1:
            return False
        if self._color == "B":
            if move_to_row < 7:
                return False
            if move_to_column < 3 or move_to_column > 5:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 7:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                if move_from_row == 8:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 9:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 9:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 7:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 7:
                        valid_move = True
                if move_from_row == 9:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                if not valid_move:
                    return False
        if self._color == "R":
            if move_to_row > 2:
                return False
            if move_to_column < 3 or move_to_column > 5:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 2:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                if move_from_row == 1:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 0:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 0:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 2:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 2:
                        valid_move = True
                if move_from_row == 0:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                if not valid_move:
                    return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        #       check if general is going to be checked
        if self._color == "R":
            game.set_red_check(False)
            blue_pieces = game.get_blue_pieces()
            for row in range(10):
                for column in range(9):
                    piece = blue_pieces[row][column]
                    if piece is not None:
                        is_check = piece.general_in_check(board, self._row, self._column)
                        if is_check:
                            game.set_game_state("B")
        else:
            game.set_blue_check(False)
            red_pieces = game.get_red_pieces()
            for row in range(10):
                for column in range(9):
                    piece = red_pieces[row][column]
                    if piece is not None:
                        is_check = piece.general_in_check(board, self._row, self._column)
                        if is_check:
                            game.set_game_state("R")
        return True


class Guard(Piece):
    """
    Represents a guard that is on the left and right of the general and can only move along the marked lines,
    of the palace and the guards cannot leave the palace
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Guard"""
        Piece.__init__(self, color, row, column)
        self._type = "Guard"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Guard"""
        board = game.get_board()
        if board[move_from_row][move_from_column] is None:
            return False
        if abs(move_to_row - move_from_row) > 1:
            return False
        if abs(move_to_column - move_from_column) > 1:
            return False
        if self._color == "B":
            if move_to_row < 7:
                return False
            if move_to_column < 3 or move_to_column > 5:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 7:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                if move_from_row == 8:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 9:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 9:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 7:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 7:
                        valid_move = True
                if move_from_row == 9:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                if not valid_move:
                    return False
        if self._color == "R":
            if move_to_row > 2:
                return False
            if move_to_column < 3 or move_to_column > 5:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 2:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                if move_from_row == 1:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 0:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 0:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 2:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 2:
                        valid_move = True
                if move_from_row == 0:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                if not valid_move:
                    return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        return True


class Horse(Piece):
    """
    Represents a horse that moves one step orthogonally and then one step diagonally outward, a horse can be transposed
    with an adjacent elephant during the setup of the board
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Horse"""
        Piece.__init__(self, color, row, column)
        self._type = "Horse"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        if abs(row - self._row) == 2 and abs(column - self._column) == 1:
            return True
        if abs(column - self._column) == 2 and abs(row - self._row) == 1:
            return True
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Horse"""
        board = game.get_board()
        if abs(move_to_row - move_from_row) > 2 or abs(move_to_column - move_from_column) > 2:
            return False
        if abs(move_to_row - move_from_row) == 2 and abs(move_to_column - move_from_column) > 1:
            return False
        if abs(move_to_column - move_from_column) == 2 and abs(move_to_row - move_from_row) > 1:
            return False
        if abs(move_to_row - move_from_row) == 2:
            if move_from_row > move_to_row:
                piece = game.get_piece(move_from_row -1, move_from_column)
                if piece is not None:
                    return False
            else:
                piece = game.get_piece(move_from_row + 1, move_from_column)
                if piece is not None:
                    return False
        if abs(move_to_column - move_from_column) == 2:
            if move_from_column > move_to_column:
                piece = game.get_piece(move_from_row, move_from_column -1)
                if piece is not None:
                    return False
            else:
                piece = game.get_piece(move_from_row, move_from_column + 1)
                if piece is not None:
                    return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        #       check if general is going to be checked
        if self._color == "R":
            general = game.get_general("B")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_blue_check(is_check)
        else:
            general = game.get_general("R")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_red_check(is_check)
        return True


class Elephant(Piece):
    """
    Represents an elephant that is on the left and right of the guards and they move one step orthogonally and then
    two steps diagonally, an elephant can be transposed with an adjacent horse during the setup of the board
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Elephant"""
        Piece.__init__(self, color, row, column)
        self._type = "Elephant"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        if abs(row - self._row) == 3 and abs(column - self._column) == 2:
            return True
        if abs(column - self._column) == 3 and abs(row - self._row) == 2:
            return True
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Elephant"""
        board = game.get_board()
        valid_move = False
        if abs(move_to_row - move_from_row) == 3 and abs(move_to_column - move_from_column) == 2:
            valid_move = True
        if abs(move_to_row - move_from_row) == 2 and abs(move_to_column - move_from_column) == 3:
            valid_move = True
        if not valid_move:
            return False
        if abs(move_to_row - move_from_row) == 3:
            if move_from_row > move_to_row:
                piece = game.get_piece(move_from_row - 1, move_from_column)
                if piece is not None:
                    return False
                if move_from_column > move_to_column:
                    piece = game.get_piece(move_from_row - 2, move_from_column-1)
                    if piece is not None:
                        return False
                else:
                    piece = game.get_piece(move_from_row - 2, move_from_column + 1)
                    if piece is not None:
                        return False
            else:
                piece = game.get_piece(move_from_row + 1, move_from_column)
                if piece is not None:
                    return False
                if move_from_column > move_to_column:
                    piece = game.get_piece(move_from_row + 2, move_from_column-1)
                    if piece is not None:
                        return False
                else:
                    piece = game.get_piece(move_from_row + 2, move_from_column + 1)
                    if piece is not None:
                        return False
        if abs(move_to_column - move_from_column) == 3:
            if move_from_column > move_to_column:
                piece = game.get_piece(move_from_row, move_from_column - 1)
                if piece is not None:
                    return False
                if move_from_row > move_to_row:
                    piece = game.get_piece(move_from_row - 1, move_from_column - 2)
                    if piece is not None:
                        return False
                else:
                    piece = game.get_piece(move_from_row + 1, move_from_column - 2)
                    if piece is not None:
                        return False
            else:
                piece = game.get_piece(move_from_row, move_from_column + 1)
                if piece is not None:
                    return False
                if move_from_row > move_to_row:
                    piece = game.get_piece(move_from_row - 1, move_from_column + 2)
                    if piece is not None:
                        return False
                else:
                    piece = game.get_piece(move_from_row + 1, move_from_column + 2)
                    if piece is not None:
                        return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        #       check if general is going to be checked
        if self._color == "R":
            general = game.get_general("B")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_blue_check(is_check)
        else:
            general = game.get_general("R")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_red_check(is_check)
        return True


class Chariot(Piece):
    """
    Represents a chariot that is exactly like a rook in chess and moves either horizontally or vertically,
    can also move in a straight line along the diagonals in either palace, the chariots begin the game in
    the corners of the board
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Chariot"""
        Piece.__init__(self, color, row, column)
        self._type = "Chariot"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        if abs(row - self._row) >= 1 and abs(column - self._column) >= 1:
            if self._row == 7:
                if self._column == 3 and column == 4 and row == 8:
                    return True
                if self._column == 3 and column == 5 and row == 9:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
                if self._column == 5 and column == 4 and row == 8:
                    return True
                if self._column == 5 and column == 3 and row == 9:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
            if self._row == 8:
                if self._column == 4 and column == 3 and row == 9:
                    return True
                if self._column == 4 and column == 5 and row == 9:
                    return True
            if self._row == 9:
                if self._column == 3 and column == 4 and row == 8:
                    return True
                if self._column == 3 and column == 5 and row == 7:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
                if self._column == 5 and column == 4 and row == 8:
                    return True
                if self._column == 5 and column == 3 and row == 7:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
            if self._row == 2:
                if self._column == 3 and column == 4 and row == 1:
                    return True
                if self._column == 3 and column == 5 and row == 0:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
                if self._column == 5 and column == 4 and row == 1:
                    return True
                if self._column == 5 and column == 3 and row == 0:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
            if self._row == 1:
                if self._column == 4 and column == 3 and row == 0:
                    return True
                if self._column == 4 and column == 5 and row == 0:
                    return True
            if self._row == 0:
                if self._column == 3 and column == 4 and row == 1:
                    return True
                if self._column == 3 and column == 5 and row == 2:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
                if self._column == 5 and column == 4 and row == 1:
                    return True
                if self._column == 5 and column == 3 and row == 2:
                    piece = board[8, 4]
                    if piece is None:
                        return True
                    else:
                        return False
        else:
            if row < self._row and column == self._column:
                for row in range(abs(row - self._row)-1):
                    if board[self._row-1 - row][column] is not None:
                        return False
                return True
            if row > self._row and column == self._column:
                for row in range(abs(row - self._row)-1):
                    if board[self._row+1 + row][column] is not None:
                        return False
                return True
            if column < self._column and row == self._row:
                for column in range(abs(column - self._column)-1):
                    if board[row][self._column-1 - column] is not None:
                        return False
                return True
            if column > self._column and row == self._row:
                for column in range(abs(column - self._column)-1):
                    if board[row][self._column+1 + column] is not None:
                        return False
                return True
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Chariot"""
        board = game.get_board()
        if board[move_from_row][move_from_column] is None:
            return False
        if abs(move_to_row - move_from_row) >= 1 and abs(move_to_column - move_from_column) >= 1:
            valid_move = False
            if move_from_row == 7:
                if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                    valid_move = True
                if move_from_column == 3 and move_to_column == 5 and move_to_row == 9:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
                if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                    valid_move = True
                if move_from_column == 5 and move_to_column == 3 and move_to_row == 9:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
            if move_from_row == 8:
                if move_from_column == 4 and move_to_column == 3 and move_to_row == 9:
                    valid_move = True
                if move_from_column == 4 and move_to_column == 5 and move_to_row == 9:
                    valid_move = True
            if move_from_row == 9:
                if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                    valid_move = True
                if move_from_column == 3 and move_to_column == 5 and move_to_row == 7:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
                if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                    valid_move = True
                if move_from_column == 5 and move_to_column == 3 and move_to_row == 7:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
            if move_from_row == 2:
                if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                    valid_move = True
                if move_from_column == 3 and move_to_column == 5 and move_to_row == 0:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
                if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                    valid_move = True
                if move_from_column == 5 and move_to_column == 3 and move_to_row == 0:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
            if move_from_row == 1:
                if move_from_column == 4 and move_to_column == 3 and move_to_row == 0:
                    valid_move = True
                if move_from_column == 4 and move_to_column == 5 and move_to_row == 0:
                    valid_move = True
            if move_from_row == 0:
                if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                    valid_move = True
                if move_from_column == 3 and move_to_column == 5 and move_to_row == 2:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
                if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                    valid_move = True
                if move_from_column == 5 and move_to_column == 3 and move_to_row == 2:
                    piece = game.get_piece(8, 4)
                    if piece is None:
                        valid_move = True
                    else:
                        valid_move = False
            if not valid_move:
                return False
        else:
            if move_to_row < move_from_row and move_to_column == move_from_column:
                for row in range(abs(move_to_row - move_from_row)-1):
                    if board[move_from_row - row-1][move_to_column] is not None:
                        return False
            if move_to_row > move_from_row and move_to_column == move_from_column:
                for row in range(abs(move_to_row - move_from_row)-1):
                    if board[move_from_row + row+1][move_to_column] is not None:
                        return False
            if move_to_column < move_from_column and move_to_row == move_from_row:
                for column in range(abs(move_to_column - move_from_column)-1):
                    if board[move_to_row][move_from_column-1 - column] is not None:
                        return False
            if move_to_column > move_from_column and move_to_row == move_from_row:
                for column in range(abs(move_to_column - move_from_column)-1):
                    if board[move_to_row][move_from_column+1 + column] is not None:
                        return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        #       check if general is going to be checked
        if self._color == "R":
            general = game.get_general("B")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_blue_check(is_check)
        else:
            general = game.get_general("R")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_red_check(is_check)
        return True


class Cannon(Piece):
    """
    Represents a cannon that moves by jumping another piece horizontally or vertically and can be anywhere on the board
    as long as there is exactly one piece between the original position and the target position, the cannon cannot jump
    if the other piece that it jumps is another cannon, the cannon begins on the row behind the soldiers
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Cannon"""
        Piece.__init__(self, color, row, column)
        self._type = "Cannon"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        if row < self._row and column == self._column:
            jump_count = 0
            for row in range(abs(row - self._row) - 1):
                piece = board[self._row - 1 - row][column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count == 1:
                return True
        if row > self._row and column == self._column:
            jump_count = 0
            for row in range(abs(row - self._row) - 1):
                piece = board[self._row + 1 + row][column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count == 1:
                return True
        if column < self._column and row == self._row:
            jump_count = 0
            for column in range(abs(column - self._column) - 1):
                piece = board[row][self._column - 1 - column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count == 1:
                return True
        if column > self._column and row == self._row:
            jump_count = 0
            for column in range(abs(column - self._column) - 1):
                piece = board[row][self._column + 1 + column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count == 1:
                return True
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Cannon"""
        board = game.get_board()
        if board[move_from_row][move_from_column] is None:
            return False
        if abs(move_to_row - move_from_row) > 1 and abs(move_to_column - move_from_column) > 1:
            return False
        if move_to_row < move_from_row and move_to_column == move_from_column:
            jump_count = 0
            for row in range(abs(move_to_row - move_from_row) - 1):
                piece = board[move_from_row - row - 1][move_to_column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count != 1:
                return False
        if move_to_row > move_from_row and move_to_column == move_from_column:
            jump_count = 0
            for row in range(abs(move_to_row - move_from_row) - 1):
                piece = board[move_from_row + row + 1][move_to_column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count != 1:
                return False
        if move_to_column < move_from_column and move_to_row == move_from_row:
            jump_count = 0
            for column in range(abs(move_to_column - move_from_column) - 1):
                piece = board[move_to_row][move_from_column - 1 - column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count != 1:
                return False
        if move_to_column > move_from_column and move_to_row == move_from_row:
            jump_count = 0
            for column in range(abs(move_to_column - move_from_column) - 1):
                piece = board[move_to_row][move_from_column + 1 + column]
                if piece is not None and piece.get_type() != "Chariot":
                    jump_count += 1
            if jump_count != 1:
                return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
        #       check if general is going to be checked
        if self._color == "R":
            general = game.get_general("B")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_blue_check(is_check)
        else:
            general = game.get_general("R")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_red_check(is_check)
        return True


class Soldier(Piece):
    """
    Represents a soldier that moves straightforward or sideways and once they reach the end of the board can only move
    sideways, a soldier can also move one space diagonally if they are in the enemy palace, the soldier begins one
    space back from the edge and on alternating points
    """

    def __init__(self, color, row, column):
        """Initializes the values of the class Soldier"""
        Piece.__init__(self, color, row, column)
        self._type = "Soldier"

    def general_in_check(self, board, row, column):
        """Determines if the general at a row and column is in check"""
        if abs(self._row - row) > 1 or abs(self._column - column) > 1:
            return False
        if self._color == "R":
            if abs(row - self._row) == 1 and abs(column - self._column) == 1:
                if self._row == 7:
                    if self._column == 3 and column == 4 and row == 8:
                        return True
                    if self._column == 5 and column == 4 and row == 8:
                        return True
                if self._row == 8:
                    if self._column == 4 and column == 3 and row == 9:
                        return True
                    if self._column == 4 and column == 5 and row == 9:
                        return True
            if row - self._row == 1:
                if column == self._column:
                    return True
            if abs(column - self._column) == 1:
                if row == self._row:
                    return True
        if self._color == "B":
            if abs(row - self._row) == 1 and abs(column - self._column) == 1:
                if self._row == 2:
                    if self._column == 3 and column == 4 and row == 1:
                        return True
                    if self._column == 5 and column == 4 and row == 1:
                        return True
                if self._row == 1:
                    if self._column == 4 and column == 3 and row == 0:
                        return True
                    if self._column == 4 and column == 5 and row == 0:
                        return True
            if row - self._row == -1:
                if column == self._column:
                    return True
            if abs(column - self._column) == 1:
                if row == self._row:
                    return True
        return False

    def moves(self, game, move_from_row, move_from_column, move_to_row, move_to_column):
        """A move for the Soldier"""
        board = game.get_board()
        if board[move_from_row][move_from_column] is None:
            return False
        if abs(move_to_row - move_from_row) > 1:
            return False
        if abs(move_to_column - move_from_column) > 1:
            return False
        if self._color == "R":
            if move_to_row < move_from_row:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 7:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 8:
                        valid_move = True
                if move_from_row == 8:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 9:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 9:
                        valid_move = True
                if not valid_move:
                    return False
        if self._color == "B":
            if move_to_row > move_from_row:
                return False
            if abs(move_to_row - move_from_row) == 1 and abs(move_to_column - move_from_column) == 1:
                valid_move = False
                if move_from_row == 2:
                    if move_from_column == 3 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                    if move_from_column == 5 and move_to_column == 4 and move_to_row == 1:
                        valid_move = True
                if move_from_row == 1:
                    if move_from_column == 4 and move_to_column == 3 and move_to_row == 0:
                        valid_move = True
                    if move_from_column == 4 and move_to_column == 5 and move_to_row == 0:
                        valid_move = True
                if not valid_move:
                    return False
        piece = game.get_piece(move_to_row, move_to_column)
        if piece is not None:
            if piece.get_color() == self._color:
                return False
            else:
                game.take_piece(self, move_to_row, move_to_column)
        else:
            game.move_piece(self, move_to_row, move_to_column)
#       check if general is going to be checked
        if self._color == "R":
            general = game.get_general("B")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_blue_check(is_check)
        else:
            general = game.get_general("R")
            is_check = self.general_in_check(board, general.get_row(), general.get_column())
            game.set_red_check(is_check)
        return True


class JanggiGame:
    """
    Represents a 9x10 Board that has pieces that move in different ways and can capture other pieces
    """

    def __init__(self):
        """Initializes the values of the class Board"""
        self._board = [[None] * 9 for rows in range(10)]
        self._blue = [[None] * 9 for rows in range(10)]
        self._red = [[None] * 9 for rows in range(10)]
        self._red_checked = False
        self._blue_checked = False
        self._current_state = ["BLUE_WON", "RED_WON", "UNFINISHED"]
        self._game_state = 2
        self._blue_turn = True
        self._red_general = General("R", 1, 4)
        self._blue_general = General("B", 8, 4)
        self._board[0][0] = Chariot("R", 0, 0)
        self._board[0][1] = Elephant("R", 0, 1)
        self._board[0][2] = Horse("R", 0, 2)
        self._board[0][3] = Guard("R", 0, 3)
        self._board[0][5] = Guard("R", 0, 5)
        self._board[0][6] = Elephant("R", 0, 6)
        self._board[0][7] = Horse("R", 0, 7)
        self._board[0][8] = Chariot("R", 0, 8)
        self._board[1][4] = self._red_general
        self._board[2][1] = Cannon("R", 2, 1)
        self._board[2][7] = Cannon("R", 2, 7)
        self._board[3][0] = Soldier("R", 3, 0)
        self._board[3][2] = Soldier("R", 3, 2)
        self._board[3][4] = Soldier("R", 3, 4)
        self._board[3][6] = Soldier("R", 3, 6)
        self._board[3][8] = Soldier("R", 3, 8)
        for row in range(4):
            for column in range(9):
                self._red[row][column] = self._board[row][column]
        self._board[6][0] = Soldier("B", 6, 0)
        self._board[6][2] = Soldier("B", 6, 2)
        self._board[6][4] = Soldier("B", 6, 4)
        self._board[6][6] = Soldier("B", 6, 6)
        self._board[6][8] = Soldier("B", 6, 8)
        self._board[7][1] = Cannon("B", 7, 1)
        self._board[7][7] = Cannon("B", 7, 7)
        self._board[8][4] = self._blue_general
        self._board[9][0] = Chariot("B", 9, 0)
        self._board[9][1] = Elephant("B", 9, 1)
        self._board[9][2] = Horse("B", 9, 2)
        self._board[9][3] = Guard("B", 9, 3)
        self._board[9][5] = Guard("B", 9, 5)
        self._board[9][6] = Elephant("B", 9, 6)
        self._board[9][7] = Horse("B", 9, 7)
        self._board[9][8] = Chariot("B", 9, 8)
        for row in range(4):
            for column in range(9):
                self._blue[6+row][column] = self._board[6+row][column]

    def get_game_state(self):
        """Gets the state of the board"""
        return self._current_state[self._game_state]

    def set_game_state(self, player):
        """Sets the state of the game"""
        if player == "R":
            self._game_state = 1
        if player == "B":
            self._game_state = 0

    def is_in_check(self, player):
        """Determines if a player is in check"""
        if player == "red":
            return self._red_checked
        if player == "blue":
            return self._blue_checked

    def set_red_check(self, is_checked):
        """Sets the state of red in check"""
        self._red_checked = is_checked

    def set_blue_check(self, is_checked):
        """Sets the state of red in check"""
        self._blue_checked = is_checked

    def get_general(self, player):
        """Gets the general of the given player"""
        if player == "R":
            return self._red_general
        else:
            return self._blue_general

    def make_move(self, move_from, move_to):
        """Makes a move for a player"""
#        print("make_move('", move_from, "','", move_to, "')")
        if move_from == move_to:
            self._blue_turn = not self._blue_turn
            return True
        column_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        move_from_column = move_from[0]
        for index in range(9):
            if move_from_column == column_list[index]:
                move_from_column = index
                break
        move_to_column = move_to[0]
        for index in range(9):
            if move_to_column == column_list[index]:
                move_to_column = index
                break
        if len(move_from) == 3:
            move_from_row = int(move_from[1] + move_from[2]) - 1
        else:
            move_from_row = int(move_from[1])-1
        if len(move_to) == 3:
            move_to_row = int(move_to[1] + move_to[2]) - 1
        else:
            move_to_row = int(move_to[1])-1
        if move_from_row < 0 or move_from_row > 9:
            return False
        if move_from_column < 0 or move_from_column > 8:
            return False
        if move_to_row < 0 or move_to_row > 9:
            return False
        if move_to_column < 0 or move_to_column > 8:
            return False
        piece = self._board[move_from_row][move_from_column]
        if piece is None:
            return False
        if piece.get_color() == "R" and self._blue_turn:
            return False
        valid_move = piece.moves(self, move_from_row, move_from_column, move_to_row, move_to_column)
        if valid_move:
            self._blue_turn = not self._blue_turn
        return valid_move

    def get_board(self):
        """Gets the main board"""
        return self._board

    def get_piece(self, row, column):
        """Gets the piece at the given row and column"""
        return self._board[row][column]

    def get_red_pieces(self):
        """Returns all of the red pieces"""
        return self._red

    def get_blue_pieces(self):
        """Returns all of the blue pieces"""
        return self._blue

    def take_piece(self, piece, row, column):
        """Takes an opposing player's piece"""
        if piece.get_color() == "R":
            self._blue[row][column] = None
            self._board[row][column] = piece
            self._red[row][column] = piece
            self._board[piece.get_row()][piece.get_column()] = None
            self._red[piece.get_row()][piece.get_column()] = None
            piece.set_column(column)
            piece.set_row(row)
        else:
            self._red[row][column] = None
            self._board[row][column] = piece
            self._blue[row][column] = piece
            self._board[piece.get_row()][piece.get_column()] = None
            self._blue[piece.get_row()][piece.get_column()] = None
            piece.set_column(column)
            piece.set_row(row)

    def move_piece(self, piece, row, column):
        """Moves a piece to another square"""
        if piece.get_color() == "R":
            self._board[row][column] = piece
            self._red[row][column] = piece
            self._board[piece.get_row()][piece.get_column()] = None
            self._red[piece.get_row()][piece.get_column()] = None
            piece.set_column(column)
            piece.set_row(row)
        else:
            self._board[row][column] = piece
            self._blue[row][column] = piece
            self._board[piece.get_row()][piece.get_column()] = None
            self._blue[piece.get_row()][piece.get_column()] = None
            piece.set_column(column)
            piece.set_row(row)

"""
game1 = JanggiGame()
x = game1.make_move('e9', 'f8')
print(x)
game1.make_move('e9', 'd9')
blue_in_check = game1.is_in_check('blue')
print(blue_in_check)
state = game1.get_game_state()
"""
