import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from database import save_settings, get_settings


class SettingsScreen:
    def __init__(self, conn):
        self.conn = conn
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.goto_start = False

        self.current_level = 1
        self.level_buttons = [
            pygame.Rect(50 + i * 100, 80, 80, 40) for i in range(5)
        ]

        self.load_level_settings(self.current_level)

        self.save_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 50)

    def load_level_settings(self, level_id):
        saved_settings = get_settings(self.conn, level_id)

        self.settings = {
            'sum': pygame.Rect(50, 150, 20, 20),
            'sub': pygame.Rect(150, 150, 20, 20),
            'mul': pygame.Rect(250, 150, 20, 20),
            'div': pygame.Rect(350, 150, 20, 20),
            'complexity': pygame.Rect(450, 150, 60, 30),
            'complexity_value': 5 if not saved_settings else saved_settings[5] or 5,
            'complexity_active': False,
            'checked': {
                'sum': True if not saved_settings else bool(saved_settings[1]),
                'sub': True if not saved_settings else bool(saved_settings[2]),
                'mul': False if not saved_settings else bool(saved_settings[3]),
                'div': False if not saved_settings else bool(saved_settings[4])
            }
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.level_buttons, 1):
                if button.collidepoint(event.pos):
                    self.current_level = i
                    self.load_level_settings(self.current_level)
                    return

            if self.save_button.collidepoint(event.pos):
                self.save_settings()
                self.goto_start = True

            for op in ['sum', 'sub', 'mul', 'div']:
                if self.settings[op].collidepoint(event.pos):
                    if not (self.settings['checked'][op] and sum(self.settings['checked'].values()) == 1):
                        self.settings['checked'][op] = not self.settings['checked'][op]
            if self.settings['complexity'].collidepoint(event.pos):
                self.settings['complexity_active'] = True

        elif event.type == pygame.KEYDOWN and self.settings['complexity_active']:
            if event.key == pygame.K_RETURN:
                self.settings['complexity_active'] = False
            elif event.key == pygame.K_BACKSPACE:
                self.settings['complexity_value'] = self.settings['complexity_value'] // 10
            elif event.unicode.isnumeric():
                current = self.settings['complexity_value']
                self.settings['complexity_value'] = min(int(str(current) + event.unicode), 99)

    def save_settings(self):
        settings = {
            'sum': self.settings['checked']['sum'],
            'sub': self.settings['checked']['sub'],
            'mul': self.settings['checked']['mul'],
            'div': self.settings['checked']['div'],
            'complexity': self.settings['complexity_value']
        }
        save_settings(self.conn, self.current_level, settings)

    def draw(self, screen):
        screen.fill((0, 20, 50))

        title = self.title_font.render("Настройки", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

        for i, button in enumerate(self.level_buttons, 1):
            color = (0, 255, 0) if i == self.current_level else (255, 255, 255)
            pygame.draw.rect(screen, color, button, 2)
            level_text = self.font.render(f"Ур.{i}", True, color)
            screen.blit(level_text, (button.x + 10, button.y + 10))

        for op, rect in [('sum', self.settings['sum']), ('sub', self.settings['sub']),
                         ('mul', self.settings['mul']), ('div', self.settings['div'])]:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            if self.settings['checked'][op]:
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(-6, -6))

            op_text = self.font.render({
                                           'sum': '+',
                                           'sub': '-',
                                           'mul': '×',
                                           'div': '÷'
                                       }[op], True, (255, 255, 255))
            screen.blit(op_text, (rect.x - 15, rect.y - 25))

        pygame.draw.rect(screen, (255, 255, 255), self.settings['complexity'], 2)
        complexity_text = self.font.render(str(self.settings['complexity_value']), True, (255, 255, 255))
        screen.blit(complexity_text, (self.settings['complexity'].x + 5, self.settings['complexity'].y + 5))

        if self.settings['complexity_active']:
            pygame.draw.rect(screen, (0, 255, 0), self.settings['complexity'], 2)

        pygame.draw.rect(screen, (0, 255, 0), self.save_button)
        save_text = self.font.render("Сохранить", True, (0, 0, 0))
        screen.blit(save_text, (self.save_button.centerx - save_text.get_width() // 2,
                                self.save_button.centery - save_text.get_height() // 2))

    def update(self):
        pass
