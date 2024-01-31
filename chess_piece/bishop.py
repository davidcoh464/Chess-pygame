from chess_piece import Piece
from chess_move import DiagonalMove
from typing import Tuple, List, Optional


class Bishop(Piece):
    """
    Represents a Bishop chess piece.
    """
    def __init__(self, is_white: bool, pos: Tuple[int, int]):
        """
        Initializes a Bishop instance.
        Args:
            is_white (bool): Indicates whether the bishop is white.
            pos (Tuple[int, int]): The initial position of the bishop on the chessboard.
        """
        super().__init__('b', is_white, pos)
        self.moves = DiagonalMove(is_white)

    def get_peace_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self.moves.get_peace_moves(board, self.get_position())

    def get_attack_moves(self, board: List[List[Optional[Piece]]]) -> List[Tuple[int, int]]:
        return self.moves.get_attack_moves(board, self.get_position())
