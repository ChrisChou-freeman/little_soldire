import pygame
from pygame import surface, event, Vector2, draw

from .lib import GameManager, com_fuc, com_type
from  . import settings

class GameEditor(GameManager):
    def __init__(self, metadata: dict[str, str]) -> None:
        super().__init__(metadata)
        self.background_lays: list[surface.Surface] = []
        self.background_lays_pos: list[Vector2] = []
        self.grid_line: list[com_type.Line] = []
        self.layers_number = 2
        self._load_content()
        self.scroll_speed = 2 * len(self.background_lays)
        self.scroll_left = False
        self.scroll_right = False
        self.show_grid = False

    def _load_content(self) -> None:
        self.background_lays = com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)
        last_backgrad_width = self.background_lays[-1].get_width()
        self.background_lays_pos = [Vector2(r * last_backgrad_width, i*80) \
                for r in range(self.layers_number)\
                for i in range(len(self.background_lays))]
        last_layer_width = self.background_lays[-1].get_width()
        for y_line in range(0, settings.SCREEN_HEIGHT, settings.TILE_SIZE[1]):
            line = com_type.Line(
                Vector2(0, y_line),
                Vector2(last_layer_width*self.layers_number, y_line)
            )
            self.grid_line.append(line)

    def _scroll_backgroud(self) -> None:
        scroll_speed = 0
        if self.scroll_left and self.background_lays_pos[len(self.background_lays)-1].x >= 0:
            return
        elif self.scroll_right and self.background_lays_pos[-1].x <= settings.SCREEN_WIDTH:
            return
        elif self.scroll_left or self.scroll_right:
            scroll_speed = (self.scroll_speed * -1) if self.scroll_right else self.scroll_speed
            lay_number = len(self.background_lays)
            for index, pos in enumerate(self.background_lays_pos):
                current_lay = (index % lay_number) + 1
                pos.x += current_lay / lay_number * scroll_speed

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.KEYDOWN:
            match key_event.key:
                case pygame.K_a | pygame.K_LEFT:
                    self.scroll_left = True
                case pygame.K_d | pygame.K_RIGHT:
                    self.scroll_right = True
                case pygame.K_ESCAPE:
                    self.metadata['game_mode'] = 'GameStart'
        elif key_event.type == pygame.KEYUP:
            match key_event.key:
                case pygame.K_a | pygame.K_LEFT:
                    self.scroll_left = False
                case pygame.K_d | pygame.K_RIGHT:
                    self.scroll_right = False

    def update(self, _) -> None:
        self._scroll_backgroud()

    def _draw_grid(self, screen: surface.Surface) -> None:
        for line in self.grid_line:
            draw.line(screen, settings.RGB_WHITE, line.start_point, line.eng_point)

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self.background_lays_pos):
            lay = self.background_lays[index%len(self.background_lays)]
            screen.blit(lay, lay_pos)
        self._draw_grid(screen)

    def clear(self, screen: surface.Surface) -> None:
        self.background_lays = []
        screen.fill(settings.RGB_BLACK)
