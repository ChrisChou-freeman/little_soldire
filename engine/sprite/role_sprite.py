from pygame import Vector2, image

from .animation_sprite import AnimationSprite
from ..lib import GameDataStruct

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self._action = 'idle'
        self.position = position
        self._set_current_action()

    def _set_current_action(self, flip=False) -> None:
        action_info = self._sprite_sheet_info.get(self._action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        super().__init__(image_sheet, self.position, fram_with, loop, flip)


class PlayerSprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2,
                 world_data_obj: GameDataStruct) -> None:
        super().__init__(sprite_sheet_info, position)
        self.world_data_obj = world_data_obj

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
            vec.x, vec.y = self.world_data_obj.collections_detect(self.rect, int(vec.x), int(vec.y))
            self.rect = self.rect.move(vec)
            self.position.x, self.position.y = self.rect.x, self.rect.y
        if action != self._action:
            self._action = action
            self._set_current_action(self.flip)
        self.play()
