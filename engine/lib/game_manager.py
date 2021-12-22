from abc import ABC, abstractmethod
from typing import Dict

from pygame import surface, event

class GameManager(ABC):
    def __init__(self, metadata: Dict[str, str]) -> None:
        self.metadata = metadata

    @abstractmethod
    def handle_input(self, key_event: event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self, screen: surface.Surface) -> None:
        ...

    @abstractmethod
    def clear(self, screen: surface.Surface) -> None:
        ...
