from typing import Tuple, List, Optional


class Piece:
    def __init__(self, name: str, is_white: bool, pos: Tuple[int, int]):
        self._name = name
        self._is_white = is_white
        self._pos = pos

    def get_name(self) -> str:
        return self._name

    def get_position(self) -> Tuple[int, int]:
        return self._pos

    def set_position(self, pos: Tuple[int, int]) -> None:
        self._pos = pos

    def is_white(self) -> bool:
        return self._is_white

    def is_black(self) -> bool:
        return not self._is_white

    @staticmethod
    def board_position(pos: Tuple[int, int]):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    @staticmethod
    def legal_attack_move(board: List[List[Optional['Piece']]], pos: Tuple[int, int], is_white: bool) -> bool:
        return Piece.board_position(pos) and board[pos[0]][pos[1]] is not None and board[pos[0]][pos[1]].is_white() != is_white

    @staticmethod
    def legal_peace_move(board: List[List[Optional['Piece']]], pos: Tuple[int, int]):
        return Piece.board_position(pos) and board[pos[0]][pos[1]] is None

    def get_all_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        return self.get_attack_moves(board) + self.get_peace_moves(board)

    def get_attack_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        pass

    def get_peace_moves(self, board: List[List[Optional['Piece']]]) -> List[Tuple[int, int]]:
        pass
