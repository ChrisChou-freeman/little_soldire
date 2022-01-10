from abc import ABC, abstractmethod

from .game_data import GameMetaData

from pygame import surface, event

class GameManager(ABC):
    def __init__(self, metadata: GameMetaData) -> None:
        self.metadata = metadata

    @abstractmethod
    def handle_input(self, key_event: event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self) -> None:
        ...

    @abstractmethod
    def clear(self, screen: surface.Surface) -> None:
        ...
