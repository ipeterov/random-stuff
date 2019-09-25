# TODO: Print params

import pygame

from tree import TreeDrawer
from three_squares import ThreeSquaresDrawer
from pythagoras_tree import PythagorasTreeDrawer


SIZE = WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = 0, 0, 0
DEFAULT_SCROLL_COORDS = {
    'dx': 0,
    'dy': 0,
}

IN_FRACTAL_CONTROLS = [
    [pygame.K_q, pygame.K_a],
    [pygame.K_w, pygame.K_s],
    [pygame.K_e, pygame.K_d],
    [pygame.K_r, pygame.K_f],
    [pygame.K_t, pygame.K_g],
    [pygame.K_y, pygame.K_h],
    [pygame.K_u, pygame.K_j],
    [pygame.K_i, pygame.K_k],
    [pygame.K_o, pygame.K_l],
    [pygame.K_p, pygame.K_SEMICOLON],
]
FRACTAL_MAPPING = {
    pygame.K_z: TreeDrawer,
    pygame.K_x: ThreeSquaresDrawer,
    pygame.K_c: PythagorasTreeDrawer,
}


def edit_param(params, name, _type, key_inc, key_dec, step=None):
    if _type in (int, float):
        value = params[name]
        diff = step(value) - value
        if pygame.key.get_pressed()[key_inc]:
            params[name] += diff
        elif pygame.key.get_pressed()[key_dec]:
            params[name] -= diff
    elif _type == bool:
        if pygame.key.get_pressed()[key_inc]:
            params[name] = True
        elif pygame.key.get_pressed()[key_dec]:
            params[name] = False


def generate_fractal_controls(params, params_schema, is_keydown):
    # Controls will be consistent because of preserved dict order
    for i, param_name in enumerate(params):
        key_increase, key_decrease = IN_FRACTAL_CONTROLS[i]
        param_type = params_schema[param_name]
        if param_type == float:
            edit_param(
                params,
                param_name,
                param_type,
                key_increase,
                key_decrease,
                step=lambda x: x * 1.003,
            )
        elif param_type == int and is_keydown:
            edit_param(
                params,
                param_name,
                param_type,
                key_increase,
                key_decrease,
                step=lambda x: x + 1,
            )
        elif param_type == bool and is_keydown:
            edit_param(
                params,
                param_name,
                param_type,
                key_increase,
                key_decrease,
            )
        

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    drawer = list(FRACTAL_MAPPING.values())[0](screen)

    scroll_coords = DEFAULT_SCROLL_COORDS.copy()

    while True:
        is_keydown = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                is_keydown = True
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                    drawer.reset_to_defaults()
                    scroll_coords = DEFAULT_SCROLL_COORDS.copy()

                for key in FRACTAL_MAPPING:
                    if pressed[key]:
                        drawer = FRACTAL_MAPPING[key](screen)

        screen.fill(BACKGROUND_COLOR)

        params = drawer.params.copy()
        generate_fractal_controls(params, drawer.PARAMS_SCHEMA, is_keydown)
        drawer.set_params(params)

        edit_param(
            scroll_coords,
            'dx',
            int,
            pygame.K_RIGHT,
            pygame.K_LEFT,
            step=lambda x: x + 1,
        )
        edit_param(
            scroll_coords,
            'dy',
            int,
            pygame.K_DOWN,
            pygame.K_UP,
            step=lambda x: x + 1,
        )

        drawer.draw(scroll_coords)
        
        pygame.display.flip()
