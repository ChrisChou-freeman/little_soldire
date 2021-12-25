from pygame import Vector2, image

from .animation_sprite import AnimationSprite

class RoleSprite:
    def __init__(self,
                 sprite_sheet_info: dict[str, dict[str, str]],
                 position: Vector2) -> None:
        self.position = position
        self._sprite_sheet_info = sprite_sheet_info
        self._animation_map: dict[str, AnimationSprite] = {}
        self._load_animation()

    def _load_animation(self) -> None:
        for name, info in self._sprite_sheet_info.items():
            img_sheet = image.load(info['image_sheet'])
            is_loop = True if info['loop'] == '1' else False
            animation_sprite = AnimationSprite(img_sheet, self.position, int(info['fram_with']), is_loop)
            self._animation_map[name] = animation_sprite

    def play(self, action: str) -> None:
        action_a_sprite = self._animation_map.get(action, None)
        if action_a_sprite is None:
            return
        action_a_sprite.play()

