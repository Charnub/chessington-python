"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player
        self.moved = False

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)
        self.moved = True

    def available_moves(self, board, direction):
        square = direction(board.find_piece(self))
        while self.is_free(board, square):
            print(square)
            if board.fullSquare(square):
                break
            square = direction(square)

    def is_free(self, board, square):
        return board.squareBound(square) and \
               (board.emptySquare(square) or self.capture_piece(board.get_piece(square)))

    def can_capture(self, board, square):
        return (board.squareBound(square) and
                board.fullSquare(square) and
                board.get_piece(square).player != self.player)

    def capture_piece(self, piece):
        return piece.player != self.player


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):

        location = board.find_piece(self)  # Finds current position of piece
        piece = 1 if self.player == Player.WHITE else -1
        single_move = Square.at(location.row + piece, location.col)  # Will move one space
        double_move = Square.at(location.row + 2 * piece, location.col)  # Will move 2 spaces

        board_moves = []

        if not board.squareBound(single_move) or board.fullSquare(single_move):  #
            board_moves = []
        elif self.moved or not board.squareBound(double_move) or board.fullSquare(double_move):
            board_moves = [single_move]
        else:
            board_moves = [single_move, double_move]

        board_capture = [Square.at(location.row + piece, location.col + 1), Square.at(location.row + piece, location.col - 1)]
        board_capture = list(filter(lambda square: self.can_capture(board, square), board_capture))

        return board_moves + board_capture


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        location = board.find_piece(self)
        knight_moves = [
            Square.at(location.row + 2, location.col + 1), Square.at(location.row + 2, location.col - 1),
            Square.at(location.row + 1, location.col + 2), Square.at(location.row + 1, location.col - 2),
            Square.at(location.row - 2, location.col + 1), Square.at(location.row - 2, location.col - 1),
            Square.at(location.row - 1, location.col + 2), Square.at(location.row - 1, location.col - 2),
        ]
        return list(filter(lambda square: self.is_free(board, square), knight_moves))


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        location = board.find_piece(self)


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []