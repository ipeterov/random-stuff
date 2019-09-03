a, b, c = [[float(x) for x in input('Введите координаты вершины треугольника № {}: '.format(i+1)).split()] for i in range(3)]
m = b[0] + c[0], b[1] + c[1]
length = ((a[0] - m[0])**2 + (a[1] - m[1])**2)**0.5
print(length)
