class AbstractDrawer:
    DEFAULT_PARAMS = {}
    PARAMS_SCHEMA = {}

    def __init__(self, screen):
        self.screen = screen
        self.reset_to_defaults()
        
    def reset_start(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        self.start = self._get_default_start(width, height)

    def reset_to_defaults(self):
        self.set_params(self.DEFAULT_PARAMS)
        self.reset_start()

    def set_params(self, new_params):
        dirty_params = new_params.copy()
        clean_params = {}
        for key, value in dirty_params.items():
            if key in self.PARAMS_SCHEMA:
                clean_params[key] = self.PARAMS_SCHEMA[key](value)
            else:
                clean_params[key] = value

        self.params = clean_params

    def draw(self, scroll_coords={'dx': 0, 'dy': 0}):
        coords = [
            self.start[0] + scroll_coords['dx'],
            self.start[1] + scroll_coords['dy'],
        ]

        self._draw(coords)

    def _get_default_start(self, width, height):
        raise NotImplementedError()

    def _draw(self, start):
        raise NotImplementedError()
