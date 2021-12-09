from pygame import Rect, Vector2, surface, draw

class MenuContainer:
    def __init__(self, position: Vector2, width: int, height: int, color: tuple[int, int, int]) -> None:
        self.show = False
        self.rec = Rect(position.x, position.y, width, height)
        self._color = color

    def draw(self, screen: surface.Surface) -> None:
        if self.show:
            draw.rect(screen, self._color, self.rec)

