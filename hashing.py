import random

def random_int():
    min = 2
    max = pow(2,64)
    return random.randint(min, max)


def index_of(symbol):
    if symbol == "X":
        return 1
    elif symbol == "O":
        return 2
    else:
        return 0
    

def initTable(rows,cols):
    zobrist_table = [[[random_int() for k in range(3)] for j in range(cols)] for i in range(rows)]
    return zobrist_table

def compute_hash(board, zobrist_table):
    h = 0
    rows = len(board)
    cols = len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != 0:
                piece = index_of(board[i][j])
                h ^= zobrist_table[i][j][piece]
    return h


def make_move_and_update_hash(self, board, move, symbol):
    row, col = move
    piece = symbol

    # XOR out the current state of the cell (if not empty)
    if board.board[row][col] != 0:
        self.current_hash ^= board.zobrist_table[row][col][index_of(board.board[row][col])]

    # Make the move
    board.board[row][col] = piece

    # XOR in the new state
    self.current_hash ^= board.zobrist_table[row][col][index_of(piece)]

def undo_move_and_update_hash(self, board, move):
    row, col = move
    piece = board.board[row][col]

    # XOR out the current piece
    self.current_hash ^= board.zobrist_table[row][col][index_of(piece)]

    # Set cell back to empty
    board.board[row][col] = 0

    # XOR in the empty space
    self.current_hash ^= board.zobrist_table[row][col][index_of(0)]

