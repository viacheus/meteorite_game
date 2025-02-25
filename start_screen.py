import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH


class StartScreen:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        self.start_button = pygame.Rect(WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 200, 400,
                                        50)
        self.goto_game = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.goto_game = True

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 80))

        title_text = self.font_title.render("Игра метеориты", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
        screen.blit(title_text, title_rect)

        start_text1 = self.font_text.render(
            "Решайте примеры. Спасайте землю.", True,
            (255, 255, 255))
        start_rect1 = start_text1.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        screen.blit(start_text1, start_rect1)

        pygame.draw.rect(screen, (255, 255, 255), self.start_button)
        button_text = self.font_text.render("начать игру", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=self.start_button.center)
        screen.blit(button_text, button_rect)
