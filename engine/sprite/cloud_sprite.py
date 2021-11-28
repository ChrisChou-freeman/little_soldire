from pygame import sprite, surface, Vector2

from .. import settings

class CloudSprite(sprite.Sprite):

    def __init__(self, image: surface.Surface, position: Vector2, speed_time: int) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.left, self.rect.top = int(position.x), int(position.y)
        self.speed_time = speed_time
        self.couter = 0

    def update(self, *_, **kwargs) -> None:
        self.couter += 1
        dt: float = kwargs.get('dt', 0.0)
        dt *= 100
        if self.rect is not None:
            if self.couter % self.speed_time == 0:
                self.rect.left += int(dt)
            if self.rect.left > settings.SCREEN_WIDTH:
                self.rect.left = -settings.SCREEN_WIDTH
