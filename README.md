Ball needs collisions with the player and the edges of the screen
It gets an actual image
Ball needs be active and passive

Collision problem
horizontal movement -> horizontal collision -> vertical movement -> vertical collision
we only check the sides of the object, but need to check both the left and right sides
and check where the ball was in the previous frame
this logic we need to apply for every side of ball (top, left, bot, right)
(tunneling problem in gamedev tunneling.png)
we see that ball don't move over the other object, but collides
we need that because ball can bounce from different sides of sprites

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

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.active = False
            self.direction.y *= -1

# Blocks
Creating layout and blocks that should scale by window size
We specified clock_map and block size to create the block grid for our game
Cycle through all rows and cols of block map to find x and y pos of each block
enumerate((5, 6, 7)) = [[1, 5], [2, 6], [3, 7]]

def stage_setup(self) -> None:
    for row_index, row in enumerate(BLOCK_MAP):
        for col_index, col in enumerate(row):
            if col != ' ':
                x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                Block(block_type=col, pos=(x, y), groups=[self.all_sprites, self.block_sprites])


function pass through block_map and compute the position of each block to place on the screen

# Damage
Block.health
if getattr(sprite, 'health', None): Checks if sprite has health attribute

# Graphics
Block is not shrinks by axis, we need to scale only middle component that is not 
changing with scaling to save the quality of the image (scale.png)

SurfaceMaker to automate process of creating images of sprites
def __init__(self):
    os.walk()
('images/blocks', ['blue', 'bronce', 'green', 'grey', 'orange', 'player', 'purple', 'red'], [])
('images/blocks\\blue', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\bronce', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\green', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\grey', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\orange', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\player', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\purple', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])
('images/blocks\\red', [], ['bottom.png', 'bottomleft.png', 'bottomright.png', 'center.png', 'left.png', 'right.png', 'top.png', 'topleft.png', 'topright.png'])


for image_name in info[2]:
    color_type = list(self.assets.keys())[index - 1]
    full_path = 'images/blocks' + f"/{color_type}/" + image_name
    surf = pygame.image.load(full_path).convert_alpha()
    self.assets[color_type][image_name.split('.')[0]] = surf

This for loop loads to assets dict the pygame Surface object with information about
the images used

image.set_colorkey((0, 0, 0))
To put away black parts of image on the corners

# Adding hearts
Player.hearts
if event.type == pygame.QUIT or self.player.hearts <= 0:

# Upgrades
Size, Speed, Heart

# CRT cathode ray tube
I added vignette to imitate the tv blinking



112
150