import pygame

from tree import TreeDrawer
from three_squares import ThreeSquaresDrawer


SIZE = WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = 0, 0, 0

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
}


def generate_fractal_controls(params, params_schema, is_keydown):
    def edit_param(name, _type, key_inc, key_dec, step=None):
        if _type in (int, float):
            value = params[name]
            diff = step(value) - value
            if pygame.key.get_pressed()[key_inc]:
                params[name] += diff
            elif pygame.key.get_pressed()[key_decrease]:
                params[name] -= diff
        elif _type == bool:
            if pygame.key.get_pressed()[key_inc]:
                params[name] = True
            elif pygame.key.get_pressed()[key_decrease]:
                params[name] = False

    # Controls will be consistent because of preserved dict order
    for i, param_name in enumerate(params):
        key_increase, key_decrease = IN_FRACTAL_CONTROLS[i]
        param_type = params_schema[param_name]
        if param_type == float:
            edit_param(
                param_name,
                param_type,
                key_increase,
                key_decrease,
                step=lambda x: x * 1.003,
            )
        elif param_type == int and is_keydown:
            edit_param(
                param_name,
                param_type,
                key_increase,
                key_decrease,
                step=lambda x: x + 1,
            )
        elif param_type == bool and is_keydown:
            edit_param(
                param_name,
                param_type,
                key_increase,
                key_decrease,
            )
        

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    drawer = list(FRACTAL_MAPPING.values())[0]()

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

                for key in FRACTAL_MAPPING:
                    if pressed[key]:
                        drawer = FRACTAL_MAPPING[key]()

        params = drawer.params.copy()
        generate_fractal_controls(params, drawer.PARAMS_SCHEMA, is_keydown)
        drawer.set_params(params)

        screen.fill(BACKGROUND_COLOR)
        drawer.draw(screen)

        pygame.display.flip()
