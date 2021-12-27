from pygame import Vector2, image, surface

from .animation_sprite import AnimationSprite

class RoleSprite(AnimationSprite):
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2) -> None:
        self._sprite_sheet_info = sprite_sheet_info
        self.position = position
        self.set_current_action()

    def set_current_action(self, action: str = 'idle') -> None:
        action_info = self._sprite_sheet_info.get(action, None)
        if action_info is None:
            return
        image_sheet = image.load(action_info['image_sheet'])
        fram_with = int(action_info['fram_with'])
        loop = True if action_info['loop'] == '1' else False
        super().__init__(image_sheet, self.position, fram_with, loop)

    def update(self, *_, **__) -> None:
        self.play()
