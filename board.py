from hashing import *
import copy


class Board:
    """Logisk representation av spelbrädet."""
    
    def __init__(self, rows: int, cols: int, to_win: int) -> None:
        self.rows = rows
        self.cols = cols
        self.to_win = to_win
        self.board = self.create_board()
        self.marked_cells = 0
        self.ordered_moves: list[tuple[int, int]] = []

    def create_board(self) -> list[list[int]]:
        """Skapa en spelplan för att representera matchens tillstånd samt för att kunna visualisera spelplanen grafiskt.

        Returns:
            list[list[int]]: Brädet representerat av en 2 dimensionell lista.
        """
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        return self.board

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """Returnera drag som inte har gjorts, för att underlätta felhantering när vi ska kontrollera om ett drag är godkänt.

        Returns:
            list[tuple[int, int]]: Lista med drag på formen (row, col).
        """
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board[row][col] == 0
        ]

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        """Kontrollera om ett drag är godkänt, för att ingen av spelarna ska kunna placera sina drag på redan markerade celler.

        Args:
            move (tuple[int, int]): Evaluerad position på brädet (row, col)

        Returns:
            bool: True om draget är godkänt annars False.
        """
        return move in self.get_empty_cells()

    def mark_cell(self, symbol: str, position: tuple[int, int]) -> None:
        """Markera en cell på en given position på spelplanen med X eller O.

        Args:
            symbol (str): Symbolen som ska placeras
            cell (tuple[int, int]): Evaluerad position på brädet (row, col)
        """
        self.board[position[0]][position[1]] = symbol
        self.marked_cells += 1
        self.ordered_moves.append((position[0], position[1]))

    def is_winning_move(self, symbol: int, move: tuple[int, int]) -> bool:
        """Kontrollera om ett drag är ett vinnande drag för att minska tiden AI:n tar på att göra vinnande drag.

        Args:
            symbol (int): Evaluerad symbol
            move (tuple[int, int]): Evaluerad position på brädet (row, col)

        Returns:
            bool: True om draget leder till vinst annars False.
        """
        temp_board = copy.deepcopy(self)
        temp_board.mark_cell(symbol, move)

        return temp_board.is_winner(symbol)

    def board_full(self) -> True:
        """Kontrollera om brädet är fullt, vilken används för att kontrollera om en omgång är slut.

        Returns:
            bool: True om brädet är fullt annars False.
        """
        return self.marked_cells == self.rows * self.cols

    def is_terminal(self) -> bool:
        """Kontrollera om någon spelare har vunnit eller om brädet är fullt för att kunna avsluta omgången.

        Returns:
            bool: True om brädstatusen är terminal annars False.
        """
        return (self.is_winner("X") or self.is_winner("O")) if True else self.board_full()
    

    def get_potential_moves(self, symbol: str) -> list[tuple[int, int]]:
        """Returnera en lista med potentiella drag kring drag som redan gjorts för att minska antalet drag som AI:n behöver evaluera i minimax algoritmen.

        Args:
            symbol (str): Spelarens symbol 

        Returns:
            list[tuple[int, int]]: Drag dikt an drag som redan gjorts.
        """
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
        self, player_symbol: str, opponent_symbol: str
    ) -> int:
        """Heuristisk metod för poängsättning av brädet vilket nyttjas i minimaxalgoritmen när AI:n ska göra sitt drag.

        Args:
            player_symbol (str): Spelarens symbol
            opponent_symbol (str): Motspelarens symbol

        Returns:
            int: Brädets relativa värde
        """
        score = 0
        already_evaluated = set()

        if self.is_winner(player_symbol):
            return float("100000") 

        if self.is_winner(opponent_symbol):
            return float("-100000")

        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (-1, 1),
        ]  # Horisontellt, vertikalt, diagonaler

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

        return score

    def evaluate_line_with_defense(
        self,
        row: int,
        col: int,
        direction: tuple[int, int],
        player_symbol: str,
        opponent_symbol: str,
    ) -> int:
        """Evaluera en "linje" från en given position i en given riktning, där både offensiv och defensiv beaktas.

        Args:
            row (int): Evaluerad rad
            col (int): Evaluerad kolumn
            direction (tuple[int, int]): Evaluerad riktning (Horisontellt, vertikalt eller diagonalt)
            player_symbol (str): Spelarens symbol
            opponent_symbol (str): Motspelarens symbol

        Returns:
            int: Linjens värde, från offensivt och defensivt perspektiv
        """
        score = 0

        player_score = self.evaluate_direction(row, col, direction, player_symbol)
        score += player_score

        opponent_score = self.evaluate_direction(row, col, direction, opponent_symbol)
        score -= opponent_score

        return score
    
    def out_of_range(self, position: tuple[int, int]) -> bool:
        """Givet ett drag, kontrollera om draget är inom brädets dimensioner, vilket nyttjas vid iteration över brädet i evaluate_line metoden.

        Args:
            position (tuple[int, int]): Position på brädet.

        Returns:
            bool: True om draget är innanför brädets dimensioner annars False.
        """
        return (
            (position[0] < 0)
            or (position[0] >= self.rows)
            or (position[1] < 0)
            or (position[1] >= self.cols)
        )

    def evaluate_direction(
        self, row: int, col: int, direction: tuple[int, int], symbol: str) -> int:
        """Utvärderar en linje i en specifik riktning för att avgöra hur stark positionen är
        är för den givna spelarsymbolen. Detta för att kunna evaluera hela brädet.

        Args:
            row (int): Evaluerad rad
            col (int): Evaluerad kolumn
            direction (tuple[int, int]): Evaluerad riktning (Horisontellt, vertikalt eller diagonalt)
            symbol (str): Spelarens symbol

        Returns:
            int: Linjens värde
        """
        
        cur_len = 0
        blocked_start = False
        blocked_end = False
        max_range = self.to_win

        head = (row + direction[0], col + direction[1])
        # Evaluera i ena riktningen upp till max_range celler
        if not self.out_of_range(head):
            while self.board[head[0]][head[1]] == symbol and cur_len < max_range:
                cur_len += 1
                head = (head[0] + direction[0], head[1] + direction[1])
                if self.out_of_range(head):
                    break
            if self.out_of_range(head) or self.board[head[0]][head[1]] != 0:
                blocked_end = True

        tail = (row - direction[0], col - direction[1])
        # Evaluera i andra riktningen upp till max_range celler
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
        """Evaluera om en spelare vunnit givet dess symbol, för att kunna veta när en omgång ska avslutas samt vilka drag som AI:n ska prioritera.

        Args:
            player_symbol (str): Spelarens symbol

        Returns:
            bool: True om spelaren vunnit eller False om spelaren inte vunnit
        """

        for row in range(self.rows):
            for col in range(self.cols - self.to_win + 1):
                if all(
                    self.board[row][col + i] == player_symbol
                    for i in range(self.to_win)
                ):
                    return True

        for col in range(self.cols):
            for row in range(self.rows - self.to_win + 1):
                if all(
                    self.board[row + i][col] == player_symbol
                    for i in range(self.to_win)
                ):
                    return True

        for row in range(self.rows - self.to_win + 1):
            for col in range(self.cols - self.to_win + 1):
                if all(
                    self.board[row + i][col + i] == player_symbol
                    for i in range(self.to_win)
                ):
                    return True

        for row in range(self.to_win - 1, self.rows):
            for col in range(self.cols - self.to_win + 1):
                if all(
                    self.board[row - i][col + i] == player_symbol
                    for i in range(self.to_win)
                ):
                    return True

        return False
