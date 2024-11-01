from graphics import *
from board import *
from player import *
from time import sleep


class Game:
    """Klass som representerar en spelomgång av en spelsession."""

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
        """Byter vilken spelares tur det är att göra ett drag."""
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def is_game_over(self) -> bool:
        """Evaluerar om en spelomgång är slut och ändrar omgångens vinnare om någon vunnit.

        Returns:
            bool: True om spelomgången är över annars False.
        """
        if self.board.is_terminal():
            if self.board.is_winner(self.player1.symbol):
                self.winner = self.player1
            elif self.board.is_winner(self.player2.symbol):
                self.winner = self.player2
            else:
                self.winner = None
            return True

    def play_round(self) -> None:
        """Spelalgoritmen för en omgång, där två spelare alternerar att göra drag tills omgången är slut."""
        while self.running:
            self.graphics.draw_board()

            # Hanterande av den nuvarande spelarens drag
            if isinstance(self.current_player, AI_Player):
                move = self.current_player.make_move(self.board)
            elif isinstance(self.current_player, User_Player):
                move = self.current_player.make_move(
                    self.board, self.graphics.cell_size
                )

            self.board.mark_cell_update_hash(self.current_player.symbol, move)

            # Kontrollera om omgången är över efter varje drag
            if self.is_game_over():
                self.graphics.draw_board()
                self.graphics.display_game_over_message(self.winner)
                self.running = False

            self.switch_turns()

    def play_again(self) -> bool:
        """Evaluerar om användaren vill spela ytterligare en omgång för att avgöra när spelsessionen ska stängas ner.

        Returns:
            bool: True om användaren vill spela igen annars False.
        """
        return self.graphics.wait_for_restart_or_quit()
