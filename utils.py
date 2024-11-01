from random import *
import numpy as np


def create_pattern_dict() -> dict[tuple[int], int]:
    """Genererar en dictionary innehållandes olika mönster av symboler och dess korresponderande värde.

    Returns:
        dict[tuple[int], int]: Dictionary med mönster som nyckel och dess värde som värde.
    """
    PLAYER = 1
    OPPONENT = -1
    pattern_dict = {}
    for x in (PLAYER, OPPONENT):
        y = -x
        # long_5
        pattern_dict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        pattern_dict[(0, x, x, x, x, 0)] = 100000 * x
        pattern_dict[(0, x, x, x, 0, x, 0)] = 100000 * x
        pattern_dict[(0, x, 0, x, x, x, 0)] = 100000 * x
        pattern_dict[(0, x, x, 0, x, x, 0)] = 100000 * x
        # go_4
        pattern_dict[(0, x, x, x, x, y)] = 10000 * x
        pattern_dict[(y, x, x, x, x, 0)] = 10000 * x
        # dead_4
        pattern_dict[(y, x, x, x, x, y)] = -10 * x
        # live_3
        pattern_dict[(0, x, x, x, 0)] = 1000 * x
        pattern_dict[(0, x, 0, x, x, 0)] = 1000 * x
        pattern_dict[(0, x, x, 0, x, 0)] = 1000 * x
        # sleep_3
        pattern_dict[(0, 0, x, x, x, y)] = 100 * x
        pattern_dict[(y, x, x, x, 0, 0)] = 100 * x
        pattern_dict[(0, x, 0, x, x, y)] = 100 * x
        pattern_dict[(y, x, x, 0, x, 0)] = 100 * x
        pattern_dict[(0, x, x, 0, x, y)] = 100 * x
        pattern_dict[(y, x, 0, x, x, 0)] = 100 * x
        pattern_dict[(x, 0, 0, x, x)] = 100 * x
        pattern_dict[(x, x, 0, 0, x)] = 100 * x
        pattern_dict[(x, 0, x, 0, x)] = 100 * x
        pattern_dict[(y, 0, x, x, x, 0, y)] = 100 * x
        # dead_3
        pattern_dict[(y, x, x, x, y)] = -10 * x
        # live_2
        pattern_dict[(0, 0, x, x, 0)] = 100 * x
        pattern_dict[(0, x, x, 0, 0)] = 100 * x
        pattern_dict[(0, x, 0, x, 0)] = 100 * x
        pattern_dict[(0, x, 0, 0, x, 0)] = 100 * x
        # sleep_2
        pattern_dict[(0, 0, 0, x, x, y)] = 10 * x
        pattern_dict[(y, x, x, 0, 0, 0)] = 10 * x
        pattern_dict[(0, 0, x, 0, x, y)] = 10 * x
        pattern_dict[(y, x, 0, x, 0, 0)] = 10 * x
        pattern_dict[(0, x, 0, 0, x, y)] = 10 * x
        pattern_dict[(y, x, 0, 0, x, 0)] = 10 * x
        pattern_dict[(x, 0, 0, 0, x)] = 10 * x
        pattern_dict[(y, 0, x, 0, x, 0, y)] = 10 * x
        pattern_dict[(y, 0, x, x, 0, 0, y)] = 10 * x
        pattern_dict[(y, 0, 0, x, x, 0, y)] = 10 * x
        # dead_2
        pattern_dict[(y, x, x, y)] = -10 * x

    return pattern_dict


def index_of(symbol: str) -> int:
    """Returnerar ett index givet en symbol på brädet (X, O, ").

    Args:
        symbol (str): Spelarens symbol, alternativt ".

    Returns:
        int: Heltalet som symbolen mappar till.
    """
    if symbol == "X":
        return 1
    elif symbol == "O":
        return -1
    else:
        return 0


def random_int() -> int:
    """Genererar ett slumpmässigt heltal mellan ett min och max tal.

    Returns:
        int: Slumpmässigt heltal.
    """
    min = 0
    max = pow(2, 64)
    return randint(min, max)


def init_table(rows: int, cols: int) -> list:
    """Initierar en zobristhashtabell för ett spelbräde med de specificerade dimensionerna (rad, kolumn).

    Args:
        rows (int): Antalet rader på spelbrädet.
        cols (int): Antalet kolumner på spelbrädet

    Returns:
        list: _description_
    """
    zobrist_table = [
        [[random_int() for k in range(3)] for j in range(rows)] for i in range(cols)
    ]
    return zobrist_table


def compute_hash(board: np.ndarray, zobrist_table: list) -> int:
    """Beräknar zobristhashen för ett givet stadie av spelbrädet.

    Args:
        board (np.ndarray): 2D array representerande brädet.
        zobrist_table (list): Zobristhashtabell med randomiserade heltal.

    Returns:
        int: Zobristhashet för brädet.
    """
    hash = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = index_of(board[i][j])
            hash ^= zobrist_table[i][j][piece]
    return hash
