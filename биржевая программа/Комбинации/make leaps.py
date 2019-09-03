from pickle import *
from lib import *

real_function = load(open('real_function', 'rb'))

dump(leaps_array(real_function), open('leaps_array', 'wb'))
