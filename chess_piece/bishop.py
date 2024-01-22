from chess_piece import Piece
from chess_move import DiagonalMove
from typing import Tuple, List
import numpy as np


class Bishop(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('b', is_white, pos)
        self.moves = DiagonalMove(is_white)

    def get_peace_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self.moves.get_peace_moves(board, self.get_position())

    def get_attack_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self.moves.get_attack_moves(board, self.get_position())
