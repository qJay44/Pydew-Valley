import pygame
import sys
import os
from settings import *
from level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Sprout land')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F6:
                        pygame.quit()
                        sys.exit()

            delta = self.clock.tick() / 1000
            self.level.run(delta)
            pygame.display.update()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    game = Game()
    game.run()
