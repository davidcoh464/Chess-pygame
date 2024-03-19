import random
import threading
from chess_board import ChessBoard
from chess_ai import Evaluation


MAX_INT32 = 2147483647


class Minimax:
    def __init__(self, board: ChessBoard, max_depth: int, stop_event: threading.Event):
        self._stop_event = stop_event
        self._board = board
        self._game_status = []
        self._max_depth = max_depth
        self._counter = 0
        self._evaluation = Evaluation(board)
        self.best_move = None

    def find_best_move(self):
        self._counter = 0
        self._minimax(depth=self._max_depth, maximizing_player=self._board.is_white_turn(),
                      alpha=-MAX_INT32, beta=MAX_INT32)
        print(self._counter)

    def _minimax(self, depth: int, maximizing_player: bool, alpha, beta):
        self._counter += 1
        if self._stop_event.is_set():
            return 0

        if depth <= 0:
            return self._evaluation.evaluate_board()

        all_moves = self._board.get_all_moves()
        if len(all_moves) == 0:
            return self._evaluation.evaluate_board()

        random.shuffle(all_moves)
        if maximizing_player:
            for move in all_moves:
                self.move_piece(move)
                score = self._minimax(depth - 1, False, alpha, beta)
                self.undo_move()
                if score > alpha:
                    alpha = score
                    if depth == self._max_depth:
                        self.best_move = move
                if alpha >= beta:
                    break
            return alpha
        else:
            for move in all_moves:
                self.move_piece(move)
                score = self._minimax(depth - 1, True, alpha, beta)
                self.undo_move()
                if score < beta:
                    beta = score
                    if depth == self._max_depth:
                        self.best_move = move
                if alpha >= beta:
                    break
            return beta

    def move_piece(self, move):
        self._game_status.append([move[0], move[1], self._board.get_piece(move[0]), self._board.get_piece(move[1])])
        self._board.move_piece(move[0], move[1])
        self._board.promote_pawn(move[1])
        self._board.change_turn()

    def undo_move(self):
        self._board.change_turn()
        [src_pos, dst_pos, src_pic, dst_pic] = self._game_status.pop()
        self._board.undo_move(src_pos, dst_pos, src_pic, dst_pic)
