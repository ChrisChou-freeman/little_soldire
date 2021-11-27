from pygame import Vector2, font, rect, surface, event
import pygame

from .. import settings

class Menu:
    def __init__(self, menu_content: str, position: Vector2, size: int) -> None:
        self.font = font.Font(None, size)
        self.menu_content = menu_content
        self.font_rend = self.font.render(self.menu_content, False, settings.RGB_WHITE)
        self.position = position
        self.size = self.font.size(self.menu_content)
        self.rect = rect.Rect(position.x, position.y, self.size[0], self.size[1])

    def _check_mouse_hover(self, x, y) -> bool:
        return self.rect.collidepoint(x, y)

    def _set_menu_hover(self) -> None:
        self.font_rend = self.font.render(self.menu_content, False, settings.RGB_BLACK, settings.RGB_WHITE)

    def _set_menu_unhover(self) -> None:
        self.font_rend = self.font.render(self.menu_content, False, settings.RGB_WHITE)

    def handle_input(self, env: event.Event) -> None:
        if env.type == pygame.MOUSEMOTION:
            pos = env.pos
            if self._check_mouse_hover(pos[0], pos[1]):
                self._set_menu_hover()
            else:
                self._set_menu_unhover()
        if env.type == pygame.MOUSEBUTTONDOWN and env.button == 1:
            pass

    def update(self) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.font_rend, self.position)

