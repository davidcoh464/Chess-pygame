from typing import Tuple, List, Optional
from chess_piece import Piece


class ContinuousMove:
    def __init__(self, is_white: bool, possible_directions: List[Tuple[int, int]]):
        self._possible_directions = possible_directions
        self._is_white = is_white

    def get_attack_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            while Piece.board_position(current_pos):
                if Piece.legal_attack_move(board, current_pos, self._is_white):
                    moves.append(current_pos)
                    break
                if board[current_pos[0]][current_pos[1]] is not None:
                    break
                current_pos = (current_pos[0] + i, current_pos[1] + j)
        return moves

    def get_peace_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            while Piece.board_position(current_pos) and Piece.legal_peace_move(board, current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] + i, current_pos[1] + j)
        return moves


class DiagonalMove(ContinuousMove):
    def __init__(self, is_white: bool):
        super().__init__(is_white=is_white, possible_directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])


class StraightMove(ContinuousMove):
    def __init__(self, is_white: bool):
        super().__init__(is_white=is_white, possible_directions=[(1, 0), (0, 1), (-1, 0), (0, -1)])
