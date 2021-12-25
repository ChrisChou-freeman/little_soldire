import os

from pygame import surface, event, Vector2

from .lib import GameManager, com_fuc, KeyMap, GameDataStruct
# from .sprite import
from . import settings

class GamePlay(GameManager):
    def __init__(self, metadata: dict[str, str]) -> None:
        super().__init__(metadata)
        self._background_lays = com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)
        self._background_lays_pos: list[Vector2] = []
        self._tiles_images = com_fuc.pygame_load_iamges_with_name(settings.TILES_IMG_PATH)
        self._item_images = com_fuc.pygame_load_iamges_with_name(settings.ITEMS_IMG_PATH)
        self._sprite_images = com_fuc.pygame_load_iamges_with_name(settings.SPRITE_IMG_PATH)
        self._layers_repets = 2
        self._current_level = 0
        self._surface_scroll_value = 0
        self._run_speed = 1 * len(self._background_lays)
        self._grenade_number = 3
        self._run_left = False
        self._run_right = False
        self._shoot = False
        self._world_data_path = os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        self._world_data = GameDataStruct.load_world_data(self._world_data_path)
        self._init_content()

    def _init_content(self) -> None:
        # init background
        last_layer_width = self._background_lays[-1].get_width()
        self._background_lays_pos = [Vector2(r * last_layer_width, i*80) \
                for r in range(self._layers_repets) \
                for i in range(len(self._background_lays))]

    def handle_input(self, key_event: event.Event) -> None:
        key_map = KeyMap(key_event)
        if key_map.key_left_press():
            self._run_left = True
        elif key_map.key_left_release():
            self._run_left = False
        elif key_map.key_right_press():
            self._run_right = True
        elif key_map.key_right_release():
            self._run_right = False
        elif key_map.key_q_press():
            pass
        elif key_map.key_jump_press():
            pass
        elif key_map.key_attack_press():
            self._shoot = True
        elif key_map.key_attack_release():
            self._shoot = False
        elif key_map.key_back_press():
            print('back')
            self.metadata['game_mode'] = settings.GAME_START

    def update(self, dt: float) -> None:
        ...

    def _draw_sprite(self,
                     screen: surface.Surface,
                     sprite: int,
                     position: Vector2) -> None:
        sprite_img_path_map: dict[str, dict[str, str]] = {}
        if sprite in settings.PLAYER_TILES:
            sprite_img_path_map = settings.PLAYER1_IMG_PATH_MAP
        elif sprite in settings.ENEMY_TILES:
            sprite_img_path_map = settings.ENEMY1_IMG_PATH_MAP
        idle_sheet = sprite_img_path_map['idle']

    def _draw_world_data(self,
            screen: surface.Surface,
            datas_info: list[dict[str, int]],
            img_type: str) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{img_type}_{img}.png'
            img_surface: surface.Surface|None = None
            position = Vector2(
                x * settings.TILE_SIZE[0] + self._surface_scroll_value,
                y * settings.TILE_SIZE[1]
            )
            if img_type == settings.IMG_TYPE_TILES:
                img_surface = self._tiles_images[tile_name]
            elif img_type == settings.IMG_TYPE_SPRITES:
                img_surface = self._sprite_images[tile_name]
                self._draw_sprite(screen, img, position)
            elif img_type == settings.IMG_TYPE_ITEMS:
                img_surface = self._item_images[tile_name]
            if img_surface is not None:
                screen.blit(img_surface, position)

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index%len(self._background_lays)]
            screen.blit(lay, lay_pos)
        self._draw_world_data(screen, self._world_data.tiles_data, settings.IMG_TYPE_TILES)
        self._draw_world_data(screen, self._world_data.items_data, settings.IMG_TYPE_ITEMS)
        self._draw_world_data(screen, self._world_data.sprites_data, settings.IMG_TYPE_SPRITES)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

