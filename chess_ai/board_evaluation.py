from chess_piece import Piece
from chess_board import ChessBoard

CHECKMATE = 1000  # The score for checkmate.
STALEMATE = 0  # The score for stalemate.


class Evaluation:
    """
    Class to evaluate the current state of a chessboard.

    This class provides methods to evaluate the current state of a chessboard,
    assigning scores based on various factors such as piece values and game end status.
    Attributes:
        _piece_values (dict): A dictionary mapping piece names to their corresponding values.
        _rows (tuple): A tuple representing the range of rows on the chessboard.
        _board (ChessBoard): The chessboard instance to be evaluated.
    """

    def __init__(self, board: ChessBoard):
        """
        Initializes an Evaluation object with the given chessboard.
        Args:
            board (ChessBoard): The chessboard instance to be evaluated.
        """
        self._piece_values = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
        self._rows = tuple(range(8))
        self._board = board

    def evaluate_board(self):
        """
        Evaluate the current state of the chessboard.

        Evaluates the current state of the chessboard and returns
        an evaluation score. The score represents the advantage of the current
        position for the white player. Positive scores indicate an advantage
        for white, negative scores indicate an advantage for black.
        Returns:
            int: The evaluation score of the current position.
        """
        if self._board.is_game_end():
            end_status = self._board.game_end_status()
            if end_status == 0:  # Black won
                return -CHECKMATE
            elif end_status == 1:  # White won
                return CHECKMATE
            else:  # Stalemate
                return STALEMATE

        evaluation_score = 0
        for row in self._rows:
            for col in self._rows:
                piece = self._board.get_piece((row, col))
                if piece:
                    if piece.is_white():
                        evaluation_score += self.evaluate_piece(piece)
                    else:
                        evaluation_score -= self.evaluate_piece(piece)
        return evaluation_score

    def evaluate_piece(self, piece: Piece):
        """
        Evaluate the value of a chess piece.

        This method evaluates the value of a given chess piece based on its type.
        Args:
            piece (Piece): The chess piece to be evaluated.
        Returns:
            int: The value of the given chess piece.
        """
        return self._piece_values.get(piece.get_name())
