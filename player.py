import pygame
import sys
from abc import ABC, abstractmethod
from collections import OrderedDict
from board import *
from graphics import *


class Player(ABC):
    """Abstrakt basspelarklass"""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @abstractmethod
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        """Abstrakt metod som måste implementeras i basspelarklassens underklasser.

        Args:
            board (list[list[int]]): Logisk representation av spelbrädet.

        Returns:
            tuple[int, int]: Cell på spelbrädet (rad, kolumn)
        """
        pass


class User_Player(Player):
    """Klass för spelare av typen användare."""

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)

    def make_move(self, board: Board, cell_size: int) -> tuple[int, int]:
        """Returnerar användarens drag baserat på vilken cell på spelplanen användaren klickar på.

        Args:
            board (Board): Logisk representation av spelbrädet.
            cell_size (int): Storleken av en cell i x*y pixlar.

        Returns:
            tuple[int, int]: Användarens drag (rad, kolumn).
        """
        
        valid_move = False
        while not valid_move:
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
        self, symbol: str, depth: int = 3, trans_table_size: int = 10000
    ) -> None:
        super().__init__(symbol)
        self.opponent_symbol = "O" if symbol == "X" else "X"
        self.depth = depth
        self.transposition_table = OrderedDict()
        self.trans_table_size = trans_table_size

    def make_move(self, board: Board) -> tuple[int, int]:
        """Returnerar AI:ns drag.

        Args:
            board (Board): Logisk representation av spelbrädet.

        Returns:
            tuple[int, int]: AI:ns drag (rad, kolumn)
        """

        if board.marked_cells == 0:
            move = (int(board.rows / 2), int(board.cols / 2))
        else:
            move = self.get_best_move(
                board,
                depth=self.depth,
                alpha=float("-inf"),
                beta=float("inf"),
                maximizing=True,
            )[1]
            
        return move

    def get_best_move(
        self,
        board: Board,
        depth: int,
        alpha: int,
        beta: int,
        maximizing: bool,
    ) -> tuple[int, int]:
        """Implementerar minimaxalgoritmen för att hitta det bästa draget AI:n kan göra givet ett spelbräde.

        Args:
            board (Board): Logisk representation av brädet
            depth (int): Djupet för hur många drag framåt vi evaluerar
            alpha (int): Bästa värde för maximerande spelaren när vi kallar på metoden
            beta (int): Bästa värde för minimerande spelaren när vi kallar på metoden
            maximizing (bool): True om maximerande spelaren ska göra ett drag annars False.

        Returns:
            tuple[int, int]: Bästa draget AI:n kan göra (rad, kolumn).
        """

        if board.current_hash in self.transposition_table and self.transposition_table[board.current_hash][1] >= depth:
            stored_score = self.transposition_table[board.current_hash][0]
            return stored_score, None

        if depth == 0 or board.is_terminal():
            board_score = board.evaluate_board(self.symbol, self.opponent_symbol)
            self.store_transposition(board.current_hash, board_score, depth)
            return board_score, None

        best_move = None
        potential_moves = (
            board.get_potential_moves(self.symbol)
            if board.marked_cells != 0
            else board.get_empty_cells()
        )

        if maximizing:
            max_eval = float(
                "-inf"
            )  # Sämsta möjliga evalueringen för den maximerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves:
                board.mark_cell_update_hash(self.symbol, move)

                # Rekursivt anrop av funktionen
                eval = self.get_best_move(board, depth - 1, alpha, beta, False)[0]
                board.unmark_cell_update_hash(move)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras.
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        if not maximizing:
            min_eval = float(
                "inf"
            )  # Sämsta möjliga evalueringen för den minimerande spelaren

            # Iteration över möjliga drag
            for move in potential_moves:
                board.mark_cell_update_hash(self.opponent_symbol, move)

                # Rekursivt anrop av funktionen
                eval = self.get_best_move(board, depth - 1, alpha, beta, True)[0]
                board.unmark_cell_update_hash(move)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                # Alpha-Beta pruning för att minska antalet noder som behöver evalueras
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def store_transposition(self, current_hash: int, score: float, depth: int) -> None:
        """Lägger till hashen för ett bräde med dess korresponderande värde i cacheminnet och hanterar dess storlek.

        Args:
            current_hash (int): Hashvärdet för brädet.
            score (float): Brädets värde.
            depth (int): Djupet brädet evalueras på.
        """
        if current_hash in self.transposition_table:
            self.transposition_table.move_to_end(current_hash)
            return None

        if len(self.transposition_table) >= self.trans_table_size:
            self.transposition_table.popitem(last=False)

        self.transposition_table[current_hash] = [score, depth]
