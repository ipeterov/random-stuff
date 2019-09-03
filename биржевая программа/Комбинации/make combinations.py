pyaterka_length = 5
desyatka_length = 10

from pickle import *
from lib import *

real_function = load(open('function_1', 'rb'))

dump(combinations_dict(real_function, pyaterka_length, desyatka_length), open('all_combinations', 'wb'))
