from chess_piece import Piece
from chess_board import ChessBoard

CHECKMATE = 10000
STALEMATE = 0


class Evaluation:
    def __init__(self, board: ChessBoard):
        self._piece_values = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
        self._rows = tuple(range(8))
        self._board = board

    def evaluate_board(self):
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
        return self._piece_values.get(piece.get_name())
