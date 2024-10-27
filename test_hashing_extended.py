from board import *
from hashing import *

board = Board(15, 15, 5)
print(board.current_hash)
board.mark_cell("X", (8,8))
print(board.current_hash)
board.mark_cell("O", (9,9))
print(board.current_hash)


board.make_move_and_update_hash((2,7), "X")
print(board.current_hash)

board.undo_move_and_update_hash((2,7))
print(board.current_hash)
