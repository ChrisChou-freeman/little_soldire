import random

from pygame import Vector2, image, sprite, rect, draw

from .animation_sprite import AnimationSprite
from .bullet_sprite import Bullet
from ..lib import GameMetaData, com_type
from .. import settings

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self._action = 'idle'
        self._jump_vect_y = 0
        self.attack_frequency = int(settings.FPS/3)
        self._attack_counter = 0
        self.health_value = 100
        self.falling = False
        self.animation_playing = True
        self.position = position
        self.tile_sprites = tile_sprites
        self.bullet_sprites = bullet_sprites
        self.metadata = metadata
        self._set_current_action(init=True)

    def hit_detect(self, role: str) -> None:
        if self.rect is None:
            return
        for sprite in self.bullet_sprites:
            if self.health_value <= 0:
                return
            if sprite.rect is None:
                continue
            if sprite.rect.colliderect(self.rect):
                bullet_type: str = sprite.__getattribute__('bullet_type')
                if bullet_type == 'player' and role == 'enemy':
                    self.health_value -= settings.PLAYER_DAMEGE
                    sprite.kill()
                elif bullet_type == 'enemy' and role == 'player':
                    self.health_value -= settings.ENEMY_DAMEGE
                    sprite.kill()

    def is_empty_health(self) -> bool:
        return self.health_value <= 0

    def alive(self) -> bool:
        if self.is_empty_health():
            return False
        return super().alive()

    def death_disappear(self) -> None:
        if self._action == 'death' and not self.animation_playing:
            self.kill()
            return

    def _set_current_action(self, flip=False, init=False) -> None:
        action_info = self._sprite_sheet_info.get(self._action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        if init:
            super().__init__(image_sheet, self.position, fram_with, loop, flip)
        else:
            self.init_animation(image_sheet, self.position, fram_with, loop, flip)

    def _get_vec_with_action(self, control_action: com_type.ControlAction) -> Vector2:
        if self.is_empty_health():
            return Vector2()
        if control_action.JUMPING and not self.falling:
            self._jump_vect_y = settings.JUMP_FORCE
            self.falling = True
        x = 0
        self._jump_vect_y += int(settings.GRAVITY)
        if self._jump_vect_y >= settings.MAX_GRAVITY:
            self._jump_vect_y = settings.MAX_GRAVITY
        y = self._jump_vect_y
        if control_action.RUN_LEFT:
            x += (settings.MOVE_SPEED*-1)
        elif control_action.RUN_RIGHT:
            x += (settings.MOVE_SPEED)
        c_d_vect = self._collition_detect(Vector2(x, y))
        if c_d_vect.y == 0:
            control_action.JUMPING = False
            self.falling = False
        return c_d_vect

    def _shoot_bullet(self, role: str) -> None:
        if self.is_empty_health():
            return
        if self.rect is None:
            return
        bullet_img = image.load(settings.BULLET_IMG_PATH)
        pos_x = self.rect.left if self.flip else self.rect.right
        pos_y = self.rect.bottom - int(self.rect.height / 2) - 5
        vect_x = -1 if self.flip else 1
        vect_y = 0
        bullet_speed = 500
        bs = Bullet(
            bullet_img,
            Vector2(pos_x, pos_y),
            Vector2(vect_x, vect_y),
            bullet_speed,
            self.tile_sprites,
            role
        )
        self.bullet_sprites.add(bs)

    def _get_action(self, control_action: com_type.ControlAction, role: str = 'player') -> None:
        action = 'idle'
        if self.is_empty_health():
            action = 'death'
        else:
            if control_action.RUN_LEFT:
                self.flip = True
                action = 'run'
            if control_action.RUN_RIGHT:
                self.flip = False
                action = 'run'
            if control_action.JUMPING or self.falling:
                action = 'jump'
            if control_action.SHOOT:
                if self._attack_counter == 0 or self._attack_counter%self.attack_frequency == 0:
                    self._shoot_bullet(role)
                self._attack_counter += 1
            else:
                self._attack_counter = 0
        if action != self._action:
            self._action = action
            self._set_current_action(self.flip)

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
            self.metadata.scroll_index = 0
            return
        forward_distance = settings.SCREEN_WIDTH//2 - self.rect.x
        self.rect.x = settings.SCREEN_WIDTH//2
        self.metadata.scroll_index = forward_distance

    def update(self, *_, **__) -> None:
        self.move()
        self._get_action(self.metadata.control_action)
        self.play()

class EnemySprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 player_sprite: sprite.Group,
                 metadata: GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, bullet_sprites, metadata)
        self.health_value = 40
        self.player_sprite = player_sprite
        self._ai_action = com_type.ControlAction()
        self.vision_rect = rect.Rect(position.x - 30, position.y, 300, 40)
        self._wander_distance = settings.MOVE_SPEED * 35
        self._wander_vectx = 0
        self._ai_counter = 0
        self._idling_time = settings.FPS * 3
        self._ai_wake_time = settings.FPS * random.choice(range(1, 3))
        self.attack_frequency = int(settings.FPS*2)
        self.detect = False
        self.lose_detect = 0

    def vision_col_detect(self) -> bool:
        if self.lose_detect > 0:
            self.lose_detect -= 1
            return True
        for sprite in self.player_sprite:
            if sprite.rect is None:
                continue
            if sprite.alive() and sprite.rect.colliderect(self.vision_rect):
                self.lose_detect = settings.FPS * 2
                return True
        return False

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
        self.vision_rect.x = self.rect.x
        if self.flip:
            self.vision_rect.x -= self.vision_rect.width - self.rect.width
        self.vision_rect.y = self.rect.y - int(self.rect.height * 0.3)

    def draw_debug_box(self) -> None:
        self.update_vision_rect()
        draw.rect(self.metadata.scrren, settings.RGB_RED, self.vision_rect, 2)

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
        # self.draw_debug_box()

