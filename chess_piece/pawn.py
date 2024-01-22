from chess_piece import Piece
from typing import Tuple, List
import numpy as np


class Pawn(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('p', is_white, pos)
        self.direction = -1 if self.is_white() else 1
        self.starting_point = 6 if self.is_white() else 1

    def get_peace_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        moves = []
        pos = self.get_position()
        front_pos = (pos[0] + self.direction, pos[1])

        if Piece.legal_peace_move(board, front_pos):
            moves.append(front_pos)
            two_squares_front = (pos[0] + 2 * self.direction, pos[1])
            if pos[0] == self.starting_point and Piece.legal_peace_move(board, two_squares_front):
                moves.append(two_squares_front)
        return moves

    def get_attack_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        moves = []
        pos = self.get_position()

        left_diagonal = (pos[0] + self.direction, pos[1] - 1)
        if Piece.legal_attack_move(board, left_diagonal, self.is_white()):
            moves.append(left_diagonal)

        right_diagonal = (pos[0] + self.direction, pos[1] + 1)
        if Piece.legal_attack_move(board, right_diagonal, self.is_white()):
            moves.append(right_diagonal)
        return moves
