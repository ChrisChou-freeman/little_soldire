from collections.abc import Callable

import pygame
from pygame import surface, Vector2, event, Rect, draw

from .. import settings

class Button:
    def __init__(self, b_img: surface.Surface, position: Vector2) -> None:
        self.position = position
        self.rect = Rect(position.x, position.y, b_img.get_width(), b_img.get_height())
        self.rect_selected = Rect(position.x-1, position.y-1, b_img.get_width()+2, b_img.get_height()+2)
        self._b_img = b_img
        self._selected = False

    def _check_hover(self, key_kent: event.Event) -> bool:
        pos = key_kent.pos
        return self.rect.collidepoint(pos[0], pos[1])

    def handle_input(self, key_event: event.Event, click_handle: Callable[[], None]):
        if key_event.type == pygame.MOUSEBUTTONDOWN:
            if key_event.button == pygame.BUTTON_LEFT:
                self._selected = True if self._check_hover(key_event) else False
        if key_event.type == pygame.MOUSEBUTTONUP:
            if key_event.button == pygame.BUTTON_LEFT:
                self._selected = False
                if self._check_hover(key_event):
                    click_handle()

    def update(self) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self._b_img, self.position)
        if self._selected:
            draw.rect(screen, settings.RGB_YELLOW, self.rect_selected, 1)

