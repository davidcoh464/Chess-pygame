from chess_piece import Piece
from chess_move import StraightMove
from typing import Tuple, List, Optional


class Rook(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('r', is_white, pos)
        self._straight_move = StraightMove(is_white)
        self._move_counter = 0

    def get_attack_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._straight_move.get_attack_moves(board, pos=self.get_position())

    def get_peace_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._straight_move.get_peace_moves(board, pos=self.get_position())

    def has_moved(self) -> bool:
        return self._move_counter != 0

    def increase_moves_counter(self):
        self._move_counter += 1

    def decrease_moves_counter(self):
        self._move_counter -= 1