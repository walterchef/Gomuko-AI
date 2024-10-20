from graphics import *
from board import *
from player import *
from time import sleep


class Game:

    def __init__(
        self, board: Board, graphics: Graphics, player1: Player, player2: Player
    ):
        self.board = board
        self.graphics = graphics
        self.player1 = player1
        self.player2 = player2
        self.current_player = (
            self.player1 if self.player1.symbol == "X" else self.player2
        )
        self.winner = None
        self.running = True

    def switch_turns(self) -> None:
        """Byt vilken spelares tur det är."""
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def is_game_over(self) -> bool:
        """Kolla om en omgång är slut."""
        if self.board.is_terminal(self.player1.symbol, self.player2.symbol):
            if self.board.check_winner(self.player1.symbol):
                self.winner = self.player1
            elif self.board.check_winner(self.player2.symbol):
                self.winner = self.player2
            else:
                self.winner = None
            return True

    def play_again(self):
        """Kolla om användaren vill spela igen."""
        return self.graphics.wait_for_restart_or_quit()

    def play(self) -> bool:
        """Spela en omgång tills att den är slut."""
        while self.running:

            self.graphics.draw_board()

            # Hantera den nuvarande spelarens drag
            if isinstance(self.current_player, AI_Player):
                move = self.current_player.make_move(self.board)
            elif isinstance(self.current_player, User_Player):
                move = self.current_player.make_move(
                    self.board, self.graphics.cell_size
                )

            # Markera draget på brädet
            self.board.mark_cell(self.current_player.symbol, move[0], move[1])

            # Kolla om en omgång är över
            if self.is_game_over():
                self.graphics.draw_board()  # Redraw the final state of the board
                self.graphics.display_game_over_message(
                    self.winner
                )  # Display winner message

                # Kolla om användaren vill spela igen
                return self.play_again()

            # Byt vems tur det är att göra ett drag om omgången inte är över
            self.switch_turns()

        return False
