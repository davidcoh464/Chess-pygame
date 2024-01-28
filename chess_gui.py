import pygame as pg
from chess_engine import ChessEngine
from typing import List, Tuple
import os
from const import *

pg.font.init()
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BOARD = pg.transform.scale(pg.image.load(os.path.join("Assets", "board.png")), (WIN_WIDTH, WIN_HEIGHT))
WINNER_FONT = pg.font.SysFont("Helvitca", 100, True, False)
PIECE_IMAGE = {}


def load_screen():
    pg.display.set_caption("Chess")
    pg.display.set_icon(pg.image.load(os.path.join('Assets', 'chess_icon.png')))
    for p in PIECES:
        PIECE_IMAGE[p] = pg.transform.scale(pg.image.load(os.path.join("Assets", p + ".png")), SQ_SIZE)


def draw_pieces(chess_engine: ChessEngine):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece_name = chess_engine.get_piece_name((row, col))
            if piece_name is not None:
                color = chess_engine.get_piece_color((row, col))
                rect = pg.Rect(col * SQ_SIZE[0], row * SQ_SIZE[1], SQ_SIZE[0], SQ_SIZE[1])
                WIN.blit(PIECE_IMAGE[color + "_" + piece_name], rect)


def highlight_selected_square(square_selected: Tuple[int, int]):
    surface = pg.Surface(SQ_SIZE)
    surface.set_alpha(60)
    surface.fill(BLUE)
    WIN.blit(surface, (square_selected[1] * SQ_SIZE[0], square_selected[0] * SQ_SIZE[1]))


def highlight_moves_squares(valid_moves: List[Tuple[int, int]]):
    surface = pg.Surface(SQ_SIZE)
    surface.set_alpha(60)
    surface.fill(GREEN)
    for move in valid_moves:
        WIN.blit(surface, (move[1] * SQ_SIZE[0], move[0] * SQ_SIZE[1]))


def draw_window(chess_engine: ChessEngine):
    WIN.blit(BOARD, (0, 0))
    if chess_engine.selected_square != ():
        highlight_selected_square(chess_engine.selected_square)
        if chess_engine.available_moves:
            highlight_moves_squares(chess_engine.available_moves)
    draw_pieces(chess_engine)
    pg.display.flip()


def draw_text(text):
    text_render = WINNER_FONT.render(text, True, GREEN, BLUE)
    WIN.blit(text_render, (WIN_WIDTH//2 - text_render.get_width()//2, WIN_HEIGHT//2 - text_render.get_height()//2))
    pg.display.flip()


def main():
    load_screen()
    chess_engine = ChessEngine()
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    chess_engine.undo_move()
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                chess_engine.on_board_click((location[1] // SQ_SIZE[1], location[0] // SQ_SIZE[0]))

        if chess_engine.board_change:
            draw_window(chess_engine)
            chess_engine.board_change = False
        if chess_engine.moving_update:

            if chess_engine.is_game_end():
                draw_text(chess_engine.game_end_status())
                pg.time.delay(3000)
                run = False
            chess_engine.moving_update = False
    pg.quit()


if __name__ == "__main__":
    main()