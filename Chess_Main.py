from tabulate import tabulate
from collections import Counter

move_dict = []
move_count = 0
position_dict = []


color_codes = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
    "black": "\033[30m",
    "reset": "\033[0m"
}


class Chess_Tile:
    def __init__(self, x, y, placed_piece=False, piece=None):
        self.x = x
        self.y = y
        self.placed_piece = placed_piece
        self.piece = piece

    def __str__(self):
        if self.placed_piece:
            return f"{self.x}, {self.y}, Piece: {self.piece.name}"
        else:
            return f"{self.x}, {self.y}, Piece: None"

    def place_piece(self, piece, previous_position=None, castling=False, board=False):
        
        if piece is None:
            print("No piece provided!")
            return

        
        print(f"Placing {piece.name if piece else 'None'} on tile ({self.x}, {self.y})")
        
        if previous_position and previous_position.piece is None:
            previous_position = piece.tile

        

        if previous_position and previous_position.piece:
            if castling:
                move_possible = True
            else:
                move_possible = previous_position.piece.Move(self, Chess_Board)   
            if move_possible:
                if not return_num_of_results(move_possible):
                    if self.placed_piece:
                        move_dict.append((move_count+1, piece.name))
                    elif previous_position.piece and previous_position.piece.name[-1] == "n":
                        move_dict.append((move_count+1, piece.name))
                    previous_position.placed_piece = False
                    previous_position.piece = None
                    self.placed_piece = True
                    self.piece = piece
                    if self.piece.name in ["White Rook", "Black Rook", "White King", "Black King"]:
                        self.piece.has_moved = True
                    if self.piece.name in ["White Pawn", "Black Pawn"] and abs(self.x - previous_position.x) == 2:
                        self.piece.en_passant_possible = True
                    piece.x, piece.y = self.x, self.y
                    piece.tile = self
                else:
                    direction = -1 if "White" in previous_position.piece.name else 1
                    previous_position.placed_piece = False
                    previous_position.piece = None
                    board.board[self.x-direction][self.y].placed_piece = False
                    board.board[self.x-direction][self.y].piece = None
                    self.placed_piece = True
                    self.piece = piece
                position_dict.append(create_board_save(board))
        else:
            self.placed_piece = True
            self.piece = piece
            piece.tile = self


class King:
    def __init__(self, x, y, name, tile, in_check=False):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.in_check = in_check
        self.tile.place_piece(self, self.tile)
        self.has_moved = False

    def __str__(self):
        return f"{self.x}, {self.y}, In Check: {self.in_check}, King"
    
    def Check(self, in_check):
        self.in_check = in_check

    def Move(self, tile, board):
        x = tile.x
        y = tile.y
        if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
            if get_pieces_attacking_square(board.board[x][y], board, self.name[0:4]) == []:
                return True
        return False


