from pygame import surface, Vector2

from .animation_sprite import AnimationSprite

class Role(AnimationSprite):
    def __init__(self,
                 image_sheet: surface.Surface,
                 position: Vector2,
                 fram_with: int,
                 loop: bool,
                 health_bar: int) -> None:
        super().__init__(image_sheet, position, fram_with, loop)
        self.health_bar = health_bar
        self._alive = True


    def update(self, *_, **__) -> None:
        self.play()

    def move(self, vec: Vector2) -> None:
        if self.rect is None:
            return
        self.rect.move(vec.x, vec.y)
