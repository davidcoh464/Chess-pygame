from typing import Tuple, List, Optional


class Piece:
    """
    Represents a generic chess piece.
    """
    def __init__(self, name: str, is_white: bool, pos: Tuple[int, int]):
        """
        Initializes a Piece instance.
        Args:
            name (str): The name of the piece.
            is_white (bool): Indicates whether the piece is white.
            pos (Tuple[int, int]): The initial position of the piece on the chessboard.
        """
        self._name = name
        self._is_white = is_white
        self._pos = pos

    def get_name(self) -> str:
        """
        Returns the name of the piece.
        Returns:
            str: The name of the piece.
        """
        return self._name

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the current position of the piece on the chessboard.
        Returns:
            Tuple[int, int]: The current position of the piece.
        """
        return self._pos

    def set_position(self, pos: Tuple[int, int]) -> None:
        """
        Sets the position of the piece on the chessboard.
        Args:
            pos (Tuple[int, int]): The new position of the piece.
        """
        self._pos = pos

    def is_white(self) -> bool:
        """
        Checks if the piece is white.
        Returns:
            bool: True if the piece is white, False otherwise.
        """
        return self._is_white

    def is_black(self) -> bool:
        """
        Checks if the piece is black.
        Returns:
            bool: True if the piece is black, False otherwise.
        """
        return not self._is_white

    @staticmethod
    def board_position(pos: Tuple[int, int]) -> bool:
        """
        Checks if the given position is within the chessboard bounds.
        Args:
            pos (Tuple[int, int]): The position to check.
        Returns:
            bool: True if the position is within bounds, False otherwise.
        """
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    @staticmethod
    def legal_attack_move(board: List[List[Optional['Piece']]], pos: Tuple[int, int], is_white: bool) -> bool:
        """
        Checks if an attack move to the given position is legal.
        Args:
            board (List[List[Optional['Piece']]]): The chessboard.
            pos (Tuple[int, int]): The position to check.
            is_white (bool): Indicates whether the attacking piece is white.
        Returns:
            bool: True if the attack move is legal, False otherwise.
        """
        return Piece.board_position(pos) and board[pos[0]][pos[1]] is not None and board[pos[0]][pos[1]].is_white() != is_white

    @staticmethod
    def legal_peace_move(board: List[List[Optional['Piece']]], pos: Tuple[int, int]) -> bool:
        """
        Checks if a peace (non-attack) move to the given position is legal.
        Args:
            board (List[List[Optional['Piece']]]): The chessboard.
            pos (Tuple[int, int]): The position to check.
        Returns:
            bool: True if the peace move is legal, False otherwise.
        """
        return Piece.board_position(pos) and board[pos[0]][pos[1]] is None

    def get_all_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        """
        Returns a list of all possible moves (both attack and peace moves) for the piece.
        Args:
            board (List[List[Optional['Piece']]]): The chessboard.
        Returns:
            List[Tuple[int, int]]: A list of all possible moves for the piece.
        """
        return self.get_attack_moves(board) + self.get_peace_moves(board)

    def get_attack_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        """
        Returns a list of valid attack moves for the piece.
        Args:
            board (List[List[Optional['Piece']]]): The chessboard.
        Returns:
            List[Tuple[int, int]]: A list of valid attack moves.
        """
        pass

    def get_peace_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        """
        Returns a list of valid peace (non-attack) moves for the piece.
        Args:
            board (List[List[Optional['Piece']]]): The chessboard.
        Returns:
            List[Tuple[int, int]]: A list of valid peace moves.
        """
        pass
