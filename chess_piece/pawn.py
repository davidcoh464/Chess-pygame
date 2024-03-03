from chess_piece import Piece
from typing import Tuple, List, Optional


class Pawn(Piece):
    """
    Represents a Pawn chess piece.
    """
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        """
        Initializes a Pawn instance.
        Args:
            is_white (bool): Indicates whether the pawn is white.
            pos (Tuple[int, int]): The initial position of the pawn on the chessboard.
        """
        super().__init__('p', is_white, pos)
        self.direction = -1 if self.is_white() else 1
        self.starting_point = 6 if self.is_white() else 1

    def get_peace_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        moves = []
        pos = self.get_position()

        front_pos = (pos[0] + self.direction, pos[1])
        if Piece.legal_peace_move(board, front_pos):
            moves.append(front_pos)
            two_squares_front = (pos[0] + 2 * self.direction, pos[1])
            if pos[0] == self.starting_point and Piece.legal_peace_move(board, two_squares_front):
                moves.append(two_squares_front)
        return moves

    def get_attack_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        moves = []
        pos = self.get_position()

        left_diagonal = (pos[0] + self.direction, pos[1] - 1)
        if Piece.legal_attack_move(board, left_diagonal, self.is_white()):
            moves.append(left_diagonal)

        right_diagonal = (pos[0] + self.direction, pos[1] + 1)
        if Piece.legal_attack_move(board, right_diagonal, self.is_white()):
            moves.append(right_diagonal)
        return moves

    def is_promote_location(self) -> bool:
        """
        Checks if the pawn has reached the end of the board and therefore can be promoted.
        Returns:
            bool: True if the pawn is reach to the promote location, False otherwise.
        """
        return (self.starting_point == 1 and self.get_position()[0] == 7) or\
            (self.starting_point == 6 and self.get_position()[0] == 0)
