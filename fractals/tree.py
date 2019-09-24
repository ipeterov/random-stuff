import math
from types import SimpleNamespace

import pygame


SIZE = WIDTH, HEIGHT = 1700, 1400
DEFAULT_PARAMS = {
    'start': (WIDTH / 2, HEIGHT),
    'starting_length': 300,
    'starting_thickness': 20,
    'thickness_multiplier': 0.7,
    'length_multiplier': 0.7,
    'angle_1': -60,
    'angle_2': 40,
    'max_depth': 14,
}


class TreeDrawer:
    PARAMS_SCHEMA = {
        'start': tuple,
        'starting_length': float,
        'starting_thickness': float,
        'thickness_multiplier': float,
        'length_multiplier': float,
        'angle_1': float,
        'angle_2': float,
        'max_depth': lambda val: min(int(val), 16),
    }

    def set_params(self, new_params):
        dirty_params = new_params.copy()
        clean_params = {}
        for key, value in dirty_params.items():
            if key in self.PARAMS_SCHEMA:
                clean_params[key] = self.PARAMS_SCHEMA[key](value)
            else:
                clean_params[key] = value

        self.params = clean_params

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

    def draw_tree(self, screen):
        self.screen = screen
        trunk = self.draw_line(
            self.params['start'],
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

    tree_drawer = TreeDrawer()
    tree_drawer.set_params(DEFAULT_PARAMS)
    tree_drawer.draw_tree(screen)

    pygame.display.flip()

    input('Press any key to quit... ')
