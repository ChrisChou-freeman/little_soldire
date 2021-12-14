from typing import NamedTuple
from dataclasses import dataclass

from pygame import Vector2

class Line(NamedTuple):
    start_point: Vector2
    eng_point: Vector2

@dataclass
class WorldDataStruct:
    tile_data: list[dict[str, int]]
    item_data: list[dict[str, int]]
    sprite_data: list[dict[str, int]]
    collition_data: dict[str, list[int]]
    level_info: dict[str, int]

    def delete_img_by_pos(self, x: int, y: int) -> None:
        pass

    def update_img_by_pos(self, x: int, y: int) -> None:
        pass

    def _get_all_pngs_info(self) -> list[list[dict[str, int]]]:
        return [self.tile_data, self. item_data, self.sprite_data]

    def add_img_by_type(self, img_info: dict[str, int], img_type: str) -> None:
        match img_type:
            case 'tile':
                self.tile_data.append(img_info)
            case 'item':
                self.item_data.append(img_info)
            case 'sprite':
                self.sprite_data.append(img_info)

    def scroll_word(self, scroll_speed: int) -> None:
        for pngs_info in self._get_all_pngs_info():
            for png_info in pngs_info:
                png_info['scroll'] += scroll_speed

