from typing import NamedTuple
from dataclasses import dataclass

from pygame import Vector2

class Line(NamedTuple):
    start_point: Vector2
    eng_point: Vector2

@dataclass
class ControlAction:
    RUN_LEFT: bool = False
    RUN_RIGHT: bool = False
    IDLE: bool = False
    JUMPING: bool = False
    SHOOT:bool = False
