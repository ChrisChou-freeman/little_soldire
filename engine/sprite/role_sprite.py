import random

from pygame import Vector2, image, sprite, rect, draw, surface, transform
import pygame

from .. import lib
from .. import settings


class AnimationSprite(sprite.Sprite):
    def __init__(self,
                 image_sheet: surface.Surface,
                 position: Vector2,
                 fram_with: int,
                 loop: bool = True,
                 flip: bool = False) -> None:
        super().__init__()
        self.init_animation(image_sheet, position, fram_with, loop, flip)

    def init_animation(self,
                       image_sheet: surface.Surface,
                       position: Vector2,
                       fram_with: int,
                       loop: bool = True,
                       flip: bool = False) -> None:
        self._current_fram = 0
        self._loop = loop
        self._counter = 0
        self._frequency = 6
        self._playing = False
        self._image_sheet = image_sheet
        self._fram_with = fram_with
        self._fram_number = self._image_sheet.get_width() / fram_with
        self.rotate_value = 0.0
        self.flip = flip
        self.image = self._get_curren_fram()
        self.rect = self.image.get_rect().move(position)

    def _get_curren_fram_area(self) -> rect.Rect:
        return rect.Rect(
            self._current_fram*self._fram_with,
            0,
            self._fram_with,
            self._image_sheet.get_height()
        )

    def _get_curren_fram(self) -> surface.Surface:
        image = transform.rotate(
            self._image_sheet.subsurface(self._get_curren_fram_area()),
            self.rotate_value
        )
        if self.flip:
            image = transform.flip(image, True, False)
        return image

    def play(self) -> bool:
        playing = True
        self._counter += 1
        if self._counter % self._frequency == 0:
            if self._current_fram < self._fram_number - 1:
                self._current_fram += 1
            elif self._current_fram == self._fram_number - 1 and self._loop:
                self._current_fram = 0
            else:
                playing = False
        self.image = self._get_curren_fram()
        return playing

class Bullet(sprite.Sprite):
    def __init__(
        self,
        metadata: lib.GameMetaData,
        image: surface.Surface,
        position: Vector2,
        vect: Vector2,
        speed: int,
        tile_sprites: sprite.Group,
        bullet_type: str,
        bullet_life_time: int) -> None:
        super().__init__()
        self.metadata = metadata
        self.image = image
        self.rect = image.get_rect().move(position)
        self.speed = speed
        self.vect = vect
        self.tile_sprites = tile_sprites
        self.bullet_type = bullet_type
        self.couter = 0
        self.life_time = bullet_life_time

    def _bullet_move(self, dt: float) -> None:
        if self.rect is None:
            return
        self.rect.x += self.metadata.scroll_value
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

    def update(self, *_, **kwargs: float) -> None:
        _ = kwargs['dt']
        self.couter += 1
        dt: float = kwargs['dt']
        self._bullet_move(dt)
        self._bullet_kill_detect()

class ExplodeSprite(AnimationSprite):
    def __init__(self,
                 image_sheet: surface.Surface,
                 position: Vector2,
                 fram_with: int,
                 loop: bool = True,
                 flip: bool = False) -> None:
        super().__init__(image_sheet, position, fram_with, loop=loop, flip=flip)
        self.explode_count = 0.0

    def update(self, *_, **kwargs: float) -> None:
        dt = kwargs['dt']
        self.explode_count += dt


class Grenade(sprite.Sprite):
    def __init__(self,
                 metadata: lib.GameMetaData,
                 image: surface.Surface,
                 explode_image: surface.Surface,
                 position: Vector2,
                 direction: int,
                 tile_sprites: sprite.Group,
                 explode_sprites: sprite.Group) -> None:
        super().__init__()
        self.tile_sprites = tile_sprites
        self.throw_speed = 7
        self.vect_y = -11
        self.metadata = metadata
        self.image = image
        self.explode_image = explode_image
        self.explode_sprites = explode_sprites
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

    def update(self, *_, **kwargs: float) -> None:
        _ = kwargs['dt']
        self._grenade_parabola()

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 grenade_sprites: sprite.Group,
                 explode_sprites: sprite.Group,
                 metadata: lib.GameMetaData) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self.position = position
        self.metadata = metadata
        self.tile_sprites = tile_sprites
        self.bullet_sprites = bullet_sprites
        self.grenade_sprites = grenade_sprites
        self.explode_sprites = explode_sprites
        self.grenade_img = image.load(settings.GRENADE_IMG_PATH)
        self.explode_img = image.load(settings.EXPLODE_IMG_PATH)
        self.bullet_img = image.load(settings.BULLET_IMG_PATH)
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

    def _set_current_action(self, flip: bool=False, init: bool=False) -> None:
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

    def _get_vec_with_action(self, control_action: lib.com_type.ControlAction) -> Vector2:
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
        bs = Bullet(
            self.metadata,
            self.bullet_img,
            Vector2(pos_x, pos_y),
            Vector2(vect_x, vect_y),
            int(regular_bullet_speed*speed_time),
            self.tile_sprites,
            role,
            int(settings.BULLET_LIFE_TIME * (1/speed_time))
        )
        self.bullet_sprites.add(bs)

    def _get_action(self, control_action: lib.com_type.ControlAction, role: str = 'player') -> None:
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
                new_grenade = Grenade(
                    self.metadata,
                    self.grenade_img,
                    self.explode_img,
                    self.position,
                    -1 if self.flip else 1,
                    self.tile_sprites,
                    self.explode_sprites
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


class PlayerSprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 grenade_sprites: sprite.Group,
                 explode_sprites: sprite.Group,
                 metadata: lib.GameMetaData) -> None:
        super().__init__(sprite_sheet_info, position, tile_sprites, bullet_sprites, grenade_sprites, explode_sprites, metadata)

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

    def update(self, *_, **kwargs: float) -> None:
        _ = kwargs['dt']
        if self.is_empty_health():
            self.metadata.GAME_OVER = True
        self.move()
        self._get_action(self.metadata.control_action)
        self.play()
        self.hit_detect('player')
        self.hub()
        self._fall_off_screen_derect()


class EnemySprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 tile_sprites: sprite.Group,
                 bullet_sprites: sprite.Group,
                 player_sprite: sprite.Group,
                 grenade_sprites: sprite.Group,
                 explode_sprites: sprite.Group,
                 metadata: lib.GameMetaData) -> None:
        super().__init__(
            sprite_sheet_info,
            position,
            tile_sprites,
            bullet_sprites,
            grenade_sprites,
            explode_sprites, metadata
        )
        self._notice_symbol = image.load(settings.NOTICE_IMG_PATH)
        self._player_sprite = player_sprite
        self._ai_action = lib.com_type.ControlAction()
        self._ai_wake_time = settings.FPS * random.choice(range(0, 3)) / 2
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
            self._ai_action = lib.com_type.ControlAction()
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
        self.rect.x += self.metadata.scroll_value
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

    def update(self, *_, **kwargs: float) -> None:
        _ = kwargs['dt']
        self._ai()
        self._out_world_kill()
        self.move()
        self._get_action(self._ai_action, 'enemy')
        self.hit_detect('enemy')
        self.animation_playing = self.play()
        self.death_disappear()
        self._draw_detected_symbol()
