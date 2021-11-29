import os
from typing import Dict, List

from pygame import surface, event, sprite, image, Vector2
import pygame

from .lib import GameManager, Menu
from .sprite import CloudSprite
from . import settings

class GameStart(GameManager):
    def __init__(self, metadata: Dict[str, str]) -> None:
        super().__init__(metadata)
        self._lay_number = 5
        self._cloud_number = 3
        self.cloud_sprites = sprite.Group()
        self.background_lays: List[surface.Surface] = []
        self.background_lays_pos = [
            Vector2(0, 0),
            Vector2(0, 0),
            Vector2(0, 230),
            Vector2(0, 250),
            Vector2(0, 250),
        ]
        self.menu_size = 45
        self.menu_gap = 40
        self.menu_list = [
            'Start',
            'Edit',
            'Quit'
        ]
        self.menus: List[Menu] = []
        self.select_menu_key = 0
        self._load_content()

    def _load_content(self) -> None:
        # load background lays
        for lay in range(self._lay_number):
            lay_img = image.load(os.path.join(settings.GAME_START_IMG_PATH, f'layer{lay}.png'))
            self.background_lays.append(lay_img)

        # load clouds
        for lay in range(self._cloud_number):
            cloud_img = image.load(os.path.join(settings.GAME_START_IMG_PATH, f'cloud_layer{lay}.png')).convert_alpha()
            cloud_sprite = CloudSprite(cloud_img, Vector2(0,0), self._cloud_number*3 - lay*3)
            self.cloud_sprites.add(cloud_sprite)

        # load menu
        for index, name in enumerate(self.menu_list):
            menu = Menu(name, Vector2(70, int(settings.SCREEN_HEIGHT/2) + self.menu_gap * index), self.menu_size)
            self.menus.append(menu)

        self._key_menu_select_handle()

    def _key_menu_select_handle(self) -> None:
        for index, menu in enumerate(self.menus):
            if index == self.select_menu_key:
                menu.be_select = True
            else:
                menu.be_select = False

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.KEYDOWN:
            match key_event.key:
                case pygame.K_w | pygame.K_UP:
                    self.select_menu_key -= 1
                    if self.select_menu_key < 0:
                        self.select_menu_key = 0
                    self._key_menu_select_handle()
                case pygame.K_s | pygame.K_DOWN:
                    self.select_menu_key += 1
                    if self.select_menu_key > len(self.menus) -1:
                        self.select_menu_key = len(self.menus) -1
                    self._key_menu_select_handle()

    def update(self, dt: float) -> None:
        self.cloud_sprites.update(dt=dt)
        for menu in self.menus:
            menu.update()

    def draw(self, screen: surface.Surface) -> None:
        for index, lay in enumerate(self.background_lays):
            screen.blit(lay, self.background_lays_pos[index])
        self.cloud_sprites.draw(screen)

        for menu in self.menus:
            menu.draw(screen)

    def clear(self, screen: surface.Surface) -> None:
        self.cloud_sprites.empty()
        screen.fill(settings.RGB_BLACK)

