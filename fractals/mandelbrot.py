from functools import reduce

import pygame

from abstract_drawer import AbstractDrawer


SIZE = WIDTH, HEIGHT = 1000, 600


class MandelbrotDrawer(AbstractDrawer):
    DEFAULT_PARAMS = {
        'max_iterations': 20,
        'size': 200,
    }

    PARAMS_SCHEMA = {
        'max_iterations': int,
        'size': float,
    }

    def color_from_gradient(self, index, max_index):
        color1 = pygame.Color('black')
        color2 = pygame.Color('white')

        return pygame.Color(
            int(color1.r + (color2.r - color1.r) * (index / max_index)),
            int(color1.g + (color2.g - color1.g) * (index / max_index)),
            int(color1.b + (color2.b - color1.b) * (index / max_index)),
        )

    def mandelbrot(self, point):
        max_i = self.params['max_iterations']

        z = 0
        for i in range(max_i):
            if abs(z) > 2:
                return self.color_from_gradient(i, max_i)
            z = z * z + point

        return pygame.Color('white')

    def _get_default_start(self, width, height):
        return width / 2, height / 2

    def _draw(self, start):
        pxarray = pygame.PixelArray(self.screen)

        for x, column in enumerate(pxarray):
            for y, pixel in enumerate(column):
                norm_x = (x - start[0]) / self.params['size']
                norm_y = (y - start[1]) / self.params['size']

                pxarray[x, y] = self.mandelbrot(complex(norm_x, norm_y))


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    drawer = MandelbrotDrawer(screen)
    drawer.draw()

    pygame.display.flip()

    input('Press any key to quit... ')
