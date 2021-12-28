from pygame import Vector2, image, surface

from .animation_sprite import AnimationSprite

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self._action = 'idle'
        self.position = position
        self._set_current_action()

    def _set_current_action(self) -> None:
        action_info = self._sprite_sheet_info.get(self._action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        super().__init__(image_sheet, self.position, fram_with, loop)


class PlayerSprite(RoleSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2) -> None:
        super().__init__(sprite_sheet_info, position)

    def update(self, *_, **kwargs) -> None:
        vec: Vector2 = kwargs['vec']
        action: str = kwargs['action']
        if self.rect is not None:
            self.rect = self.rect.move(vec)
        if action != self._action:
            self._action = action
            self._set_current_action()
        self.play()
