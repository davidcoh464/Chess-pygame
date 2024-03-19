import threading
from chess_board import ChessBoard
from chess_ai import ChessAI


class ChessEngine:
    def __init__(self, is_human_white: bool):
        """
        Initializes a ChessEngine instance.
        """
        self.selected_square = ()
        self.board_change = True
        self.available_moves: list[tuple[int, int]] = []
        self.moving_update = False
        self._game_status = []
        self._chess_board = ChessBoard()
        self._stop_ai_event = threading.Event()
        self._is_human_white = is_human_white
        self.ai_run = False
        self._ai_engine = ChessAI(stop_event=self._stop_ai_event)

    def get_piece_name(self, pos: tuple[int, int]):
        """
        Gets the name of the piece at the specified position.
        Args:
            pos (tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            str: The name of the piece at the specified position.
        """
        return self._chess_board.get_piece_name(pos)

    def get_piece_moves(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the piece at the specified position.
        Args:
            pos (tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            list[tuple[int, int]]: List of valid moves for the piece at the specified position.
        """
        return self._chess_board.get_piece_moves(pos)

    def is_check(self):
        """
        Checks if the current player's king is in check.
        Returns:
            bool: True if the king is in check, False otherwise.
        """
        return self._chess_board.is_check()

    def get_turn(self) -> str:
        """
        Gets the color of the player whose turn it is.
        Returns:
            str: 'white' or 'black' depends on which turn is it.
        """
        return 'white' if self._chess_board.is_white_turn() else 'black'

    def is_stop_set(self):
        return self._stop_ai_event.is_set()

    def set_stop_ai(self):
        self._stop_ai_event.set()

    def unset_stop_ai(self):
        self._stop_ai_event.clear()

    def is_ai_turn(self):
        return self._chess_board.is_white_turn() != self._is_human_white

    def is_ai_running(self):
        return self.ai_run

    def move_ai(self):
        if self.is_ai_turn():
            self.ai_run = True

            if self.is_stop_set():
                self.unset_stop_ai()
            self._ai_engine.find_best_move(self._chess_board)

            move = self._ai_engine.best_move
            if not self.is_stop_set() and move is not None:
                self.move_piece(move[0], move[1])
                self.moving_update = True
                self.board_change = True
            else:
                self.unset_stop_ai()

            self.ai_run = False

    def move_piece(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> None:
        """
        Moves a piece on the chessboard and updates the game state.
        Args:
            src_pos (tuple[int, int]): The source position (row, col) of the piece to be moved.
            dst_pos (tuple[int, int]): The destination position (row, col) for the piece.
        """
        self._game_status.append([src_pos, dst_pos, self._chess_board.get_piece(src_pos), self._chess_board.get_piece(dst_pos)])
        self._chess_board.move_piece(src_pos, dst_pos)
        self._chess_board.promote_pawn(dst_pos)
        self._chess_board.change_turn()

    def undo_move(self):
        """
        Undoes the last move and restores the previous game state.
        """
        if len(self._game_status) > 0:
            if self.is_ai_turn():
                self.set_stop_ai()
            self._chess_board.change_turn()
            [src_pos, dst_pos, src_pic, dst_pic] = self._game_status.pop()
            self._chess_board.undo_move(src_pos, dst_pos, src_pic, dst_pic)

            if len(self._game_status) > 0 and self._is_human_white != self._chess_board.is_white_turn():
                self._chess_board.change_turn()
                [src_pos, dst_pos, src_pic, dst_pic] = self._game_status.pop()
                self._chess_board.undo_move(src_pos, dst_pos, src_pic, dst_pic)

            self.board_change = True
            self.selected_square = ()
            self.available_moves = []

    def get_piece_color(self, pos: tuple[int, int]) -> str:
        """
        Gets the color of the piece at the specified position.
        Args:
            pos (tuple[int, int]): The position (row, col) on the chessboard.
        Returns:
            str: 'white' or 'black' depends on if the piece is white or black.
        """
        return 'white' if self._chess_board.is_white_piece(pos) else 'black'

    def is_game_end(self) -> bool:
        """
        Checks if the game has ended (either through checkmate or stalemate).
        Returns:
            bool: True if the game has ended, False otherwise.
        """
        return self._chess_board.is_game_end()

    def game_end_status(self) -> str:
        """
        Gets the status of the game at the end: 'Black won', 'White won', or 'Stalemate'.
        Returns:
            str: The status of the game at the end.
        """
        status = self._chess_board.game_end_status()
        return "Black won" if status == 0 else 'White won' if status == 1 else 'Stalemate'

    def on_board_click(self, pos: tuple[int, int]):
        """
        Handles a click on the chessboard square.
        Args:
            pos (tuple[int, int]): The position (row, col) of the clicked square.
        """
        is_piece_turn = self._chess_board.is_white_piece(pos) == self._chess_board.is_white_turn()
        if self.selected_square != pos and is_piece_turn:
            self.available_moves = self.get_piece_moves(pos)
            self.selected_square = pos
            self.board_change = True
        elif self.selected_square != () and not is_piece_turn:
            if pos in self.available_moves:
                self.move_piece(self.selected_square, pos)
                self.moving_update = True
            self.available_moves = []
            self.selected_square = ()
            self.board_change = True
