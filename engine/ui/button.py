from typing import Optional
from collections.abc import Callable

import pygame as pg

from .. import settings

class Button:
    def __init__(
            self,
            b_img: pg.surface.Surface,
            position: pg.Vector2,
            btn_name: str) -> None:
        self.btn_name = btn_name
        self.position = position
        self.rect = pg.Rect(position.x, position.y, b_img.get_width(), b_img.get_height())
        self.rect_selected = pg.Rect(
            position.x-1,
            position.y-1,
            b_img.get_width()+2,
            b_img.get_height()+2
        )
        self._b_img = b_img
        self._selected = False

    def _check_hover(self, key_kent: pg.event.Event) -> bool:
        pos = key_kent.pos
        return self.rect.collidepoint(pos[0], pos[1])

    def handle_input(self, key_event: pg.event.Event, click_handle: Optional[Callable[[], None]]=None) -> bool:
        if key_event.type == pg.MOUSEBUTTONDOWN:
            if key_event.button == pg.BUTTON_LEFT:
                self._selected = True if self._check_hover(key_event) else False
        elif key_event.type == pg.MOUSEBUTTONUP:
            if key_event.button == pg.BUTTON_LEFT:
                self._selected = False
                if self._check_hover(key_event):
                    if click_handle is not None: click_handle()
                    return True
        return False

    def update(self) -> None:
        pass

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.blit(self._b_img, self.position)
        if self._selected:
            pg.draw.rect(screen, settings.RGB_YELLOW, self.rect_selected, 1)

