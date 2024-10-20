from game import *
from player import *
from graphics import *
from board import *


def main() -> None:

    is_playing = True

    test = "test"
    test = "test2"

    while is_playing:

        board = Board(19, 19, 5)
        graphics = Graphics(board)

        symbols = graphics.choose_symbol()

        user_symbol = symbols[0]
        ai_symbol = symbols[1]

        player1 = User_Player("test", user_symbol)
        player2 = AI_Player("test", ai_symbol)
        game: Game = Game(board, graphics, player1, player2)

        is_playing = game.play()


if __name__ == "__main__":
    main()
