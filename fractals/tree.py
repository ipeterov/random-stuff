import math
from types import SimpleNamespace

import pygame

from abstract_drawer import AbstractDrawer


SIZE = WIDTH, HEIGHT = 500, 500


class TreeDrawer(AbstractDrawer):
    DEFAULT_PARAMS = {
        'starting_length': 100,
        'starting_thickness': 10,
        'thickness_multiplier': 0.7,
        'length_multiplier': 0.7,
        'angle_1': -60,
        'angle_2': 40,
        'max_depth': 7,
    }

    PARAMS_SCHEMA = {
        'starting_length': float,
        'starting_thickness': float,
        'thickness_multiplier': float,
        'length_multiplier': float,
        'angle_1': float,
        'angle_2': float,
        'max_depth': int,
    }

    def draw_line(self, start, angle, length, thickness):
        end = (
            start[0] + math.cos(math.radians(angle)) * length,
            start[1] + math.sin(math.radians(angle)) * length,
        )

        # If thickness becomes 0, it wont be drawn at all
        thickness = int(thickness) or 1

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            start,
            end,
            thickness,
        )

        line = SimpleNamespace()
        line.end = end
        line.angle = angle
        line.length = length
        line.thickness = thickness
        return line


    def draw_branches(self, parent, depth, max_depth):
        if depth > max_depth:
            return

        new_thickness = parent.thickness * self.params['thickness_multiplier']
        new_length = parent.length * self.params['length_multiplier']

        for new_angle in (self.params['angle_1'], self.params['angle_2']):
            new_line = self.draw_line(
                parent.end,
                parent.angle + new_angle,
                new_length,
                new_thickness,
            )

            if depth < max_depth:
                self.draw_branches(new_line, depth + 1, max_depth)

    def get_start(self, width, height):
        return (width / 2, height)

    def _draw(self, screen, start):
        self.screen = screen
        trunk = self.draw_line(
            start,
            -90,
            self.params['starting_length'],
            self.params['starting_thickness'],
        )
        self.draw_branches(
            trunk,
            depth=1,
            max_depth=self.params['max_depth'],
        )


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    drawer = TreeDrawer()
    drawer.draw(screen)

    pygame.display.flip()

    input('Press any key to quit... ')
