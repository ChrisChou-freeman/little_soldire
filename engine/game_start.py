import os

import pygame as pg

from . import lib, ui, sprite as _sprite, settings

class GameStart(lib.GameManager):
    def __init__(self, metadata: lib.GameMetaData) -> None:
        super().__init__(metadata)
        self.cloud_sprites = pg.sprite.Group()
        self._background_lays: list[pg.surface.Surface] = []
        self._background_lays_pos = [
            pg.Vector2(0, 0),
            pg.Vector2(0, 0),
            pg.Vector2(0, 230),
            pg.Vector2(0, 250),
            pg.Vector2(0, 250),
        ]
        self._lay_number = 5
        self._cloud_number = 3
        self._menu_size = 45
        self._menu_gap = 40
        self._menu_list = [
            settings.GAME_PLAY,
            settings.GAME_EDITOR,
            settings.GAME_EXIT
        ]
        self._menus: list[ui.Menu] = []
        self._select_menu_key = 0
        self._load_content()

    def _load_content(self) -> None:
        # load background lays
        for lay in range(self._lay_number):
            lay_img = pg.image.load(os.path.join(settings.GAME_START_IMG_PATH, f'layer{lay}.png'))
            self._background_lays.append(lay_img)
        # load clouds
        for lay in range(self._cloud_number):
            cloud_img = pg.image.load(os.path.join(settings.GAME_START_IMG_PATH, f'cloud_layer{lay}.png')).convert_alpha()
            cloud_sprite = _sprite.CloudSprite(cloud_img, pg.Vector2(0,0), self._cloud_number*3 - lay*3)
            self.cloud_sprites.add(cloud_sprite)
        # load menu
        for index, name in enumerate(self._menu_list):
            menu = ui.Menu(name, pg.Vector2(70, int(settings.SCREEN_HEIGHT/2) + self._menu_gap * index), self._menu_size)
            self._menus.append(menu)
        self._key_menu_select_handle()

    def _key_menu_select_handle(self) -> None:
        for index, menu in enumerate(self._menus):
            menu.be_select = True if index == self._select_menu_key else False

    def _menus_swich(self, mode: str) -> None:
        '''change current selected menu'''
        val = 1
        if mode == 'up':
            val *= -1
        self._select_menu_key += val
        if self._select_menu_key < 0:
            self._select_menu_key = 0
        elif self._select_menu_key > len(self._menus) - 1:
            self._select_menu_key = len(self._menus) - 1
        self._key_menu_select_handle()

    def handle_input(self, key_event: pg.event.Event) -> None:
        key_map = lib.KeyMap(key_event)
        if key_map.key_up_press():
            self._menus_swich('up')
        elif key_map.key_down_press():
            self._menus_swich('down')
        elif key_map.key_enter_press():
            self.metadata.game_mode = self._menu_list[self._select_menu_key]

    def update(self, dt: float) -> None:
        self.cloud_sprites.update(dt=dt)
        for menu in self._menus:
            menu.update()

    def draw(self) -> None:
        screen = self.metadata.scrren
        for index, lay in enumerate(self._background_lays):
            screen.blit(lay, self._background_lays_pos[index])
        self.cloud_sprites.draw(screen)
        for menu in self._menus:
            menu.draw(screen)

    def clear(self, screen: pg.surface.Surface) -> None:
        self.cloud_sprites.empty()
        screen.fill(settings.RGB_BLACK)
