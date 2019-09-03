def trade(combinations):
    import pickle
    function = pickle.load(open('function_2', 'rb'))
    comission = 0.0003

    def array_make_relative(array):
        returned_array = []
        for number in array:
            returned_array.append(round(number - array[0],4))
        return returned_array

    def trade(coord, money, combination):
        if 0 not in function[coord: coord + 10]:
            multiplier = ((function[coord + combination['max_i']] - comission) / function[coord + combination['min_i']] - 1) * 100 + 1
            money *= multiplier
            print(money)
        return money

    money = 10**300
    operation_count = 0
    sucsessful_count = 0
    for key in combinations:
        combinations[key]['multiplier'] = 1

    for i in range(len(function) - 15):
        name = str(array_make_relative(function[i : i+5]))
        if name in combinations:
            prev_money = money
            money = trade(i+5, money, combinations[name])
            if money < 10e-323:
                break
            combinations[name]['multiplier'] *= money / prev_money
            operation_count += 1

    for key in combinations:
        if combinations[key]['multiplier'] > 1:
            sucsessful_count += 1

    return operation_count, round(sucsessful_count / len(combinations) * 100, 3)
    #open('log.txt', 'a').write('operation count: ' + str(operation_count) + ', sucsessful percent: ' + str(round(sucsessful_count / len(combinations) * 100, 3)) + '\n')
    #print('Operation count: ' + str(operation_count) + '.')
    #print('Sucsessful combinations percentage: ' + str(round(sucsessful_count / len(combinations) * 100, 3)) + '.')
