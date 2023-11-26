import pygame

from os import walk


class SurfaceMaker:
    def __init__(self):
        for index, info in enumerate(walk('images/blocks')):
            if index == 0:
                self.assets = {color: {} for color in info[1]}
            else:
                for image_name in info[2]:
                    color_type = list(self.assets.keys())[index - 1]
                    full_path = 'images/blocks' + f"/{color_type}/" + image_name
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.assets[color_type][image_name.split('.')[0]] = surf

                    # prints COLOR images/blocks/COLOR/DETAIL.PNG
                    # COLOR from self.assets
                    # DETAIL.PNG from list('bottom.png'...., 'topright.png')
                    # print(color_type, full_path)

    # create all graphics
    # create one surface with the graphics with any size
    # ret that image to the blocks or the player

    def get_surf(self, block_type, size):
        image = pygame.Surface(size)
        image.set_colorkey((0, 0, 0))
        sides = self.assets.get(block_type)

        image.blit(sides.get('topleft'), (0, 0))
        image.blit(sides.get('topright'), (size[0] - sides['topright'].get_width(), 0))  # BLOCK_WIDTH - PNG SIZE
        image.blit(sides.get('bottomright'), (size[0] - sides['bottomright'].get_width(), size[1] - sides['bottomright'].get_height()))
        image.blit(sides.get('bottomleft'), (0, size[1] - sides['bottomright'].get_height()))

        top_width = size[0] - (sides.get('topleft').get_width() + sides.get('topright').get_width())  # BLOCK_WIDTH - 2 * sides.['middle'].get_width()
        scaled_top_surf = pygame.transform.scale(sides.get('top'), (top_width, sides.get('top').get_height()))
        image.blit(scaled_top_surf, (sides.get('topleft').get_width(), 0))

        left_height = size[1] - (sides.get('topleft').get_height() + sides.get('bottomleft').get_height())
        scaled_left_surf = pygame.transform.scale(sides.get('left'), (sides.get('left').get_width(), left_height))
        image.blit(scaled_left_surf, (0, sides.get('topleft').get_height()))

        right_height = size[1] - (sides.get('topright').get_height() + sides.get('bottomright').get_height())
        scaled_right_surf = pygame.transform.scale(sides.get('right'), (sides.get('right').get_width(), right_height))
        image.blit(scaled_right_surf, (size[0] - sides.get('right').get_width(), sides.get('topright').get_height()))

        bot_width = size[0] - (sides.get('bottomleft').get_width() + sides.get('bottomleft').get_width())
        scaled_bot_surf = pygame.transform.scale(sides.get('bottom'), (bot_width, sides.get('bottom').get_height()))
        image.blit(scaled_bot_surf, (sides.get('bottomleft').get_width(), size[1] - sides.get('bottom').get_height()))

        center_width = size[0] - (sides.get('right').get_width() + sides.get('left').get_width())
        center_height = size[1] - (sides.get('top').get_height() + sides.get('bottom').get_height())
        scaled_center = pygame.transform.scale(sides.get('center'), (center_width, center_height))
        image.blit(scaled_center, sides.get('topleft').get_size())

        return image
