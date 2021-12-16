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
        all_imgs_info = self._get_all_imgs_info()
        flag = False
        imgs = 0
        img = 0
        for imgs_index, imgs_info in enumerate(all_imgs_info):
            for img_index, png_info in enumerate(imgs_info):
                if png_info['x'] == x and png_info['y'] == y:
                    flag = True
                    imgs = imgs_index
                    img = img_index
                if flag:
                    del all_imgs_info[imgs][img]
                    return

    def _get_all_imgs_info(self) -> list[list[dict[str, int]]]:
        return [self.tile_data, self.item_data, self.sprite_data]

    def add_img_by_type(self, img_info: dict[str, int], img_type: str) -> None:
        self.delete_img_by_pos(img_info['x'], img_info['y'])
        match img_type:
            case 'tile':
                self.tile_data.append(img_info)
            case 'item':
                self.item_data.append(img_info)
            case 'sprite':
                self.sprite_data.append(img_info)

