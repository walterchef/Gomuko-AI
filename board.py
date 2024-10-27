from hashing import *
import numpy as np


class Board:
    """Logisk representation av spelbrädet."""
    
    def __init__(self, rows: int, cols: int, to_win: int) -> None:
        self.rows = rows
        self.cols = cols
        self.to_win = to_win
        self.board = self.create_board()
        self.marked_cells = 0
        self.ordered_moves: list[tuple[int, int]] = []
        self.zobrist_table = initTable(rows, cols)  # Initialize the Zobrist table
        self.current_hash = compute_hash(self.board, self.zobrist_table)  # Initial hash

    def create_board(self) -> np.ndarray:
        """Create the game board as a NumPy array for faster access."""
        return np.full((self.rows, self.cols), "", dtype=object)

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """Returnera drag som inte har gjorts, för att underlätta felhantering när vi ska kontrollera om ett drag är godkänt.

        Returns:
            list[tuple[int, int]]: Lista med drag på formen (row, col).
        """
        return [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.board[row][col] == ""
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
        
    
    def make_move_and_update_hash(self, move: tuple[int, int], symbol: str) -> None:
        row, col = move
        current_symbol = self.board[row][col]
                
        # XOR out the current symbol
        self.current_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
        
        # Make the move
        self.board[row][col] = symbol
        self.marked_cells += 1
        self.ordered_moves.append(move)
        
        # XOR in the new symbol
        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]


    def undo_move_and_update_hash(self, move: tuple[int, int]) -> None:
        row, col = move
        symbol = self.board[row][col]
        
        # XOR out the symbol
        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]
        
        # Undo the move
        self.board[row][col] = ""
        self.marked_cells -= 1
        self.ordered_moves.pop()
                
        # XOR in the empty symbol
        self.current_hash ^= self.zobrist_table[row][col][index_of("")]


    def is_winning_move(self, symbol: int, move: tuple[int, int]) -> bool:
        """Kontrollera om ett drag är ett vinnande drag för att minska tiden AI:n tar på att göra vinnande drag.

        Args:
            symbol (int): Evaluerad symbol
            move (tuple[int, int]): Evaluerad position på brädet (row, col)

        Returns:
            bool: True om draget leder till vinst annars False.
        """
        self.make_move_and_update_hash(move, symbol)
        result = self.is_winner(symbol)
        self.undo_move_and_update_hash(move)
        return result

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
        return self.is_winner("X") or self.is_winner("O") or self.board_full()

    

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
                    and self.board[neighbor[0]][neighbor[1]] == ""
                ):
                    potential_moves.add(neighbor)
        
        potential_moves = list(potential_moves)
        
        winning_moves = []
        none_winning_moves = []
        for move in potential_moves:
            if self.is_winning_move(symbol, move):
                winning_moves.append(move)
            else:
                none_winning_moves.append(move)
        sorted_moves = winning_moves + none_winning_moves
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
            return 1000000

        if self.is_winner(opponent_symbol):
            return -1000000
        
        if self.board_full():
            return 0

        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (-1, 1),
        ]  # Horisontellt, vertikalt, diagonaler

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "":
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
        score = self.evaluate_direction(row, col, direction, player_symbol)
        score -= self.evaluate_direction(row, col, direction, opponent_symbol)
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
        
        score = 0
        cur_len = 0
        blocked_start = False
        blocked_end = False
        max_range = self.to_win

        dr, dc = direction

        # Forward direction
        for i in range(1, max_range):
            r = row + dr * i
            c = col + dc * i
            if not (0 <= r < self.rows and 0 <= c < self.cols):
                blocked_end = True
                break
            if self.board[r][c] == symbol:
                cur_len += 1
            elif self.board[r][c] == "":
                break
            else:
                blocked_end = True
                break

        # Backward direction
        for i in range(1, max_range):
            r = row - dr * i
            c = col - dc * i
            if not (0 <= r < self.rows and 0 <= c < self.cols):
                blocked_start = True
                break
            if self.board[r][c] == symbol:
                cur_len += 1
            elif self.board[r][c] == "":
                break
            else:
                blocked_start = True
                break

        # Scoring based on cur_len and block status
        # Early termination if maximum possible score is achieved
        if cur_len == self.to_win - 1:
            if not blocked_start and not blocked_end:
                return 10000
            elif not blocked_start or not blocked_end:
                return 5000
        elif cur_len == self.to_win - 2:
            if not blocked_start and not blocked_end:
                return 1000
            elif not blocked_start or not blocked_end:
                return 500
        elif cur_len == self.to_win - 3:
            if not blocked_start and not blocked_end:
                return 100
            elif not blocked_start or not blocked_end:
                return 50

        return score

    def is_winner(self, symbol: str) -> bool:
        """Evaluera om en spelare vunnit givet dess symbol, för att kunna veta när en omgång ska avslutas samt vilka drag som AI:n ska prioritera.

        Args:
            player_symbol (str): Spelarens symbol

        Returns:
            bool: True om spelaren vunnit eller False om spelaren inte vunnit
        """

        # Horizontal
        for row in range(self.rows):
            if self.check_consecutive(symbol, self.board[row, :]):
                return True
        # Vertical
        for col in range(self.cols):
            if self.check_consecutive(symbol, self.board[:, col]):
                return True
        # Diagonal (top-left to bottom-right)
        for offset in range(-self.rows + 1, self.cols):
            diag = self.board.diagonal(offset)
            if self.check_consecutive(symbol, diag):
                return True
        # Diagonal (top-right to bottom-left)
        for offset in range(-self.rows + 1, self.cols):
            diag = np.fliplr(self.board).diagonal(offset)
            if self.check_consecutive(symbol, diag):
                return True
        return False


    def check_consecutive(self, symbol: str, array: np.ndarray) -> bool:
        """Check if there are `to_win` consecutive symbols in the array."""
        count = 0
        for cell in array:
            if cell == symbol:
                count += 1
                if count >= self.to_win:
                    return True
            else:
                count = 0
        return False
