import time
from types import SimpleNamespace

import pygame
import pygame.gfxdraw

from abstract_drawer import AbstractDrawer


SIZE = WIDTH, HEIGHT = 500, 500


class ThreeSquaresDrawer(AbstractDrawer):
    DEFAULT_PARAMS = {
        'starting_width': 200,
        'multiplier': 0.4,
        'depth': 1,
        'color': True,
        'gfx': True,
    }

    PARAMS_SCHEMA = {
        'starting_width': float,
        'multiplier': float,
        'depth': int,
        'color': bool,
        'gfx': bool,
    }

    def center_square(self, x, y, size, color=(255, 255, 255), gfx=False):
        if gfx:
            pygame.gfxdraw.box(
                self.screen,
                pygame.Rect(
                    x - size / 2,
                    y - size / 2,
                    size,
                    size,
                ),
                color,
            )

            rect = SimpleNamespace()
            rect.centerx = x
            rect.centery = y
            rect.width = size
            return  rect
        else:
            return pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(
                    x - size / 2,
                    y - size / 2,
                    size,
                    size,
                ),
            )

    @staticmethod
    def normalize_direction(direction):
        return direction % 360

    def draw_small_squares(self, big_square, direction, depth, max_depth):
        new_size = big_square.width * self.params['multiplier']
        distance_between_centers = big_square.width / 2 + new_size / 2

        for new_direction in map(
            self.normalize_direction,
            (direction - 90, direction, direction + 90),
        ):
            if new_direction == 0:
                new_square = self.center_square(
                    big_square.centerx,
                    big_square.centery - distance_between_centers,
                    new_size,
                    color=(255, 255, 255) if self.params['color'] else (255, 255, 255),
                    gfx=self.params['gfx'],
                )
            elif new_direction == 90:
                new_square = self.center_square(
                    big_square.centerx + distance_between_centers,
                    big_square.centery,
                    new_size,
                    color=(0, 255, 255) if self.params['color'] else (255, 255, 255),
                    gfx=self.params['gfx'],
                )
            elif new_direction == 180:
                new_square = self.center_square(
                    big_square.centerx,
                    big_square.centery + distance_between_centers,
                    new_size,
                    color=(255, 0, 255) if self.params['color'] else (255, 255, 255),
                    gfx=self.params['gfx'],
                )
            elif new_direction == 270:
                new_square = self.center_square(
                    big_square.centerx - distance_between_centers,
                    big_square.centery,
                    new_size,
                    color=(255, 255, 0) if self.params['color'] else (255, 255, 255),
                    gfx=self.params['gfx'],
                )

            if depth < max_depth:
                self.draw_small_squares(
                    new_square,
                    new_direction,
                    depth + 1,
                    max_depth,
                )

    def get_start(self, width, height):
        return width / 2, height / 2

    def _draw(self, screen, start):
        self.screen = screen
        startx, starty = start
        starting_square = self.center_square(
            startx,
            starty,
            self.params['starting_width'],
            color=(0, 128, 255) if self.params['color'] else (255, 255, 255),
            gfx=self.params['gfx'],
        )
        self.draw_small_squares(
            starting_square,
            direction=0,
            depth=1,
            max_depth=self.params['depth'],
        )


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    drawer = ThreeSquaresDrawer()
    drawer.draw(screen)

    pygame.display.flip()

    input('Press any key to quit... ')
