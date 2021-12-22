import os

import pygame
from pygame import surface, event, Vector2

from .lib import GameManager, com_fuc, KeyMap
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
        self._run_speed = 1 * len(self._background_lays)
        self._run_left = False
        self._run_right = False
        self._shoot = False
        self._surface_scroll_value = 0
        self._world_data_path = os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        self._word_data = com_fuc.load_world_data(self._world_data_path)
        self._init_content()

    def _init_content(self) -> None:
        pass

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.KEYDOWN:
            if key_event.key in [pygame.K_a, pygame.K_LEFT]:
                self._run_left = True
            elif key_event.key in [pygame.K_d, pygame.K_RIGHT]:
                self._run_right = True
            elif key_event.key == pygame.K_q:
                pass
            elif key_event.key == pygame.K_j:
                self._shoot = True
            elif key_event.key == pygame.K_k:
                pass
        elif key_event.type == pygame.KEYUP:
            if key_event.key in [pygame.K_a, pygame.K_LEFT]:
                self._run_left = False
            elif key_event.key in [pygame.K_d, pygame.K_RIGHT]:
                self._run_right = False
            elif key_event.key == pygame.K_j:
                self._shoot = False

    def update(self, dt: float) -> None:
        ...

    def draw(self, screen: surface.Surface) -> None:
        ...

    def clear(self, screen: surface.Surface) -> None:
        ...

