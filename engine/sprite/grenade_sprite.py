from .. import lib
from .. import settings

from pygame import sprite, surface, Vector2, rect

class Grenade(sprite.Sprite):
    def __init__(self,
                 metadata: lib.GameMetaData,
                 image: surface.Surface,
                 position: Vector2,
                 direction: int,
                 tile_sprites: sprite.Group) -> None:
        super().__init__()
        self.tile_sprites = tile_sprites
        self.throw_speed = 7
        self.vect_y = -11
        self.metadata = metadata
        self.image = image
        self.explode_time = settings.FPS * 3
        self.rect = image.get_rect().move(position)
        self.direction = direction

    def _collition_detect(self) -> Vector2:
        vect = Vector2(self.throw_speed * self.direction, self.vect_y)
        self.vect_y += settings.GRAVITY
        if self.vect_y >= settings.MAX_GRAVITY:
            self.vect_y = settings.MAX_GRAVITY
        for tile in self.tile_sprites:
            if self.rect is None or tile.rect is None:
                continue
            is_collide_x = tile.rect.colliderect(
                rect.Rect(self.rect.x + vect.x, self.rect.y, self.rect.width, self.rect.height)
            )
            if is_collide_x:
                vect.x *= -1
            is_collide_y = tile.rect.colliderect(
                rect.Rect(self.rect.x, self.rect.y + vect.y, self.rect.width, self.rect.height)
            )
            if is_collide_y:
                if vect.y < 0:
                    vect.y = tile.rect.bottom - self.rect.top
                else:
                    vect.x = 0
                    vect.y = tile.rect.top - self.rect.bottom
        return vect

    def _grenade_parabola(self) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_value
        m_vect = self._collition_detect()
        self.rect = self.rect.move(m_vect)

    def update(self, **_) -> None:
        self._grenade_parabola()

