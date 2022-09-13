import pygame as pg
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self) -> None:
        self.display_surface = pg.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('../data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Wild flower
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name)

        # Collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pg.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites
                )

        Generic(
            pos=(0, 0),
            surf=pg.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # analytics
                    if player.drawHitbox and sprite == player:
                        pg.draw.rect(self.display_surface, 'red', offset_rect, 5)
                        hitbox_rect = player.hitbox_rect.copy()
                        hitbox_rect.center = offset_rect.center
                        pg.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pg.draw.rect(self.display_surface, 'blue', target_pos, 5)


