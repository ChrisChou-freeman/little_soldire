from pygame import surface, event

from .lib import GameManager

class GamePlay(GameManager):

    def __init__(self, metadata: dict[str, str]) -> None:
        super().__init__(metadata)

    def handle_input(self, key_event: event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        pass

    def clear(self, screen: surface.Surface) -> None:
        pass
