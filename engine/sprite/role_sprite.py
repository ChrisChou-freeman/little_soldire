from pygame import Vector2, image, sprite, rect

from .animation_sprite import AnimationSprite
from ..lib import GameMetaData
from .. import settings

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self._action = 'idle'
        self.position = position
        self.tile_sprites = tile_sprites
        self.metadata = metadata
        self._set_current_action()

    def _set_current_action(self, flip=False) -> None:
        action_info = self._sprite_sheet_info.get(self._action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        super().__init__(image_sheet, self.position, fram_with, loop, flip)

    def _collition_detect(self, vect: Vector2) -> Vector2:
        new_vect = Vector2(vect.x, vect.y)
        for sprite in self.tile_sprites:
            if self.rect is None or sprite.rect is None:
                return new_vect
            is_collide_x =  sprite.rect.colliderect(
                rect.Rect(self.rect.x + vect.x, self.rect.y, self.rect.width, self.rect.height)
            )
            if is_collide_x:
                new_vect.x = 0
            is_collide_y = sprite.rect.colliderect(
                rect.Rect(self.rect.x, self.rect.y + vect.y, self.rect.width, self.rect.height)
            )
            if is_collide_y:
                if vect.y > 0:
                    new_vect.y = sprite.rect.top - self.rect.bottom
                elif vect.y < 0:
                    new_vect.y = sprite.rect.bottom - self.rect.top
        return new_vect

class PlayerSprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, metadata)

    def move_forward_word(self) -> None:
        if self.rect is None:
            return
        if self.rect.centerx < settings.SCREEN_WIDTH//2:
            return
        forward_distance = settings.SCREEN_WIDTH//2 - self.rect.centerx
        self.rect.centerx = settings.SCREEN_WIDTH//2
        self.metadata.scroll_index = forward_distance

    def update(self, *_, **kwargs) -> None:
        vec: Vector2 = kwargs['vec']
        action: str = kwargs['action']
        if action.startswith('run_'):
            if action == 'run_left':
                self.flip = True
            elif action == 'run_right':
                self.flip = False
            action = 'run'
        if self.rect is not None:
            vec = self._collition_detect(vec)
            if vec.y != 0:
                action = 'jump'
            self.rect = self.rect.move(vec)
            self.position.x, self.position.y = self.rect.x, self.rect.y
        self.move_forward_word()
        if action != self._action:
            self._action = action
            self._set_current_action(self.flip)
        self.play()

class EnemySprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, metadata)

    def update(self, *_, **__) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_index
        if self.rect.right < -20:
            self.kill()
