from typing import NamedTuple
from dataclasses import dataclass

from pygame import Vector2, rect

from .. import settings

class Line(NamedTuple):
    start_point: Vector2
    eng_point: Vector2

@dataclass
class WorldDataStruct:
    tiles_data: list[dict[str, int]]
    items_data: list[dict[str, int]]
    sprites_data: list[dict[str, int]]
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

    def _delete_img_by_pos_with_type(self, x: int, y: int, img_type: str) -> None:
        imgs_list: list[dict[str, int]]|None = None
        if img_type == settings.IMG_TYPE_TILES:
            imgs_list = self.tiles_data
        elif img_type == settings.IMG_TYPE_SPRITES:
            imgs_list = self.sprites_data
        elif img_type == settings.IMG_TYPE_ITEMS:
            imgs_list = self.items_data
        if imgs_list is None:
            return
        for index, img in enumerate(imgs_list):
            if img['x'] == x and img['y'] == y:
                del imgs_list[index]
                return

    def _get_all_imgs_info(self) -> list[list[dict[str, int]]]:
        return [self.tiles_data, self.items_data, self.sprites_data]

    def add_img_by_type(self, img_info: dict[str, int], img_type: str) -> None:
        self._delete_img_by_pos_with_type(img_info['x'], img_info['y'], img_type)
        if img_type == settings.IMG_TYPE_TILES:
            self.tiles_data.append(img_info)
        elif img_type == settings.IMG_TYPE_SPRITES:
            self.sprites_data.append(img_info)
        elif img_type == settings.IMG_TYPE_ITEMS:
            self.items_data.append(img_info)

    def collections_detect_x(self, rect: rect.Rect, x_speed: int) -> int:
        return x_speed

    def collections_detect_y(self, rect: rect.Rect, y_speed: int) -> int:
        return y_speed

