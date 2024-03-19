import threading
from chess_engine import ChessBoard
from typing import Optional, Tuple
from copy import deepcopy
from chess_ai import Minimax


class ChessAI:
    def __init__(self, stop_event: threading.Event):
        self._stop_event = stop_event
        self.best_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self._max_depth = 3

    def find_best_move(self, board: ChessBoard):
        board = deepcopy(board)
        self.best_move = None
        minimax = Minimax(board, self._max_depth, self._stop_event)
        minimax.find_best_move()
        self.best_move = minimax.best_move
