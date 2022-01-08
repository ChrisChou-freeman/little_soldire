import os

import pygame
from pygame import surface, event, Vector2, sprite

from . import lib
from . import sprite as _sprite
from . import settings

class GamePlay(lib.GameManager):
    def __init__(self, metadata: lib.GameMetaData) -> None:
        super().__init__(metadata)
        self._background_lays = lib.com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)
        self._background_lays_pos: list[Vector2] = []
        self._tiles_images = lib.com_fuc.pygame_load_iamges_with_name(settings.TILES_IMG_PATH)
        self._item_images = lib.com_fuc.pygame_load_iamges_with_name(settings.ITEMS_IMG_PATH)
        self._sprite_images = lib.com_fuc.pygame_load_iamges_with_name(settings.SPRITE_IMG_PATH)
        self._layers_repets = 2
        self._current_level = 0
        self._grenade_number = 3
        self._shoot = False
        self._world_data = lib.GameDataStruct.load_world_data(
            os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        )
        self._player_sprites = sprite.Group()
        self._enemy_sprites = sprite.Group()
        self._tile_sprites = sprite.Group()
        self._item_sprites = sprite.Group()
        self._bullet_sprites = sprite.Group()
        self._debug_sprites = sprite.Group()
        self._init_content()

    def _init_sprite(self,
                     sprite: int,
                     position: Vector2) -> None:
        if sprite in settings.PLAYER_TILES:
            player_sprite = _sprite.PlayerSprite(
                settings.PLAYER1_IMG_PATH_MAP,
                position,
                self._tile_sprites,
                self._bullet_sprites,
                self.metadata
            )
            self._player_sprites.add(player_sprite)
        elif sprite in settings.ENEMY_TILES:
            enemy_sprite = _sprite.EnemySprite(
                settings.ENEMY1_IMG_PATH_MAP,
                position,
                self._tile_sprites,
                self._bullet_sprites,
                self._player_sprites,
                self.metadata
            )
            self._enemy_sprites.add(enemy_sprite)

    def _init_word_data(self,
                        data_type: str,
                        datas_info: list[dict[str, int]]) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{data_type}_{img}.png'
            position = Vector2(
                x * settings.TILE_SIZE[0],
                y * settings.TILE_SIZE[1]
            )
            if data_type == settings.IMG_TYPE_TILES:
                img_surface = self._tiles_images[tile_name]
                self._tile_sprites.add(_sprite.TileSprite(img_surface, position, self.metadata))
            elif data_type == settings.IMG_TYPE_SPRITES:
                self._init_sprite(img, position)
            elif data_type == settings.IMG_TYPE_ITEMS:
                img_surface = self._item_images[tile_name]
                self._item_sprites.add(_sprite.ItemSprite(img_surface, position, self.metadata))

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
        key_map = lib.KeyMap(key_event)
        if key_map.key_left_press():
            self.metadata.control_action.RUN_LEFT = True
        elif key_map.key_left_release():
            self.metadata.control_action.RUN_LEFT = False
        elif key_map.key_right_press():
            self.metadata.control_action.RUN_RIGHT = True
        elif key_map.key_right_release():
            self.metadata.control_action.RUN_RIGHT = False
        elif key_map.key_q_press():
            pass
        elif key_map.key_jump_press():
            self.metadata.control_action.JUMPING = True
        elif key_map.key_attack_press():
            self.metadata.control_action.SHOOT = True
        elif key_map.key_attack_release():
            self.metadata.control_action.SHOOT = False
        elif key_map.key_back_press():
            self.metadata.game_mode = settings.GAME_START

    def _update_backgroud_scroll(self) -> None:
        for index, background_vec in enumerate(self._background_lays_pos):
            lay_index = index%len(self._background_lays)
            background_vec.x += self.metadata.scroll_index * ((lay_index+1)/len(self._background_lays))

    def update(self, dt: float) -> None:
        self._tile_sprites.update()
        self._item_sprites.update()
        self._player_sprites.update(dt=dt)
        self._enemy_sprites.update(dt=dt)
        self._bullet_sprites.update(dt=dt)
        self._update_backgroud_scroll()

    def death_shady(self, screen: surface.Surface) -> None:
        if not self.metadata.GAME_OVER:
            return
        sur = surface.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        sur.fill(settings.RGBA_BLACK)
        screen.blit(sur, (0, 0))

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index%len(self._background_lays)]
            screen.blit(lay, lay_pos)
        self._tile_sprites.draw(screen)
        self._item_sprites.draw(screen)
        self._player_sprites.draw(screen)
        self._enemy_sprites.draw(screen)
        self._bullet_sprites.draw(screen)
        self.death_shady(screen)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

