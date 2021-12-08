import pygame
from pygame import surface, Vector2, event, Rect

class Button:
    def __init__(self, b_img: surface.Surface, position: Vector2) -> None:
        self.b_img = b_img
        self.position = position
        self.rect = Rect(position.x, position.y, self.b_img.get_width(), self.b_img.get_height())

    def _check_hover(self, key_kent: event.Event) -> bool:
        pos = key_kent.pos
        return self.rect.collidepoint(pos[0], pos[1])

    def handle_input(self, key_event: event.Event):
        if key_event.type == pygame.MOUSEBUTTONDOWN:
            if key_event.button == pygame.BUTTON_LEFT:
                hover = self._check_hover(key_event)
                if hover:
                    print('click')

    def update(self) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.b_img, self.position)
