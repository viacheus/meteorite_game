import random

import pygame
from pygame import mixer

from constants import WINDOW_WIDTH
from earth import Earth
from levels import Level, create_levels
from meteorite import Meteor
from database import save_score


class Game:
    def __init__(self, db_conn):
        self.all_sprites = pygame.sprite.Group()
        self.good_exp_sound = mixer.Sound("data/good_sound.wav")

        self.db_conn = db_conn
        # Создаем уровни на основе настроек из базы данных
        self.levels = create_levels(self.db_conn)

        self.init_game()

        self.score_font = pygame.font.Font(None, 54)
        self.score_text = self.score_font.render(str(self.score) + "m", True, (255, 0, 0))
        self.score_rect = self.score_text.get_rect(center=(100, 100))

        self.level_font = pygame.font.Font(None, 54)
        self.level_text = self.score_font.render("current level" + str(self.level_ctr), True, (255, 0, 0))
        self.level_rect = self.score_text.get_rect(center=(100, 100))

    def init_game(self):
        # Инициализация новой игры
        self.score = 0
        self.level_ctr = 1
        self.level = self.levels[self.level_ctr - 1]
        self.meteor_rate = 3000  # Частота появления метеоритов в миллисекундах
        self.game_over = False
        self.goto_start_screen = False
        self.goto_final_screen = False
        self.current_answer = ""  # Текущий ввод игрока
        self.meteors = set()  # Активные метеориты
        self.current_time = 0
        self.last_meteor_time = 0

        # Очистка и создание начальной сцены
        for sprite in self.all_sprites:
            sprite.kill()
        grass = Earth()
        grass.rect = grass.image.get_rect()
        grass.rect.x = 0
        grass.rect.y = 700
        self.all_sprites.add(grass)
        self.levels = create_levels(self.db_conn)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_0, pygame.K_9 + 1):
                # Добавление цифр к ответу
                number = event.key - pygame.K_0
                self.current_answer += str(number)
            elif event.key == pygame.K_RETURN:
                # Проверка ответа при нажатии Enter
                meteors_to_remove = set()
                for meteor in self.meteors:
                    if meteor.check_answer(self.current_answer):
                        meteors_to_remove.add(meteor)
                        self.good_exp_sound.play()
                        meteor.kill()

                prev_score = self.score
                self.score += len(meteors_to_remove)
                # Переход на следующий уровень каждые 4 очка
                if self.score // 4 != prev_score // 4:
                    self.level_ctr += 1
                    if self.level_ctr == len(self.levels):
                        self.goto_final_screen = True
                    else:
                        self.level = self.levels[self.level_ctr - 1]

                self.meteors -= meteors_to_remove
                self.current_answer = ""

    def update(self):
        self.current_time = pygame.time.get_ticks()
        # Создание нового метеорита через заданные промежутки времени
        if self.current_time - self.last_meteor_time >= self.meteor_rate:
            meteor = Meteor(problem_tuple=self.level.get_problem())
            meteor.rect = meteor.image.get_rect()
            meteor.rect.x = random.randrange(WINDOW_WIDTH - 135)
            meteor.rect.y = 0
            self.all_sprites.add(meteor)
            self.meteors.add(meteor)
            self.last_meteor_time = self.current_time

        # Проверка столкновения метеорита с землей
        for meteor in list(self.meteors):
            if meteor.update():
                self.game_over = True
                self.goto_final_screen = True
                save_score(self.db_conn, "Player", self.score, not self.game_over)
                break

        self.all_sprites.update()

    def draw(self, screen):
        screen.fill((0, 0, 50))

        score_text = self.score_font.render(f"{self.score} m", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(60, 30))

        level_text = self.level_font.render(f"Level {self.level_ctr}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(425, 30))

        screen.blit(score_text, score_rect)  # показывать счет
        screen.blit(level_text, level_rect)
        self.all_sprites.draw(screen)
