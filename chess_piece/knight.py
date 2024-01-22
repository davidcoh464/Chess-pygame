from chess_piece import Piece
from chess_move import HorseMove
from typing import Tuple, List
import numpy as np


class Knight(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('n', is_white, pos)
        self.horse_move = HorseMove(is_white)

    def get_peace_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self.horse_move.get_peace_moves(board, self.get_position())

    def get_attack_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        return self.horse_move.get_attack_moves(board, self.get_position())
