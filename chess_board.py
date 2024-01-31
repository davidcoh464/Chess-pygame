from typing import Optional, List, Tuple, Union
from chess_piece import Piece, Rook, King, Knight, Bishop, Queen, Pawn


class ChessBoard:
    def __init__(self):
        """
        Initializes a ChessBoard instance with the starting position.
        """
        self._board: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self._is_white_turn = True
        self._white_king_location = (7, 4)
        self._black_king_location = (0, 4)

        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for row, is_white in [(0, False), (7, True)]:
            for col, piece_class in enumerate(piece_order):
                self._board[row][col] = piece_class(is_white=is_white, pos=(row, col))

        for row, is_white in [(1, False), (6, True)]:
            for col in range(8):
                self._board[row][col] = Pawn(is_white=is_white, pos=(row, col))

    def is_white_turn(self) -> bool:
        """
        Returns:
             bool: True if it is currently the white player's turn, False otherwise.
        """
        return self._is_white_turn

    def change_turn(self):
        """
        Switches the turn from the current player to the opposite player.
        """
        self._is_white_turn = not self._is_white_turn

    def get_board(self) -> List[List[Optional[Piece]]]:
        """
        Returns the current state of the chessboard.
        Returns:
            List[List[Optional[Piece]]]: The 8x8 chessboard.
        """
        return self._board

    def get_piece(self, pos: Tuple[int, int]) -> Optional[Piece]:
        """
        Returns the piece at the specified position on the chessboard.
        Args:
            pos (Tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            Optional[Piece]: The piece at the specified position or None if the position is empty.
        """
        return self._board[pos[0]][pos[1]]

    def get_piece_name(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Returns the name of the piece at the specified position on the chessboard.
        Args:
            pos (Tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            Optional[str]: The name of the piece at the specified position or None if the position is empty.
        """
        if self._board[pos[0]][pos[1]] is not None:
            return self._board[pos[0]][pos[1]].get_name()
        return None

    def is_white_piece(self, pos: Tuple[int, int]) -> Optional[bool]:
        """
        Returns whether the piece at the specified position is white or black.
        Args:
            pos (Tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            Optional[bool]: True if the piece is white, False if black, and None if the position is empty.
        """
        if self._board[pos[0]][pos[1]] is not None:
            return self._board[pos[0]][pos[1]].is_white()
        return None

    def _get_king_location(self) -> Tuple[int, int]:
        """
        Returns the current location of the king for the player whose turn it is.
        Returns:
            Tuple[int, int]: The row and column indices of the king's position.
        """
        return self._white_king_location if self.is_white_turn() else self._black_king_location

    def _set_king_location(self, pos: Tuple[int, int]):
        """
        Sets the current location of the king for the player whose turn it is.
        Args:
            pos (Tuple[int, int]): The new position (row, col) of the king.
        """
        if self.is_white_turn():
            self._white_king_location = pos
        else:
            self._black_king_location = pos

    def is_check(self) -> bool:
        """
        Checks if the current player's king is in check.
        Returns:
            bool: True if the king is in check, False otherwise.
        """
        pos = self._get_king_location()
        piece: Optional[King] = self._board[pos[0]][pos[1]]
        return piece.is_check(self._board)

    def is_check_move(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int]):
        """
        Checks if a move puts the current player's king in check.
        Args:
            src_pos (Tuple[int, int]): The source position (row, col) of the piece to be moved.
            dst_pos (Tuple[int, int]): The destination position (row, col) for the piece.
        Returns:
            bool: True if the move puts the king in check, False otherwise.
        """
        src_pic = self._board[src_pos[0]][src_pos[1]]
        dst_pic = self._board[dst_pos[0]][dst_pos[1]]
        self.move_piece(src_pos, dst_pos)
        is_check = self.is_check()
        self.undo_move(src_pos, dst_pos, src_pic, dst_pic)
        return is_check

    def get_piece_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns all valid moves for the piece at the specified position.
        Args:
            pos (Tuple[int, int]): The position (row, col) of the piece on the chessboard.
        Returns:
            List[Tuple[int, int]]: A list of valid moves for the piece at the specified position.
        """
        return self.get_piece_peace_moves(pos) + self.get_piece_attack_moves(pos)

    def get_piece_peace_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns valid non-attack (peaceful) moves for the piece at the specified position.
        Args:
            pos (Tuple[int, int]): The position (row, col) of the piece on the chessboard.
        Returns:
            List[Tuple[int, int]]: A list of valid peaceful moves for the piece.
        """
        piece: Optional[Piece] = self._board[pos[0]][pos[1]]
        if piece is not None:
            return [index for index in piece.get_peace_moves(self._board) if not self.is_check_move(pos, index)]
        return []

    def get_piece_attack_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns valid attack moves for the piece at the specified position.
        Args:
            pos (Tuple[int, int]): The position (row, col) of the piece on the chessboard.
        Returns:
            List[Tuple[int, int]]: A list of valid attack moves for the piece.
        """
        piece: Optional[Piece] = self._board[pos[0]][pos[1]]
        if piece is not None:
            return [index for index in piece.get_attack_moves(self._board) if not self.is_check_move(pos, index)]
        return []

    def move_piece(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int]):
        """
        Moves a piece from the source position to the destination position.
        Args:
            src_pos (Tuple[int, int]): The source position (row, col) of the piece to be moved.
            dst_pos (Tuple[int, int]): The destination position (row, col) for the piece.
        """
        src_pic: Optional[Piece] = self._board[src_pos[0]][src_pos[1]]
        self._board[dst_pos[0]][dst_pos[1]] = src_pic
        self._board[src_pos[0]][src_pos[1]] = None
        if src_pic is not None:
            src_pic.set_position(dst_pos)
            if isinstance(src_pic, King):
                self._set_king_location(dst_pos)
                src_pic.increase_moves_counter()
                # if is a castle move
                if src_pos[1] - dst_pos[1] == 2:
                    self.move_piece((src_pos[0], 0), (src_pos[0], src_pos[1] - 1))
                elif dst_pos[1] - src_pos[1] == 2:
                    self.move_piece((src_pos[0], 7), (src_pos[0], src_pos[1] + 1))
            elif isinstance(src_pic, Rook):
                src_pic.increase_moves_counter()

    def undo_move(self, src_pos: Tuple[int, int], dst_pos: Tuple[int, int],
                  src_pic: Optional[Piece], dst_pic: Optional[Piece]):
        """
        Undoes a previous move, restoring the chessboard to its state before the move.
        Args:
            src_pos (Tuple[int, int]): The source position (row, col) of the piece that was moved.
            dst_pos (Tuple[int, int]): The destination position (row, col) for the piece.
            src_pic (Optional[Piece]): The piece that was at the source position before the move.
            dst_pic (Optional[Piece]): The piece that was at the destination position before the move.
        """
        if src_pic is not None:
            src_pic.set_position(src_pos)
            if isinstance(src_pic, King):
                self._set_king_location(src_pos)
                src_pic.decrease_moves_counter()
                # undo castle move
                if src_pos[1] - dst_pos[1] == 2:
                    self.undo_move((src_pos[0], 0), (src_pos[0], src_pos[1] - 1),
                                   self._board[src_pos[0]][src_pos[1] - 1], self._board[src_pos[0]][0])
                elif dst_pos[1] - src_pos[1] == 2:
                    self.undo_move((src_pos[0], 7), (src_pos[0], src_pos[1] + 1),
                                   self._board[src_pos[0]][src_pos[1] + 1], self._board[src_pos[0]][7])
            elif isinstance(src_pic, Rook):
                src_pic.decrease_moves_counter()
        self._board[src_pos[0]][src_pos[1]] = src_pic
        self._board[dst_pos[0]][dst_pos[1]] = dst_pic

    def is_game_end(self) -> bool:
        """
        Checks if the game has ended (either through checkmate or stalemate).
        Returns:
            bool: True if the game has ended, False otherwise.
        """
        for row in range(8):
            for col in range(8):
                pos = (row, col)
                if self.is_white_piece(pos) == self.is_white_turn():
                    if self.get_piece_moves(pos):
                        return False
        return True

    def game_end_status(self) -> str:
        """
        Returns the status of the game at the end: 'Black won', 'White won', or 'Stalemate'.
        Returns:
            str: The status of the game at the end.
        """
        if self.is_check():
            return 'Black won' if self.is_white_turn() else 'White won'
        return 'Stalemate'

    def promote_pawn(self, pos: Tuple[int, int]):
        """
        Promotes a pawn to a queen if it reaches the promotion location.
        Args:
            pos (Tuple[int, int]): The pawn position to be promoted.
        """
        piece: Optional[Union[Piece, Pawn]] = self._board[pos[0]][pos[1]]
        if piece is not None and piece.get_name() == 'p' and piece.is_promote_location():
            self._board[piece.get_position()[0]][piece.get_position()[1]] = Queen(is_white=piece.is_white(), pos=piece.get_position())
