from chess_board import ChessBoard


class ChessEngine:
    def __init__(self):
        self.selected_square = ()
        self.board_change = True
        self.available_moves: list[tuple[int, int]] = []
        self.moving_update = False
        self._game_status = []
        self._chess_board = ChessBoard()

    def get_piece_name(self, pos: tuple[int, int]):
        return self._chess_board.get_piece_name(pos)

    def get_piece_moves(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        return self._chess_board.get_piece_moves(pos)

    def is_check(self):
        return self._chess_board.is_check()

    def move_piece(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> None:
        self._game_status.append([src_pos, dst_pos,
                                  self._chess_board.get_piece(src_pos), self._chess_board.get_piece(dst_pos)])
        self._chess_board.move_piece(src_pos, dst_pos)
        self._chess_board.promote_pawn(self._chess_board.get_piece(dst_pos))
        self._chess_board.change_turn()

    def undo_move(self):
        if len(self._game_status) > 0:
            self._chess_board.change_turn()
            [src_pos, dst_pos, src_pic, dst_pic] = self._game_status.pop()
            self._chess_board.undo_move(src_pos, dst_pos, src_pic, dst_pic)
            self.board_change = True
            self.selected_square = ()
            self.available_moves = []

    def get_piece_color(self, pos: tuple[int, int]) -> str:
        return 'white' if self._chess_board.is_white_piece(pos) else 'black'

    def is_game_end(self) -> bool:
        return self._chess_board.is_game_end()

    def game_end_status(self) -> str:
        return self._chess_board.game_end_status()

    def on_board_click(self, pos: tuple[int, int]):
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
