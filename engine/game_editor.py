from typing import Dict, List

from pygame import surface, event

from .lib import GameManager, com_fuc
from  . import settings

class GameEditor(GameManager):
    def __init__(self, metadata: Dict[str, str]) -> None:
        super().__init__(metadata)
        self.background_lays: List[surface.Surface] = []
        self._load_content()

    def _load_content(self) -> None:
        self.background_lays = com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)

    def handle_input(self, key_event: event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        for index, lay in enumerate(self.background_lays):
            screen.blit(lay, (0,index * 80))

    def clear(self, screen: surface.Surface) -> None:
        self.background_lays = []
        screen.fill(settings.RGB_BLACK)
