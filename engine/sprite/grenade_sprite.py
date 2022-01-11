from .. import lib

from pygame import sprite, surface, Vector2

class Grenade(sprite.Sprite):
    def __init__(self,
                 metadata: lib.GameMetaData,
                 image: surface.Surface,
                 position: Vector2,
                 vect: Vector2) -> None:
        super().__init__()
        self.grenade_speed = 7
        self.vect_y = -11
        self.metadata = metadata
        self.image = image
        self.rect = image.get_rect().move(position)
        self.vect = vect

    def _collition_detect(self, vect: Vector2) -> None:
        ...

    def _grenade_parabola(self) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_value

    def update(self, **_) -> None:
        self._grenade_parabola()
