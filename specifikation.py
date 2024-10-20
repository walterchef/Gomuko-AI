
"""

Fem-i-rad mot AI implementerad med minimax

Datastruktur

1) En brädklass, där varje brädobjekt har instansvariablerna:
    * rader: antalet rader som brädet består av
    * kolumner: antalet kolumner brädet består av
    * vinst: hur många symboler i rad en spelare behöver för att vinna
    * bräde: en 2-dimensionell lista som representerar spelplanen

2) En abstrakt spelarklass som har instansvariablerna:
    * symbol: vilken symbol (X,Y) som representerar spelaren
    
3) En användarspelarklass, som ärver från den abstrakta spelarklassen och därför har samma instansvariabler:
    * symbol: vilken symbol (X,Y) som representerar spelaren
    
4) En ai-spelarklass, som ärver från den abstrakta spelarklassen och därför har samma instansvariabler, men har också:
    * symbol: vilken symbol (X,Y) som representerar spelaren
    * svårighetsgrad: Hur bra är ai:n på att spela spelet
    
5) En spelklass, där varje instanscerat spelobjekt representerar en spelomgång. Ett spelobjekt har följande instansvariabler:
    * Spelare1: Ett spelarobjekt (Människa eller AI)
    * Spelare2: Ett spelarobjekt (Människa eller AI)
    * Bräde: Ett brädobjekt



Algoritm

I kronologisk ordning sker följande när ett ny spelomgång påbörjas:

    1) Användaren får välja om den vill spela som X eller O.
    2) Om användaren väljer X ombes den göra första draget, annars gör AI:n första draget.
    3) Spelarna turas om att göra drag tills att någon vinner eller det blir oavgjort.
    4) Användaren får välja om den vill spela igen eller avsluta. 
    
"""


class Board:
    
    def __init__(self, rows, cols, win):
        self.rows = int(rows)
        self.cols = int(cols)
        self.win = int(win)
        self.board = self.create_board()
        
     
    def create_board(self) -> list[list[int]]:
        """Skapa en spelplan"""
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        return self.board
    #Skapa ett bräde för aktuellt objekt
        
    def get_empty_cells(self) -> list[tuple[int, int]]: 
        return [(row,col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] == 0]
    #Returnera lista med tomma positioner på brädet
    
    def valid_move(self, row: int, col: int) -> bool:
        return (row, col) in self.get_empty_cells()
    #Kolla om ett drag är "godkänt", dvs att positionen på brädet är ledig
    
    def mark_cell(self, symbol: str, row: int, col: int) -> None:
        self.board[row][col] = symbol
        self.marked_cells += 1
        self.ordered_moves.append((row, col))
    
    
        temp_board = copy.deepcopy(self)
        temp_board.mark_cell(symbol, *move)
        
        return temp_board.check_winner(symbol)
    #Markera en cell på brädet med en symbol (X,O)       
                
    def board_full(self) -> bool:
        return self.marked_cells == self.rows * self.cols
    #Kolla om alla brädets celler är markerade

    def is_terminal(self) -> bool:
        if self.check_winner(player1_symbol) or self.check_winner(player2_symbol):
            return True
    
        return self.board_full()
        

        return (move[0] < 0) or (move[0] >= self.rows) or (move[1] < 0) or (move[1] >=self.cols)
    #Kolla om ett bräde har en vinnande spelare eller om brädet är fullt     
    
    def get_potential_moves(self, symbol: str) -> set[tuple[int, int]]:
        """Returnera ett set med potentiella drag kring drag som redan genomförts"""
        potential_moves = set()
        
        # Gränsvektorer för att kontrollera cellerna kring en given position (upp, ner, vänster, höger, diagonaler)
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
       
        for move in self.ordered_moves:
            for direction in directions:
                neighbor = (move[0] + direction[0], move[1] + direction[1])

                if not self.out_of_range(neighbor) and self.board[neighbor[0]][neighbor[1]] == 0:
                    potential_moves.add(neighbor)
        
        
        sorted_moves = []
        for move in list(potential_moves):
            if self.is_winning_move(symbol, move):
                sorted_moves.insert(0, move)
            else:
                sorted_moves.append(move)
        
        return sorted_moves
    #Returnera lista med tomma celler intill drag som redan gjorts. 
    
    def evaluate_board(self, player_symbol: str, opponent_symbol: str) -> int:
        score = 0
        already_evaluated = set()  
        
        if self.check_winner(player_symbol):
            return float("100000000") 
        
        if self.check_winner(opponent_symbol):
            return float("-100000000") 

        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:  
                    continue

                for direction in directions:
                    line_score = self.evaluate_line_with_defense(row, col, direction, player_symbol, opponent_symbol)
                    score += line_score

        return score
    #Heuristisk funktion för att returnera det relativa värdet av brädets aktuella status.


from abc import ABC, abstractmethod 

