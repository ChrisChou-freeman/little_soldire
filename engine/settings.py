import os

PRO_PATH = os.path.dirname(os.path.abspath(__file__))

# engine stuff
FULL_SCRREN = True
SHOW_FPS = True
FPS = 60
SCREEN_ORG_WIDTH = 800
SCREEN_ORG_HEIGHT = 450
GLOBAL_SCALE = 1
MAX_LEVEL = 5
SCREEN_WIDTH = SCREEN_ORG_WIDTH * GLOBAL_SCALE
SCREEN_HEIGHT = SCREEN_ORG_HEIGHT * GLOBAL_SCALE
MOVE_SPEED = 3
# GRAVITY = MOVE_SPEED * 0.7
GRAVITY = 0.75
MAX_GRAVITY = 6
JUMP_FORCE = -11

# game rules
GRENADE_NUMBER = 3
PLAYER_DAMEGE = 15
ENEMY_DAMEGE = 10
GRENADE_DAMEGE = 50
BULLET_LIFE_TIME = FPS * 1

# game asset something
TILE_SIZE = (32, 32)
GAME_START_IMG_PATH = os.path.join(PRO_PATH, 'content/image/game_start')
GAME_PLAY_BACK_IMG_PATH = os.path.join(PRO_PATH, 'content/image/background')
TILES_BTN_IMG_PATH = os.path.join(PRO_PATH, 'content/image/button/tileMenu.png')
BULLET_IMG_PATH = os.path.join(PRO_PATH, 'content/image/bullet.png')
GRENADE_IMG_PATH = os.path.join(PRO_PATH, 'content/image/grenade.png')
EXPLODE_IMG_PATH = os.path.join(PRO_PATH, 'content/image/vex/explosion.png')
NOTICE_IMG_PATH = os.path.join(PRO_PATH, 'content/image/notice.png')
TILES_IMG_PATH = os.path.join(PRO_PATH, 'content/image/tiles')
SPRITE_IMG_PATH = os.path.join(PRO_PATH, 'content/image/sprites')
ITEMS_IMG_PATH = os.path.join(PRO_PATH, 'content/image/items')
WORLD_DATA_PATH = os.path.join(PRO_PATH, 'content/data/world/')
PLAYER1_IMG_PATH_MAP = {
    'idle': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/player/idle.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'run': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/player/run.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'jump': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/player/jump.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'death': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/player/death.png'),
        'fram_with': '35',
        'loop': '0'
    }
}
ENEMY1_IMG_PATH_MAP = {
     'idle_hit': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/idle_hit.png'),
        'fram_with': '28',
        'loop': '1'
    },
     'idle': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/idle.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'run_hit': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/run_hit.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'run': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/run.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'jump': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/jump.png'),
        'fram_with': '28',
        'loop': '1'
    },
    'death_hit': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/death_hit.png'),
        'fram_with': '35',
        'loop': '0'
    },
    'death': {
        'image_sheet': os.path.join(PRO_PATH, 'content/image/enemy/death.png'),
        'fram_with': '35',
        'loop': '0'
    }
}
IMG_TYPE_TILES = TILES_IMG_PATH.split('/')[-1]
IMG_TYPE_ITEMS = ITEMS_IMG_PATH.split('/')[-1]
IMG_TYPE_SPRITES = SPRITE_IMG_PATH.split('/')[-1]
PLAYER_TILES = [1,]
ENEMY_TILES = [2,]

# no collition sprite list
NO_COLLITION_SPRITE = (9, 10)

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

# rgba color
RGBA_BLACK = (0, 0, 0, 100)

#other
GAME_TITLE = 'little soldire'
