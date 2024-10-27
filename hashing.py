import random

def index_of(symbol):
    if symbol == "X":
        return 1
    elif symbol == "O":
        return 2
    else:
        return 0

def initTable(rows, cols):
    """Initialize the Zobrist table with random 64-bit integers."""
    zobrist_table = [
        [
            [random.getrandbits(64) for _ in range(3)]  # For symbols: 0, "X", "O"
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]
    return zobrist_table

def compute_hash(board, zobrist_table):
    """Compute the Zobrist hash for the current board state."""
    h = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = index_of(board[i][j])
            if piece != 0:
                h ^= zobrist_table[i][j][piece]
    return h
