from typing import Tuple, List, Optional
from chess_piece import Piece


class PreciseMove:
    """
    Represents a precise movement (King, Knight) pattern on a chessboard.
    """
    def __init__(self, is_white: bool, possible_directions: List[Tuple[int, int]]):
        """
        Initializes a PreciseMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
            possible_directions (List[Tuple[int, int]]): A list of possible movement directions.
        """
        self._possible_directions = possible_directions
        self._is_white = is_white

    def get_attack_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns a list of valid attack moves for a precise movement pattern from the given position.
        Args:
            board (List[List[Optional[Piece]]]): The chessboard.
            pos (Tuple[int, int]): The current position.
        Returns:
            List[Tuple[int, int]]: A list of valid attack moves.
        """
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            if Piece.legal_attack_move(board, current_pos, self._is_white):
                moves.append(current_pos)
        return moves

    def get_peace_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns a list of valid peace (non-attack) moves for a precise movement pattern from the given position.
        Args:
            board (List[List[Optional[Piece]]]): The chessboard.
            pos (Tuple[int, int]): The current position.
        Returns:
            List[Tuple[int, int]]: A list of valid peace moves.
        """
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            if Piece.legal_peace_move(board, current_pos):
                moves.append(current_pos)
        return moves


class KnightMove(PreciseMove):
    """
    Represents a knight movement pattern on a chessboard.
    Inherits from PreciseMove.
    """
    def __init__(self, is_white: bool):
        """
        Initializes a KnightMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
        """
        super().__init__(is_white=is_white, possible_directions=[(-2, -1), (-2, 1), (2, 1), (2, -1),
                                                                 (-1, -2), (-1, 2), (1, 2), (1, -2)])


class KingMove(PreciseMove):
    """
    Represents a king movement pattern on a chessboard.
    Inherits from PreciseMove.
    """
    def __init__(self, is_white: bool):
        """
        Initializes a KingMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
        """
        super().__init__(is_white=is_white, possible_directions=[(-1, -1), (-1, 0), (-1, 1), (0, -1),
                                                                 (0, 1), (1, -1), (1, 0), (1, 1)])
