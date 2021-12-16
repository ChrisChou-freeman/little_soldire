from pygame import surface, Vector2, font

from .. import settings

class Tip:
    def __init__(self, msg: str, position: Vector2, size: int) -> None:
        self.position  = position
        self.font = font.Font(None, size)
        self.size = self.font.size(msg)
        self.render_font = self.font.render(msg, False, settings.RGB_WHITE)

    def _get_position(self) -> Vector2:
        return Vector2(self.position.x - self.size[0], self.position.y)

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.render_font, self._get_position())
