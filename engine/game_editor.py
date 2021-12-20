import os

import pygame
from pygame import surface, event, Vector2, draw, image, rect

from  . import settings
from .ui import Button, ButtonContainer, Tip
from .lib import GameManager, com_fuc, com_type

TIP_MSG = {
    'regular': [
        's to save changes',
        'g to show or hide Grid Line',
        'c set selected tile \'s collision'
    ],
    'show_container': [
        '<tab> to switch tiles'
    ]
}

class GameEditor(GameManager):
    def __init__(self, metadata: dict[str, str]) -> None:
        super().__init__(metadata)
        self._background_lays = com_fuc.pygame_load_images_list(settings.GAME_PLAY_BACK_IMG_PATH)
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
        self._holde_mouse_right = False
        self._surface_scroll_value = 0
        self._world_data_path = os.path.join(settings.WORLD_DATA_PATH, f'{self._current_level}.pk')
        self._world_data = com_fuc.load_world_data(self._world_data_path)
        self._tip: dict[str, list[Tip]] = {}
        self._init_content()

    def _init_content(self) -> None:
        # init background
        last_backgrad_width = self._background_lays[-1].get_width()
        self._background_lays_pos = [Vector2(r * last_backgrad_width, i*80) \
                for r in range(self._layers_repets) \
                for i in range(len(self._background_lays))]
        last_layer_width = self._background_lays[-1].get_width()
        for y_line in range(0, settings.SCREEN_HEIGHT, settings.TILE_SIZE[1]):
            line = com_type.Line(
                Vector2(0, y_line),
                Vector2(last_layer_width*self._layers_repets, y_line)
            )
            self._grid_line.append(line)
        # init grid
        for x_line in range(0, last_layer_width*self._layers_repets, settings.TILE_SIZE[0]):
            line = com_type.Line(
                Vector2(x_line, 0),
                Vector2(x_line, settings.SCREEN_HEIGHT)
            )
            self._grid_line.append(line)
        # init tip
        tip_start = [settings.SCREEN_WIDTH - 10, settings.SCREEN_HEIGHT-settings.SCREEN_HEIGHT/10]
        tip_gap = 30
        for tip_type, msgs in TIP_MSG.items():
            if self._tip.get(tip_type) is None:
                self._tip[tip_type] = []
            for index, msg in enumerate(msgs):
                tip_obj = Tip(msg, Vector2(tip_start[0], tip_start[1] - tip_gap*index), 25)
                self._tip[tip_type].append(tip_obj)

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
                dif_lay_speed = int(current_lay / lay_number * scroll_speed)
                pos.x += dif_lay_speed
                if index == len(self._background_lays_pos) - 1:
                    last_layer_scl_speed = dif_lay_speed
            self._surface_scroll_value += last_layer_scl_speed

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
            elif key_event.button == pygame.BUTTON_RIGHT:
                self._holde_mouse_right = True
        elif key_event.type == pygame.MOUSEBUTTONUP:
            if key_event.button == pygame.BUTTON_LEFT:
                self._holde_mouse_left = False
            elif key_event.button == pygame.BUTTON_RIGHT:
                self._holde_mouse_right = False
        elif key_event.type == pygame.MOUSEMOTION:
            mouse_x = key_event.pos[0] - self._surface_scroll_value
            tile_x, tile_y = mouse_x//32, key_event.pos[1]//32
            if tile_y > settings.SCREEN_HEIGHT//32-1:
                return
            if self._holde_mouse_left \
                    and self._has_grid_area(key_event) \
                    and self.metadata['level_edit_tile'] != '':
                # draw tiles
                tile_type, tile_name = self.metadata['level_edit_tile'].split('_')
                png_data = {
                    'x': tile_x,
                    'y': tile_y,
                    'img': int(tile_name.split('.')[0])
                }
                self._world_data.add_img_by_type(png_data, tile_type)
            elif self._holde_mouse_right \
                    and self._has_grid_area(key_event):
                self._world_data.delete_img_by_pos(tile_x, tile_y)

    def handle_input(self, key_event: event.Event) -> None:
        self._tiles_button.handle_input(key_event, self._tiles_button_click)
        self._menu_container.handle_input(key_event)
        if key_event.type == pygame.KEYDOWN:
            if key_event.key in [pygame.K_a, pygame.K_LEFT]:
                self._scroll_left = True
            elif key_event.key in [pygame.K_d, pygame.K_RIGHT]:
                self._scroll_right = True
            elif key_event.key == pygame.K_g:
                self._show_grid = False if self._show_grid else True
            elif key_event.key == pygame.K_ESCAPE:
                self.metadata['game_mode'] = 'GameStart'
            elif key_event.key == pygame.K_s:
                com_fuc.write_world_data(self._world_data_path, self._world_data)
            elif key_event.key == pygame.K_c and self.metadata['level_edit_tile'] != '':
                tile_type, tile = self.metadata['level_edit_tile'].split('.')[0].split('_')
                self._world_data.set_unset_tile_collition(tile_type, int(tile))
        elif key_event.type == pygame.KEYUP:
            if key_event.key in [pygame.K_a, pygame.K_LEFT]:
                self._scroll_left = False
            elif key_event.key in [pygame.K_d, pygame.K_RIGHT]:
                self._scroll_right = False
        self._draw_tiles(key_event)

    def update(self, _) -> None:
        self._scroll_backgroud()

    def _draw_grid(self, screen: surface.Surface) -> None:
        if not self._show_grid:
            return
        for line in self._grid_line:
            start_point = Vector2(
                line.start_point.x + self._surface_scroll_value,
                line.start_point.y
            )
            eng_point = Vector2(
                line.eng_point.x + self._surface_scroll_value,
                line.eng_point.y
            )
            draw.line(screen, settings.RGB_WHITE, start_point, eng_point)

    def _draw_collition_box(self,
                            screen: surface.Surface,
                            tile_type: str,
                            tile: int,
                            rect_obj: rect.Rect) -> None:
        if not self._world_data.is_colliction(tile_type, tile):
            return
        draw.rect(screen, settings.RGB_RED, rect_obj, 1)

    def _rander_world_data(self,
            screen: surface.Surface,
            datas_info: list[dict[str, int]],
            img_type: str) -> None:
        for data_info in datas_info:
            x, y, img = data_info['x'], data_info['y'], data_info['img']
            tile_name = f'{img_type}_{img}.png'
            img_surface: surface.Surface|None = None
            if img_type == settings.IMG_TYPE_TILES:
                img_surface = self._tiles_images[tile_name]
            elif img_type == settings.IMG_TYPE_SPRITES:
                img_surface = self._sprite_images[tile_name]
            elif img_type == settings.IMG_TYPE_ITEMS:
                img_surface = self._item_images[tile_name]
            x_pos = x * settings.TILE_SIZE[0] + self._surface_scroll_value
            y_pos = y * settings.TILE_SIZE[1]
            if img_surface is not None:
                screen.blit(img_surface, Vector2(x_pos, y_pos))
                self._draw_collition_box(
                    screen,
                    img_type,
                    img,
                    rect.Rect(x_pos, y_pos, img_surface.get_width(), img_surface.get_height())
                )

    def _draw_tips(self, screen: surface.Surface) -> None:
        tips_list: list[Tip] = []
        if self._menu_container.show:
            tips_list = self._tip['show_container']
        else:
            tips_list = self._tip['regular']
        for tip in tips_list:
            tip.draw(screen)

    def draw(self, screen: surface.Surface) -> None:
        for index,lay_pos in enumerate(self._background_lays_pos):
            lay = self._background_lays[index%len(self._background_lays)]
            screen.blit(lay, lay_pos)
        self._draw_grid(screen)
        self._rander_world_data(screen, self._world_data.tiles_data, settings.IMG_TYPE_TILES)
        self._rander_world_data(screen, self._world_data.items_data, settings.IMG_TYPE_ITEMS)
        self._rander_world_data(screen, self._world_data.sprites_data, settings.IMG_TYPE_SPRITES)
        self._tiles_button.draw(screen)
        self._menu_container.draw(screen)
        self._draw_tips(screen)

    def clear(self, screen: surface.Surface) -> None:
        self._background_lays = []
        screen.fill(settings.RGB_BLACK)

