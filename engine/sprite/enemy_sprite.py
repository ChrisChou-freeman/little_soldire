import random

from pygame import Vector2, sprite, rect, draw, image

from ..lib import GameMetaData, com_type
from .. import settings
from . import role_sprite

class EnemySprite(role_sprite.RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 player_sprite: sprite.Group,
                 metadata: GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, bullet_sprites, metadata)
        self._notice_symbol = image.load(settings.NOTICE_IMG_PATH)
        self._player_sprite = player_sprite
        self._ai_action = com_type.ControlAction()
        self._ai_wake_time = settings.FPS * random.choice(range(0, 2))
        self._vision_rect = rect.Rect(position.x - 30, position.y, 300, 40)
        self._ai_counter = 0
        self.health_value = 40
        self._wander_distance = settings.MOVE_SPEED * 35
        self._wander_vectx = 0
        self._idling_time = settings.FPS * 3
        self.lose_detect = 0
        self.detect_time = settings.FPS // 2
        self.attack_frequency = int(settings.FPS*2)
        self._be_hiting = int(settings.FPS * 0.5)

    def vision_col_detect(self) -> bool:
        if self.lose_detect > 0:
            self.lose_detect -= 1
            return True
        for sprite in self._player_sprite:
            if sprite.rect is None:
                continue
            if sprite.alive() and sprite.rect.colliderect(self._vision_rect):
                self.lose_detect = settings.FPS * 2
                return True
        return False

    def be_hit_vision(self) -> None:
        self._be_hiting -= 1
        if self._be_hiting <= 0:
            return
        if self.action == 'idle':
            self.action = f'{self.action}_hit'

    def _ai_wander(self) -> None:
        if self.vision_col_detect():
            self._ai_action = com_type.ControlAction()
            self._ai_action.SHOOT = True
            return
        self._ai_action.SHOOT = False
        if not self._ai_action.RUN_LEFT or not self._ai_action.RUN_RIGHT:
            if self._ai_counter % self._idling_time == 0:
                if self._wander_vectx == 0:
                    self._ai_action.RUN_LEFT = True
                else:
                    self._ai_action.RUN_RIGHT = True
        if self._ai_action.RUN_LEFT:
            if (self._wander_vectx*-1)  >= self._wander_distance:
                self._ai_action.RUN_LEFT = False
        elif self._ai_action.RUN_RIGHT:
            if self._wander_vectx >= 0:
                self._ai_action.RUN_RIGHT = False

    def _ai(self) -> None:
        if self.is_empty_health():
            return
        if self._ai_wake_time > 0:
            self._ai_wake_time -= 1
            return
        self._ai_counter += 1
        self._ai_wander()

    def move(self) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_index
        move_rect = self._get_vec_with_action(self._ai_action)
        self._wander_vectx += int(move_rect.x)
        self.rect = self.rect.move(move_rect)
        self.position.x, self.position.y = self.rect.x, self.rect.y
        self.update_vision_rect()

    def update_vision_rect(self) -> None:
        if self.rect is None:
            return
        self._vision_rect.x = self.rect.x
        if self.flip:
            self._vision_rect.x -= self._vision_rect.width - self.rect.width
        self._vision_rect.y = self.rect.y - int(self.rect.height * 0.3)

    def draw_debug_box(self) -> None:
        self.update_vision_rect()
        draw.rect(self.metadata.scrren, settings.RGB_RED, self._vision_rect, 2)

    def _draw_detected_symbol(self) -> None:
        if not self.vision_col_detect() or self.rect is None:
            return
        f = 1 if not self.flip else -1
        self.metadata.scrren.blit(
            self._notice_symbol,
            Vector2(
                self.rect.x - (self._notice_symbol.get_width()/2*f),
                self.rect.y - self._notice_symbol.get_height()
            )
        )

    def _out_world_kill(self) -> None:
        if self.rect is None:
            return
        if self.rect.right < -50 or self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

    def update(self, *_, **__) -> None:
        self._ai()
        self._out_world_kill()
        self.move()
        self._get_action(self._ai_action, 'enemy')
        self.hit_detect('enemy')
        self.animation_playing = self.play()
        self.death_disappear()
        self._draw_detected_symbol()

