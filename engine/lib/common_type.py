from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum, auto

from pygame import Vector2, rect

from .. import settings

class Line(NamedTuple):
    start_point: Vector2
    eng_point: Vector2

class GameMode(Enum):
    GAME_START = auto()
    GAME_PLAY = auto()
    GAME_EDITE = auto()
    GAME_EXIT = auto()

@dataclass
class WorldDataStruct:
    tiles_data: list[dict[str, int]]
    items_data: list[dict[str, int]]
    sprites_data: list[dict[str, int]]
    collition_data: dict[str, list[int]]
    level_info: dict[str, int]

    def delete_tile_by_pos(self, x: int, y: int) -> None:
        all_imgs_info = self._get_all_tiles_info()
        flag = False
        tile_type = ''
        tile = 0
        for t_type, tiles in all_imgs_info.items():
            for tile_index, tile_info in enumerate(tiles):
                if tile_info['x'] == x and tile_info['y'] == y:
                    flag = True
                    tile_type = t_type
                    tile = tile_index
                if flag:
                    del all_imgs_info[tile_type][tile]
                    return

    def _delete_tile_by_pos_with_type(self, x: int, y: int, img_type: str) -> None:
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

    def _get_tile_info_by_xy(self, x: int, y: int) -> tuple[str, dict[str, int]]:
        all_tiles_info = self._get_all_tiles_info()
        for tile_type, tiles in all_tiles_info.items():
            for tile_info in tiles:
                if tile_info['x'] == x and tile_info['y'] == y:
                    return (tile_type, tile_info)
        return ('', {})

    def _get_all_tiles_info(self) -> dict[str, list[dict[str, int]]]:
        return {
            settings.IMG_TYPE_TILES: self.tiles_data,
            settings.IMG_TYPE_ITEMS: self.items_data,
            settings.IMG_TYPE_SPRITES: self.sprites_data
        }

    def add_tile_by_type(self, img_info: dict[str, int], img_type: str) -> None:
        self._delete_tile_by_pos_with_type(img_info['x'], img_info['y'], img_type)
        if img_type == settings.IMG_TYPE_TILES:
            self.tiles_data.append(img_info)
        elif img_type == settings.IMG_TYPE_SPRITES:
            self.sprites_data.append(img_info)
        elif img_type == settings.IMG_TYPE_ITEMS:
            self.items_data.append(img_info)

    def set_unset_tile_collition(self, tile_type: str, tile: int) -> None:
        if self.collition_data.get(tile_type) is None:
            self.collition_data[tile_type] = []
        if tile in self.collition_data[tile_type]:
            self.collition_data[tile_type].remove(tile)
            return
        self.collition_data[tile_type].append (tile)

    def is_colliction_by_xy(self, x: int, y: int) -> bool:
        tile_type, tile_info = self._get_tile_info_by_xy(x, y)
        if self.collition_data.get(tile_type) is None:
            return False
        return tile_info['img'] in self.collition_data[tile_type]

    def is_colliction(self, tile_type: str, tile: int) -> bool:
        if self.collition_data.get(tile_type) is None:
            return False
        return tile in self.collition_data[tile_type]

    def collections_detect_x(self, rect: rect.Rect, x_speed: int) -> int:
        detect_x = rect.right + 1 if x_speed > 0 else rect.left + 1
        detect_y = rect.bottom
        if self.is_colliction_by_xy(detect_x//settings.TILE_SIZE[0], detect_y//settings.TILE_SIZE[1]):
            x_speed = 0
        return x_speed

    def collections_detect_y(self, rect: rect.Rect, y_speed: int) -> int:
        detect_x = rect.left
        detect_y = rect.top + 1 if y_speed < 0 else rect.bottom + 1
        if self.is_colliction_by_xy(detect_x//settings.TILE_SIZE[0], detect_y//settings.TILE_SIZE[1]):
            y_speed = 0
        return y_speed

