import pygame as pg
from settings import *
from support import *
from timer import Timer


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool),
            'tool_switch': Timer(200),
            'seed_use': Timer(350, self.use_seed),
            'seed_switch': Timer(200)
        }

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
            'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
            'up_water': [], 'down_water': [], 'left_water': [], 'right_water': [],
        }

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pg.key.get_pressed()

        if not self.timers['tool_use'].active:
            # directions
            if keys[pg.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pg.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # tool use
            if keys[pg.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0

            # change tool
            if keys[pg.K_q] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index = self.tool_index + 1 if self.tool_index != len(self.tools) - 1 else 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pg.K_LCTRL]:
                self.timers['seed_use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0

            # change seed
            if keys[pg.K_e] and not self.timers['seed_switch'].active:
                self.timers['seed_switch'].activate()
                self.seed_index = self.seed_index + 1 if self.seed_index != len(self.seeds) - 1 else 0
                self.selected_seed = self.seeds[self.seed_index]

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)

