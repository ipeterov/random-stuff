import my_geom_lib
            
triangle = my_geom_lib.Figure([[float(x) for x in input('Введите координаты вершины треугольника № {}: '.format(i+1)).split()] for i in range(3)])
dot = [float(x) for x in input('Введите координаты точки: ').split()]

if triangle.is_in(dot):
    print('В треугольнике.')
else:
    print('Не в треугольнике')
