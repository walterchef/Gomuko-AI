# tests/test_hashing_methods.py
import unittest
from board import Board
from hashing import initTable, compute_hash, index_of
import copy
import numpy as np

class TestHashingMethods(unittest.TestCase):
    def setUp(self):
        """Initialize a Board instance with a deterministic Zobrist table."""
        self.rows = 5
        self.cols = 5
        self.to_win = 4
        self.seed = 42  # Fixed seed for deterministic Zobrist table
        self.zobrist_table = initTable(self.rows, self.cols, seed=self.seed)
        self.board = Board(rows=self.rows, cols=self.cols, to_win=self.to_win)
        self.board.zobrist_table = self.zobrist_table  # Ensure deterministic table
        self.board.current_hash = compute_hash(self.board.board, self.zobrist_table)
    
    def test_make_move_updates_hash_correctly(self):
        """Test that making a move updates the hash correctly."""
        move = (2, 2)
        symbol = "X"
        expected_hash = self.board.current_hash
        current_symbol = ""
        row, col = move
        
        # XOR out the empty symbol
        expected_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
        
        # XOR in the new symbol
        expected_hash ^= self.zobrist_table[row][col][index_of(symbol)]
        
        # Make the move
        self.board.make_move_and_update_hash(move, symbol)
        
        # Assert hash matches expected
        self.assertEqual(self.board.current_hash, expected_hash, "Hash after making move does not match expected value.")
        
        # Assert board state
        self.assertEqual(self.board.board[row][col], symbol, "Board cell does not contain the correct symbol after move.")
    
    def test_undo_move_updates_hash_correctly(self):
        """Test that undoing a move updates the hash correctly."""
        move = (2, 2)
        symbol = "X"
        row, col = move
        
        # Make the move first
        self.board.make_move_and_update_hash(move, symbol)
        
        # Calculate expected hash after making the move
        expected_hash_after_move = compute_hash(self.board.board, self.zobrist_table)
        
        # Now, undo the move
        self.board.undo_move_and_update_hash(move)
        
        # Calculate expected hash after undoing the move
        expected_hash_after_undo = compute_hash(self.board.board, self.zobrist_table)
        
        # Assert hash matches expected after undo
        self.assertEqual(self.board.current_hash, expected_hash_after_undo, "Hash after undoing move does not match expected value.")
        
        # Assert board state is reverted
        self.assertEqual(self.board.board[row][col], "", "Board cell was not cleared after undoing move.")
    
    def test_make_and_undo_multiple_moves(self):
        """Test that making and undoing multiple moves updates the hash correctly."""
        moves = [((0, 0), "X"), ((1, 1), "O"), ((2, 2), "X")]
        expected_hash = self.board.current_hash
        
        # Make moves
        for move, symbol in moves:
            row, col = move
            current_symbol = ""
            expected_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
            expected_hash ^= self.zobrist_table[row][col][index_of(symbol)]
            self.board.make_move_and_update_hash(move, symbol)
            self.assertEqual(self.board.current_hash, expected_hash, f"Hash mismatch after making move {move}.")
            self.assertEqual(self.board.board[row][col], symbol, f"Board cell {move} incorrect after move.")
        
        # Undo moves
        for move, symbol in reversed(moves):
            row, col = move
            current_symbol = symbol
            expected_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
            expected_hash ^= self.zobrist_table[row][col][index_of("")]
            self.board.undo_move_and_update_hash(move)
            self.assertEqual(self.board.current_hash, expected_hash, f"Hash mismatch after undoing move {move}.")
            self.assertEqual(self.board.board[row][col], "", f"Board cell {move} not cleared after undoing move.")
    
    def test_hash_consistency_after_repeated_moves(self):
        """Test that repeated making and undoing of the same move maintains hash consistency."""
        move = (2, 2)
        symbol = "X"
        for _ in range(10):
            # Make the move
            self.board.make_move_and_update_hash(move, symbol)
            expected_hash = compute_hash(self.board.board, self.zobrist_table)
            self.assertEqual(self.board.current_hash, expected_hash, "Hash mismatch after making move.")
            self.assertEqual(self.board.board[move[0]][move[1]], symbol, "Board cell incorrect after making move.")
            
            # Undo the move
            self.board.undo_move_and_update_hash(move)
            expected_hash = compute_hash(self.board.board, self.zobrist_table)
            self.assertEqual(self.board.current_hash, expected_hash, "Hash mismatch after undoing move.")
            self.assertEqual(self.board.board[move[0]][move[1]], "", "Board cell not cleared after undoing move.")
    
    def test_hash_after_specific_sequence_of_moves(self):
        """Test hash consistency after a specific sequence of moves and undos."""
        sequence = [((0, 0), "X"), ((1, 0), "O"), ((0, 1), "X"), ((1, 1), "O"), ((0, 2), "X")]
        expected_hash = self.board.current_hash
        
        # Apply sequence of moves
        for move, symbol in sequence:
            row, col = move
            current_symbol = ""
            expected_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
            expected_hash ^= self.zobrist_table[row][col][index_of(symbol)]
            self.board.make_move_and_update_hash(move, symbol)
            self.assertEqual(self.board.current_hash, expected_hash, f"Hash mismatch after making move {move}.")
            self.assertEqual(self.board.board[row][col], symbol, f"Board cell {move} incorrect after move.")
        
        # Undo all moves
        for move, symbol in reversed(sequence):
            row, col = move
            current_symbol = symbol
            expected_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
            expected_hash ^= self.zobrist_table[row][col][index_of("")]
            self.board.undo_move_and_update_hash(move)
            self.assertEqual(self.board.current_hash, expected_hash, f"Hash mismatch after undoing move {move}.")
            self.assertEqual(self.board.board[row][col], "", f"Board cell {move} not cleared after undoing move.")
    
    def test_index_of_mapping(self):
        """Test that index_of maps symbols correctly."""
        self.assertEqual(index_of("X"), 1, "index_of failed for symbol 'X'.")
        self.assertEqual(index_of("O"), 2, "index_of failed for symbol 'O'.")
        self.assertEqual(index_of(""), 0, "index_of failed for empty symbol.")
        self.assertEqual(index_of(" "), 0, "index_of failed for space symbol.")
        self.assertEqual(index_of("Invalid"), 0, "index_of failed for invalid symbol.")
    
    def test_marked_cells_count(self):
        """Test that marked_cells correctly counts the number of moves."""
        moves = [((0,0), "X"), ((1,1), "O"), ((2,2), "X")]
        for move, symbol in moves:
            self.board.make_move_and_update_hash(move, symbol)
        self.assertEqual(self.board.marked_cells, len(moves), "marked_cells count incorrect after making moves.")
        
        for _ in moves:
            move, symbol = moves.pop()
            self.board.undo_move_and_update_hash(move)
        self.assertEqual(self.board.marked_cells, 0, "marked_cells count incorrect after undoing all moves.")


    
if __name__ == '__main__':
    unittest.main(verbosity=2)



