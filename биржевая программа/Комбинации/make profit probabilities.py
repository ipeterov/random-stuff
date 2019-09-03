pyaterka_length = 5
quantity_range = range(3,15)
_length = 10
repeat_q = 2
length = 1000
profit_after_comma = 6


from pickle import *
from lib import *

real_function = load(open('function', 'rb'))
leaps_array = load(open('leaps_array', 'rb'))

dump(profit_probabilities(semerka_length_range, desyatka_length, repeat_q, length, leaps_array, profit_after_comma), open('profit_probabilities', 'wb'))

