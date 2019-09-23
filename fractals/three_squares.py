import time
from types import SimpleNamespace

import pygame
import pygame.gfxdraw


SIZE = WIDTH, HEIGHT = 1700, 1700
STARTING_WIDTH = 700
MULTIPLIER = 0.4
DEPTH = 5
COLOR = True
GFX = True
STEP_TIME = 0.1


def center_square(x, y, size, color=(255, 255, 255), gfx=False):
	if gfx:
		pygame.gfxdraw.box(
			screen,
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
			screen,
			color,
			pygame.Rect(
				x - size / 2,
				y - size / 2,
				size,
				size,
			),
		)


def normalize_direction(direction):
	return direction % 360


def draw_small_squares(big_square, direction, depth, max_depth):
	new_size = big_square.width * MULTIPLIER
	distance_between_centers = big_square.width / 2 + new_size / 2

	for new_direction in map(
		normalize_direction,
		(direction - 90, direction, direction + 90),
	):
		if new_direction == 0:
			new_square = center_square(
				big_square.centerx,
				big_square.centery - distance_between_centers,
				new_size,
				color=(255, 255, 255) if COLOR else (255, 255, 255),
				gfx=GFX,
			)
		elif new_direction == 90:
			new_square = center_square(
				big_square.centerx + distance_between_centers,
				big_square.centery,
				new_size,
				color=(0, 255, 255) if COLOR else (255, 255, 255),
				gfx=GFX,
			)
		elif new_direction == 180:
			new_square = center_square(
				big_square.centerx,
				big_square.centery + distance_between_centers,
				new_size,
				color=(255, 0, 255) if COLOR else (255, 255, 255),
				gfx=GFX,
			)
		elif new_direction == 270:
			new_square = center_square(
				big_square.centerx - distance_between_centers,
				big_square.centery,
				new_size,
				color=(255, 255, 0) if COLOR else (255, 255, 255),
				gfx=GFX,
			)

		if depth < max_depth:
			draw_small_squares(new_square, new_direction, depth + 1, max_depth)

	if STEP_TIME:
		time.sleep(0.2)
		pygame.display.flip()



if __name__ == '__main__':
	pygame.init()

	screen = pygame.display.set_mode(SIZE)

	starting_square = center_square(
		WIDTH / 2,
		HEIGHT / 2,
		STARTING_WIDTH,
		color=(0, 128, 255) if COLOR else (255, 255, 255),
		gfx=GFX,
	)
	draw_small_squares(
		starting_square,
		direction=0,
		depth=1,
		max_depth=DEPTH,
	)

	pygame.display.flip()
	input('Press any key to quit... ')
