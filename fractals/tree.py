import math
from types import SimpleNamespace

import pygame


SIZE = WIDTH, HEIGHT = 1700, 1400
STARTING_LENGTH = 300
STARTING_THICKNESS = 20
THICKNESS_MULTIPLIER = 0.7
LENGTH_MULTIPLIER = 0.7
ANGLE_1 = -60
ANGLE_2 = 40
MAX_DEPTH = 14


class TreeDrawer:
	def __init__(self, params):
		self.params = params

	def set_params(self, new_params):
		self.params = new_params

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

	screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

	tree_drawer = TreeDrawer(
		params={
			'start': (WIDTH / 2, HEIGHT),
			'starting_length': STARTING_LENGTH,
			'starting_thickness': STARTING_THICKNESS,
			'thickness_multiplier': THICKNESS_MULTIPLIER,
			'length_multiplier': LENGTH_MULTIPLIER,
			'angle_1': ANGLE_1,
			'angle_2': ANGLE_2,
			'max_depth': MAX_DEPTH,
		}
	)
	tree_drawer.draw_tree(screen)

	pygame.display.flip()

	input('Press any key to quit... ')
