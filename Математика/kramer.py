import mymathlib

matrix = mymathlib.input_matrix()
xs = [float(x) for x in input('Суммы: : ').split()]

print('Ответ:', mymathlib.kramer(matrix, xs))
