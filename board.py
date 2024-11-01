import copy
from utils import *
import numpy as np


class Board:
    """Logisk representation av spelbrädet."""

    def __init__(self, rows: int, cols: int, to_win: int) -> None:
        self.rows = rows
        self.cols = cols
        self.to_win = to_win
        self.board_map = self.create_board(self.rows, self.cols)
        self.marked_cells = 0
        self.moves_made: list[tuple[int, int]] = []
        self.zobrist_table = init_table(rows, cols)
        self.current_hash = compute_hash(self.board_map, self.zobrist_table)

    def create_board(self, rows: int, cols: int) -> np.ndarray:
        """Skapar ett spelbräde för att representera matchens tillstånd.

        Args:
            rows (int): Antalet rader på spelbrädet.
            cols (int): Antalet kolumner på spelbrädet

        Returns:
            np.ndarray: Spelbrädet representerat av en 2-dimensionell numpay-array.
        """
        return np.full((rows, cols), "")

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """Returnerar en lista tomma celler på brädet (rad, kolumn).

        Returns:
            list[tuple[int, int]]: Lista med tomma celler på formen (rad, kolumn).
        """
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board_map[row][col] == ""
        ]

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        """Kontrollerar om ett drag är godkänt, för att ingen av spelarna ska kunna placera sina drag på redan markerade celler.

        Args:
            move (tuple[int, int]): Evaluerad cell på brädet (rad, kolumn).

        Returns:
            bool: True om draget är godkänt annars False.
        """
        return move in self.get_empty_cells()

    def mark_cell_update_hash(self, symbol: str, cell: tuple[int, int]) -> None:
        """Markerar en cell på spelbrädet och uppdaterar brädets hashvärde.

        Args:
            symbol (str): Symbol av typen (X, O).
            cell (tuple[int, int]): Cell på spelbrädet som ska markeras (rad, kolumn).
        """
        row, col = cell

        self.board_map[row][col] = symbol

        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]

        self.marked_cells += 1
        self.moves_made.append(cell)

    def unmark_cell_update_hash(self, cell: tuple[int, int]) -> None:
        """Gör om en markerad cell till en tom cell och uppdaterar brädets hashvärde.

        Args:
            cell (tuple[int, int]): Cell på spelbrädet som ska avmarkeras (rad, kolumn)
        """
        row, col = cell
        symbol = self.board_map[row][col]

        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]

        self.board_map[row][col] = ""

        self.marked_cells -= 1
        self.moves_made.remove(cell)

    def is_full(self) -> bool:
        """Kontrollerar om brädet är fullt, för att kunna avgöra när en omgång är slut.

        Returns:
            bool: True om brädet är fullt annars False.
        """
        return self.marked_cells == self.rows * self.cols

    def is_terminal(self) -> bool:
        """Kontrollera om någon spelare har vunnit eller om brädet är fullt.

        Returns:
            bool: True om brädstatusen är terminal annars False.
        """
        if self.marked_cells >= (2 * self.to_win - 1):
            return (self.is_winner("X") or self.is_winner("O")) or self.is_full()

    def out_of_range(self, position: tuple[int, int]) -> bool:
        """Kontrollerar om en koordinat (rad, kolumn) är inom brädets dimensioner.

        Args:
            position (tuple[int, int]): Koordinat (rad, kolumn).

        Returns:
            bool: True om positionen är innanför brädets dimensioner annars False.
        """
        row, col = position
        return (
            (row < 0)
            or (row >= self.rows)
            or (col < 0)
            or (col >= self.cols)
        )

    def get_potential_moves(self, symbol: str) -> list[tuple[int, int]]:
        """Returnerar en lista med potentiella drag, med dragen sorterade efter hur bra de förväntas vara.

        Args:
            symbol (str): Symbol representerande spelaren (X, O).

        Returns:
            list[tuple[int, int]]: Lista med drag (rad, kolumn).
        """
        potential_moves = {}
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (-1, 1),
        ]

        for move in self.moves_made:
            for direction in directions:
                neighbor = (move[0] + direction[0], move[1] + direction[1])

                if (
                    self.out_of_range(neighbor)
                    or self.board_map[neighbor[0]][neighbor[1]] != ""
                ):
                    continue

                score = self.evaluate_move_increment(
                    neighbor, symbol, "O" if symbol == "X" else "X"
                )
                potential_moves[neighbor] = score

        return sorted(potential_moves, key=potential_moves.get, reverse=True)

    def evaluate_board(self, player_symbol: str, opponent_symbol: str) -> int:
        """Poängsätter hur starkt brädet är för en spelare givet hur symbolerna är placerade.

        Args:
            player_symbol (str): Symbol representerande spelaren (X, O).
            opponent_symbol (str): Symbol representerande motspelaren (X, O).

        Returns:
            int: Brädets relativa värde.
        """
        score = 0
        for move in self.moves_made:
            score += self.evaluate_move_increment(move, player_symbol, opponent_symbol)

        return score

    def evaluate_move_increment(
        self, last_move: tuple[int, int], player_symbol: int, opponent_symbol: int
    ) -> int:
        """
        Beräknar förändringen av brädets poäng som ett resultat av ett drag.

        Args:
            last_move (tuple[int, int]): Koordinater för senaste draget (rad, kolumn)
            player_symbol (str): Symbol representerande spelaren (X, O).
            opponent_symbol (str): Symbol representerande motspelaren (X, O).
            
        Returns:
            int: Brädets poäng efter draget.
        """
        pattern_dict = create_pattern_dict()
        row, col = last_move
        score = 0
        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ]

        symbol_map = {player_symbol: 1, opponent_symbol: -1, "": 0}

        for direction in directions:
            line = []
            for i in range(-self.to_win + 1, self.to_win):
                r, c = row + i * direction[0], col + i * direction[1]
                if not self.out_of_range((r, c)):
                    line.append(symbol_map.get(self.board_map[r][c]))
                else:
                    line.append(None)

            valid_line = tuple(cell for cell in line if cell is not None)

            for pattern, pattern_score in pattern_dict.items():
                for i in range(len(valid_line) - len(pattern) + 1):
                    if tuple(valid_line[i : i + len(pattern)]) == pattern:
                        score += pattern_score

        return score

    def is_winner(self, symbol: str) -> bool:
        """Evaluerar om en spelare vunnit givet dess symbol, det vill säga har to_win symboler i rad.

        Args:
            symbol (str): Symbol representerande spelaren (X, O)

        Returns:
            bool: True om spelaren vunnit annars False
        """

        target = np.array([symbol] * self.to_win)

        for row in self.board_map:
            for col in range(self.cols - self.to_win + 1):
                if np.array_equal(row[col : col + self.to_win], target):
                    return True

        for col in range(self.cols):
            column = self.board_map[:, col]
            for row in range(self.rows - self.to_win + 1):
                if np.array_equal(column[row : row + self.to_win], target):
                    return True

        for row in range(self.rows - self.to_win + 1):
            for col in range(self.cols - self.to_win + 1):
                diagonal = self.board_map[
                    range(row, row + self.to_win), range(col, col + self.to_win)
                ]
                if np.array_equal(diagonal, target):
                    return True

        for row in range(self.to_win - 1, self.rows):
            for col in range(self.cols - self.to_win + 1):
                diagonal = self.board_map[
                    range(row, row - self.to_win, -1), range(col, col + self.to_win)
                ]
                if np.array_equal(diagonal, target):
                    return True

        return False


