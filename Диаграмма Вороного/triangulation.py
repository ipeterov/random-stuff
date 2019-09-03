width = 500
height = 500
coeff = 1.97

def area(triangle):
    return (triangle[0][0] -triangle[2][0]) * (triangle[1][1] - triangle[2][1]) - (triangle[0][1] - triangle[2][1]) * (triangle[1][0] - triangle[2][0])

def is_in(dot, triangle):
    area_sum = area(triangle[0], triangle[1], dot) + area(triangle[1], triangle[2], dot) + area(triangle[2], triangle[0], dot)
    if area_sum - 3 < area(triangle) < area_sum + 3:
        return 1
    else:
        return 0

class triangulation():
    def __init__(self):
        import math
        self.triangles = []
        self.triangles.append([(0,0), (width,0), (width/2, math.sqrt(3)/2*height )])

    def complicate(self):
        import random, math

        def totwo():
            def y_coord(x, x1, y1, x2, y2):
                try:
                    return (x-x1)*(y2-y1)/(x2-x1) + y1
                except:
                    return (x-x1)*(y2-y1) + y1
            temp_coords = triangle
            opposite_coord = temp_coords.pop(random.randint(0, len(temp_coords) - 1))
            x = round((temp_coords[0][0] + temp_coords[1][0]) / 2, 0)
            y = y_coord(x, temp_coords[0][0], temp_coords[0][1], temp_coords[1][0], temp_coords[1][1])
            dot = x, y
            new_t0 = [temp_coords[0], opposite_coord, dot]
            new_t1 = [temp_coords[1], opposite_coord, dot]
            return new_t0, new_t1

        def tothree():
            x = round((triangle[0][0] + triangle[1][0] + triangle[2][0]) / 3, 0)
            y = round((triangle[0][1] + triangle[1][1] + triangle[2][1]) / 3, 0)
            dot = x, y
            new_t0 = [triangle[0], triangle[1], dot]
            new_t1 = [triangle[1], triangle[2], dot]
            new_t2 = [triangle[2], triangle[0], dot]
            return new_t0, new_t1, new_t2

        triangle = self.triangles.pop(random.randint(0, len(self.triangles) - 1))
        a = math.sqrt(abs(triangle[0][0] - triangle[1][0])**2 + abs(triangle[0][1] - triangle[1][1])**2)
        b = math.sqrt(abs(triangle[1][0] - triangle[2][0])**2 + abs(triangle[1][1] - triangle[2][1])**2)
        c = math.sqrt(abs(triangle[2][0] - triangle[0][0])**2 + abs(triangle[2][1] - triangle[0][1])**2)

        if min(a,b,c) * coeff < max(a,b,c):
            print(0)
            triangles = totwo()
        else:
            print(1)
            triangles = tothree()

        for element in triangles:
            self.triangles.append(element)

def test(complexity = 20):
    a = triangulation()
    for i in range(complexity):
        a.complicate()
    import tkinter
    root = tkinter.Tk()
    canv = tkinter.Canvas(root, width = width, height = height)
    for triangle in a.triangles:
        canv.create_polygon(triangle, fill = 'white', outline = 'black')
    canv.pack()
    root.mainloop()

x == 0

test()
