from typing import Dict, List
import os

from pygame import surface, event, sprite, image, Vector2

from .lib import GameManager
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
        self._load_content()
        self.menu_list = [
            'Start',
            'Edit',
            'Quit'
        ]

    def _load_content(self) -> None:
        # load background lays
        for lay in range(self._lay_number):
            lay_img = image.load(os.path.join(settings.GAME_START_IMG_PATH, f'layer{lay}.png'))
            self.background_lays.append(lay_img)

        for lay in range(self._cloud_number):
            cloud_img = image.load(os.path.join(settings.GAME_START_IMG_PATH, f'cloud_layer{lay}.png')).convert_alpha()
            cloud_sprite = CloudSprite(cloud_img, Vector2(0,0), self._cloud_number + 3 - lay)
            self.cloud_sprites.add(cloud_sprite)


    def handle_input(self, key_event: event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.cloud_sprites.update(dt=dt)

    def draw(self, screen: surface.Surface) -> None:
        for index, lay in enumerate(self.background_lays):
            screen.blit(lay, self.background_lays_pos[index])
        self.cloud_sprites.draw(screen)

    def clear(self, screen: surface.Surface) -> None:
        self.cloud_sprites.empty()
        screen.fill(settings.RGB_BLACK)
