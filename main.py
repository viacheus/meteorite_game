import pygame
import sys
import os
import random

from pygame import mixer

from character import character
from earth import Earth
from meteorite import Meteor

pygame.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Meteorite")
clock = pygame.time.Clock()


def start_background_music():
    mixer.music.load("data/guitar1.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=-1)


def main():
    start_background_music()
    good_exp_sound = mixer.Sound("data/good_sound.wav")
    running = True
    game_over = False
    last_meteor_time = 0
    meteors = set()
    current_answer = ""

    all_sprites = pygame.sprite.Group()

    grass = Earth()
    grass.rect = grass.image.get_rect()
    grass.rect.x = 0
    grass.rect.y = 700
    all_sprites.add(grass)
    score = 0
    level = 1
    score_font = pygame.font.Font(None, 54)
    score_text = score_font.render(str(score) + "m", True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(100, 100))

    level_font = pygame.font.Font(None, 54)
    level_text = score_font.render("current level" + str(level), True, (255, 0, 0))
    level_rect = score_text.get_rect(center=(100, 100))

    game_over_font = pygame.font.Font(None, 74)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    restart_font = pygame.font.Font(None, 40)
    restart_text = restart_font.render("Press r to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()
                return
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key in range(pygame.K_0, pygame.K_9 + 1):
                    number = event.key - pygame.K_0
                    current_answer += str(number)
                elif event.key == pygame.K_RETURN:
                    meteors_to_remove = set()
                    for meteor in meteors:
                        if meteor.check_answer(current_answer):
                            meteors_to_remove.add(meteor)
                            good_exp_sound.play()
                            meteor.kill()

                    prev_score = score
                    score += len(meteors_to_remove)
                    if score // 3 != prev_score // 3:
                        level += 1

                    meteors -= meteors_to_remove
                    current_answer = ""

        if not game_over:

            if current_time - last_meteor_time >= 3000:  # через сколько секунд спавн метеорита для лакримозы здесь всегда верное условие
                meteor = Meteor()
                meteor.rect = meteor.image.get_rect()
                meteor.rect.x = random.randrange(WINDOW_WIDTH - 40)
                meteor.rect.y = 0
                all_sprites.add(meteor)
                meteors.add(meteor)
                last_meteor_time = current_time

            for meteor in list(meteors):
                if meteor.update():
                    game_over = True
                    break

        screen.fill((0, 0, 50))

        score_text = score_font.render(f"{score} m", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(60, 30))

        level_text = level_font.render(f"Level {level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(425, 30))

        screen.blit(score_text, score_rect)  # показывать счет
        screen.blit(level_text, level_rect)
        all_sprites.draw(screen)

        if not game_over:
            all_sprites.update()
        else:
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(FPS)

    # pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    main()
