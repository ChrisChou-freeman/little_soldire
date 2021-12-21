from pygame import surface, event, Vector2

from .lib import GameManager, com_fuc
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

    def handle_input(self, key_event: event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        pass

    def clear(self, screen: surface.Surface) -> None:
        pass
