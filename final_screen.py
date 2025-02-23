import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class FinalScreen:
    def __init__(self):
        self.game_over_font = pygame.font.Font(None, 74)
        self.game_over_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.game_won_font = pygame.font.Font(None, 74)
        self.game_won_text = self.game_won_font.render("VICTORY", True, (0, 255, 0))
        self.game_won_rect = self.game_won_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.restart_font = pygame.font.Font(None, 40)
        self.restart_text = self.restart_font.render("Press r to restart", True, (255, 255, 255))
        self.restart_rect = self.restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.goto_game = False
        self.game_over = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.goto_game = True

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 20, 50))
        if self.game_over:
            screen.blit(self.game_over_text, self.game_over_rect)
        else:
            screen.blit(self.game_won_text, self.game_won_rect)
        screen.blit(self.restart_text, self.restart_rect)
