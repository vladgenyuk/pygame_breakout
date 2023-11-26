import time
import pygame

from surfacemaker import SurfaceMaker
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(
            self,
            groups: pygame.sprite.Group,
            surface_maker: SurfaceMaker
    ) -> None:
        super().__init__(groups)

        self.hearts = 3

        self.surface_maker = surface_maker
        self.image = self.surface_maker.get_surf('player', (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        # self.image.fill('red')

        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
        self.old_rect = self.rect.copy()

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 500

    def upgrade(self, upgrade_type) -> None:
        if upgrade_type == 'speed':
            self.speed += 50
        if upgrade_type == 'heart':
            self.hearts += 1
        if upgrade_type == 'size':
            new_width = self.rect.width * 1.1
            self.image = self.surface_maker.get_surf('player', (new_width, self.rect.height))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x

    def keyboard_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def screen_constraint(self) -> None:
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def update(self, dt: time) -> None:
        self.old_rect = self.rect.copy()
        self.keyboard_input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraint()
