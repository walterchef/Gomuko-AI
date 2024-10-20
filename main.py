from game import *
from player import *
from graphics import *
from board import *


def main() -> None:

    is_playing = True

    while is_playing: 
    # Spela tills att en användare väljer att avsluta spelet.

        board = Board(19, 19, 5)
        graphics = Graphics(board)

        symbols = graphics.choose_symbol()

        user_symbol = symbols[0]
        ai_symbol = symbols[1]

        player1 = User_Player(user_symbol)
        player2 = AI_Player(ai_symbol)
        
        game: Game = Game(board, graphics, player1, player2) # Instancering av en ny spelomgång 

        is_playing = game.play() # Fortsätt spela om användaren väljer att fortsätta, annars avsluta


if __name__ == "__main__":
    main()
