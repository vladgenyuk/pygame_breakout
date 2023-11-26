import time
import pygame

from random import choice

from sprites.player import Player
from sprites.block import Block

from settings import *


class Ball(pygame.sprite.Sprite):

    def __init__(
            self,
            groups: pygame.sprite.Group,
            player: Player,
            blocks: 'Block',
            main: bool
    ) -> None:
        super().__init__(groups)

        self.main = main
        self.speed = 500
        self.size = 39
        self.damage = 1
        self.active = False

        self.image = self.create_ball()

        # collision objects
        self.player = player
        self.blocks = blocks
        self.all_sprites = groups

        # position setup
        self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2((choice((-1, 1)), -1)) #  x = random(-1, 1) y = -1 at the start to move ball to the top

        # sounds
        self.impact_sound = pygame.mixer.Sound('sounds/impact.mp3')
        self.impact_sound.set_volume(0.5)

        self.fail_sound = pygame.mixer.Sound('sounds/fail.wav ')
        self.fail_sound.set_volume(0.5)

    def upgrade(self, upgrade_type: str) -> None:
        if upgrade_type == 'ball_size':
            self.size += 4
            self.image = self.create_ball()
            self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)
        if upgrade_type == 'damage':
            self.damage += 1
        if upgrade_type == 'duplet':
            Ball(self.all_sprites, self.player, self.blocks, False)
            Ball(self.all_sprites, self.player, self.blocks, False)

    def create_ball(self) -> pygame.surface.Surface:
        ball = pygame.image.load('images/pokeball.png').convert_alpha()
        scaled = pygame.transform.scale(ball, (self.size, self.size))  # stretch to 1280 x 720
        return scaled

    def window_collision(self, direction: str) -> None:
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom >= WINDOW_HEIGHT and self.main:
                self.active = False
                self.direction.y *= -1
                self.player.hearts -= 1
                self.fail_sound.play()

    def collision(self, direction: str) -> None:
        # find overlapping objects
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.impact_sound.play()

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.impact_sound.play()

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(self.damage)

            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.impact_sound.play()

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.impact_sound.play()

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(self.damage)

    def update(self, dt: time) -> None:
        if self.active:

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()  # ball moves with sqrt(2) degree in diagonal direction, need to set it 1

            # create old rect (save)
            self.old_rect = self.rect.copy()

            # movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.window_collision('horizontal')

            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)
            self.collision('vertical')
            self.window_collision('vertical')
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.image = self.create_ball()
