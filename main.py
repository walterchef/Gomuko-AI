from game import *
from player import *
from graphics import *
from board import *


def main() -> None:
    """Kör huvudprogrammet, som utgör en hel spelsession, som spelas tills att användaren väljer att avsluta spelet.
    """
    running = True
    
    while running:
        board: Board = Board(rows = 15, cols = 15, to_win = 5)
        graphics: Graphics = Graphics(board)
        user_symbol, ai_symbol = graphics.choose_symbol()

        player1 = User_Player(user_symbol)
        player2 = AI_Player(ai_symbol)
        
        # Instansiering av en ny spelomgång 
        game: Game = Game(board, graphics, player1, player2)   

        game.play_round() 
        
        if not game.play_again():
            running = False


if __name__ == "__main__":
    main()
