import pygame
import copy
import sys
import random
from abc import ABC, abstractmethod
from collections import OrderedDict
from board import *


class Player(ABC):

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @abstractmethod
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        pass


class User_Player(Player):
    """Klass för spelare av typen användare."""

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)

    def make_move(self, board: list[list[int]], cell_size: int) -> tuple[int, int]:
        """Returnera användarens drag baserat på vilken cell på spelplanen användaren klickar på.

        Args:
            board (list[list[int]]): Logisk representation av brädet
            cell_size (int): Storleken av en cell i x*y pixlar

        Returns:
            tuple[int, int]: Användarens drag (row, col)
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // cell_size
                    col = pos[0] // cell_size
                    if board.is_valid_move((row, col)):
                        return (row, col)


class AI_Player(Player):
    """Klass för spelare av typen AI."""

    def __init__(
        self, symbol: str, max_depth: int = 2, trans_table_size: int = 100000, debug: bool = False
    ) -> None:  
        super().__init__(symbol)
        self.opponent_symbol = "O" if symbol == "X" else "X"
        self.max_depth = max_depth
        self.debug = debug
        self.transposition_table = OrderedDict()
        self.trans_table_size = trans_table_size

    def make_move(self, board: Board) -> tuple[int, int]:
        """Returnera AI:ns drag baserat på svårighetsgraden.

        Args:
            board (Board): Logisk representation av spelbrädet

        Returns:
            tuple[int, int]: AI:ns drag (row, col)
        """

        if board.marked_cells == 0:
            # First move: choose the center
            move = (board.rows // 2, board.cols // 2)
            return move

        best_score = float("-inf")
        best_move = None

        potential_moves = board.get_potential_moves(self.symbol)

        for move in potential_moves:
            board.make_move_and_update_hash(self.symbol, move)
            score = self.minimax(
                board,
                depth=0,  
                max_depth=self.max_depth,
                alpha=float("-inf"),
                beta=float("inf"),
                maximizing=False,  
            )
            board.undo_move_and_update_hash(move)
                                        
                                    

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is None:
            raise ValueError("AI could not find a valid move!")
        
        return best_move
        
    def minimax(
        self,
        board: Board,
        depth: int,
        max_depth: int,
        alpha: int,
        beta: int,
        maximizing: bool,
    ) -> tuple[int, int]:  
        """Returnera det bästa möjliga draget med minimaxalgoritmen för svårighetsgrad två av AI:n.

        Args:
            board (Board): Logisk representation av brädet
            depth (int): Djup när vi kallar på metoden
            max_depth (int): Maximala djupet algoritmen tillåts evaluera till
            alpha (int): Bästa värde för maximerande spelaren när vi kallar på metoden
            beta (int): Bästa värde för minimerande spelaren när vi kallar på metoden
            maximizing (bool): True om minimerande spelaren kallar på metoden annars False 

        Returns:
            tuple[int, int]: Bästa draget AI:n kan göra (row, col)
        """
        
        if board.current_hash in self.transposition_table:
                stored_score = self.transposition_table[board.current_hash]
                return stored_score

        if depth == max_depth or board.is_terminal():
                board_score = board.evaluate_board(
                    self.symbol, self.opponent_symbol
                )
                #weighted_score = self.weighted_board_score(board_score, depth)
                self.store_transposition(board.current_hash, board_score)
                return board_score


        potential_moves = (
            board.get_potential_moves(self.symbol)
            if board.marked_cells != 0
            else board.get_empty_cells()
        ) 

        if maximizing:
            max_eval = float("-inf") # Sämsta möjliga evalueringen för den maximerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves: 
                board.make_move_and_update_hash(self.symbol, move)


                # Rekursivt anrop av funktionen
                evaluation = self.minimax(
                    board, depth + 1, max_depth, alpha, beta, False
                )
                board.undo_move_and_update_hash(move)
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    
                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras.
                alpha = max(alpha, max_eval) 
                if beta <= alpha:
                    break

            return max_eval

        if not maximizing:
            min_eval = float("inf") # Sämsta möjliga evalueringen för den minimerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves: 
                board.make_move_and_update_hash(self.opponent_symbol, move)

                
                #Rekursivt anrop av funktionen
                evaluation = self.minimax(
                    board, depth + 1, max_depth, alpha, beta, True
                )
                board.undo_move_and_update_hash(move)
                
                if evaluation < min_eval:
                    min_eval = evaluation

                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras
                beta = min(beta, min_eval) 
                if beta <= alpha:
                    break


            return min_eval


    def print_depth(depth, str):
        indent = "  " * (3 - depth)
        print(indent + str)
    
    
    @staticmethod
    def weighted_board_score(score, depth):
        return score
        if score >= 1000000:
            return score - depth
        elif score <= -1000000:
            return score + depth
        else:
            return score
        
    
    def store_transposition(self, current_hash: int, score: float) -> None:
        """Store the evaluated score in the transposition table with size limit."""
        if current_hash in self.transposition_table:
            # Move to the end to show that it was recently used
            self.transposition_table.move_to_end(current_hash)
            return  # Already stored
    
        if len(self.transposition_table) >= self.trans_table_size:
            # Remove the first (least recently used) item
            self.transposition_table.popitem(last=False)
    
        self.transposition_table[current_hash] = score


