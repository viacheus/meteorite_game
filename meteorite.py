import pygame

from common import load_image
import random


class Meteor(pygame.sprite.Sprite):
    MATH_PROBLEMS = { # какие примеры
        ("2+3", 5),
        ("4+2", 6),
        ("8-3", 5),
        ("3×2", 6),
        ("10-7", 3),
        ("2×4", 8),
        ("7+1", 8),
        ("6+6", 12),
        ("15-8", 7),
        ("3+4", 7),
        ("1+1", 2),
        ("1+2", 3),
        ("1+3", 4),
        ("1+4", 5),
        ("1+5", 6),
        ("1+6", 7),
        ("1+7", 8),
        ("1+8", 9),
        ("1+9", 10),
        ("1+10", 11),
        ("1+11", 12),
        ("1+12", 13),
        ("1+13", 14),
        ("1+14", 15),
        ("1+15", 16),
        ("1+16", 17),
        ("1+17", 18),
        ("1+18", 19),
        ("1+19", 20),
        ("1+20", 21),
        ("2+1", 3),
        ("2+2", 4),
        ("2+3", 5),
        ("2+4", 6),
        ("2+5", 7),
        ("2+6", 8),
        ("2+7", 9),
        ("2+8", 10),
        ("2+9", 11),
        ("2+10", 12),
        ("2+11", 13),
        ("2+12", 14),
        ("2+13", 15),
        ("2+14", 16),
        ("2+15", 17),
        ("2+16", 18),
        ("2+17", 19),
        ("2+18", 20),
        ("2+19", 21),
        ("2+20", 22),
        ("3+1", 4),
        ("3+2", 5),
        ("3+3", 6),
        ("3+4", 7),
        ("3+5", 8),
        ("3+6", 9),
        ("3+7", 10),
        ("3+8", 11),
        ("3+9", 12),
        ("3+10", 13),
        ("3+11", 14),
        ("3+12", 15),
        ("3+13", 16),
        ("3+14", 17),
        ("3+15", 18),
        ("3+16", 19),
        ("3+17", 20),
        ("3+18", 21),
        ("3+19", 22),
        ("3+20", 23),
        ("4+1", 5),
        ("4+2", 6),
        ("4+3", 7),
        ("4+4", 8),
        ("4+5", 9),
        ("4+6", 10),
        ("4+7", 11),
        ("4+8", 12),
        ("4+9", 13),
        ("4+10", 14),
        ("4+11", 15),
        ("4+12", 16),
        ("4+13", 17),
        ("4+14", 18),
        ("4+15", 19),
        ("4+16", 20),
        ("4+17", 21),
        ("4+18", 22),
        ("4+19", 23),
        ("4+20", 24),
        ("5+1", 6),
        ("5+2", 7),
        ("5+3", 8),
        ("5+4", 9),
        ("5+5", 10),
        ("5+6", 11),
        ("5+7", 12),
        ("5+8", 13),
        ("5+9", 14),
        ("5+10", 15),
        ("5+11", 16),
        ("5+12", 17),
        ("5+13", 18),
        ("5+14", 19),
        ("5+15", 20),
        ("5+16", 21),
        ("5+17", 22),
        ("5+18", 23),
        ("5+19", 24),
        ("5+20", 25),
        ("20+15", 35),
        ("20+16", 36),
        ("20+17", 37),
        ("20+18", 38),
        ("20+19", 39),
        ("20+20", 40)
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
