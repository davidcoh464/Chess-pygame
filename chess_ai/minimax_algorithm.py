import random
import threading
from chess_board import ChessBoard
from chess_ai import Evaluation

MAX_INT32 = 2147483647


class Minimax:
    """
    Class implementing the Minimax algorithm for decision-making in chess.

    This class uses the Minimax algorithm to determine the best move for a given chess position.
    Args:
        board (ChessBoard): The current chessboard state.
        max_depth (int): The maximum search depth for the Minimax algorithm.
        stop_event (threading.Event): Event to signal the algorithm to stop searching.
    """

    def __init__(self, board: ChessBoard, max_depth: int, stop_event: threading.Event):
        self._stop_event = stop_event
        self._board = board
        self._game_status = []
        self._max_depth = max_depth
        self._counter = 0
        self._evaluation = Evaluation(board)
        self.best_move = None

    def find_best_move(self):
        """
        Find the best move for the current board state using Minimax algorithm.
        """
        self._counter = 0
        # self._minimax(depth=self._max_depth, maximizing_player=self._board.is_white_turn(), alpha=-MAX_INT32, beta=MAX_INT32)
        self._negamax(depth=self._max_depth, color=1 if self._board.is_white_turn() else -1,
                      alpha=-MAX_INT32, beta=MAX_INT32)
        print(self._counter)

    def _minimax(self, depth: int, maximizing_player: bool, alpha, beta):
        """
        Recursive function to perform Minimax search.
        Args:
            depth (int): Current depth of the search.
            maximizing_player (bool): True if maximizing player (White), False if minimizing player (Black).
            alpha (int): The best value that the maximizing player currently can guarantee.
            beta (int): The best value that the minimizing player currently can guarantee.
        Returns:
            int: The evaluated score of the current position.
        """
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

    def _negamax(self, depth: int, color: int, alpha, beta):
        """
        Recursive function implementing the Negamax search algorithm.
        Args:
            depth (int): The current depth of the search.
            color (int): The sign representing the player's turn (+1 for white, -1 for black).
            alpha (int): The best value that the maximizing player currently can guarantee.
            beta (int): The best value that the minimizing player currently can guarantee.
        Returns:
            int: The evaluated score of the current position.
        """
        self._counter += 1

        if self._stop_event.is_set():
            return 0

        if depth <= 0:
            return color * self._evaluation.evaluate_board()

        all_moves = self._board.get_all_moves()
        if len(all_moves) == 0:
            return color * self._evaluation.evaluate_board()

        random.shuffle(all_moves)
        for move in all_moves:
            self.move_piece(move)
            score = -self._negamax(depth - 1, -color, -beta, -alpha)
            self.undo_move()
            if score > alpha:
                alpha = score
                if depth == self._max_depth:
                    self.best_move = move
            if alpha >= beta:
                break
        return alpha

    def move_piece(self, move):
        """
        Make a move on the board.
        Args:
            move: The move to be made.
        """
        self._game_status.append([move[0], move[1], self._board.get_piece(move[0]), self._board.get_piece(move[1])])
        self._board.move_piece(move[0], move[1])
        self._board.promote_pawn(move[1])
        self._board.change_turn()

    def undo_move(self):
        """
        Undo the last move made.
        """
        self._board.change_turn()
        [src_pos, dst_pos, src_pic, dst_pic] = self._game_status.pop()
        self._board.undo_move(src_pos, dst_pos, src_pic, dst_pic)
