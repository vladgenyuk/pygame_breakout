import sys
import time
import pygame

from random import choice

from sprites import Player, Ball, Block, Upgrade
from surfacemaker import SurfaceMaker
from crt_styling import CRT
from settings import *


class Game:
    def __init__(self) -> None:

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout')

        # sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()

        # setup
        self.surface_maker = SurfaceMaker()
        self.player = Player(self.all_sprites, self.surface_maker)
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites, True)
        self.crt = CRT()

        # hearts
        self.heart_surf = pygame.image.load('images/other/heart.png').convert_alpha()

        # sounds
        self.upgrade_sound = pygame.mixer.Sound('sounds/upgrade.wav')
        self.upgrade_sound.set_volume(0.5)
        self.music = pygame.mixer.Sound('sounds/music.mp3')
        self.music.set_volume(0.5)
        self.music.play(loops=-1)

    def set_score(self, score: int) -> None:
        with open('score.txt', 'w') as f:
            f.write(str(score))

    def get_score(self) -> int:
        with open('score.txt', 'r') as f:
            return int(f.read())

    def display_hearts(self) -> None:
        for i in range(self.player.hearts):
            x = 2 + i * (self.heart_surf.get_width() + 2)
            self.display_surface.blit(self.heart_surf, (x, 4))

    def display_damage(self) -> None:
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text_surface = font.render(str(f'Damage: {self.ball.damage}'), True, (0, 0, 0))
        self.display_surface.blit(text_surface, (WINDOW_WIDTH - 100, 4))

    def create_upgrade(self, pos: tuple) -> None:
        upgrade_type = choice(UPGRADES)
        Upgrade(pos, upgrade_type, [self.all_sprites, self.upgrade_sprites])

    def upgrade_collision(self) -> None:
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            if sprite.upgrade_type in ['speed', 'heart', 'size']:
                self.player.upgrade(sprite.upgrade_type)
                self.upgrade_sound.play()
            elif sprite.upgrade_type in ['duplet', 'damage', 'ball_size']:
                self.ball.upgrade(sprite.upgrade_type)
                self.upgrade_sound.play()
            else:
                choice(self.block_sprites.sprites()).kill()
                self.upgrade_sound.play()

    def create_bg(self, size: tuple, image: str) -> pygame.surface.Surface:
        bg_original = pygame.image.load(image).convert()
        scaled = pygame.transform.scale(bg_original, size)  # stretch to 1280 x 720
        return scaled

    def stage_setup(self, level: list) -> None:
        BLOCK_HEIGHT = WINDOW_HEIGHT / len(LEVEL_1) - GAP_SIZE
        BLOCK_WIDTH = WINDOW_WIDTH / len(LEVEL_1[0]) - GAP_SIZE
        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                if col != ' ':
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = TOP_OFFSET + row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(
                        block_type=col,
                        pos=(x, y),
                        groups=[self.all_sprites, self.block_sprites],
                        surface_maker=self.surface_maker,
                        create_upgrade=self.create_upgrade
                    )

    def game(self, level: int) -> None:
        last_time = time.time()

        bg = self.create_bg((WINDOW_WIDTH, WINDOW_HEIGHT), 'images/menu.jpg')
        if level == 1:
            bg = self.create_bg((WINDOW_WIDTH, WINDOW_HEIGHT), 'images/level1.jpg')
            self.stage_setup(LEVEL_1)
        elif level == 2:
            bg = self.create_bg((WINDOW_WIDTH, WINDOW_HEIGHT), 'images/level2.png')
            self.stage_setup(LEVEL_2)

        while True:
            if not bool(self.block_sprites):
                score = self.player.hearts * 2 + self.ball.damage
                print(f"Score: {score}")
                self.set_score(score)
                pygame.quit()
                sys.exit()

            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for sprite in self.all_sprites:
                            if type(sprite).__name__ == 'Ball':
                                sprite.active = True

            # update the game
            self.all_sprites.update(dt)
            self.upgrade_collision()

            # draw the frame
            self.display_surface.blit(bg, (0, 0))
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()
            self.display_damage()

            self.crt.draw()

            pygame.display.update()

    def display_menu_text(self) -> None:
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_surface = font.render("Level 1", True, (0, 0, 0))
        self.display_surface.blit(text_surface, (580, 170))
        text_surface = font.render("Level 2", True, (0, 0, 0))
        self.display_surface.blit(text_surface, (580, 320))
        text_surface = font.render("Exit", True, (0, 0, 0))
        self.display_surface.blit(text_surface, (610, 470))
        score = f'Max score: {self.get_score()}'
        text_surface = font.render(str(score), True, (255, 255, 255))
        self.display_surface.blit(text_surface, (440, 100))

    def menu(self) -> None:
        click = False
        bg = self.create_bg((WINDOW_WIDTH, WINDOW_HEIGHT), 'images/menu.jpg')
        while True:
            self.display_hearts()
            self.display_surface.fill((255, 255, 255))

            button_1 = pygame.Rect((WINDOW_WIDTH - 400) // 2, 150, 400, 100)
            button_2 = pygame.Rect((WINDOW_WIDTH - 400) // 2, 300, 400, 100)
            button_3 = pygame.Rect((WINDOW_WIDTH - 400) // 2, 450, 400, 100)

            mx, my = pygame.mouse.get_pos()

            if button_1.collidepoint((mx, my)):
                if click:
                    self.game(1)
            if button_2.collidepoint((mx, my)):
                if click:
                    self.game(2)
            if button_3.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()

            click = False

            self.display_surface.blit(bg, (0, 0))
            pygame.draw.rect(self.display_surface, (255, 0, 0), button_1)
            pygame.draw.rect(self.display_surface, (255, 0, 0), button_2)
            pygame.draw.rect(self.display_surface, (255, 0, 0), button_3)
            self.display_menu_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()

    def run(self) -> None:
        self.menu()


if __name__ == "__main__":
    game = Game()
    game.run()
