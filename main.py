import pygame

from pygame import mixer, QUIT

from final_screen import FinalScreen
from constants import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game
from start_screen import StartScreen
from settings_screen import SettingsScreen
from database import init_db
from high_scores_screen import HighScoresScreen


def start_background_music():
    mixer.music.load("data/guitar1.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=-1)


def main():
    pygame.init()
    mixer.init()

    db_conn = init_db()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Meteorite")
    clock = pygame.time.Clock()
    start_background_music()

    game = Game(db_conn)
    final_screen = FinalScreen()
    start_screen = StartScreen()
    settings_screen = SettingsScreen(db_conn)
    high_scores_screen = HighScoresScreen(db_conn)

    running = True
    current_screen = start_screen
    previous_screen = None

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            current_screen.handle_event(event)

        current_screen.update()
        current_screen.draw(screen)

        if current_screen == start_screen:
            if start_screen.goto_game:
                current_screen = game
                start_screen.goto_game = False
            elif start_screen.goto_settings:
                current_screen = settings_screen
                start_screen.goto_settings = False
            elif start_screen.goto_high_scores:
                current_screen = high_scores_screen
                start_screen.goto_high_scores = False
        elif current_screen == game and game.goto_final_screen:
            current_screen = final_screen
            game.goto_final_screen = False
            final_screen.game_over = game.game_over
            final_screen.score = game.score
        elif current_screen == final_screen:
            if final_screen.goto_game:
                current_screen = game
                final_screen.goto_game = False
                game.init_game()
            elif final_screen.goto_high_scores:
                current_screen = high_scores_screen
                final_screen.goto_high_scores = False
            elif final_screen.goto_start:
                current_screen = start_screen
                final_screen.goto_start = False
                game = Game(db_conn)  # Create a fresh game instance
        elif current_screen == settings_screen and settings_screen.goto_start:
            current_screen = start_screen
            settings_screen.goto_start = False
        elif current_screen == high_scores_screen and high_scores_screen.goto_start:
            if isinstance(previous_screen, FinalScreen):
                current_screen = final_screen
            else:
                current_screen = start_screen
            high_scores_screen.goto_start = False

        # Keep track of previous screen for proper back navigation
        if current_screen != high_scores_screen:
            previous_screen = current_screen

        pygame.display.flip()
        clock.tick(FPS)
    db_conn.close()
    mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
