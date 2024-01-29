from typing import Tuple, List, Optional
from chess_piece import Piece


class PreciseMove:
    def __init__(self, is_white: bool, possible_directions: List[Tuple[int, int]]):
        self._possible_directions = possible_directions
        self._is_white = is_white

    def get_attack_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            if Piece.legal_attack_move(board, current_pos, self._is_white):
                moves.append(current_pos)
        return moves

    def get_peace_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            if Piece.legal_peace_move(board, current_pos):
                moves.append(current_pos)
        return moves


class HorseMove(PreciseMove):
    def __init__(self, is_white: bool):
        super().__init__(is_white=is_white,
                         possible_directions=[(-2, -1), (-2, 1), (2, 1), (2, -1),
                                              (-1, -2), (-1, 2), (1, 2), (1, -2)])


class KingMove(PreciseMove):
    def __init__(self, is_white: bool):
        super().__init__(is_white=is_white,
                         possible_directions=[(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                              (0, 1), (1, -1), (1, 0), (1, 1)])
