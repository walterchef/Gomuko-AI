from random import *
import numpy as np

def index_of(symbol: str) -> int:
    """Map symbols to indices for Zobrist hashing."""
    if symbol == "X":
        return 0
    elif symbol == "O":
        return 1
    else:
        return -1  # Empty


def randomInt():
    min = 0
    max = pow(2, 64)
    return randint(min, max)

def initTable(rows: int, cols: int) -> list:
    ZobristTable = [[[randomInt() for k in range(2)] for j in range(rows)] for i in range(cols)]
    return ZobristTable


def compute_hash(board: np.ndarray, zobrist_table: list) -> int:
    """Compute the Zobrist hash for the current board state."""
    h = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = index_of(board[i][j])
            if piece != -1:
                h ^= zobrist_table[i][j][piece]
    return h


test = initTable(5,5)
print(test)