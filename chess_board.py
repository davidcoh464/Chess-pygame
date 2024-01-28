import numpy as np
from typing import Optional, List, Tuple, Union
from chess_piece import Piece, Rook, King, Knight, Bishop, Queen, Pawn


class ChessBoard:
    def __init__(self):
        self._board: np.ndarray[Optional[Piece]] = np.empty((8, 8), dtype=object)
        self._is_white_turn = True
        self._white_king_location = (7, 3)
        self._black_king_location = (0, 3)

        piece_order = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
        for row, is_white in zip([0, 7], [False, True]):
            for col, piece_class in enumerate(piece_order):
                self._board[row, col] = piece_class(is_white=is_white, pos=(row, col))

        for row, is_white in zip([1, 6], [False, True]):
            for col in range(8):
                self._board[row, col] = Pawn(is_white=is_white, pos=(row, col))

    def is_white_turn(self) -> bool:
        return self._is_white_turn

    def change_turn(self):
        self._is_white_turn = not self._is_white_turn

    def get_board(self) -> np.ndarray[Optional[Piece]]:
        return self._board

    def get_piece(self, pos: Tuple[int, int]) -> Optional[Piece]:
        return self._board[pos]

    def get_piece_name(self, pos: Tuple[int, int]) -> Optional[str]:
        if self._board[pos] is not None:
            return self._board[pos].get_name()
        return None

    def is_white_piece(self, pos: Tuple[int, int]) -> Optional[bool]:
        if self._board[pos] is not None:
            return self._board[pos].is_white()
        return None

    def _get_king_location(self) -> Tuple[int, int]:
        return self._white_king_location if self.is_white_turn() else self._black_king_location

    def _set_king_location(self, pos: Tuple[int, int]):
        if self.is_white_turn():
            self._white_king_location = pos
        else:
            self._black_king_location = pos

    def is_check(self) -> bool:
        # checking for check, by checking from the king to the other pieces
        pos = self._get_king_location()
        return self._board[pos].is_check(self._board)

    def is_check_move(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int]):
        src_pic = self._board[src_pos]
        dst_pic = self._board[dst_pos]
        self.move_piece(src_pos, dst_pos)
        is_check = self.is_check()
        self.undo_move(src_pos, dst_pos, src_pic, dst_pic)
        return is_check

    def get_piece_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        return self.get_piece_peace_moves(pos) + self.get_piece_attack_moves(pos)

    def get_piece_peace_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        if self._board[pos] is not None:
            return [index for index in self._board[pos].get_peace_moves(self._board)
                    if not self.is_check_move(pos, index)]
        return []

    def get_piece_attack_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        if self._board[pos] is not None:
            return [index for index in self._board[pos].get_attack_moves(self._board)
                    if not self.is_check_move(pos, index)]
        return []

    def move_piece(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int]):
        src_pic: Optional[Piece] = self._board[src_pos]
        self._board[dst_pos] = src_pic
        self._board[src_pos] = None
        if src_pic is not None:
            src_pic.set_position(dst_pos)
            if src_pic.get_name() == 'k':
                self._set_king_location(dst_pos)

    def undo_move(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int],
                  src_pic: Optional[Piece], dst_pic: Optional[Piece]):
        if src_pic is not None:
            src_pic.set_position(src_pos)
            if src_pic.get_name() == 'k':
                self._set_king_location(src_pos)
        self._board[src_pos] = src_pic
        self._board[dst_pos] = dst_pic

    def is_game_end(self) -> bool:
        for row in range(self._board.shape[0]):
            for col in range(self._board.shape[1]):
                pos = (row, col)
                if self.is_white_piece(pos) == self.is_white_turn():
                    if self.get_piece_moves(pos):
                        return False
        return True

    def game_end_status(self) -> str:
        if self.is_check():
            return 'Black won' if self.is_white_turn() else 'White won'
        return 'Stalemate'

    def promote_pawn(self, piece: Optional[Union[Piece, Pawn]]):
        if piece is not None and piece.get_name() == 'p' and piece.is_promote_location():
            self._board[piece.get_position()] = Queen(is_white=piece.is_white(), pos=piece.get_position())
