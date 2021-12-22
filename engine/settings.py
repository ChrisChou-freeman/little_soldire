import os

PRO_PATH = os.path.dirname(os.path.abspath(__file__))

# engine stuff
FULL_SCRREN = False
SHOW_FPS = True
FPS = 60
SCREEN_ORG_WIDTH = 800
SCREEN_ORG_HEIGHT = 450
GLOBAL_SCALE = 1
MAX_LEVEL = 5
SCREEN_WIDTH = SCREEN_ORG_WIDTH * GLOBAL_SCALE
SCREEN_HEIGHT = SCREEN_ORG_HEIGHT * GLOBAL_SCALE

# game asset something
TILE_SIZE = (32, 32)
GAME_START_IMG_PATH = os.path.join(PRO_PATH, 'content/image/game_start')
GAME_PLAY_BACK_IMG_PATH = os.path.join(PRO_PATH, 'content/image/background')
TILES_BTN_IMG_PATH = os.path.join(PRO_PATH, 'content/image/button/tileMenu.png')
TILES_IMG_PATH = os.path.join(PRO_PATH, 'content/image/tiles')
SPRITE_IMG_PATH = os.path.join(PRO_PATH, 'content/image/sprites')
ITEMS_IMG_PATH = os.path.join(PRO_PATH, 'content/image/items')
WORLD_DATA_PATH = os.path.join(PRO_PATH, 'content/data/world/')
IMG_TYPE_TILES = TILES_IMG_PATH.split('/')[-1]
IMG_TYPE_ITEMS = ITEMS_IMG_PATH.split('/')[-1]
IMG_TYPE_SPRITES = SPRITE_IMG_PATH.split('/')[-1]

# game mode
GAME_START = 'Game Start'
GAME_PLAY = 'Play'
GAME_EDITOR = 'Editor'
GAME_EXIT = 'Exit'

# rgb color
RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)
RGB_YELLOW = (255, 255, 0)
RGB_GRAY = (190, 190, 190)
RGB_RED = (255, 0, 0)

#other
GAME_TITLE = 'little soldire'
