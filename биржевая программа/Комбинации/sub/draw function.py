from lib import *
from pickle import *
function = input()
f = load(open(function,'rb'))[0:1000]
for i in range(len(f)):
    f[i] *= 10000
paint_graph(f)
