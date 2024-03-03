from typing import Tuple, List, Optional
from chess_piece import Piece


class ContinuousMove:
    """
    Represents a continuous movement (Bishop, Rook, Queen) pattern on a chessboard.
    """
    def __init__(self, is_white: bool, possible_directions: List[Tuple[int, int]]):
        """
        Initializes a ContinuousMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
            possible_directions (List[Tuple[int, int]]): A list of possible movement directions.
        """
        self._possible_directions = possible_directions
        self._is_white = is_white

    def get_attack_moves(self, board: List[List[Optional[Piece]]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns a list of valid attack moves for a continuous movement pattern from the given position.
        Args:
            board (List[List[Optional[Piece]]]): The chessboard.
            pos (Tuple[int, int]): The current position.
        Returns:
            List[Tuple[int, int]]: A list of the valid attack moves.
        """
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
        """
        Returns a list of valid peace (non-attack) moves for a continuous movement pattern from the given position.
        Args:
            board (List[List[Optional[Piece]]]): The chessboard.
            pos (Tuple[int, int]): The current position.
        Returns:
            List[Tuple[int, int]]: A list of valid peace moves.
        """
        moves = []
        for i, j in self._possible_directions:
            current_pos = (pos[0] + i, pos[1] + j)
            while Piece.board_position(current_pos) and Piece.legal_peace_move(board, current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] + i, current_pos[1] + j)
        return moves


class DiagonalMove(ContinuousMove):
    """
    Represents a diagonal movement (left or right) pattern on a chessboard.
    Inherits from ContinuousMove.
    """
    def __init__(self, is_white: bool):
        """
        Initializes a DiagonalMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
        """
        super().__init__(is_white=is_white, possible_directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])


class StraightMove(ContinuousMove):
    """
    Represents a straight (vertical or horizontal) movement pattern on a chessboard.
    Inherits from ContinuousMove.
    """
    def __init__(self, is_white: bool):
        """
        Initializes a StraightMove instance.
        Args:
            is_white (bool): Indicates whether the movement is for a white piece.
        """
        super().__init__(is_white=is_white, possible_directions=[(1, 0), (0, 1), (-1, 0), (0, -1)])
