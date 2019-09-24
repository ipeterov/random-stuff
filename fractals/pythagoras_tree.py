import math
from types import SimpleNamespace

import pygame

from abstract_drawer import AbstractDrawer


SIZE = WIDTH, HEIGHT = 500, 500


class PythagorasTreeDrawer(AbstractDrawer):
    DEFAULT_PARAMS = {
        'angle': 30,
        'starting_size': 100,
        'max_depth': 2,
    }

    PARAMS_SCHEMA = {
        'angle': float,
        'starting_size': float,
        'max_depth': int,
    }

    @staticmethod
    def counterclockwise_rotate(points, anchor_index, angle):
        rad_angle = math.radians(-angle)
        anchor = points[anchor_index]

        new_points = []
        for point in points:
            if point == anchor:
                new_points.append(point)
                continue

            anc_point = point - anchor
            new_point = anchor + pygame.math.Vector2(
                anc_point.x * math.cos(rad_angle) - anc_point.y * math.sin(rad_angle),
                anc_point.x * math.sin(rad_angle) + anc_point.y * math.cos(rad_angle),
            )
            new_points.append(new_point)

        return new_points

    def draw_square(self, start, size, lean, angle):
        assert lean in ('left', 'right')
        
        if lean == 'left':
            left, bottom = start
            anchor_index = 0
        else:
            left, bottom = start[0] - size, start[1]
            anchor_index = 1
            angle *= -1

        points = [
            pygame.math.Vector2(left, bottom),
            pygame.math.Vector2(left + size, bottom),
            pygame.math.Vector2(left + size, bottom - size),
            pygame.math.Vector2(left, bottom - size),
        ]

        points = self.counterclockwise_rotate(points, anchor_index, angle)

        pygame.draw.polygon(
            self.screen,
            (255, 255, 255),
            points,
        )

        square = SimpleNamespace()
        square.points = points
        square.size = size
        square.angle = angle

        return square

    def draw_small_squares(self, big_square, depth):
        angle = self.params['angle']
        rad_angle = math.radians(angle)
        left_square = self.draw_square(
            big_square.points[-1],
            math.cos(rad_angle) * big_square.size,
            lean='left',
            angle=big_square.angle + angle,
        )
        right_square = self.draw_square(
            big_square.points[-2],
            math.sin(rad_angle) * big_square.size,
            lean='right',
            angle=90 - angle - big_square.angle,
        )

        if depth < self.params['max_depth']:
            self.draw_small_squares(left_square, depth + 1)
            self.draw_small_squares(right_square, depth + 1)

    def _get_start(self, width, height):
        return width / 2 - self.params['starting_size'] / 2, height

    def _draw(self, start):
        starting_square = self.draw_square(
            start,
            self.params['starting_size'],
            lean='left',
            angle=0,
        )
        self.draw_small_squares(
            starting_square,
            depth=1,
        )


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    drawer = PythagorasTreeDrawer(screen)
    drawer.draw()

    pygame.display.flip()

    input('Press any key to quit... ')
