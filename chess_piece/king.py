from chess_piece import Piece
from chess_move import DiagonalMove, StraightMove, KingMove, HorseMove
from typing import Tuple, List, Optional
import numpy as np


class King(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('k', is_white, pos)
        self._diagonal_move = DiagonalMove(is_white)
        self._straight_move = StraightMove(is_white)
        self._horse_move = HorseMove(is_white)
        self._king_move = KingMove(is_white)

    def get_peace_moves(self, board: np.ndarray[Optional[Piece]]) -> List[Tuple[int, int]]:
        return self._king_move.get_peace_moves(board, self.get_position())

    def get_attack_moves(self, board: np.ndarray[Optional[Piece]]) -> List[Tuple[int, int]]:
        return self._king_move.get_attack_moves(board, self.get_position())

    def is_check(self, board: np.ndarray[Optional[Piece]]) -> bool:
        pos = self.get_position()

        for index in self._diagonal_move.get_attack_moves(board, pos):
            name = board[index].get_name()
            if name in ['q', 'b']:
                return True
            if name == 'p' and pos in board[index].get_attack_moves(board):
                return True

        for index in self._straight_move.get_attack_moves(board, pos):
            if board[index].get_name() in ['q', 'r']:
                return True

        for index in self._king_move.get_attack_moves(board, pos):
            if board[index].get_name() == 'k':
                return True

        for index in self._horse_move.get_attack_moves(board, pos):
            if board[index].get_name() == 'n':
                return True
        return False
