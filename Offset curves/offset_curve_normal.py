import matplotlib.pyplot as plt
from math import *
import numpy as np

"""
Идеи:
* Переписать все классы чтобы они использовали класс dot
* Переписать метод next_point, подумать над его архитектурой
"""

class point:
    def __init__(self, x, y):
        self.x = x; self.y = y
        
    def dist(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        
    def get_tuple(self):
        return (self.x, self.y)

class line:
    def __init__(self, *args, **kwargs):
        
        if type(args[0]) in (tuple, list):
            dot1, dot2 = args[0], args[1]
            if dot2[0] - dot1[0] != 0:
                self.k = (dot2[1] - dot1[1]) / (dot2[0] - dot1[0])
            else:
                self.k = float('inf')
            self.b = dot1[1] - self.k * dot1[0]
            
        elif type(args[0]) in (int, float):
            self.k, self.b = args[0], args[1]
        
        self.ang = atan(self.k)
    
    def is_under(self, dot):
        f = dot[0] * self.k + self.b
        if f < dot[0]:
            return False
        else:
            return True
            
    def perpendicular(self, dot):
        if self.k != float('inf'):
            p_k = tan(self.ang + pi / 2)
        else:
            p_k = 0
        p_b = dot[1] - p_k * dot[0]
        
        return line(p_k, p_b)
        
    def intersection_point(self, other_line):
        x = -1 * (self.b - other_line.b) / (self.k - other_line.k)
        y = self.k * x + self.b
        
        return (x, y)
        
    def next_point(self, point1, point2, dist):
        x, y = point2[0] - point1[0], point2[1] - point1[1]
        if x == y == 0:
            return None
        else:
            hypot = (x**2 + y**2)**0.5
            coeff = dist / hypot
            dx, dy = x * coeff, y * coeff
            return point(point2[0] + dx, point2[1] + dy)

class curve:
    def __init__(self, dots):
        # coords - кортеж с кортежами по 2 float, координатами точек
        self.dots = dots
        self.lines = [line(dots[i-1], dots[i]) for i in range(len(dots))]
        self.center = [sum(list(x)) / len(list(x)) for x in zip(*self.dots)]
        self.center_rel_positions = [x.is_under(self.center) for x in self.lines]

    def is_in(self, dot):
        matches = True
        for i in range(len(self.lines)):
            if self.lines[i].is_under(dot) != self.center_rel_positions[i]:
                matches = False
                break
        
        return matches
            
    def make_offset_curve(self, dist):
        offset_dots = []
        for i in range(-2, len(self.dots) - 2):
            tangent = line(self.dots[i], self.dots[i+2])
            normal = tangent.perpendicular(self.dots[i+1])
            intersect = tangent.intersection_point(normal)
            offset_dot_vars = normal.next_point(intersect, self.dots[i+1], dist), normal.next_point(self.dots[i+1], intersect, dist)
            if offset_dots:
                if offset_dot_vars[0]:
                    offset_dots.append(min(offset_dot_vars, key=lambda x: x.dist(offset_dots[-1])))
            else:
                offset_dots.append(normal.next_point(self.dots[i+1],intersect, dist))

        return offset_dots

orig_curve_dots = []
with open('points.txt', 'r') as f:
    for string in f:
        dot = [float(x) for x in string.split()]
        orig_curve_dots.append(dot) #if dot not in orig_curve_dots: 

orig_curve = curve(orig_curve_dots)
offset_dots = orig_curve.make_offset_curve(0.5)
orig_curve_dots.append(orig_curve_dots[-1])
offset_dots.append(offset_dots[-1])
offset_dots = [dot.get_tuple() for dot in offset_dots]

plt.plot(*zip(*orig_curve_dots), marker='s')
plt.plot(*zip(*offset_dots), marker='s')
plt.axes().set_aspect('equal')
plt.axis([-5,5,-5,5])
plt.show()

