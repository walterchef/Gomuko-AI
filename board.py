from hashing import *
import copy
from utils import *


class Board:
    """Logisk representation av spelbrädet."""
    
    def __init__(self, rows: int, cols: int, to_win: int) -> None:
        self.rows = rows
        self.cols = cols
        self.to_win = to_win
        self.board = self.create_board()
        self.marked_cells = 0
        self.ordered_moves: list[tuple[int, int]] = []
        self.pattern_dict = create_pattern_dict()
        self.zobrist_table = initTable(rows, cols)  # Initialize the Zobrist table
        self.current_hash = compute_hash(self.board, self.zobrist_table)  # Initial hash

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
        
    
    def undo_move(self, move: tuple[int, int]):
        self.board[move[0]][move[1]] = 0
        self.marked_cells -= 1
        self.ordered_moves.remove((move[0], move[1]))
        
        
    def make_move_and_update_hash(self, symbol: str, move: tuple[int, int]) -> None:
        row, col = move
        
        # XOR out the current symbol (if any) from the hash before changing the board state
        current_symbol = self.board[row][col]
        if current_symbol != 0:  # Only remove if there is an actual piece
            self.current_hash ^= self.zobrist_table[row][col][index_of(current_symbol)]
        
        # Apply the move on the board
        self.board[row][col] = symbol
        
        # XOR in the new symbol to update the hash to match the new board state
        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]
        
        # Track the move
        self.marked_cells += 1
        self.ordered_moves.append(move)

        
    
    def undo_move_and_update_hash(self, move: tuple[int, int]) -> None:
        row, col = move
        symbol = self.board[row][col]
        
        # XOR out the current symbol from the hash
        self.current_hash ^= self.zobrist_table[row][col][index_of(symbol)]
        
        # Remove the piece from the board
        self.board[row][col] = 0  # Set back to empty
        
        # XOR in the "empty" symbol to reflect that the cell is now empty
        self.current_hash ^= self.zobrist_table[row][col][index_of(0)]
        
        # Track the undo
        self.marked_cells -= 1
        self.ordered_moves.remove(move)


    def is_winning_move(self, symbol: int, move: tuple[int, int]) -> bool:
        """Kontrollera om ett drag är ett vinnande drag för att minska tiden AI:n tar på att göra vinnande drag.

        Args:
            symbol (int): Evaluerad symbol
            move (tuple[int, int]): Evaluerad position på brädet (row, col)

        Returns:
            bool: True om draget leder till vinst annars False.
        """
        self.mark_cell(symbol, move)
        result = self.is_winner(symbol)
        self.undo_move(symbol, move)
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
        return (self.is_winner("X") or self.is_winner("O")) if True else self.board_full()
    

    def get_potential_moves(self, symbol: str) -> list[tuple[int, int]]:
        """Returnera en lista med potentiella drag kring drag som redan gjorts för att minska antalet drag som AI:n behöver evaluera i minimax algoritmen.

        Args:
            symbol (str): Spelarens symbol 

        Returns:
            list[tuple[int, int]]: Drag dikt an drag som redan gjorts.
        """
        potential_moves = {}
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1)
        ]
        

        for move in self.ordered_moves:
            for direction in directions:
                neighbor = (move[0] + direction[0], move[1] + direction[1])

                if self.out_of_range(neighbor) or self.board[neighbor[0]][neighbor[1]] != 0:
                    continue

                # Calculate score based on neighbor proximity to the current move
                score = self.evaluate_move_increment(neighbor, symbol, "O" if symbol == "X" else "X")
                potential_moves[neighbor] = score

        # Sort moves by score in descending order
        return sorted(potential_moves, key=potential_moves.get, reverse=True)

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
        directions = [
            (1, 0),   # Horizontal
            (0, 1),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1)   # Diagonal up-right
        ]
        
        # Convert symbols to a map for pattern matching
        symbol_map = {
            player_symbol: 1,
            opponent_symbol: -1,
            0: 0
        }
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    continue  # Skip empty cells

                for direction in directions:
                    # Collect cells along the direction in a list, mapped to symbol_map values
                    line = []
                    for i in range(-self.to_win + 1, self.to_win):
                        r, c = row + i * direction[0], col + i * direction[1]
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            line.append(symbol_map.get(self.board[r][c], 0))
                        else:
                            line.append(None)  # Out of bounds
                    
                    # Only keep the valid section of the line within the board
                    valid_line = tuple(cell for cell in line if cell is not None)

                    # Match patterns in the valid section of the line
                    for pattern, pattern_score in self.pattern_dict.items():
                        # Check if the pattern matches a substring in the line
                        for i in range(len(valid_line) - len(pattern) + 1):
                            if tuple(valid_line[i:i + len(pattern)]) == pattern:
                                score += pattern_score

        return score
    

    def evaluate_move_increment(self, last_move: tuple[int, int], player_symbol: int, opponent_symbol: int) -> int:
        """
        Calculate the incremental board score resulting from a move, considering patterns around the last move.
        
        Args:
            last_move (tuple[int, int]): Coordinates of the last move.
            player_symbol (int): Symbol for the AI player (e.g., 1).
            opponent_symbol (int): Symbol for the opponent (e.g., -1).
        
        Returns:
            int: Incremental score change from the move.
        """
        row, col = last_move
        score = 0
        directions = [
            (1, 0),   # Horizontal
            (0, 1),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1)   # Diagonal up-right
        ]
        
        # Map symbols to their pattern values (1, -1, 0)
        symbol_map = {
            player_symbol: 1,
            opponent_symbol: -1,
            0: 0
        }

        # Evaluate patterns in all directions around the last move
        for direction in directions:
            line = []
            for i in range(-self.to_win + 1, self.to_win):
                r, c = row + i * direction[0], col + i * direction[1]
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    line.append(symbol_map.get(self.board[r][c], 0))  # Map symbols using symbol_map
                else:
                    line.append(None)  # Out of bounds

            # Only keep the valid part of the line within board boundaries
            valid_line = tuple(cell for cell in line if cell is not None)

            # Match patterns in the valid section of the line
            for pattern, pattern_score in self.pattern_dict.items():
                # Check if the pattern matches a substring in the line
                for i in range(len(valid_line) - len(pattern) + 1):
                    if tuple(valid_line[i:i + len(pattern)]) == pattern:
                        score += pattern_score

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

