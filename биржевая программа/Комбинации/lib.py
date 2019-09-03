def array_make_relative(array):
    returned_array = []
    for number in array:
        returned_array.append(round(number - array[0],5))
    return returned_array

def combinations_dict(array, pyaterka_length, desyatka_length, min_quantity = 3, probability_edge = 0.99, min_profit = 0, bad_combinations = 0, sectors = 0):
    combinations = {}
    if sectors == 1:
        min_quantity = 1
    comission = 0.0003

    from pickle import load, dump

    def nearest_key_in_dictionary(dictionary, number):
        min_difference = -100
        for key in dictionary:
            if min_difference != -100:
                if abs(key - number) < min_difference:
                    nearest_key = key
                    min_difference = abs(key - number)
            else:
                nearest_key = key
                min_difference = abs(key - number)
        return nearest_key

    for i in range(len(array) - pyaterka_length - desyatka_length + 1):
        if 0 not in array[i: i + 15]:
            name = str(array_make_relative(array[i:i + pyaterka_length]))
            if str(array_make_relative(array[i:i + pyaterka_length])) not in combinations:
                combinations[name] = {'self':array_make_relative(array[i:i + pyaterka_length]), 'after':array_make_relative(array[i + pyaterka_length:i + pyaterka_length + desyatka_length]), 'quantity' : 1}
            else:
                combinations[name]['quantity'] += 1
                combinations[name]['after'] = sum_array([combinations[name]['after'], array_make_relative(array[i + pyaterka_length:i + pyaterka_length + desyatka_length])])
    for element in combinations:
        for i in range(len(combinations[element]['after'])):
            combinations[element]['after'][i] = round(combinations[element]['after'][i] / combinations[element]['quantity'], 7)

    profit_probabilities = load(open('profit_probabilities', 'rb'))
    for key in combinations.copy():
        q = combinations[key]['quantity']
        if q > profit_probabilities['max_semerka_length']:
                q = profit_probabilities['max_semerka_length']
        combinations[key]['min_i'] = combinations[key]['after'].index(min(combinations[key]['after']))
        combinations[key]['max_i'] = combinations[key]['after'].index(max(combinations[key]['after']))
        min_i = combinations[key]['min_i']
        max_i = combinations[key]['max_i']
        diff = combinations[key]['after'][max_i] - combinations[key]['after'][min_i]
        profit = combinations[key]['after'][max_i] - combinations[key]['after'][min_i] - comission
        profit_acceptable = 0
        profit_probability_acceptable = 0
        if (bad_combinations and profit < min_profit) or ((not bad_combinations) and profit > min_profit):
            profit_acceptable = 1
        #print(profit_probabilities[q][nearest_key_in_dictionary(profit_probabilities[q], diff)], probability_edge)
        if sectors == 1 or profit_probabilities[q][nearest_key_in_dictionary(profit_probabilities[q], diff)] > probability_edge:
            profit_probability_acceptable = 1
        if combinations[key]['quantity'] < min_quantity or not profit_probability_acceptable or not profit_acceptable:
            del combinations[key]

    #dump(combinations, open('name1', 'wb'))
    return combinations

def sum_array(input_arrays):
    max_len = 0
    max_len_i = -1
    for i in range(len(input_arrays)):
        if len(input_arrays[i]) > max_len:
            max_len = len(input_arrays[i])
            max_len_i = i
    for i in range(len(input_arrays)):
        if i != max_len_i:
            for j in range(len(input_arrays[i])):
                input_arrays[max_len_i][j] += input_arrays[i][j]
    return input_arrays[max_len_i]

def real_like_random_array(length, leaps_array):
    from random import random
    real_like_random_array = []
    real_like_random_array.append(0)
    number_sum = leaps_array[0] - 0.00000001
    for i in range(1, length):
        number = random() * number_sum
        j = 1
        while not (leaps_array[j][0][0] <= number and number <= leaps_array[j][0][1]):
            j += 1
        real_like_random_array.append(round(real_like_random_array[i-1] + leaps_array[j][1], 4))
    return real_like_random_array

def paint_graph(array, y_zoom = 1, label_quantity = 4):
    import tkinter
    root = tkinter.Tk()
    width = len(array)
    height = max(abs(max(array)), abs(min(array))) * 2 + 20
    canv = tkinter.Canvas(root, width = width, height = height, bg = 'lightblue', cursor = "pencil")
    coords = []
    for i in range(len(array)):
        coords.append([i, -array[i] * y_zoom + height/2])
    canv.create_line(coords, smooth = 1, splinesteps = 0)
    canv.pack()
    root.mainloop()

