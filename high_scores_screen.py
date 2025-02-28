import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from database import get_high_scores


class HighScoresScreen:
    def __init__(self, conn):
        self.conn = conn
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        self.goto_start = False
        self.back_button = pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 100, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.goto_start = True

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 20, 50))

        title = self.font_title.render("Рекорды", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WINDOW_WIDTH / 2, 50))
        screen.blit(title, title_rect)

        scores = get_high_scores(self.conn)
        for i, score in enumerate(scores):
            score_text = f"{i + 1}. {score[2]} очков"
            text = self.font_text.render(score_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 120 + i * 40))
            screen.blit(text, text_rect)

        pygame.draw.rect(screen, (200, 200, 200), self.back_button)
        back_text = self.font_text.render("Назад", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)
