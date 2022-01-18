from abc import ABC, abstractmethod

import pygame as pg

from .game_data import GameMetaData


class GameManager(ABC):
    def __init__(self, metadata: GameMetaData) -> None:
        self.metadata = metadata

    @abstractmethod
    def handle_input(self, key_event: pg.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self) -> None:
        ...

    @abstractmethod
    def clear(self, screen: pg.surface.Surface) -> None:
        ...