def profit_probabilities(semerka_length_range, desyatka_length, repeat_q, length, leaps_array, profit_after_comma):
    def sub_random_function_data(random_function):
        '''Получаем средние значения десятки для k повторений десятки'''
        import math
        result = []
        for k in range(max(semerka_length_range)+1):
            result.append([])
        for k in semerka_length_range:
            for i in range(0, length - k * desyatka_length, k * desyatka_length): #Пробегаемся по всем семёркам
                buff_desyatka = []
                for j in range(desyatka_length):
                    buff_desyatka.append(0)
                for j in range(0, k*desyatka_length, desyatka_length): #Получаем среднее для десятки
                    for l in range(desyatka_length):
                        buff_desyatka[l] += random_function[i+j+l] - random_function[i+j]
                for j in range(desyatka_length):
                    buff_desyatka[j] /= k
                buff = round((max(buff_desyatka)-min(buff_desyatka)), profit_after_comma) #Получаем прибыль для усреднённой десяти и округляем её
                result[k].append(buff)
        return result
    result = []
    for i in range(max(semerka_length_range)+1):
        result.append([])
    for i in range(repeat_q):
        random_function = real_like_random_array(length, leaps_array)
        buff = sub_random_function_data(random_function)
        for j in range(len(buff)):
            result[j] += buff[j]
            print(result[j])
            #больший процент успешных комбинаций при не-отсеивании!!!!!!!!!!!!!!!!!!!!!!!
    result_dict = {}
    for i in range(min(semerka_length_range),len(result)):
        sub_dict = {}
        for j in range(len(result[i])):
            if result[i][j] not in sub_dict:
                sub_dict[result[i][j]] = 1
            else:
                sub_dict[result[i][j]] += 1
        key_list = []
        for key in sub_dict:
                key_list.append(key)
        key_list.sort()
        for k in range(1, len(key_list)):
            sub_dict[key_list[k]] += sub_dict[key_list[k-1]]
            sub_dict[key_list[k-1]] /= (length * repeat_q) / (desyatka_length * i) - 1
            sub_dict[key_list[k-1]] = round(sub_dict[key_list[k-1]], 2)
        sub_dict[key_list[len(key_list)-1]] /= (length  / (desyatka_length * i) - 1)* repeat_q
        sub_dict[key_list[len(key_list)-1]] = round(sub_dict[key_list[len(key_list)-1]], 3)
        result_dict[i] = sub_dict
    result_dict['max_semerka_length'] = max(semerka_length_range)
    return result_dict

def leaps_array(function):
    relative_function = []
    for i in range(1, len(function)):
        if function[i-1] != 0 and function[i] != 0:
            relative_function.append(function[i]-function[i-1])
    leap_dict = {}
    for leap in relative_function:
        if round(leap,4) not in leap_dict:
            leap_dict[round(leap,4)] = 1
        else:
            leap_dict[round(leap,4)] +=1
    for key in leap_dict:
        leap_dict[key] /= len(function) - 1
    prev_number = 0
    sub_array = []
    for key in leap_dict:
        sub_array.append([leap_dict[key], key])
    sub_array.sort(key = lambda array: array[0])
    sub_array.reverse()
    leap_array = []
    leap_sum = 0
    for array in sub_array:
        leap_sum += array[0]
    leap_array.append(leap_sum)
    leap_array.append([[0, sub_array[0][0]], sub_array[0][1]])
    for i in range(1, len(sub_array)):
        prev_number = leap_array[i][0][1]
        leap_array.append([[prev_number, prev_number + sub_array[i][0]], sub_array[i][1]])
    return leap_array

def play(function, combinations, pyaterka_length = 5, desyatka_length = 10, comission = 0.0003):
    current_money = 1
    for i in range(len(function) - pyaterka_length - desyatka_length):
        if str(array_make_relative(function[i: i + pyaterka_length])) in combinations and 0 not in function[i + pyaterka_length: i + pyaterka_length + desyatka_length]:
            desyatka = combinations[str(array_make_relative(function[i: i + pyaterka_length]))]['after']
            max_digit = desyatka[0]
            max_digit_j = 0
            for j in range(1,len(desyatka)):
                if desyatka[j] > max_digit:
                    max_digit = desyatka[j]
                    max_digit_j = j
            min_digit = desyatka[0]
            min_digit_j = 0
            for j in range(1,max_digit_j):
                if desyatka[j] < min_digit:
                    min_digit = desyatka[j]
                    min_digit_j = j
            current_money += (function[i+ pyaterka_length+max_digit_j] - function[i+ pyaterka_length+min_digit_j] - comission) * 100 / function[i+ pyaterka_length+min_digit_j]
    return current_money

def sort_combinations(all_combinations, self_length, after_length):
    from pickle import load, dump
    from copy import copy

    sectors = load(open('sectors', 'rb'))

    good_combinations = {}
    bad_combinations = {}

    for sector in sectors:
        bad_combinations.update(combinations_dict(sector, self_length, after_length, bad_combinations = 1, sectors = 1))
        good_combinations.update(combinations_dict(sector, self_length, after_length, sectors = 1))


    for combination in copy(all_combinations):
        if combination in bad_combinations or combination not in good_combinations:
            del all_combinations[combination]

    return all_combinations

def trade(combinations, self_length, after_length):
    import pickle
    function = pickle.load(open('function_2', 'rb'))
    comission = 0.0003

    def array_make_relative(array):
        returned_array = []
        for number in array:
            returned_array.append(round(number - array[0],4))
        return returned_array

    def do_transactions(coord, money, combination):
        if 0 not in function[coord: coord + after_length]:
            multiplier = ((function[coord + combination['max_i']] - comission) / function[coord + combination['min_i']] - 1) * 100 + 1
            money *= multiplier
            #print(money)
        return money

    money = 1
    operation_count = 0
    sucsessful_count = 0
    for key in combinations:
        combinations[key]['multiplier'] = 1

    for i in range(len(function) - self_length - after_length):
        name = str(array_make_relative(function[i : i+self_length]))
        if name in combinations:
            prev_money = money
            money = do_transactions(i+self_length, money, combinations[name])
            combinations[name]['multiplier'] *= money / prev_money
            operation_count += 1
            if money < 10e-323:
                break

    for key in combinations:
        if combinations[key]['multiplier'] > 1:
            sucsessful_count += 1

    if len(combinations):
        sucsessful_percentage = round(sucsessful_count / len(combinations) * 100, 3)
    else:
        sucsessful_percentage = 'no combinations'

    return money, operation_count, sucsessful_percentage
    #open('log.txt', 'a').write('operation count: ' + str(operation_count) + ', sucsessful percent: ' + str(round(sucsessful_count / len(combinations) * 100, 3)) + '\n')
    #print('Operation count: ' + str(operation_count) + '.')
    #print('Sucsessful combinations percentage: ' + str(round(sucsessful_count / len(combinations) * 100, 3)) + '.')
