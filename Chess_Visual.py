'''import pygame

from Chess_Main import *

pygame.init()

WIDTH, HEIGHT = 1366, 768
width = 600
ROWS, COLS = 8, 8
SQUARE_SIZE = 70
offset_x = 150
offset_y = 100


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

def draw_chess_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (
                offset_x + col * SQUARE_SIZE,
                offset_y + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            ))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("gray")
        draw_chess_board()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()'''

import pygame
import os
import sys
import Chess_Main

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 560, 560
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# --- Colors ---
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)
HIGHLIGHT = (255, 255, 0)

# --- Chess Board State (Backend Data) ---
move_count = 0
Chess_Board = Chess_Main.ChessBoard()
'''Chess_Board.board[4][4].place_piece(Chess_Board.board[6][4].piece, Chess_Board.board[6][4], board=Chess_Board)
move_count += 1
Chess_Board.board[4][2].place_piece(Chess_Board.board[7][5].piece, Chess_Board.board[7][5], board=Chess_Board)
move_count += 1'''

IMAGES = {}
def load_images():
    pieces = [
        'White Pawn', 'White Rook', 'White Knight', 'White Bishop', 'White Queen', 'White King',
        'Black Pawn', 'Black Rook', 'Black Knight', 'Black Bishop', 'Black Queen', 'Black King'
    ]
    for piece in pieces:
        path = os.path.join("C:\\Users\\Rishik\\PycharmProjects\\pythonProject\\images", piece + ".png")
        if os.path.exists(path):
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            print(f"Missing image: {path}")
            sys.exit()

# --- Draw Functions ---
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board):
    # Loop through each tile and, if there's a piece, draw it.
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]  # Chess_Tile object
            # If there is a piece on the tile, draw it.
            if tile != "--" and tile.piece is not None:
                piece_name = tile.piece.name  # e.g. 'White Pawn'
                if piece_name in IMAGES:
                    win.blit(IMAGES[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    print(f"Image for {piece_name} not found.")

def draw_highlight(win, row, col):
    pygame.draw.rect(win, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

# --- Move Logic ---
def move_piece(start, end):
    start_row, start_col = start
    end_row, end_col = end

    start_tile = Chess_Board.board[start_row][start_col]
    target_tile = Chess_Board.board[end_row][end_col]


    if start_tile.piece is None:
        return False

    #print(f"Attempting move for {start_tile.piece} from ({start_row}, {start_col}) to ({end_row}, {end_col})")


    target_tile.place_piece(start_tile.piece, start_tile, board=Chess_Board)
    Chess_Main.display_board(Chess_Board.board)

    #print(f"Move successful for {start_tile.piece} from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    start_tile.piece = None

    return True


# --- Main Game Loop ---
def main():
    clock = pygame.time.Clock()
    selected_square = None
    load_images()
    running = True

    while running:
        clock.tick(60)
        draw_board(WIN)
        draw_pieces(WIN, Chess_Board.board)

        if selected_square:
            draw_highlight(WIN, *selected_square)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                #print(f"Mouse clicked at pixels {mouse_pos} -> board position ({row}, {col})")

                if selected_square:
                    if move_piece(selected_square, (row, col)):
                        selected_square = None
                    else:
                        print("Invalid move. Try again.")
                        selected_square = None
                else:
                    selected_square = (row, col)

    pygame.quit()

if __name__ == "__main__":
    main()

print(Chess_Board.board[4][2])

