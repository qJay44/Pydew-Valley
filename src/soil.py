import pygame as pg
import numpy as np
from settings import *
from pytmx.util_pygame import load_pygame


class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class SoilLayer:
    def __init__(self, all_sprites) -> None:

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pg.sprite.Group()

        # graphics
        self.soil_surf = pg.image.load('../graphics/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pg.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = np.empty((v_tiles, h_tiles), dtype=str)
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x] = 'F'

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x] = 'X'
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf=self.soil_surf,
                        groups=[self.all_sprites, self.soil_sprites]
                    )

    def _debug(self):
        with np.printoptions(threshold=np.inf):
            print(self.grid)


