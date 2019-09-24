class AbstractDrawer:
    DEFAULT_PARAMS = {}
    PARAMS_SCHEMA = {}

    def __init__(self, screen):
        self.screen = screen
        self.reset_to_defaults()
        
    def reset_to_defaults(self):
        self.params = self.DEFAULT_PARAMS.copy()

    def set_params(self, new_params):
        dirty_params = new_params.copy()
        clean_params = {}
        for key, value in dirty_params.items():
            if key in self.PARAMS_SCHEMA:
                clean_params[key] = self.PARAMS_SCHEMA[key](value)
            else:
                clean_params[key] = value

        self.params = clean_params

    def draw(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        start = self._get_start(width, height)
        self._draw(start)

    def _get_start(self, width, height):
        raise NotImplementedError()

    def _draw(self, start):
        raise NotImplementedError()