class Rook:
    def __init__(self, x, y, name, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.tile.place_piece(self, self.tile)
        self.has_moved = False

    def __str__(self):
        return f"{self.x}, {self.y}, Rook"

    def Move(self, tile, board):
        x, y = tile.x, tile.y
        
        if self.x == x:
            values = get_values_between(self.y, y)
            for j in values:
                if board.board[x][j].placed_piece:
                    return False

        elif self.y == y:
            values = get_values_between(self.x, x)
            for i in values:
                if board.board[i][y].placed_piece:
                    return False

        else:
            return False

        return True

    def update_check(self, king_tile, board):
        x, y = king_tile.x, king_tile.y

        if self.x == x:
            values = get_values_between(self.y, y)
            for j in values:
                if board.get_piece_at(x, j) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
        elif self.y == y:
            values = get_values_between(self.x, x)
            for i in values:
                if board.get_piece_at(i, y) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
        
        return False


class Bishop:
    def __init__(self, x, y, name, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.tile.place_piece(self, self.tile)

    def __str__(self):
        return f"{self.x}, {self.y}, Bishop"

    def Move(self, tile, board):
        x, y = tile.x, tile.y

        if abs(self.x - x) == abs(self.y - y):
            values_x= get_values_between(self.x, x)
            values_y = get_values_between(self.y, y)
            for i, j in zip(values_x, values_y):
                if board.board[i][j].placed_piece:
                    return False
            return True
        
        else:
            return False

    def update_check(self, king_tile, board):
        x, y = king_tile.x, king_tile.y

        if abs(self.x - x) == abs(self.y - y):
            values_x= get_values_between(self.x, x)
            values_y = get_values_between(self.y, y)
            for i, j in zip(values_x, values_y):
                if board.get_piece_at(i, j) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
        
        else:
            return False


class Knight:
    def __init__(self, x, y, name, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.tile.place_piece(self, self.tile)

    def __str__(self):
        return f"{self.x}, {self.y}, Knight"

    def Move(self, tile, board):
        x, y = tile.x, tile.y
        if tile.piece not in ["White Knight", "Black Knight"]:
            if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
                return True
        else:
            return False

    def update_check(self, king_tile, board):
        x, y = king_tile.x, king_tile.y
        if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
            king_tile.piece.Check(True)
            return True
        
        return False


class Queen:
    def __init__(self, x, y, name, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.tile.place_piece(self, self.tile)

    def __str__(self):
        return f"{self.x}, {self.y}, Queen"

    def Move(self, tile, board):
        x, y = tile.x, tile.y
        
        if self.x == x:
            values = get_values_between(self.y, y)
            for j in values:
                if board.board[x][j].placed_piece:
                    return False

        elif self.y == y:
            values = get_values_between(self.x, x)
            for i in values:
                if board.board[i][y].placed_piece:
                    return False
        
        elif abs(self.x - x) == abs(self.y - y):
            values_x= get_values_between(self.x, x)
            values_y = get_values_between(self.y, y)
            for i, j in zip(values_x, values_y):
                if board.board[i][j].placed_piece:
                    return False
            return True
        
        else:
            return False
        
        return True

    def update_check(self, king_tile, board):
        x, y = king_tile.x, king_tile.y

        if self.x == x:
            values = get_values_between(self.y, y)
            for j in values:
                if board.get_piece_at(x, j) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
        elif self.y == y:
            values = get_values_between(self.x, x)
            for i in values:
                if board.get_piece_at(i, y) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
        elif abs(self.x - x) == abs(self.y - y):
            values_x= get_values_between(self.x, x)
            values_y = get_values_between(self.y, y)
            for i, j in zip(values_x, values_y):
                if board.get_piece_at(i, j) is not None:
                    return False
            king_tile.piece.Check(True)
            return True
           
        return False


chess_pieces_promotion = {
    "White Rook": Rook,
    "White Knight": Knight,
    "White Bishop": Bishop,
    "White Queen": Queen,
    "Black Rook": Rook,
    "Black Knight": Knight,
    "Black Bishop": Bishop,
    "Black Queen": Queen,
}


class Pawn:
    def __init__(self, x, y, name, tile):
        self.x = x
        self.y = y
        self.tile = tile
        self.name = name
        self.tile.place_piece(self, self.tile)
        self.en_passant_possible = False

    def __str__(self):
        return f"{self.x}, {self.y}"

    def Move(self, tile, board):
        x, y = tile.x, tile.y
        direction = -1 if "White" in self.name else 1
        if self.y == y and board.board[x][y].placed_piece:
            return False
        if self.x + direction == x and self.y == y:
            return True
        if self.x + 2 * direction == x and self.y == y and (self.x == 1 or self.x == 6):
            return True
        if abs(self.y - y) == 1 and self.x + direction == x:
            if tile.placed_piece:
                return True
            elif Chess_Board.board[tile.x - direction][y].piece.name in ["White Pawn", "Black Pawn"] and Chess_Board.board[tile.x - direction][y].piece.en_passant_possible:
                return True, True
        return False

    def update_check(self, king_tile, board):
        x, y = king_tile.x, king_tile.y
        direction = -1 if "White" in self.name else 1
        if abs(self.y - y) == 1 and self.x + direction == x and king_tile.placed_piece:
            king_tile.piece.Check(True)
            return True
        return False

    def promote(self, promotion_piece, board):
        piece = chess_pieces_promotion[promotion_piece]
        board[self.x][self.y].piece = piece(self.x, self.y, promotion_piece, board[self.x][self.y])


class ChessBoard:
    def __init__(self):
        self.board =  setup_board(create_board())

    def get_piece_at(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            tile = self.board[x][y]
            return tile.piece if tile.placed_piece else None
        return None


def create_board():
    board = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(Chess_Tile(i, j))
        board.append(row)
    return board


def setup_board(board):
    Rook(0, 0, "Black Rook", board[0][0])
    Knight(0, 1, "Black Knight", board[0][1])
    Bishop(0, 2, "Black Bishop", board[0][2])
    Queen(0, 3, "Black Queen", board[0][3])
    King(0, 4, "Black King", board[0][4])
    Bishop(0, 5, "Black Bishop", board[0][5])
    Knight(0, 6, "Black Knight", board[0][6])
    Rook(0, 7, "Black Rook", board[0][7])
    
    for col in range(8):
         Pawn(1, col, "Black Pawn", board[1][col])
    
    for col in range(8):
         Pawn(6, col, "White Pawn", board[6][col])
    
    Rook(7, 0, "White Rook", board[7][0])
    Knight(7, 1, "White Knight", board[7][1])
    Bishop(7, 2, "White Bishop", board[7][2])
    Queen(7, 3, "White Queen", board[7][3])
    King(7, 4, "White King", board[7][4])
    Bishop(7, 5, "White Bishop", board[7][5])
    Knight(7, 6, "White Knight", board[7][6])
    Rook(7, 7, "White Rook", board[7][7])
    return board


chess_pieces = {
    "White Rook": "♖",
    "White Knight": "♘",
    "White Bishop": "♗",
    "White Queen": "♕",
    "White King": "♔",
    "White Pawn": "♙",
    "Black Rook": "♜",
    "Black Knight": "♞",
    "Black Bishop": "♝",
    "Black Queen": "♛",
    "Black King": "♚",
    "Black Pawn": "♟"
}


def display_board(board):
    display = []
    for row in board:
        display_row = []
        for tile in row:
            if tile.placed_piece and tile.piece:
                if tile.piece.name[0] == "W":
                    display_row.append(f"{color_codes['white']}{chess_pieces[tile.piece.name]}n{color_codes['reset']}")
                else:
                    display_row.append(f"{color_codes['black']}{chess_pieces[tile.piece.name]}n{color_codes['reset']}")
            else:
                display_row.append("")
        display.append(display_row)
    print(tabulate(display, tablefmt="fancy_grid"))
    return display


def get_values_between(start, end):
    if start < end:
        return list(range(start + 1, end))
    return list(range(start - 1, end, -1))


def check_50_move_rule():
    if len(move_dict) > 0:
        start = move_dict[-1][0]
    else:
        start = 0
    if move_count - start >= 50:
        return True
    return False


def get_pieces_attacking_square(tile, board, color_not_attacking):
    pieces = []
    for i in range(8):
        for j in range(8):
            piece = board.get_piece_at(i, j)
            if piece and piece.name in ["White Pawn", "Black Pawn"]:
                if piece.name == "White Pawn":
                    if abs(j - tile.y) == 1 and abs(tile.x - i) == 1:
                        if color_not_attacking not in piece.name:
                            pieces.append(piece)

                elif piece.name == "Black Pawn":
                    if abs(j - tile.y) == 1 and abs(tile.x - i) == 1:
                        if color_not_attacking not in piece.name:
                            pieces.append(piece)
        
            elif piece:
                if piece.Move(tile, board):
                    if color_not_attacking not in piece.name:
                        pieces.append(piece)

    return pieces


king_moves = {
    0: (-1, -1),
    1: (-1, 0),
    2: (-1, 1),
    3: (0, -1),
    4: (0, 1),
    5: (1, -1),
    6: (1, 0),
    7: (1, 1)
}


def check_checkmate(king_tile_x,king_tile_y, color_not_checking, board):
    for x in range(8):
        if 0 <= king_tile_x + king_moves[x][0] < 8 and 0 <= king_tile_y + king_moves[x][1] < 8:
            if board.get_piece_at(king_tile_x + king_moves[x][0], king_tile_y + king_moves[x][1]):
                continue
            elif not get_pieces_attacking_square(board.board[king_tile_x + king_moves[x][0]][king_tile_y + king_moves[x][1]], board, color_not_checking):
                return False
            else:
                continue
    
    pieces = get_pieces_attacking_square(board.board[king_tile_x][king_tile_y], board, color_not_checking)
    for piece in pieces:
        for x in range(8):
            for y in range(8):
                if board.board[x][y].piece and board.board[x][y].piece.Move(board.board[piece.x][piece.y], board):
                    return False            

    for piece in pieces:
        if piece not in ["White Knight", "Black Knight", "White Pawn", "Black Pawn"]:
            tiles_to_block = zip(get_values_between(piece.x, king_tile_x), get_values_between(piece.y, king_tile_y))
            tiles_to_block = list(tiles_to_block)
            for x in tiles_to_block:
                if not get_pieces_attacking_square(board.board[x[0]][x[1]], board, color_not_checking):
                    return False

    if board.board[king_tile_x][king_tile_y].piece.in_check:
        return True
    else:
        return False


def check_stalemate(board, color_checking):
    pieces = [y.piece for x in board.board for y in x if y.piece and y.piece.name[0] == color_checking[0]]
    for x in range(8):
        for y in range(8):
            for piece in pieces:
                if piece.Move(board.board[x][y], board):
                    return False
    
    return True


def castle(king_tile, rook_tile, board):
    if king_tile.piece.has_moved or rook_tile.piece.has_moved or king_tile.piece.in_check or king_tile.x != rook_tile.x:
        return False
    sqaures_passing_through = len(get_values_between(king_tile.y, rook_tile.y))
    if sqaures_passing_through not in [2, 3]:
        return False
    sqaure_in_between = zip([king_tile.x]*sqaures_passing_through, get_values_between(king_tile.y, rook_tile.y))
    sqaure_in_between_list = list(sqaure_in_between)
    for x in sqaure_in_between_list:
        if board.get_piece_at(x[0], x[1]):
            return False
    if king_tile.y < rook_tile.y:
        Chess_Board.board[king_tile.x][king_tile.y+2].place_piece(king_tile.piece, king_tile, True)
        Chess_Board.board[rook_tile.x][rook_tile.y-2].place_piece(rook_tile.piece, rook_tile, True)
        rook_tile.place_piece(rook_tile.piece, board.board[king_tile.x][king_tile.y-1], True)
    else:
        Chess_Board.board[king_tile.x][king_tile.y-2].place_piece(king_tile.piece, king_tile, True)
        Chess_Board.board[rook_tile.x][rook_tile.y+3].place_piece(rook_tile.piece, rook_tile, True)
    return True


def return_num_of_results(result):
    if isinstance(result, tuple) or isinstance(result, list):
        if len(result) == 2:
            return True
        elif len(result) == 1:
            return False
    else:
        return False


def create_board_save(board):
    return "\n".join(["".join(board.board[x][y].piece.name if board.board[x][y].piece else "." for y in range(8)) for x in range(8)])


def threefold_checker(lst):
    counts = Counter(lst)
    return any(count >= 3 for count in counts.values())


Chess_Board = ChessBoard()
display_board(Chess_Board.board)

'''Chess_Board.board[4][4].place_piece(Chess_Board.board[6][4].piece, Chess_Board.board[6][4], board=Chess_Board)
move_count += 1
Chess_Board.board[4][2].place_piece(Chess_Board.board[7][5].piece, Chess_Board.board[7][5], board=Chess_Board)
move_count += 1'''
#Example of how to move

display_board(Chess_Board.board)