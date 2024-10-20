from utils import *
import copy


class Board:

    def __init__(self, rows: int, cols: int, win: int) -> None:
        self.rows = int(rows)
        self.cols = int(cols)
        self.win = int(win)
        self.board = self.create_board()
        self.marked_cells = 0
        self.ordered_moves: list[tuple[int, int]] = []

    def create_board(self) -> list[list[int]]:
        """Skapa en spelplan."""
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        return self.board

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """Returnera lista med tomma celler, dvs drag som inte gjorts."""
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board[row][col] == 0
        ]

    def valid_move(self, row: int, col: int) -> bool:
        """Kolla om ett drag är godkänt, baserat på celler som inte är markerade."""
        return (row, col) in self.get_empty_cells()

    def mark_cell(self, symbol: str, row: int, col: int) -> None:
        """Markera en cell på spelplanen med X eller O."""
        self.board[row][col] = symbol
        self.marked_cells += 1
        self.ordered_moves.append((row, col))

    def is_winning_move(self, symbol: int, move: tuple[int, int]) -> bool:
        """Kolla om ett drag är ett vinnande drag."""
        temp_board = copy.deepcopy(self)
        temp_board.mark_cell(symbol, *move)

        return temp_board.is_winner(symbol)

    def board_full(self) -> None:
        """Kolla om brädet är fullt."""
        return self.marked_cells == self.rows * self.cols

    def is_terminal(self, player1_symbol: str, player2_symbol: str) -> bool:
        """Kolla om någon spelare har vunnit eller om brädet är fullt."""
        if self.is_winner(player1_symbol) or self.is_winner(player2_symbol):
            return True

        return self.board_full()

    def out_of_range(self, move: tuple[int, int]) -> bool:
        """Givet ett drag, kontrollera om draget är inom brädets dimensioner."""
        return (
            (move[0] < 0)
            or (move[0] >= self.rows)
            or (move[1] < 0)
            or (move[1] >= self.cols)
        )

    def get_potential_moves(self, symbol) -> list[tuple[int, int]]:
        """Returnera en lista med potentiella drag kring drag som redan genomförts."""
        potential_moves = set()

        # Gränsvektorer för att kontrollera cellerna kring en given position (upp, ner, vänster, höger, diagonaler)
        directions = [
            (dx, dy)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if not (dx == 0 and dy == 0)
        ]

        for move in self.ordered_moves:
            for direction in directions:
                neighbor = (move[0] + direction[0], move[1] + direction[1])

                if (
                    not self.out_of_range(neighbor)
                    and self.board[neighbor[0]][neighbor[1]] == 0
                ):
                    potential_moves.add(neighbor)

        sorted_moves = []
        for move in list(potential_moves):
            if self.is_winning_move(symbol, move):
                sorted_moves.insert(0, move)
            else:
                sorted_moves.append(move)

        return sorted_moves

    def evaluate_board(
        self, player_symbol: str, opponent_symbol: str, depth: int
    ) -> int:
        score = 0
        already_evaluated = set()

        if self.is_winner(player_symbol):
            return float("10000000") - depth

        if self.is_winner(opponent_symbol):
            return float("-10000000") + depth

        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Horizontal, vertical, diagonal

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    continue  # Hoppa över redan markerade celler

                for direction in directions:
                    # Generera en unik key för respektive evaluerad "linje"
                    line_key = (row, col, direction)
                    if line_key in already_evaluated:
                        continue  # Hoppa över redan evaluerade "linjer"

                    line_score = self.evaluate_line_with_defense(
                        row, col, direction, player_symbol, opponent_symbol
                    )
                    score += line_score
                    already_evaluated.add(line_key)

        return score - depth

    def evaluate_line_with_defense(
        self,
        row: int,
        col: int,
        direction: tuple[int, int],
        player_symbol: str,
        opponent_symbol: str,
    ) -> int:
        """Evaluera en "linje" från en given position i en given riktning, där både offensiv och defensiv beaktas."""
        score = 0

        # Evaluera den egna "linjen" (offensiv)
        player_score = self.evaluate_direction(row, col, direction, player_symbol)
        score += player_score

        # Evaluera motståndarens "linje" (defensiv)
        opponent_score = self.evaluate_direction(row, col, direction, opponent_symbol)
        score -= opponent_score

        return score

    def evaluate_direction(
        self, row: int, col: int, direction: tuple[int, int], symbol: str
    ) -> int:
        """Evaluera en "linje i en specifik riktning för en given spelare."""
        cur_len = 0
        blocked_start = False
        blocked_end = False
        max_range = self.win

        head = (row + direction[0], col + direction[1])
        # Evaluera framåt upp till max_range celler
        if not self.out_of_range(head):
            while self.board[head[0]][head[1]] == symbol and cur_len < max_range:
                cur_len += 1
                head = (head[0] + direction[0], head[1] + direction[1])
                if self.out_of_range(head):
                    break
            if self.out_of_range(head) or self.board[head[0]][head[1]] != 0:
                blocked_end = True

        tail = (row - direction[0], col - direction[1])
        # Evaluera bakåt upp till max_range celler
        if not self.out_of_range(tail):
            while self.board[tail[0]][tail[1]] == symbol and cur_len < max_range:
                cur_len += 1
                tail = (tail[0] - direction[0], tail[1] - direction[1])
                if self.out_of_range(tail):
                    break
            if self.out_of_range(tail) or self.board[tail[0]][tail[1]] != 0:
                blocked_start = True

        # Poängsättning baserat på antal symboler i rad
        score = 0
        if cur_len == 4:
            if not blocked_start and not blocked_end:
                score = 10000
            elif not blocked_start or not blocked_end:
                score = 5000
        elif cur_len == 3:
            if not blocked_start and not blocked_end:
                score = 1000
            elif not blocked_start or not blocked_end:
                score = 500
        elif cur_len == 2:
            if not blocked_start and not blocked_end:
                score = 100
            elif not blocked_start or not blocked_end:
                score = 50

        return score

    def is_winner(self, player_symbol: str) -> bool:

        for row in range(self.rows):
            for col in range(self.cols - self.win + 1):
                if all(
                    self.board[row][col + i] == player_symbol for i in range(self.win)
                ):
                    return True

        for col in range(self.cols):
            for row in range(self.rows - self.win + 1):
                if all(
                    self.board[row + i][col] == player_symbol for i in range(self.win)
                ):
                    return True

        for row in range(self.rows - self.win + 1):
            for col in range(self.cols - self.win + 1):
                if all(
                    self.board[row + i][col + i] == player_symbol
                    for i in range(self.win)
                ):
                    return True

        for row in range(self.win - 1, self.rows):
            for col in range(self.cols - self.win + 1):
                if all(
                    self.board[row - i][col + i] == player_symbol
                    for i in range(self.win)
                ):
                    return True

        return False
