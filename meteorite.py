import pygame

from common import load_image
import random


class Meteor(pygame.sprite.Sprite):
    MATH_PROBLEMS = {
        ("2+3", 5),
        ("4+2", 6),
        ("8-3", 5),
        ("3×2", 6),
        ("10-7", 3),
        ("2×4", 8),
        ("7+1", 8),
        ("6+6", 12),
        ("15-8", 7),
        ("3+4", 7)
    }

    def __init__(self, *group, problem_tuple=None):
        super().__init__(*group)
        self.image = load_image("meteor.png")
        self.problem, self.answer = problem_tuple if problem_tuple else random.choice(tuple(self.MATH_PROBLEMS))

        self.image_with_text = pygame.Surface((self.image.get_width(), self.image.get_height() + 20), pygame.SRCALPHA)
        self.image_with_text.blit(self.image, (0, 5))
        font = pygame.font.Font(None, 24)
        text = font.render(self.problem, True, (0, 255, 0))
        text_rect = text.get_rect(centerx=self.image.get_width() // 2,
                                  top=self.image.get_height() + 5)
        self.image_with_text.blit(text, text_rect)
        self.image = self.image_with_text
        self.rect = self.image.get_rect()

    def check_answer(self, current_answer):
        try:
            return int(current_answer) == self.answer
        except ValueError:
            return False

    def update(self):
        self.rect = self.rect.move(0, 1)
        if self.rect.y > 635:
            self.kill()
            return True
        return False
