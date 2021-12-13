import os

from pygame import surface, event, Vector2, draw, image
import pygame

from .lib import GameManager, com_fuc, com_type
from .ui import Button, ButtonContainer
from  . import settings

class GameEditor(GameManager):
    def __init__(self, metadata: dict[str, str]) -> None:
        super().__init__(metadata)
        self._background_lays: list[surface.Surface] = []
        self._background_lays_pos: list[Vector2] = []
        self._grid_line: list[com_type.Line] = []
        self._tiles_button = Button(image.load(settings.TILES_BTN_IMG_PATH), Vector2(20, 20), '')
        self._tiles_images = com_fuc.pygame_load_iamges_with_name(settings.TILES_IMG_PATH)
        self._item_images = com_fuc.pygame_load_iamges_with_name(settings.ITEMS_IMG_PATH)
        self._sprite_images = com_fuc.pygame_load_iamges_with_name(settings.SPRITE_IMG_PATH)
        self._menu_container = ButtonContainer(
            Vector2(0, 0),
            settings.SCREEN_WIDTH,
            int(settings.SCREEN_HEIGHT/3),
            settings.RGB_GRAY,
            [self._tiles_images, self._item_images, self._sprite_images],
            metadata
        )
        self._layers_repets = 2
        self._current_level = 0
        self._scroll_speed = 2 * len(self._background_lays)
        self._scroll_left = False
        self._scroll_right = False
        self._show_grid = False
        self._holde_mouse_left = False
        self._world_data_path = os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        self._world_data = com_fuc.load_world_data(self._world_data_path)
        self._load_content()

    def _load_content(self) -> None:
        self._background_lays = com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)
        last_backgrad_width = self._background_lays[-1].get_width()
        self._background_lays_pos = [Vector2(r * last_backgrad_width, i*80) \
                for r in range(self._layers_repets)\
                for i in range(len(self._background_lays))]
        last_layer_width = self._background_lays[-1].get_width()
        for y_line in range(0, settings.SCREEN_HEIGHT, settings.TILE_SIZE[1]):
            line = com_type.Line(
                Vector2(0, y_line),
                Vector2(last_layer_width*self._layers_repets, y_line)
            )
            self._grid_line.append(line)
        for x_line in range(0, last_layer_width*self._layers_repets, settings.TILE_SIZE[0]):
            line = com_type.Line(
                Vector2(x_line, 0),
                Vector2(x_line, settings.SCREEN_HEIGHT)
            )
            self._grid_line.append(line)

    def _scroll_backgroud(self) -> None:
        scroll_speed = 0
        if self._scroll_left and self._background_lays_pos[len(self._background_lays)-1].x >= 0:
            return
        elif self._scroll_right and (self._background_lays_pos[-1].x + self._background_lays[-1].get_width()) <= settings.SCREEN_WIDTH:
            return
        elif self._scroll_left or self._scroll_right:
            scroll_speed = (self._scroll_speed * -1) if self._scroll_right else self._scroll_speed
            lay_number = len(self._background_lays)
            last_layer_scl_speed = 0
            for index, pos in enumerate(self._background_lays_pos):
                current_lay = (index % lay_number) + 1
                dif_lay_speed = current_lay / lay_number * scroll_speed
                pos.x += dif_lay_speed
                if index == len(self._background_lays_pos) - 1:
                    last_layer_scl_speed = dif_lay_speed
            for line in self._grid_line:
                line.start_point.x += last_layer_scl_speed
                line.eng_point.x += last_layer_scl_speed

    def _tiles_button_click(self) -> None:
        if self._menu_container.show:
            self._menu_container.show = False
            self._tiles_button.position.y -= self._menu_container.rec.height
            self._tiles_button.rect.top -= self._menu_container.rec.height
            self._tiles_button.rect_selected.top -= self._menu_container.rec.height
        else:
            self._menu_container.show = True
            self._tiles_button.position.y += self._menu_container.rec.height
            self._tiles_button.rect.top += self._menu_container.rec.height
            self._tiles_button.rect_selected.top += self._menu_container.rec.height

    def _has_grid_area(self, key_event: event.Event) -> bool:
        pos = key_event.pos
        if self._menu_container.show and self._menu_container.rec.collidepoint(pos):
            return False
        if self._tiles_button.rect.collidepoint(pos):
            return False
        return True

    def _draw_tiles(self, key_event: event.Event) -> None:
        if key_event.type == pygame.MOUSEBUTTONDOWN:
            if key_event.button == pygame.BUTTON_LEFT:
                self._holde_mouse_left = True
        elif key_event.type == pygame.MOUSEBUTTONUP:
            if key_event.button == pygame.BUTTON_LEFT:
                self._holde_mouse_left = False
        if self._holde_mouse_left and self._has_grid_area(key_event):
            # draw tiles
            tile_x, tile_y = key_event.pos[0]//32, key_event.pos[1]//32
            tile_type, tile_name = self.metadata['level_edit_tile'].split('_')
            png_data = {'x': tile_x, 'y': tile_y, 'img': int(tile_name.split('.')[0])}
            match tile_type:
                case 'tile':
                    self._world_data.tile_data.append(png_data)
                case 'item':
                    self._world_data.item_data.append(png_data)
                case 'sprite':
                    self._world_data.sprite_data.append(png_data)

    def handle_input(self, key_event: event.Event) -> None:
        self._tiles_button.handle_input(key_event, self._tiles_button_click)
        self._menu_container.handle_input(key_event)
        if key_event.type == pygame.KEYDOWN:
            match key_event.key:
                case pygame.K_a | pygame.K_LEFT:
                    self._scroll_left = True
                case pygame.K_d | pygame.K_RIGHT:
                    self._scroll_right = True
                case pygame.K_g:
                    self._show_grid = False if self._show_grid else True
                case pygame.K_ESCAPE:
                    self.metadata['game_mode'] = 'GameStart'
        elif key_event.type == pygame.KEYUP:
            match key_event.key:
                case pygame.K_a | pygame.K_LEFT:
                    self._scroll_left = False
                case pygame.K_d | pygame.K_RIGHT:
                    self._scroll_right = False
        self._draw_tiles(key_event)

    def update(self, _) -> None:
        self._scroll_backgroud()

    def _draw_grid(self, screen: surface.Surface) -> None:
        if not self._show_grid:
            return
        for line in self._grid_line:
            draw.line(screen, settings.RGB_WHITE, line.start_point, line.eng_point)

    def _rander_world_data(self,
            screen: surface.Surface,
            datas_info: list[dict[str, int]],
            img_type: str) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{img_type}_{img}.png'
            img_surface: surface.Surface|None = None
            match img_type:
                case 'tile':
                    img_surface = self._tiles_images[tile_name]
                case 'sprite':
                    img_surface = self._sprite_images[tile_name]
                case 'items':
                    img_surface = self._item_images[tile_name]
            if img_surface is not None:
                screen.blit(img_surface, Vector2(x*32, y*32))

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index%len(self._background_lays)]
            screen.blit(lay, lay_pos)
        self._draw_grid(screen)
        self._tiles_button.draw(screen)
        self._menu_container.draw(screen)
        self._rander_world_data(screen, self._world_data.tile_data, 'tile')
        self._rander_world_data(screen, self._world_data.item_data, 'item')
        self._rander_world_data(screen, self._world_data.sprite_data, 'sprite')

    def clear(self, screen: surface.Surface) -> None:
        self._background_lays = []
        screen.fill(settings.RGB_BLACK)

