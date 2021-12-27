from pygame import sprite, Vector2, surface

class ItemSprite(sprite.Sprite):
    def __init__(self, image: surface.Surface, position: Vector2) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(position)
