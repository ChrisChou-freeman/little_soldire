from pygame import Rect, Vector2, surface, draw, event

from .button import Button
from .. import settings
from ..lib import com_fuc

class ButtonContainer:
    def __init__(
            self,
            position: Vector2,
            width: int,
            height: int,
            color: tuple[int, int, int],
            tiles_path: str,
            metadata: dict[str, str]) -> None:
        self.tiles_path = tiles_path
        self.metadata = metadata
        self.show = False
        self.rec = Rect(position.x, position.y, width, height)
        self._color = color
        self._button_list: list[Button] = []
        self.btn_border = 15
        self._load_buttons()

    def _load_buttons(self) -> None:
        tiles_imgs = com_fuc.pygame_load_iamges_with_name(self.tiles_path)
        cols = self.rec.width//(settings.TILE_SIZE[0] + self.btn_border)
        rows = len(tiles_imgs) // cols
        if len(tiles_imgs) % cols > 0:
            rows += 1
        current_col = 0
        current_row = 0
        for file_name, tile_img in tiles_imgs.items():
            tile_position = Vector2(
                current_col*settings.TILE_SIZE[0] + current_col*self.btn_border,
                current_row*settings.TILE_SIZE[1] + current_row*self.btn_border
            )
            btn = Button(tile_img, tile_position, file_name)
            current_col += 1
            if current_col == cols:
                current_row += 1
                current_col = 0
            self._button_list.append(btn)

    def handle_input(self, key_event: event.Event) -> None:
        if not self.show:
            return
        for btn in self._button_list:
            click = btn.handle_input(key_event)
            if click:
                self.metadata['level_edit_tile'] = btn.btn_name
                print(self.metadata)

    def _selected_btn(self, screen: surface.Surface, btn: Button) -> None:
        rect = Rect(
            btn.rect.left-1,
            btn.rect.top-1,
            btn.rect.width+2,
            btn.rect.height+2
        )
        draw.rect(screen, settings.RGB_RED, rect, 2)

    def draw(self, screen: surface.Surface) -> None:
        if not self.show:
            return
        draw.rect(screen, self._color, self.rec)
        for btn in self._button_list:
            if btn.btn_name == self.metadata['level_edit_tile']:
                self._selected_btn(screen, btn)
            btn.draw(screen)

