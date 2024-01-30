from chess_piece import Piece, Rook
from chess_move import DiagonalMove, StraightMove, KingMove, HorseMove
from typing import Tuple, List, Optional


class King(Piece):
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        super().__init__('k', is_white, pos)
        self._diagonal_move = DiagonalMove(is_white)
        self._straight_move = StraightMove(is_white)
        self._horse_move = HorseMove(is_white)
        self._king_move = KingMove(is_white)
        self._move_counter = 0

    def get_peace_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._king_move.get_peace_moves(board, self.get_position())

    def get_attack_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self._king_move.get_attack_moves(board, self.get_position())

    def is_check(self, board: List[List[Optional[Piece]]]) -> bool:
        pos = self.get_position()

        for index in self._diagonal_move.get_attack_moves(board, pos):
            name = board[index[0]][index[1]].get_name()
            if name in ['q', 'b']:
                return True
            if name == 'p' and pos in board[index[0]][index[1]].get_attack_moves(board):
                return True

        for index in self._straight_move.get_attack_moves(board, pos):
            if board[index[0]][index[1]].get_name() in ['q', 'r']:
                return True

        for index in self._king_move.get_attack_moves(board, pos):
            if board[index[0]][index[1]].get_name() == 'k':
                return True

        for index in self._horse_move.get_attack_moves(board, pos):
            if board[index[0]][index[1]].get_name() == 'n':
                return True
        return False

    def increase_moves_counter(self):
        self._move_counter += 1

    def decrease_moves_counter(self):
        self._move_counter -= 1

    def has_moved(self) -> bool:
        return self._move_counter != 0

    def castle_move(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        rook1: Optional[Piece | Rook] = board[self._pos[0]][0]
        rook2: Optional[Piece | Rook] = board[self._pos[0]][7]
        moves = []
        if not self.has_moved():
            if rook1 and rook1.get_name() == 'r' and not rook1.has_moved() and\
                    all(board[self._pos[0]][col] is None for col in range(1, self._pos[1]))\
                    and not self.is_check(board):
                moves.append((self._pos[0], self._pos[1] - 2))
            if rook2 and rook2.get_name() == 'r' and not rook2.has_moved() and \
                    all(board[self._pos[0]][col] is None for col in range(self._pos[1] + 1, 7))\
                    and (len(moves) == 1 or not self.is_check(board)):
                moves.append((self._pos[0], self._pos[1] + 2))
        return moves
