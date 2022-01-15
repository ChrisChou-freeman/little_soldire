import os
import random

import pygame as pg

from . import lib, sprite as _sprite, settings, ui

CONTINUE_MENU_LIST = [
    'Restart',
    'Exit'
]

class GamePlay(lib.GameManager):
    def __init__(self, metadata: lib.GameMetaData) -> None:
        super().__init__(metadata)
        self._background_lays = lib.com_fuc.pygame_load_images_list(
            settings.GAME_PLAY_BACK_IMG_PATH)
        self._tiles_images = lib.com_fuc.pygame_load_iamges_with_name(
            settings.TILES_IMG_PATH)
        self._item_images = lib.com_fuc.pygame_load_iamges_with_name(
            settings.ITEMS_IMG_PATH)
        self._sprite_images = lib.com_fuc.pygame_load_iamges_with_name(
            settings.SPRITE_IMG_PATH)
        self._init()

    def _init(self) -> None:
        self.metadata.control_action = lib.com_type.ControlAction()
        self.metadata.GAME_OVER = False
        self._background_lays_pos: list[pg.Vector2] = []
        self._layers_repets = 2
        self._current_level = 0
        self._grenade_number = 3
        self._shoot = False
        self._game_pause = False
        self._world_data = lib.GameDataStruct.load_world_data(
            os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        )
        self._player_sprites = pg.sprite.Group()
        self._enemy_sprites = pg.sprite.Group()
        self._tile_sprites = pg.sprite.Group()
        self._item_sprites = pg.sprite.Group()
        self._bullet_sprites = pg.sprite.Group()
        self._debug_sprites = pg.sprite.Group()
        self._grenade_sprites = pg.sprite.Group()
        self._explode_sprites = pg.sprite.Group()
        self._continue_menu_list: list[ui.Menu] = []
        self._selected_continue_menu = 0
        self._init_content()

    def _init_continue_menus(self) -> None:
        menu_size = 35
        menu_gap = 30
        for index, m in enumerate(CONTINUE_MENU_LIST):
            menu = ui.Menu(
                m,
                pg.Vector2(
                    settings.SCREEN_WIDTH//2,
                    settings.SCREEN_HEIGHT//2 + menu_gap * index
                ),
                menu_size,
                True
            )
            self._continue_menu_list.append(menu)

    def _init_sprite(self,
                     sprite: int,
                     position: pg.Vector2) -> None:
        if sprite in settings.PLAYER_TILES:
            player_sprite = _sprite.PlayerSprite(
                settings.PLAYER1_IMG_PATH_MAP,
                position,
                self._tile_sprites,
                self._bullet_sprites,
                self._grenade_sprites,
                self._explode_sprites,
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
                self._grenade_sprites,
                self._explode_sprites,
                self.metadata
            )
            self._enemy_sprites.add(enemy_sprite)

    def _init_word_data(self,
                        data_type: str,
                        datas_info: list[dict[str, int]]) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{data_type}_{img}.png'
            position = pg.Vector2(
                x * settings.TILE_SIZE[0],
                y * settings.TILE_SIZE[1]
            )
            if data_type == settings.IMG_TYPE_TILES:
                img_surface = self._tiles_images[tile_name]
                self._tile_sprites.add(_sprite.TileSprite(
                    img_surface, position, self.metadata))
            elif data_type == settings.IMG_TYPE_SPRITES:
                self._init_sprite(img, position)
            elif data_type == settings.IMG_TYPE_ITEMS:
                img_surface = self._item_images[tile_name]
                self._item_sprites.add(_sprite.ItemSprite(
                    img_surface, position, self.metadata))

    def _init_content(self) -> None:
        # init background
        last_layer_width = self._background_lays[-1].get_width()
        self._background_lays_pos = [pg.Vector2(r * last_layer_width, i*80)
                                     for r in range(self._layers_repets)
                                     for i in range(len(self._background_lays))]
        # init tiles and items
        self._init_word_data(settings.IMG_TYPE_ITEMS,
                             self._world_data.items_data)
        self._init_word_data(settings.IMG_TYPE_TILES,
                             self._world_data.tiles_data)
        self._init_word_data(settings.IMG_TYPE_SPRITES,
                             self._world_data.sprites_data)
        # init continue menu
        self._init_continue_menus()

    def handle_input_player(self, key_map: lib.KeyMap) -> None:
        if key_map.key_left_press():
            self.metadata.control_action.RUN_LEFT = True
        elif key_map.key_left_release():
            self.metadata.control_action.RUN_LEFT = False
        elif key_map.key_right_press():
            self.metadata.control_action.RUN_RIGHT = True
        elif key_map.key_right_release():
            self.metadata.control_action.RUN_RIGHT = False
        elif key_map.key_q_press():
            self.metadata.control_action.THROW_GRENADE = True
        elif key_map.key_jump_press():
            self.metadata.control_action.JUMPING = True
        elif key_map.key_attack_press():
            self.metadata.control_action.SHOOT = True
        elif key_map.key_attack_release():
            self.metadata.control_action.SHOOT = False
        elif key_map.key_back_press():
            self._game_pause = True

    def handle_input_continue(self, key_map: lib.KeyMap) -> None:
        # for index, menu in enumerate(self._continue_menu_list):
        if key_map.key_enter_press():
            if CONTINUE_MENU_LIST[self._selected_continue_menu] == 'Restart':
                self._init()
            elif CONTINUE_MENU_LIST[self._selected_continue_menu] == 'Exit':
                self.metadata.game_mode = settings.GAME_START
        elif key_map.key_up_press():
            self._selected_continue_menu -= 1
            if self._selected_continue_menu < 0:
                self._selected_continue_menu = 0
        elif key_map.key_down_press():
            self._selected_continue_menu += 1
            if self._selected_continue_menu > len(self._continue_menu_list)-1:
                self._selected_continue_menu = len(self._continue_menu_list)-1
        elif key_map.key_back_press():
            self._game_pause = False

    def handle_input(self, key_event: pg.event.Event) -> None:
        key_map = lib.KeyMap(key_event)
        if self.metadata.GAME_OVER or self._game_pause:
            self.handle_input_continue(key_map)
        else:
            self.handle_input_player(key_map)

    def _update_backgroud_scroll(self) -> None:
        for index, background_vec in enumerate(self._background_lays_pos):
            lay_index = index % len(self._background_lays)
            background_vec.x += (self.metadata.scroll_value_x) * \
                ((lay_index+1)/len(self._background_lays))
            background_vec.y += self.metadata.scroll_value_y * \
                ((lay_index+1)/len(self._background_lays))

    def _screen_shake_control(self) -> None:
        if self.metadata.screen_shake <= 0:
            self.metadata.screen_shake = 0
            self.metadata.screen_shake_x= 0
            self.metadata.screen_shake_y= 0
            return
        self.metadata.screen_shake -= 1
        random_value = random.randint(0, 8) -4
        self.metadata.screen_shake_x = random_value
        self.metadata.screen_shake_y = random_value

    def update(self, dt: float) -> None:
        self._screen_shake_control()
        for index, menu in enumerate(self._continue_menu_list):
            menu.be_select = True if index == self._selected_continue_menu else False
            menu.update()
        if self._game_pause:
            return
        self._tile_sprites.update(dt=dt)
        self._item_sprites.update(dt=dt)
        self._player_sprites.update(dt=dt)
        self._enemy_sprites.update(dt=dt)
        self._bullet_sprites.update(dt=dt)
        self._grenade_sprites.update(dt=dt)
        self._explode_sprites.update(dt=dt)
        self._update_backgroud_scroll()

    def _continue_menu(self, screen: pg.surface.Surface) -> None:
        for menu in self._continue_menu_list:
            menu.draw(screen)

    def _draw_death_fade(self, screen: pg.surface.Surface) -> None:
        if self.metadata.GAME_OVER or self._game_pause:
            sur = pg.surface.Surface(
                (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
            sur.fill(settings.RGBA_BLACK)
            screen.blit(sur, (0, 0))
            self._continue_menu(screen)

    def draw(self) -> None:
        screen = self.metadata.scrren
        for index, lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index % len(self._background_lays)]
            new_lay_pos = pg.Vector2(
                lay_pos.x + self.metadata.screen_shake_x,
                lay_pos.y + self.metadata.screen_shake_y
            )
            screen.blit(lay, new_lay_pos)
        self._tile_sprites.draw(screen)
        self._item_sprites.draw(screen)
        self._player_sprites.draw(screen)
        self._enemy_sprites.draw(screen)
        self._bullet_sprites.draw(screen)
        self._grenade_sprites.draw(screen)
        self._explode_sprites.draw(screen)
        self._draw_death_fade(screen)

    def clear(self, screen: pg.surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)
