import sys
import typing

import pygame as pg

from . import settings, game_start, game_editor, game_play, lib, ui


class MainGame:

    def __init__(self) -> None:
        pg.init()
        self._screen = self._create_screen()
        self._clock = pg.time.Clock()
        self._game_metadata = lib.GameMetaData(
            game_mode=settings.GAME_START,
            level_edit_tile='',
            scroll_value_x=0,
            scroll_value_y=0,
            screen_shake_x=0,
            screen_shake_y=0,
            screen_shake=0,
            control_action=lib.com_type.ControlAction(),
            scrren=self._screen
        )
        self._game_mode: dict[str, type[lib.GameManager]] = {
            settings.GAME_START: game_start.GameStart,
            settings.GAME_EDITOR: game_editor.GameEditor,
            settings.GAME_PLAY: game_play.GamePlay
        }
        self._game_manager: typing.Optional[lib.GameManager] = None

    def _create_screen(self) -> pg.surface.Surface:
        flag = pg.FULLSCREEN | pg.SCALED if settings.FULL_SCRREN else 0
        screen = pg.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), flag)
        pg.display.set_caption(settings.GAME_TITLE)
        return screen

    def _handle_input(self, key_event: pg.event.Event) -> None:
        if key_event.type == pg.QUIT:
            self._quit()
        if self._game_manager is not None:
            self._game_manager.handle_input(key_event)

    def _draw_fps(self) -> None:
        if not settings.SHOW_FPS:
            return
        tip_obj = ui.Tip(
            f'FPS:{round(self._clock.get_fps())}',
            pg.Vector2(settings.SCREEN_WIDTH - 20, 25), 25)
        tip_obj.draw(self._screen)

    def _draw(self) -> None:
        if self._game_manager is not None:
            self._game_manager.draw()
        self._draw_fps()

    def _update(self, dt: float) -> None:
        if self._game_manager is not None:
            self._game_manager.update(dt)
        pg.display.update()

    def _quit(self) -> None:
        pg.quit()
        sys.exit()

    def run(self) -> None:
        while True:
            switch_mode = self._game_metadata.game_mode
            if switch_mode == settings.GAME_EXIT:
                self._quit()
            if not isinstance(self._game_manager, self._game_mode[switch_mode]):
                if self._game_manager is not None:
                    del self._game_manager
                self._game_manager = self._game_mode[switch_mode](self._game_metadata)
            for key_event in pg.event.get():
                self._handle_input(key_event)
            self._draw()
            self._update(float(self._clock.get_time()/1000))
            self._clock.tick(settings.FPS)
