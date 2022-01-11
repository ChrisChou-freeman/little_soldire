from pygame import Vector2, image, sprite, rect

from .animation_sprite import AnimationSprite
from . import bullet_sprite
from . import grenade_sprite
from ..lib import GameMetaData, com_type
from .. import settings

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 grenade_sprites: sprite.Group,
                 explode_sprites: sprite.Group,
                 metadata: GameMetaData) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self.position = position
        self.metadata = metadata
        self.tile_sprites = tile_sprites
        self.bullet_sprites = bullet_sprites
        self.grenade_sprites = grenade_sprites
        self.explode_sprites = explode_sprites
        self.grenade_img = image.load(settings.GRENADE_IMG_PATH)
        self.action = 'idle'
        self._jump_vect_y = 0.0
        self.attack_frequency = int(settings.FPS/3)
        self.be_hiting_time = 0
        self._attack_counter = 0
        self.health_value = 100
        self._falling = False
        self.animation_playing = True
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
                    self.be_hiting_time = int(settings.FPS/10)
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
        if self.action == 'death' and not self.animation_playing:
            self.kill()
            return

    def _set_current_action(self, flip=False, init=False) -> None:
        action_info = self._sprite_sheet_info.get(self.action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        if init:
            super().__init__(image_sheet, self.position, fram_with, loop, flip)
        else:
            self.init_animation(image_sheet, self.position, fram_with, loop, flip)
        if self.image is None:
            return
        # self.image.set_colorkey(settings.RGB_WHITE)

    def _get_vec_with_action(self, control_action: com_type.ControlAction) -> Vector2:
        if self.is_empty_health():
            return Vector2()
        if control_action.JUMPING and not self._falling:
            self._jump_vect_y = settings.JUMP_FORCE
            self._falling = True
        x = 0
        self._jump_vect_y += settings.GRAVITY
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
            self._falling = False
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
        # bullet_speed = 0
        regular_bullet_speed = 500
        speed_time = 0.0
        if role == 'player':
            # bullet_speed = 500
            speed_time = 1.0
        else:
            speed_time = 0.5
        bs = bullet_sprite.Bullet(
            self.metadata,
            bullet_img,
            Vector2(pos_x, pos_y),
            Vector2(vect_x, vect_y),
            int(regular_bullet_speed*speed_time),
            self.tile_sprites,
            role,
            int(settings.BULLET_LIFE_TIME * (1/speed_time))
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
            if control_action.JUMPING or self._falling:
                action = 'jump'
            if control_action.SHOOT:
                if self._attack_counter == 0 or self._attack_counter%self.attack_frequency == 0:
                    self._shoot_bullet(role)
                self._attack_counter += 1
            else:
                self._attack_counter = 0
            if control_action.THROW_GRENADE:
                new_grenade = grenade_sprite.Grenade(
                    self.metadata,
                    self.grenade_img,
                    self.position,
                    -1 if self.flip else 1,
                    self.tile_sprites
                )
                self.grenade_sprites.add(new_grenade) 
                control_action.THROW_GRENADE = False
        if self.be_hiting_time > 0:
            self.be_hiting_time -= 1
            be_hit_action = f'{action}_hit'
            if be_hit_action in self._sprite_sheet_info:
                action = be_hit_action

        if action != self.action:
            self.action = action
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

