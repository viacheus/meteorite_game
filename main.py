import pygame
import sys
import os
import random
from character import character
from earth import Earth
from meteorite import Meteor

pygame.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


def main():
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

    game_over_font = pygame.font.Font(None, 74)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key in range(pygame.K_0, pygame.K_9 + 1):
                    number = event.key - pygame.K_0
                    current_answer += str(number)
                elif event.key == pygame.K_RETURN:
                    meteors_to_remove = set()
                    for meteor in meteors:
                        if meteor.check_answer(current_answer):
                            meteors_to_remove.add(meteor)
                            meteor.kill()
                    meteors -= meteors_to_remove
                    current_answer = ""

        if not game_over:
            if current_time - last_meteor_time >= 3000:  # через сколько секунд спавн метеорита
                meteor = Meteor()
                meteor.rect = meteor.image.get_rect()
                meteor.rect.x = random.randrange(WINDOW_WIDTH - 30)
                meteor.rect.y = 0
                all_sprites.add(meteor)
                meteors.add(meteor)
                last_meteor_time = current_time

            for meteor in list(meteors):
                if meteor.update():
                    game_over = True
                    break

        screen.fill((0, 0, 50))
        all_sprites.draw(screen)
        if not game_over:
            all_sprites.update()
        else:
            screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
