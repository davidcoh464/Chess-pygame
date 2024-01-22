from chess_piece import Piece
from chess_move import StraightMove
from typing import Tuple, List
import numpy as np


class Rook(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('q', is_white, pos)
        self._straight_move = StraightMove(is_white)

    def get_attack_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self._straight_move.get_attack_moves(board, pos=self.get_position())

    def get_peace_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self._straight_move.get_peace_moves(board, pos=self.get_position())
