import os

FULL_SCRREN = False
FPS = 60
SCREEN_ORG_WIDTH = 800
SCREEN_ORG_HEIGHT = 450
GLOBAL_SCALE = 1
RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)
RGB_YELLOW = (255, 255, 0)
TILE_SIZE = (32, 32)
SCREEN_WIDTH = SCREEN_ORG_WIDTH * GLOBAL_SCALE
SCREEN_HEIGHT = SCREEN_ORG_HEIGHT * GLOBAL_SCALE
PRO_PATH = os.path.dirname(os.path.abspath(__file__))
GAME_START_IMG_PATH = os.path.join(PRO_PATH, 'content/image/game_start')
GAME_PLAY_BACK_IMG_PATH = os.path.join(PRO_PATH, 'content/image/background')
TILES_BTN_IMG_PATH = os.path.join(PRO_PATH, 'content/image/button/tileMenu.png')
