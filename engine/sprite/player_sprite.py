import pygame
from pygame import Vector2, sprite, draw

from . import role_sprite
from ..lib import GameMetaData
from .. import settings

class PlayerSprite(role_sprite.RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, bullet_sprites,metadata)

    def move(self) -> None:
        if self.rect is None:
            return
        if self.rect.x <= 0 and self.metadata.control_action.RUN_LEFT:
            return
        self.rect = self.rect.move(self._get_vec_with_action(self.metadata.control_action))
        self.position.x, self.position.y = self.rect.x, self.rect.y
        # scroll screen
        if self.rect.x < settings.SCREEN_WIDTH//2:
            self.metadata.scroll_value = 0
            return
        forward_distance = settings.SCREEN_WIDTH//2 - self.rect.x
        self.rect.x = settings.SCREEN_WIDTH//2
        self.metadata.scroll_value = forward_distance

    def hub(self) -> None:
        x = 10
        y = 10
        ratio = self.health_value / 100
        screen = self.metadata.scrren
        pygame.draw.rect(screen, settings.RGB_RED, (x, y, 150, 20))
        pygame.draw.rect(screen, settings.RGB_YELLOW, (x, y, int(150 * ratio), 20))

    def _fall_off_screen_derect(self) -> None:
        if self.rect is None:
            return
        if self.rect.top >= settings.SCREEN_HEIGHT:
            self.health_value = 0

    def update(self, *_, **__) -> None:
        if self.is_empty_health():
            self.metadata.GAME_OVER = True
        self.move()
        self._get_action(self.metadata.control_action)
        self.play()
        self.hit_detect('player')
        self.hub()
        self._fall_off_screen_derect()

