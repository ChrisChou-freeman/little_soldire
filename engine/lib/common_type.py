from typing import NamedTuple
from dataclasses import dataclass

from pygame import Vector2

class Line(NamedTuple):
    start_point: Vector2
    eng_point: Vector2

@dataclass
class WorldDataStruct:
    tile_data: list[dict[str, int]]
    collition_data: dict[str, list[int]]
    level_info: dict[str, int]
