import pygame as pg
from chess_engine import ChessEngine
from typing import List, Tuple
import os
import threading
from const import *

pg.font.init()
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BOARD = pg.transform.scale(pg.image.load(os.path.join("Assets", "board.png")), (WIN_WIDTH, WIN_HEIGHT))
FONT = pg.font.SysFont("Helvitca", 90, bold=True)
PIECE_IMAGE = {}

KEY_COLOR_MAPPING = {
    pg.K_0: "image",
    pg.K_1: LIME_GREEN,
    pg.K_2: DARK_GRAY,
    pg.K_3: GREEN_GRAY,
    pg.K_4: BLUE_GRAY,
    pg.K_5: RED,
    pg.K_6: BROWN,
    pg.K_7: OLIVE,
    pg.K_8: DARK_PURPLE,
    pg.K_9: ORANGE
}


def load_screen():
    """
    Load the initial screen settings, set the window caption and icon, and load piece images.
    This function initializes the Pygame display settings, sets the window caption and icon,
    and loads the images of chess pieces.
    """
    pg.display.set_caption("Chess")
    pg.display.set_icon(pg.image.load(os.path.join('Assets', 'chess_icon.png')))
    for p in PIECES:
        PIECE_IMAGE[p] = pg.transform.scale(pg.image.load(os.path.join("Assets", p + ".png")), SQ_SIZE)


def draw_pieces(chess_engine: ChessEngine):
    """
    Draw chess pieces on the game window.
    Args:
        chess_engine (ChessEngine): The instance of the ChessEngine class representing the game state.
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece_name = chess_engine.get_piece_name((row, col))
            if piece_name is not None:
                color = chess_engine.get_piece_color((row, col))
                rect = pg.Rect(col * SQ_SIZE[0], row * SQ_SIZE[1], SQ_SIZE[0], SQ_SIZE[1])
                WIN.blit(PIECE_IMAGE[color + "_" + piece_name], rect)


def highlight_selected_square(square_selected: Tuple[int, int]):
    """
    Highlight the currently selected square on the game window.
    Args:
        square_selected (Tuple[int, int]): The coordinates (row, col) of the selected square.
    """
    surface = pg.Surface(SQ_SIZE)
    surface.set_alpha(60)
    surface.fill(BLUE)
    WIN.blit(surface, (square_selected[1] * SQ_SIZE[0], square_selected[0] * SQ_SIZE[1]))


def highlight_moves_squares(valid_moves: List[Tuple[int, int]]):
    """
    Highlight the squares representing valid moves on the game window.
    Args:
        valid_moves (List[Tuple[int, int]]): List of coordinates (row, col) representing valid moves.
    """
    surface = pg.Surface(SQ_SIZE)
    surface.set_alpha(120)
    surface.fill(GREEN)
    for move in valid_moves:
        WIN.blit(surface, (move[1] * SQ_SIZE[0], move[0] * SQ_SIZE[1]))


def draw_board(selected_color: tuple | str):
    if selected_color == "image":
        WIN.blit(BOARD, (0, 0))
    else:
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                square_color = selected_color if (r+c) % 2 == 1 else WHITE
                pg.draw.rect(WIN, square_color, pg.Rect(c * SQ_SIZE[0], r * SQ_SIZE[1], SQ_SIZE[0], SQ_SIZE[1]))


def draw_window(chess_engine: ChessEngine, selected_color: tuple | str):
    """
    Draw the entire game window, including the chessboard and pieces.
    Args:
        chess_engine (ChessEngine): The instance of the ChessEngine class representing the game state.
        selected_color (tuple | str): the board color
    """
    draw_board(selected_color)
    if chess_engine.selected_square != ():
        highlight_selected_square(chess_engine.selected_square)
        if chess_engine.available_moves:
            highlight_moves_squares(chess_engine.available_moves)
    draw_pieces(chess_engine)
    pg.display.flip()


def draw_text(text):
    """
    Draw text on the game window.
    Args:
        text (str): The text to be displayed on the window.
    """
    text_render = FONT.render(text, True, GREEN, BLUE)
    WIN.blit(text_render, (WIN_WIDTH//2 - text_render.get_width()//2, WIN_HEIGHT//2 - text_render.get_height()//2))
    pg.display.flip()


def main():
    """
    The main loop of the chess game.
    This function initializes the game, handles user input, and continuously updates the game window.
    """
    load_screen()
    chess_engine = ChessEngine(is_human_white=True)
    clock = pg.time.Clock()
    run = True

    is_game_end = False
    game_end_time = 0

    is_check = False
    game_check_time = 0
    selected_color = KEY_COLOR_MAPPING.get(pg.K_0)

    while run:
        clock.tick(FPS)
        if not is_game_end and chess_engine.is_ai_turn() and not chess_engine.is_ai_running():
            thread_ai_move = threading.Thread(target=ChessEngine.move_ai, args=(chess_engine,), daemon=True)
            thread_ai_move.start()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif is_game_end:
                if pg.time.get_ticks() - game_end_time > 10000:
                    run = False
                    break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    chess_engine.undo_move()

                elif event.key == pg.K_EQUALS:
                    depth = chess_engine.increase_depth()
                    draw_text(f"{depth}")

                elif event.key == pg.K_MINUS:
                    depth = chess_engine.decrease_depth()
                    draw_text(f"{depth}")

                elif event.key in KEY_COLOR_MAPPING:
                    selected_color = KEY_COLOR_MAPPING[event.key]
                    chess_engine.board_change = True

            elif not chess_engine.is_ai_turn() and event.type == pg.MOUSEBUTTONDOWN:
                chess_engine.on_board_click((event.pos[1] // SQ_SIZE[1], event.pos[0] // SQ_SIZE[0]))

        if is_check:
            if pg.time.get_ticks() - game_check_time > 1000:
                is_check = False
                chess_engine.board_change = True
            elif chess_engine.board_change or chess_engine.moving_update:
                is_check = False

        if chess_engine.board_change:
            draw_window(chess_engine, selected_color)
            chess_engine.board_change = False

        if chess_engine.moving_update:
            if chess_engine.is_game_end():
                draw_text(chess_engine.game_end_status())
                game_end_time = pg.time.get_ticks()
                is_game_end = True
            elif chess_engine.is_check():
                draw_text(f"{chess_engine.get_turn()} check")
                is_check = True
                game_check_time = pg.time.get_ticks()
        chess_engine.moving_update = False
    pg.quit()


if __name__ == "__main__":
    main()
