from pygame import sprite, surface, Vector2

class Grenade(sprite.Sprite):
    def __init__(self,
                 image: surface.Surface,
                 position: Vector2) -> None:
        super().__init__()

    def update(self, *_, **__) -> None:
        pass
