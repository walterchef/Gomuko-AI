import pygame
import copy
import sys
import random
from abc import ABC, abstractmethod
from board import *


class Player(ABC):

    def __init__(self, name: str, symbol: str) -> None:
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        pass


class User_Player(Player):

    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)

    def make_move(self, board: list[list[int]], cell_size: int) -> tuple[int, int]:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // cell_size
                    col = pos[0] // cell_size
                    if board.valid_move(row, col):
                        return (row, col)


class AI_Player(Player):
    """Klass för spelare av typen AI."""

    def __init__(
        self, name: str, symbol: str, difficulty: int = 2
    ) -> None:  
        super().__init__(name, symbol)
        self.opponent_symbol = "O" if symbol == "X" else "X"
        self.difficulty = difficulty

    def make_move(self, board: Board) -> tuple[int, int]:
        if self.difficulty == 0:
            return self.random_move(board)

        elif self.difficulty == 1 or self.difficulty == 2:

            if board.marked_cells == 0:
                move = (int(board.rows / 2), int(board.cols / 2))
            else:
                move = self.minimax(
                    board,
                    depth=0,
                    max_depth=2,
                    alpha=float("-inf"),
                    beta=float("inf"),
                    maximizing=True,
                )[1]
                if move is None:
                    raise ValueError("AI could not find a valid move!")
            return move

    def random_move(self, board: Board):
        empty_cells = board.get_empty_cells()
        return random.choice(empty_cells)

    @staticmethod
    def print_depth(depth, str):
        indent = "  " * (3 - depth)
        print(indent + str)

    def minimax(
        self,
        board: Board,
        depth: int,
        max_depth: int,
        alpha: int,
        beta: int,
        maximizing,
    ):  # depth och maxdepth
        AI_Player.print_depth(depth, f"Enter Minimax: depth = {depth}")

        if depth == max_depth or board.is_terminal(self.symbol, self.opponent_symbol):
            board_score = board.evaluate_board(
                self.symbol, self.opponent_symbol, depth
            )  # + (-depth) if not maximizing else depth

            AI_Player.print_depth(depth, f"Exit Minimax, eval = {board_score}")
            return board_score, None

        best_move = None
        potential_moves = (
            board.get_potential_moves(self.symbol)
            if board.marked_cells != 0
            else board.get_empty_cells()
        )

        if maximizing:
            max_eval = float("-inf")

            for move in potential_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.symbol, *move)
                AI_Player.print_depth(depth, f"move = {move}")

                evaluation = self.minimax(
                    temp_board, depth + 1, max_depth, alpha, beta, False
                )[0]

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

                alpha = max(alpha, max_eval)  # eval
                if beta <= alpha:
                    break

            AI_Player.print_depth(
                depth, f"Exit Minimax, eval = {max_eval}, best move = {best_move}"
            )

            return max_eval, best_move

        if not maximizing:
            min_eval = float("inf")

            for move in potential_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.opponent_symbol, *move)
                AI_Player.print_depth(depth, f"move = {move}")

                evaluation = self.minimax(
                    temp_board, depth + 1, max_depth, alpha, beta, True
                )[0]

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

            AI_Player.print_depth(
                depth, f"Exit Minimax, eval = {min_eval}, best move = {best_move}"
            )

            return min_eval, best_move
