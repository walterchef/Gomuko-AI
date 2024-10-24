import pygame
import copy
import sys
import random
from abc import ABC, abstractmethod
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
        self, symbol: str, max_depth: int = 2
    ) -> None:  
        super().__init__(symbol)
        self.opponent_symbol = "O" if symbol == "X" else "X"
        self.max_depth = max_depth

    def make_move(self, board: Board) -> tuple[int, int]:
        """Returnera AI:ns drag baserat på svårighetsgraden.

        Args:
            board (Board): Logisk representation av spelbrädet

        Returns:
            tuple[int, int]: AI:ns drag (row, col)
        """

        if board.marked_cells == 0:
            move = (int(board.rows / 2), int(board.cols / 2))
        else:
            move = self.minimax(
                board,
                depth=0,
                max_depth=self.max_depth,
                alpha=float("-inf"),
                beta=float("inf"),
                maximizing=True,
            )[1]
            if move is None:
                raise ValueError("AI could not find a valid move!")
        return move    
    

    @staticmethod
    def weighted_board_score(score, depth):
        if score == 1000000:
            return score - depth
        elif score == -1000000:
            return score + depth
        else:
            return score
        
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
        AI_Player.print_depth(depth, f"Enter Minimax: depth = {depth}")

        if depth == max_depth or board.is_terminal(): # Evaluera brädets poäng när vi nått maximalt djup eller ett terminalt stadie.
            board_score = board.evaluate_board(
                self.symbol, self.opponent_symbol
            )
            
            AI_Player.print_depth(depth, f"Exit Minimax, eval = {board_score}")
            return self.weighted_board_score(board_score, depth), None


        best_move = None
        potential_moves = (
            board.get_potential_moves(self.symbol)
            if board.marked_cells != 0
            else board.get_empty_cells()
        ) 

        if maximizing:
            max_eval = float("-inf") # Sämsta möjliga evalueringen för den maximerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves: 
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.symbol, move)
                AI_Player.print_depth(depth, f"move = {move}")

                # Rekursivt anrop av funktionen
                evaluation = self.minimax(
                    temp_board, depth + 1, max_depth, alpha, beta, False
                )[0]

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                    
                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras.
                alpha = max(alpha, max_eval) 
                if beta <= alpha:
                    break

            AI_Player.print_depth(
                depth, f"Exit Minimax, eval = {max_eval}, best move = {best_move}"
            )

            return max_eval, best_move

        if not maximizing:
            min_eval = float("inf") # Sämsta möjliga evalueringen för den minimerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves: 
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.opponent_symbol, move)
                AI_Player.print_depth(depth, f"move = {move}")
                
                #Rekursivt anrop av funktionen
                evaluation = self.minimax(
                    temp_board, depth + 1, max_depth, alpha, beta, True
                )[0]

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras
                beta = min(beta, min_eval) 
                if beta <= alpha:
                    break

            AI_Player.print_depth(
                depth, f"Exit Minimax, eval = {min_eval}, best move = {best_move}"
            )

            return min_eval, best_move


    def print_depth(depth, str):
        indent = "  " * (3 - depth)
        print(indent + str)