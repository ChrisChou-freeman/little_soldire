import os
import pickle
from dataclasses import dataclass
from typing import Optional

from pygame import surface

from .. import settings
from .common_type import ControlAction

@dataclass
class GameMetaData:
    game_mode: str
    level_edit_tile: str
    scroll_value_x: int
    scroll_value_y: int
    screen_shake: int
    screen_shake_x: int
    screen_shake_y: int
    control_action: ControlAction
    scrren: surface.Surface
    GAME_OVER: bool = False

@dataclass
class GameDataStruct:
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
        imgs_list: Optional[list[dict[str, int]]] = None
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

    @classmethod
    def load_world_data(cls, world_data_path: str) -> 'GameDataStruct':
        world_data_obj: GameDataStruct
        if not os.path.exists(world_data_path):
            world_data_obj = GameDataStruct([], [], [], {}, {})
            return world_data_obj
        with open(world_data_path, 'rb') as file_obj:
            world_data_obj = pickle.load(file_obj)
            return world_data_obj

    def write_world_data(self, world_data_path: str) -> None:
        with open(world_data_path, 'wb') as  file_obj:
            pickle.dump(self, file_obj)

