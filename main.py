from game import *
from player import *
from graphics import *
from board import *


def main() -> None:
    """Spela tills att användaren väljer att avsluta spelet"""
    while True:
        board = Board(15, 15, 5)
        graphics = Graphics(board)
        user_symbol, ai_symbol = graphics.choose_symbol()

        player1 = User_Player(user_symbol)
        player2 = AI_Player(ai_symbol)
        
        # Instansiering av en ny spelomgång 
        game: Game = Game(board, graphics, player1, player2) 

        game.play() 
        
        # Kontrollera om användaren vill spela igen, annars avsluta spelsessionen
        if not game.play_again():
            break


if __name__ == "__main__":
    main()
