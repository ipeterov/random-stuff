import time

import pygame
import numpy as np


SIZE = WIDTH, HEIGHT = 1000, 1000
SCALE = 3
MAX_ITERATIONS = 50

DEFAULT_X, DEFAULT_Y = -0.5, 0
DEFAULT_ZOOM = 1


def mandelbrot_array(screen_size, centerx, centery, zoom):
    width, height = screen_size
    aspect_ratio = width / height

    X = np.linspace(-aspect_ratio, aspect_ratio, width)
    Y = np.linspace(-1, 1, height)

    X /= zoom
    Y /= zoom

    X += centerx
    Y += centery

    C = X[:, None] + 1J * Y
    Z = np.zeros_like(C)

    exit_times = MAX_ITERATIONS * np.ones(C.shape, np.int32)
    mask = exit_times > 0

    for k in range(MAX_ITERATIONS):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        mask, old_mask = abs(Z) < 2, mask
        exit_times[mask ^ old_mask] = k

    return exit_times



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Mandelbrot')

    screen = pygame.display.set_mode(SIZE)

    compute_size = SIZE[0] / SCALE, SIZE[1] / SCALE

    x, y = DEFAULT_X, DEFAULT_Y
    zoom = DEFAULT_ZOOM

    was_pressed = pygame.key.get_pressed()
    last_cycle_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed = pygame.key.get_pressed()
        time_passed = time.time() - last_cycle_time

        if pressed[pygame.K_r]:
            zoom *= 1.3 ** time_passed
        elif pressed[pygame.K_f]:
            zoom /= 1.3 ** time_passed

        if pressed[pygame.K_a]:
            x -= 0.5 / zoom * time_passed
        elif pressed[pygame.K_d]:
            x += 0.5 / zoom * time_passed
        
        if pressed[pygame.K_s]:
            y += 0.5 / zoom * time_passed
        elif pressed[pygame.K_w]:
            y -= 0.5 / zoom * time_passed

        if pressed[pygame.K_SPACE]:
            x, y = DEFAULT_X, DEFAULT_Y
            zoom = DEFAULT_ZOOM

        was_pressed = pressed
        last_cycle_time = time.time()

        exit_times = mandelbrot_array(compute_size, x, y, zoom)
        pixel_array = exit_times / (MAX_ITERATIONS / 255)
        
        if SCALE == 1:
            pygame.surfarray.blit_array(screen, pixel_array)
        else:
            temp_surface = pygame.Surface(compute_size)
            pygame.surfarray.blit_array(temp_surface, pixel_array)
            pygame.transform.smoothscale(temp_surface, SIZE, screen)

        pygame.display.flip()
