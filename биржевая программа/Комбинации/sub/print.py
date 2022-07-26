from pickle import *
name = input()
print(load(open(name, 'rb')))
