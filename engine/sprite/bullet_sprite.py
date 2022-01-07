from pygame import sprite, surface, Vector2

from .. import settings

class Bullet(sprite.Sprite):
    def __init__(
        self,
        image: surface.Surface,
        position: Vector2,
        vect: Vector2,
        speed: int,
        tile_sprites: sprite.Group,
        bullet_type: str) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect().move(position)
        self.speed = speed
        self.vect = vect
        self.tile_sprites = tile_sprites
        self.bullet_type = bullet_type
        self.couter = 0
        self.life_time = settings.BULLET_LIFE_TIME

    def _bullet_move(self, dt: float) -> None:
        if self.rect is None:
            return
        move_x = dt * self.speed * self.vect.x
        self.rect.x += round(move_x)

    def _bullet_kill_detect(self) -> None:
        if self.rect is None:
            return
        if self.rect.right < -50:
            self.kill()
        elif self.rect.left > settings.SCREEN_WIDTH + 50:
            self.kill()
        elif self.couter > self.life_time:
            self.kill()
        for sprite in self.tile_sprites:
            if sprite.rect is None:
                continue
            if sprite.rect.colliderect(self.rect):
                self.kill()
                return

    def update(self, *_, **kwargs) -> None:
        self.couter += 1
        dt: float = kwargs['dt']
        self._bullet_move(dt)
        self._bullet_kill_detect()