class Player(ABC):
    
    def __init__(self, symbol: str) -> None:
        self.name = name
        self.symbol = symbol
    
    @abstractmethod
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        pass
    #Abstrakt metod som klasser som ärver från den abstrakta klassen måste innehålla.


class Human_Player(Player):
    
    def __init__(self, symbol: str) -> None:
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
    #Returnera ett drag (row, col) baserat på användarens val               
                    
        
class AI_Player(Player):
    
    def __init__(self, symbol: str, difficulty: int = 2) -> None: # Ändra så att användaren kan välja svårighetsgrad
        super().__init__(name, symbol)
        self.opponent_symbol = "O" if symbol == "X" else "X"
        self.difficulty = difficulty
            
    def make_move(self, board: Board) -> tuple[int, int]:
        if self.difficulty == 0:
            return self.random_move(board)
        
        elif self.difficulty == 1 or self.difficulty == 2:
            
            if board.marked_cells == 0:
                move = (int(board.rows/2), int(board.cols/2))
            else:
                move = self.minimax(board, depth=0, max_depth=3, alpha=float("-inf"), beta=float("inf"), maximizing=True)[1]
                if move is None:
                    raise ValueError("AI could not find a valid move!")
            return move  
    #Returnera ett drag (row, col) baserat på returvärdet från minimax-funktionen
   
    def minimax(self, board: Board, depth: int, max_depth: int, alpha: int, beta: int, maximizing) -> tuple[int, tuple[int, int]]: #depth och maxdepth
        AI_Player.print_depth(depth, f"Enter Minimax: depth = {depth}")

        
        if depth == max_depth or board.is_terminal(self.symbol, self.opponent_symbol):
            board_score = board.evaluate_board(self.symbol, self.opponent_symbol) + (-depth) if not maximizing else depth
            
            AI_Player.print_depth(depth, f"Exit Minimax, eval = {board_score}")
            return board_score, None
        
        best_move = None
        potential_moves = board.get_potential_moves(self.symbol) if board.marked_cells != 0 else board.get_empty_cells()
        
        
        
        if maximizing:
            max_eval = float("-inf")
            
            for move in potential_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.symbol, *move)
                AI_Player.print_depth(depth, f"move = {move}")
                
                
                evaluation = self.minimax(temp_board, depth+1, max_depth, alpha, beta, False)[0]
              
              
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                
                alpha = max(alpha, max_eval) #eval
                if beta <= alpha:
                    break
            
            AI_Player.print_depth(depth, f"Exit Minimax, eval = {max_eval}, best move = {best_move}")

            return max_eval, best_move 
        
    
        if not maximizing:
            min_eval = float("inf")
            
            for move in potential_moves:
                temp_board = copy.deepcopy(board)
                temp_board.mark_cell(self.opponent_symbol, *move)
                AI_Player.print_depth(depth, f"move = {move}")

                
                
                evaluation = self.minimax(temp_board, depth + 1, max_depth, alpha, beta, True)[0]
            
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            
            AI_Player.print_depth(depth, f"Exit Minimax, eval = {min_eval}, best move = {best_move}")

            return min_eval, best_move
    #Returnera det bästa möjliga draget AI:n kan göra baserat på brädets aktuella status
    

class Game:
    
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None
        self.running = True
      
    def switch_turns(self) -> None:
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
    #Byt vems tur det är att göra ett drag
    
    def check_game_over(self) -> bool:
        if self.board.is_terminal(self.player1.symbol, self.player2.symbol):
            if self.board.check_winner(self.player1.symbol):
                self.winner = self.player1
            elif self.board.check_winner(self.player2.symbol):
                self.winner = self.player2
            else:
                self.winner = None
            return True
    #Kolla om en omgång är slut, dvs om någon vunnit eller om det blev oavgjort   
        
    def play(self) -> None:
    
        while self.running:
    
            self.graphics.draw_board()
           
            if isinstance(self.current_player, AI_Player):
                move = self.current_player.make_move(self.board)
                
            elif isinstance(self.current_player, Human_Player):
                move = self.current_player.make_move(self.board, self.graphics.cell_size)
                
            
            self.board.mark_cell(self.current_player.symbol, move[0], move[1])

            
            if self.check_game_over():
                self.graphics.draw_board()
                self.graphics.display_game_over_message(self.winner)
            
                if not self.graphics.wait_for_restart_or_quit():
                    self.running = False
                else:
                    self.__init__(self.board.rows, self.board.cols, self.board.win)
                    self.play
                break            
        
            self.switch_turns()    
    #while-slinga som implementerar spelalgoritmen, där användare och AI turas om att göra drag tills game_over.


def main() -> None:
    """Vi skapar 2 spelare, ett bräde och passerar de när vi initierar ett nytt spelobjekt"""
    board = Board(19, 19, 5)
    player1 = Human_Player("X")
    player2 = AI_Player("O", 2)
    
    game = Game(board, player1, player2)
    
    while game.running():
        game.play()
    
    
    
# cellklass
# namngivning 







                        
    

        
    
    
    

                    
                    
        
        
    

        
