import pygame

from pygame import mixer, QUIT

from final_screen import FinalScreen
from constants import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game
from start_screen import StartScreen


def start_background_music():
    mixer.music.load("data/guitar1.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=-1)


def main():
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Meteorite")
    clock = pygame.time.Clock()
    start_background_music()
    game = Game()
    final_screen = FinalScreen()
    start_screen = StartScreen()

    running = True

    current_screen = start_screen

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            current_screen.handle_event(event)

        current_screen.update()
        current_screen.draw(screen)

        if current_screen == start_screen and start_screen.goto_game:
            current_screen = game
            start_screen.goto_game = False
        elif current_screen == game and game.goto_final_screen:
            current_screen = final_screen
            game.goto_final_screen = False
            final_screen.game_over = game.game_over
        elif current_screen == final_screen and final_screen.goto_game:
            current_screen = game
            final_screen.goto_game = False
            game.init_game()

        pygame.display.flip()
        clock.tick(FPS)
    mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
