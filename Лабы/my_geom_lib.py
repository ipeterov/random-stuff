class BoundingBox:

    def __init__(self, dots):
        xs, ys = zip(*dots)
        self.x1 = min(xs)
        self.y1 = min(ys)
        self.x2 = max(xs)
        self.y2 = max(ys)

    def is_in(self, dot):
        # dot - кортеж с 2 float, координатами точки
        if self.x1 < dot[0] < self.x2 and self.y1 < dot[1] < self.y2:
            return True
        else:
            return False


class Line:

    def __init__(self, dot1, dot2):
        if dot2[0] - dot1[0] != 0:
            self.k = (dot2[1] - dot1[1]) / (dot2[0] - dot1[0])
        else:
            self.k = float('inf')
        self.b = dot1[1] - self.k * dot1[0]

    def is_under(self, dot):
        f = dot[0] * self.k + self.b
        if f < dot[0]:
            return False
        else:
            return True


class Figure:

    def __init__(self, dots):
        # coords - кортеж с кортежами по 2 float, координатами точек
        self.dots = dots
        self.lines = [Line(dots[i - 1], dots[i]) for i in range(len(dots))]
        self.bbox = BoundingBox(self.dots)
        self.center = [sum(list(x)) / len(list(x)) for x in zip(*self.dots)]
        self.center_rel_positions = [x.is_under(self.center) for x in self.lines]

    def is_in(self, dot):
        if self.bbox.is_in(dot):
            return all((self.lines[i].is_under(dot) == self.center_rel_positions[i] for i in range(len(self.lines))))
        else:
            return False


