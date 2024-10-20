from board import *
from player import *

# Assuming the Board class has been defined as you shared before
board1 = Board(19, 19, 5)  # Creating a 19x19 board with win condition of 5 in a row

# Marking X positions
x_positions = [(0, 0), (0, 1), (0, 2), (1,0), (2,0), (3,0), (1, 2), (2, 4)]
for x_pos in x_positions:
    board1.mark_cell("X", x_pos[0], x_pos[1])

# Marking O positions
o_positions = [(4,0), (1, 1), (2, 1), (3, 1), (2, 2), (3, 3), (0, 3), (1, 3)] #(0,4) is winning move
for o_pos in o_positions:
    board1.mark_cell("O", o_pos[0], o_pos[1])
      
# print(board1.get_potential_moves())
    
ai = AI_Player("O", "O", difficulty=2)


# print(board1.get_potential_moves())


move = ai.make_move(board1)
print(move)
board1.mark_cell("O", *move)    
print()



