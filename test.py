import cProfile
import pstats
from player import AI_Player
from board import Board
from graphics import Graphics
from game import Game  # Assuming your Game class is in game.py

# def run_profiled_game():
#     # Initialize game components
#     board = Board(rows=15, cols=15, to_win=5)
#     graphics = Graphics(board)
#     player1 = AI_Player(symbol="X", max_depth=3)
#     player2 = AI_Player(symbol="O", max_depth=3)  # Assuming AI vs AI for profiling
#     game = Game(board, graphics, player1, player2)
    
#     # Create a profiler instance
#     profiler = cProfile.Profile()
#     profiler.enable()  # Start profiling
    
#     game.play()  # Run the game
    
#     profiler.disable()  # Stop profiling
    
#     # Save profiling data to a file
#     profiler.dump_stats("profile_output.prof")
    
#     # Optionally, print profiling results to the console
#     stats = pstats.Stats(profiler).strip_dirs().sort_stats("cumtime")
#     stats.print_stats(20)  # Adjust the number to see more or fewer lines

# if __name__ == "__main__":
#     run_profiled_game()



def test_hash_consistency():
    board = Board(rows=5, cols=5, to_win=4)
    original_hash = board.current_hash
    move = (2, 2)
    symbol = "X"
    board.make_move_and_update_hash(move, symbol)
    assert board.current_hash != original_hash, "Hash should change after move."
    board.undo_move_and_update_hash(move)
    assert board.current_hash == original_hash, "Hash should revert after undo."


