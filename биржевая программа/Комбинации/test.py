from lib import *
from pickle import *

self_lengths = [5]
after_lengths = [40]
quantities = [12]
profits = [0]
probability_edges = [0.98]

max_i = len(self_lengths) * len(after_lengths) * len(quantities) * len(profits) * len(probability_edges)
i = 0

for self_length in self_lengths:
    for after_length in after_lengths:
        for quantity in quantities:
            for profit in profits:
                for probability_edge in probability_edges:
                    print(i / max_i)
                    real_function = load(open('function_1', 'rb'))
                    combinations = combinations_dict(real_function, self_length, after_length, min_quantity = quantity, probability_edge = probability_edge, min_profit = profit)
                    sorted_combinations = sort_combinations(combinations, self_length, after_length)
                    income, operation_count, sucsessful_percentage = trade(sorted_combinations, self_length, after_length)
                    if operation_count:
                        income_per_operation = income ** (1/operation_count)
                    else:
                        income_per_operation = 'no operations'
                    open('log.txt', 'a').write('Income per operation: {}, income: {}, operation count: {}, sucsessful operations percentage: {}, self_length: {}, after_length: {}, quantity: {}, min_profit: {}, probability_edge: {}. \n'.format(income_per_operation, income, operation_count, sucsessful_percentage, self_length, after_length, quantity, profit, probability_edge))
                    i += 1
