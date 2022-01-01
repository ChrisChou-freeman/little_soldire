import os

from pygame import surface, event, Vector2, sprite

from .lib import GameManager, com_fuc, KeyMap, GameDataStruct
from .sprite import RoleSprite, TileSprite, ItemSprite, PlayerSprite
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
        self._run_speed = 3
        self._grenade_number = 3
        self._gravity = self._run_speed*0.7
        self._run_left = False
        self._run_right = False
        self._shoot = False
        self._world_data_path = os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        self._world_data = GameDataStruct.load_world_data(self._world_data_path)
        self._player_sprites = sprite.Group()
        self._enemy_sprites = sprite.Group()
        self._tile_sprite = sprite.Group()
        self._item_sprite = sprite.Group()
        self._player_acttion = 'idle'
        self._init_content()

    def _init_sprite(self,
                     sprite: int,
                     position: Vector2) -> None:
        if sprite in settings.PLAYER_TILES:
            player_sprite = PlayerSprite(settings.PLAYER1_IMG_PATH_MAP, position, self._world_data)
            self._player_sprites.add(player_sprite)
        elif sprite in settings.ENEMY_TILES:
            enemy_sprite = RoleSprite(settings.ENEMY1_IMG_PATH_MAP, position)
            self._enemy_sprites.add(enemy_sprite)

    def _init_word_data(self,
                        data_type: str,
                        datas_info: list[dict[str, int]]) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{data_type}_{img}.png'
            position = Vector2(
                x * settings.TILE_SIZE[0] + self._surface_scroll_value,
                y * settings.TILE_SIZE[1]
            )
            if data_type == settings.IMG_TYPE_TILES:
                img_surface = self._tiles_images[tile_name]
                self._tile_sprite.add(TileSprite(img_surface, position))
            elif data_type == settings.IMG_TYPE_SPRITES:
                self._init_sprite(img, position)
            elif data_type == settings.IMG_TYPE_ITEMS:
                img_surface = self._item_images[tile_name]
                self._item_sprite.add(ItemSprite(img_surface, position))

    def _init_content(self) -> None:
        # init background
        last_layer_width = self._background_lays[-1].get_width()
        self._background_lays_pos = [Vector2(r * last_layer_width, i*80) \
                for r in range(self._layers_repets) \
                for i in range(len(self._background_lays))]
        # init tiles and items
        self._init_word_data(settings.IMG_TYPE_ITEMS, self._world_data.items_data)
        self._init_word_data(settings.IMG_TYPE_TILES, self._world_data.tiles_data)
        self._init_word_data(settings.IMG_TYPE_SPRITES, self._world_data.sprites_data)

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
            self.metadata['game_mode'] = settings.GAME_START

    def _get_player_vec(self) -> Vector2:
        x = 0
        y = self._gravity
        if self._run_left:
            x += (self._run_speed*-1)
        elif self._run_right:
            x += (self._run_speed)
        return Vector2(x, y)

    def _get_player_acttion(self) -> str:
        action = 'idle'
        if self._run_left:
            action = 'run_left'
        elif self._run_right:
            action = 'run_right'
        return action

    def update(self, dt: float) -> None:
        self._tile_sprite.update()
        self._item_sprite.update()
        self._player_sprites.update(
            dt=dt,
            vec=self._get_player_vec(),
            action=self._get_player_acttion()
        )
        self._enemy_sprites.update(dt=dt)

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index%len(self._background_lays)]
            screen.blit(lay, lay_pos)
        self._tile_sprite.draw(screen)
        self._item_sprite.draw(screen)
        self._player_sprites.draw(screen)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

