from pygame import Vector2, font, surface

from .. import settings

class Menu:
    def __init__(self, menu_content: str, position: Vector2, size: int) -> None:
        self.font = font.Font(None, size)
        self.menu_content = menu_content
        self.font_rend = self.font.render(self.menu_content, False, settings.RGB_WHITE)
        self.position = position
        self.be_select = False

    def _set_menu_hover(self) -> None:
        self.font_rend = self.font.render(
            self.menu_content,
            False,
            settings.RGB_BLACK,
            settings.RGB_YELLOW
        )

    def _set_menu_unhover(self) -> None:
        self.font_rend = self.font.render(self.menu_content, False, settings.RGB_WHITE)

    def update(self) -> None:
        if self.be_select:
            self._set_menu_hover()
        else:
            self._set_menu_unhover()

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.font_rend, self.position)

