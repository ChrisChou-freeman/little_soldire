import sys

import pygame
from pygame import event, display, surface

from . import settings, game_start, game_editor
from .lib import GameManager

class MainGame:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self._create_screen()
        self.game_metadata = {
            'game_mode': 'GameStart'
        }
        self.game_mode: dict[str, type[GameManager]] = {
            'GameStart': game_start.GameStart,
            'EditGame': game_editor.GameEditor
        }
        self.game_manager: GameManager|None = None

    def _create_screen(self) -> surface.Surface:
        flag = pygame.FULLSCREEN|pygame.SCALED if settings.FULL_SCRREN else 0
        screen = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), flag)
        display.set_caption('little soldire')
        return screen

    def _handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.QUIT \
                or (key_event.type == pygame.KEYDOWN and key_event.key == pygame.K_ESCAPE):
                self._quit()
        if self.game_manager is not None:
            self.game_manager.handle_input(key_event)

    def _draw(self) -> None:
        if self.game_manager is not None:
            self.game_manager.draw(self.screen)

    def _update(self, dt: float) -> None:
        if self.game_manager is not None:
            self.game_manager.update(dt)
        pygame.display.update()

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        clock = pygame.time.Clock()
        while True:
            switch_mode = self.game_metadata['game_mode']
            if not isinstance(self.game_manager, self.game_mode[switch_mode]):
                if self.game_manager is not None:
                   self.game_manager.clear(self.screen)
                self.game_manager = self.game_mode[switch_mode](self.game_metadata)
            for key_event in event.get():
                self._handle_input(key_event)
            self._draw()
            self._update(float(clock.get_time()/1000))
            clock.tick(settings.FPS)

