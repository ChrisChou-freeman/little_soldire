from pygame import surface, Vector2, sprite, rect, transform

class AnimationSprite(sprite.Sprite):
    def __init__(self,
                 image_sheet: surface.Surface,
                 position: Vector2,
                 fram_with: int,
                 loop: bool=True,
                 flip:bool=False) -> None:
        super().__init__()
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
        image = transform.rotate(self._image_sheet.subsurface(self._get_curren_fram_area()), self.rotate_value)
        if self.flip:
            image = transform.flip(image, True, False)
        return image

    def play(self) -> None:
        self._counter += 1
        if self._counter % self._frequency == 0:
            if self._current_fram < self._fram_number - 1:
                self._current_fram += 1
            elif self._current_fram == self._fram_number - 1 and self._loop:
                self._current_fram = 0
        self.image = self._get_curren_fram()

