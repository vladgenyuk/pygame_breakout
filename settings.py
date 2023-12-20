WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

LEVEL_1 = [
    '11111111111111111',
    '44455775544111111',
    '33333333333333333',
    '22222222222111111',
    '11111111111 ',
    '            ',
    '             ',
    '            ',
    '            '
]
# LEVEL_1 = [
#     # '11111111111111111',
#     # '11111111111111111',
#     # '11111111111111111',
#     # '11111111111111111',
#     '11111111111111111',
#     '11111111111111111',
#     '11111111111111111',
#     '            ',
#     '            '
# ]

LEVEL_2 = [
    '            ',
    '777777777777777',
    '656756776575756',
    '555555555555555',
    '121221122112211',
    '333333333333333',
    '            ',
    '            ',
    '            ',
]

COLOR_PALETTE = {
    '1': 'blue',
    '2': 'green',
    '3': 'red',
    '4': 'orange',
    '5': 'purple',
    '6': 'bronce',
    '7': 'grey',
}

DAMAGE = 1
GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(LEVEL_1) - GAP_SIZE
BLOCK_WIDTH = WINDOW_WIDTH / len(LEVEL_1[0]) - GAP_SIZE
TOP_OFFSET = WINDOW_HEIGHT // 30

UPGRADES = ['speed', 'heart', 'size', 'duplet', 'damage', 'ball_size', 'delete']
