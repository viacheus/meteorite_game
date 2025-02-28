import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class FinalScreen:
    def __init__(self):
        self.game_over_font = pygame.font.Font(None, 74)
        self.game_over_text = self.game_over_font.render(
            "GAME OVER", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.game_won_font = pygame.font.Font(None, 74)
        self.game_won_text = self.game_won_font.render(
            "VICTORY", True, (0, 255, 0))
        self.game_won_rect = self.game_won_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.score_font = pygame.font.Font(None, 48)
        self.restart_font = pygame.font.Font(None, 40)
        self.restart_text = self.restart_font.render(
            "Press r to restart", True, (255, 255, 255))
        self.restart_rect = self.restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.scores_button = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 50)
        self.menu_button = pygame.Rect(
            WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 170, 200, 50)

        self.goto_game = False
        self.goto_high_scores = False
        self.goto_start = False
        self.game_over = False
        self.score = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_r or event.unicode.lower() == 'к'):
            self.goto_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.scores_button.collidepoint(event.pos):
                self.goto_high_scores = True
            elif self.menu_button.collidepoint(event.pos):
                self.goto_start = True

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 20, 50))
        if self.game_over:
            screen.blit(self.game_over_text, self.game_over_rect)
        else:
            screen.blit(self.game_won_text, self.game_won_rect)

        score_text = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        screen.blit(score_text, score_rect)

        screen.blit(self.restart_text, self.restart_rect)

        pygame.draw.rect(screen, (200, 200, 200), self.scores_button)
        scores_text = self.restart_font.render("Рекорды", True, (0, 0, 0))
        scores_rect = scores_text.get_rect(center=self.scores_button.center)
        screen.blit(scores_text, scores_rect)

        pygame.draw.rect(screen, (200, 200, 200), self.menu_button)
        menu_text = self.restart_font.render("В меню", True, (0, 0, 0))
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
