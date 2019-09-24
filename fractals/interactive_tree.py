import pygame

from tree import TreeDrawer, DEFAULT_PARAMS

SIZE = WIDTH, HEIGHT = 1700, 1400
BLACK = 0, 0, 0


def edit_param(params, param_name, key_increase, key_decrease):
    if pygame.key.get_pressed()[key_increase]:
        params[param_name] *= 1.05
    elif pygame.key.get_pressed()[key_decrease]:
        params[param_name] /= 1.05


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

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    tree_drawer = TreeDrawer()
    params = DEFAULT_PARAMS.copy()
    tree_drawer.set_params(params)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        edit_param(params, 'starting_length', pygame.K_q, pygame.K_a)
        edit_param(params, 'starting_thickness', pygame.K_w, pygame.K_s)
        edit_param(params, 'thickness_multiplier', pygame.K_e, pygame.K_d)
        edit_param(params, 'length_multiplier', pygame.K_r, pygame.K_f)
        edit_param(params, 'angle_1', pygame.K_t, pygame.K_g)
        edit_param(params, 'angle_2', pygame.K_y, pygame.K_h)
        edit_param(params, 'max_depth', pygame.K_u, pygame.K_j)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            params = DEFAULT_PARAMS.copy()

        screen.fill(BLACK)
        tree_drawer.set_params(params)
        tree_drawer.draw_tree(screen)

        pygame.display.flip()
