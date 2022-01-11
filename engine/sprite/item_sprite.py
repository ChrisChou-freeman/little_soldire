from pygame import sprite, Vector2, surface

from .. import lib

class ItemSprite(sprite.Sprite):
    def __init__(self,
                 image: surface.Surface,
                 position: Vector2,
                 metadata: lib.GameMetaData) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(position)
        self.metadata = metadata

    def update(self, **_) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_value
        if self.rect.right < 0:
            self.kill()
