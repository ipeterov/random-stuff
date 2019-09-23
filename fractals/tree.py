import math
from types import SimpleNamespace

import pygame


SIZE = WIDTH, HEIGHT = 1700, 1400
STARTING_LENGTH = 400
STARTING_THICKNESS = 20
THICKNESS_MULTIPLIER = 0.7
LENGTH_MULTIPLIER = 0.7
ANGLE_1 = -20
ANGLE_2 = 40
MAX_DEPTH = 14


def draw_line(start, angle, length, thickness):
	end = (
		start[0] + math.cos(math.radians(angle)) * length,
		start[1] + math.sin(math.radians(angle)) * length,
	)

	# If thickness becomes 0, it wont be drawn at all
	thickness = int(thickness) or 1

	pygame.draw.line(
		screen,
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


def draw_branches(parent, depth, max_depth):
	if depth > max_depth:
		return

	new_thickness = parent.thickness * THICKNESS_MULTIPLIER
	new_length = parent.length * LENGTH_MULTIPLIER

	for new_angle in (ANGLE_1, ANGLE_2):
		new_line = draw_line(
			parent.end,
			parent.angle + new_angle,
			new_length,
			new_thickness,
		)

		if depth < max_depth:
			draw_branches(new_line, depth + 1, max_depth)


if __name__ == '__main__':
	pygame.init()

	screen = pygame.display.set_mode(SIZE)

	trunk = draw_line(
		(WIDTH / 2, HEIGHT),
		-90,
		STARTING_LENGTH,
		STARTING_THICKNESS,
	)
	draw_branches(
		trunk,
		depth=1,
		max_depth=MAX_DEPTH,
	)

	pygame.display.flip()

	input('Press any key to quit... ')
