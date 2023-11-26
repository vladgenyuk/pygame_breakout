import pygame

from random import randint

from surfacemaker import SurfaceMaker
from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(
            self,
            block_type: str,
            pos: tuple,
            groups: pygame.sprite.Group,
            surface_maker: SurfaceMaker,
            create_upgrade
    ) -> None:
        super().__init__(groups)

        self.surface_maker = surface_maker
        self.image = self.surface_maker.get_surf(COLOR_PALETTE.get(str(block_type)), (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.health = int(block_type)

        self.create_upgrade = create_upgrade

    def get_damage(self, amount: int) -> None:
        self.health -= amount

        if self.health > 0:
            self.image = self.surface_maker.get_surf(COLOR_PALETTE.get(str(self.health)), (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            if randint(0, 10) < 5:
                self.create_upgrade(self.rect.center)
            self.kill()
