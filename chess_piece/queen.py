from chess_move import DiagonalMove, StraightMove
from chess_piece import Piece
from typing import Tuple, List, Optional


class Queen(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('q', is_white, pos)
        self._diagonal_move = DiagonalMove(is_white)
        self._straight_move = StraightMove(is_white)

    def get_attack_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._diagonal_move.get_attack_moves(board, pos=self.get_position()) + \
            self._straight_move.get_attack_moves(board, pos=self.get_position())

    def get_peace_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._diagonal_move.get_peace_moves(board, pos=self.get_position()) + \
            self._straight_move.get_peace_moves(board, pos=self.get_position())
