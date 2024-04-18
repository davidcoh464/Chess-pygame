import threading
from chess_engine import ChessBoard
from typing import Optional, Tuple
from copy import deepcopy
from chess_ai import Minimax


class ChessAI:
    """
    Class representing an AI player in chess.

    This class utilizes the algorithm to find the best move for the given chess position.
    Args:
        stop_event (threading.Event): Event to signal the algorithm to stop searching.
    """
    def __init__(self, stop_event: threading.Event):
        """
        Initialize the ChessAI instance.
        Args:
            stop_event (threading.Event): Event to signal the algorithm to stop searching.
        """
        self._stop_event = stop_event
        self.best_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.max_depth = 3

    def find_best_move(self, board: ChessBoard):
        """
        Find the best move for the given chess position.
        Args:
            board (ChessBoard): The current chessboard state.
        """
        board = deepcopy(board)
        self.best_move = None
        minimax = Minimax(board, self.max_depth, self._stop_event)
        minimax.find_best_move()
        self.best_move = minimax.best_move
