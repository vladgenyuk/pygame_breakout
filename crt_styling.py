import pygame

from random import randint

from settings import *


class CRT:
    def __init__(self):
        vignette = pygame.image.load('images/other/tv.png').convert_alpha()
        self.scaled_vignette = pygame.transform.scale(vignette, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.create_crt_lines()

    def draw(self):
        self.scaled_vignette.set_alpha(randint(60, 75))
        self.display_surface.blit(self.scaled_vignette, (0, 0))

    def create_crt_lines(self):
        line_height = 4
        line_amount = WINDOW_HEIGHT // line_height
        for line in range(line_amount):
            y = line * line_height
            pygame.draw.line(self.scaled_vignette, (10, 10, 10, 100), (0, y), (WINDOW_WIDTH, y), 1)
