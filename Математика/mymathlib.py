import copy


def submatrix(matrix, x, y):
    matrix = copy.deepcopy(matrix)
    matrix.pop(x)
    for i in range(len(matrix)):
        matrix[i].pop(y)

    return matrix


def replace_column(matrix, new_column, place):
    matrix = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        matrix[i][place] = new_column[i]
    return matrix


def input_matrix():
    size = int(input('Размерность: '))

    matrix = []
    for i in range(size):
        nums = [int(x) for x in input('Строка № ' + str(i) + ': ').split()]

        if len(nums) != size:
            raise Exception
        else:
            matrix.append(nums)

    return matrix


def find_determinant_2x2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]


def find_determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return find_determinant_2x2(matrix)
    else:
        additional_minors_sum = 0
        for i in range(len(matrix)):
            additional_minors_sum += matrix[i][0] * \
                find_determinant(submatrix(matrix, i, 0)) * (-1)**i
        return additional_minors_sum


def kramer(coeffs, xs):
    da = find_determinant(coeffs)

    dxs = []
    for i in range(len(xs)):
        new_matrix = replace_column(coeffs, xs, i)
        dxs.append(find_determinant(new_matrix))

    for i in range(len(dxs)):
        dxs[i] /= da

    return dxs
