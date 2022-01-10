from pygame import sprite, surface, Vector2

from ..lib import GameMetaData

class TileSprite(sprite.Sprite):
    def __init__(self,
                 image: surface.Surface,
                 position: Vector2,
                 metadata: GameMetaData) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(position)
        self.metadata = metadata

    def update(self, *_, **__) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_value
        if self.rect.right < 0:
            self.kill()
