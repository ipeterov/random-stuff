import wrapt_timeout_decorator


class Delta:
    is_strong = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Дельта ({self.x}, {self.y})"

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def _get_class(self, other):
        if self.is_strong >= other.is_strong:
            return self.__class__
        else:
            return other.__class__

    def __add__(self, other):
        return self._get_class(other)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self._get_class(other)(self.x - other.x, self.y - other.y)


class Point(Delta):
    is_strong = True

    def __repr__(self):
        return f"Точка ({self.x}, {self.y})"


GRID_SIZE = 20
START = Point(0, 0)
END = Point(GRID_SIZE, GRID_SIZE)


# NOT WORKING


def traverse(point):
    if point == END:
        return 1

    paths_count = 0

    if point.x < GRID_SIZE:
        paths_count += traverse(point + Delta(1, 0))

    if point.y < GRID_SIZE:
        paths_count += traverse(point + Delta(0, 1))

    print(point, paths_count)

    return paths_count


@wrapt_timeout_decorator.timeout(60)
def solve():
    return traverse(START)
