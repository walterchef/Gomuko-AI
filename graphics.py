import pygame
from board import *


class Graphics:
    def __init__(
        self, board, background_color=(30, 150, 140), line_color=(23, 140, 132)
    ):
        self.board = board
        self.background_color = background_color
        self.line_color = line_color
        self.cell_size = self.calculate_cell_size()
        self.line_width = self.calculate_line_width()
        self.width = self.board.cols * self.cell_size
        self.height = self.board.rows * self.cell_size
        self.screen = self.initialize_screen()

    def calculate_cell_size(self) -> int:
        """Anpassar storleken på respektive cell efter skärmens storlek.

        Returns:
            int: Storleken på en cell.
        """
        max_board_pixel_size = 800
        min_size = 40
        max_size = 700
        return min(
            max(
                max_board_pixel_size // max(self.board.rows, self.board.cols), min_size
            ),
            max_size,
        )

    def calculate_line_width(self) -> int:
        """Anpassar bredden på spelbrädets linjer efter storleken på en cell.

        Returns:
            int: Linjernas bredd.
        """
        min_width = 1
        max_width = 10
        return min(max(self.cell_size // 15, min_width), max_width)

    def initialize_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Five in a Row")
        return screen

    def draw_board(self) -> None:
        """Ritar upp den logiska representationen av brädet med markerade celler."""
        self.screen.fill(self.background_color)
        self.display_grid_lines()
        self.display_pieces()
        pygame.display.update()

    def display_grid_lines(self) -> None:
        """Ritar upp rutnätets linjer"""
        for col in range(1, self.board.cols):
            pygame.draw.line(
                self.screen,
                self.line_color,
                (col * self.cell_size, 0),
                (col * self.cell_size, self.height),
                self.line_width,
            )
        for row in range(1, self.board.rows):
            pygame.draw.line(
                self.screen,
                self.line_color,
                (0, row * self.cell_size),
                (self.width, row * self.cell_size),
                self.line_width,
            )

    def display_pieces(self) -> None:
        """Ritar ut symbolerna X och O givet hur det logiska brädet ser ut."""
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.board_map[row][col] == "X":
                    self.draw_cross((row, col))
                elif self.board.board_map[row][col] == "O":
                    self.draw_circle((row, col))

    def draw_cross(self, cell: tuple[int, int]) -> None:
        """Ritar ett X i en given cell på spelbrädet.

        Args:
            cell (tuple[int, int]): Cellen som ska markeras (rad, kolumn).
        """
        row, col = cell
        offset = self.cell_size // 5
        start_desc = (col * self.cell_size + offset, row * self.cell_size + offset)
        end_desc = (
            col * self.cell_size + self.cell_size - offset,
            row * self.cell_size + self.cell_size - offset,
        )
        pygame.draw.line(
            self.screen, (66, 66, 66), start_desc, end_desc, self.line_width * 2
        )
        start_asc = (
            col * self.cell_size + offset,
            row * self.cell_size + self.cell_size - offset,
        )
        end_asc = (
            col * self.cell_size + self.cell_size - offset,
            row * self.cell_size + offset,
        )
        pygame.draw.line(
            self.screen, (66, 66, 66), start_asc, end_asc, self.line_width * 2
        )

    def draw_circle(self, cell: tuple[int, int]) -> None:
        """Ritar ett O i en given cell på spelbrädet.

        Args:
            cell (tuple[int, int]): Cellen som ska markeras (rad, kolumn).
        """
        row, col = cell
        center = (
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )
        radius = self.cell_size // 3
        pygame.draw.circle(
            self.screen, (66, 66, 66), center, radius, self.line_width * 2
        )

    def draw_button(self, text: str, rect, color) -> None:
        """Ritar upp en knapp med en specificerad text, storlek och färg.

        Args:
            text (str): Text som ska stå på knappen.
            rect (_type_): Storleken och position på skärmen.
            color (_type_): Färgen på knappen.
        """
        pygame.draw.rect(self.screen, color, rect)
        font = pygame.font.Font(None, 40)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def choose_symbol(self) -> tuple[str, str]:
        """Användaren väljer om den vill spela som X eller O.

        Returns:
            tuple[str, str]: Användarens symbol, motspelarens symbol.
        """
        x_button_color = (0, 128, 0)
        o_button_color = (128, 0, 0)
        button_width, button_height = 100, 50
        x_button_rect = pygame.Rect(
            self.width // 2 - 150, self.height // 2, button_width, button_height
        )
        o_button_rect = pygame.Rect(
            self.width // 2 + 50, self.height // 2, button_width, button_height
        )

        font = pygame.font.Font(None, 60)
        self.draw_board()

        welcome_text = font.render("Welcome to Five in a Row", True, (255, 255, 255))
        welcome_rect = welcome_text.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(welcome_text, welcome_rect)
        self.draw_button("X", x_button_rect, x_button_color)
        self.draw_button("O", o_button_rect, o_button_color)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if x_button_rect.collidepoint(mouse_pos):
                        return ("X", "O")
                    if o_button_rect.collidepoint(mouse_pos):
                        return ("O", "X")

    def display_game_over_message(self, winner=None) -> None:
        """Skriver ut ett medellande, med omgångens resultat när en spelomgång är över.

        Args:
            winner (_type_, optional): Vinnaren av omgången. Som standard sätt till None.
        """
        message = "It's a draw!" if winner is None else f"{winner.symbol.upper()} WINS!"
        font = pygame.font.Font(None, 60)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def wait_for_restart_or_quit(self) -> bool:
        """Evaluerar om användaren vill spela ytterligare en omgång när en omgång är slut.

        Returns:
            bool: True om användaren vill spela igen annars False.
        """
        play_again_button = pygame.Rect(
            self.width // 2 - 100, self.height // 2 + 50, 200, 40
        )
        quit_button = pygame.Rect(
            self.width // 2 - 100, self.height // 2 + 100, 200, 40
        )

        self.draw_button("PLAY AGAIN", play_again_button, (0, 255, 0))
        self.draw_button("QUIT GAME", quit_button, (255, 0, 0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        return True
                    if quit_button.collidepoint(event.pos):
                        return False
                    


