from typing import List, Dict
from chess_board import ChessBoard
from chess_piece import Piece

CHECKMATE = 100000  # The score for checkmate.
STALEMATE = 0  # The score for stalemate.

PAWN_SCORE = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 7, 7, 7, 7, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 3, 4, 4, 3, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_SCORE = [
    [-10, -8, -6, -6, -6, -6, -8, -10],
    [-8, -4, 0, 0, 0, 0, -4, -8],
    [-6, 0, 4, 6, 6, 4, 0, -6],
    [-6, 2, 6, 8, 8, 6, 2, -6],
    [-6, 0, 6, 8, 8, 6, 0, -6],
    [-6, 2, 4, 6, 6, 4, 2, -6],
    [-8, -4, 0, 2, 2, 0, -4, -8],
    [-10, -8, -6, -6, -6, -6, -8, -10]
]

BISHOP_SCORE = [
    [5, 0, 0, 0, 0, 0, 0, 5],
    [0, 5, 0, 0, 0, 0, 5, 0],
    [0, 0, 10, 5, 5, 10, 0, 0],
    [0, 0, 10, 15, 15, 10, 0, 0],
    [0, 0, 10, 15, 15, 10, 0, 0],
    [0, 0, 10, 5, 5, 10, 0, 0],
    [0, 5, 0, 0, 0, 0, 5, 0],
    [5, 0, 0, 0, 0, 0, 0, 5]
]

ROOK_SCORE = [
    [0, 0, 4, 10, 10, 4, 0, 0],
    [4, 4, 4, 10, 10, 4, 4, 4],
    [1, 1, 2, 5, 5, 2, 1, 1],
    [1, 2, 3, 10, 10, 3, 2, 1],
    [1, 2, 3, 10, 10, 3, 2, 1],
    [1, 1, 2, 5, 5, 2, 1, 1],
    [4, 4, 4, 10, 10, 4, 4, 4],
    [0, 0, 4, 10, 10, 4, 0, 0]
]

QUEEN_SCORE = [
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, -5, -5, -5, -5, -5, -5, -5]
]

KING_SCORE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 5, 0, 0],
    [0, 5, 5, 10, 10, 5, 5, 0],
    [0, 5, 10, 10, 10, 10, 5, 0],
    [0, 5, 10, 10, 10, 10, 5, 0],
    [0, 0, 5, 10, 10, 5, 0, 0],
    [0, 5, 5, -5, -5, 5, 5, 0],
    [0, 0, 10, 0, 0, 0, 10, 0]
]

PIECE_VALUE: Dict[str, int] = {"k": 0, "q": 900, "r": 500, "b": 310, "n": 300, "p": 100}

POSITION_SCORE: Dict[str, List[List[int]]] = {
    "n": KNIGHT_SCORE,
    "b": BISHOP_SCORE,
    "q": QUEEN_SCORE,
    "r": ROOK_SCORE,
    "p": PAWN_SCORE,
    "k": KING_SCORE
}


class Evaluation:
    """
    Class to evaluate the current state of a chessboard.

    This class provides methods to evaluate the current state of a chessboard,
    assigning scores based on various factors such as piece values and game end status.
    Attributes:
        _rows (tuple): A tuple representing the range of rows on the chessboard.
        _board (ChessBoard): The chessboard instance to be evaluated.
    """

    def __init__(self, board: ChessBoard):
        """
        Initializes an Evaluation object with the given chessboard.
        Args:
            board (ChessBoard): The chessboard instance to be evaluated.
        """
        self._rows = tuple(range(8))
        self._board = board

    def evaluate_board(self):
        """
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
                        evaluation_score += Evaluation.evaluate_piece(piece, row, col)
                    else:
                        evaluation_score -= Evaluation.evaluate_piece(piece, 7 - row, col)
        return evaluation_score

    @staticmethod
    def evaluate_piece(piece: Piece, row, col):
        """
        Evaluate the value of a chess piece.

        This method evaluates the value of a given chess piece based on its type.
        Args:
            piece (Piece): The chess piece to be evaluated.
            row: (int) The piece row
            col: (int) The piece column
        Returns:
            int: The value of the given chess piece.
        """
        return PIECE_VALUE[piece.get_name()] + POSITION_SCORE[piece.get_name()][row][col]
