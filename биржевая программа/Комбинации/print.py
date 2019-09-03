from pickle import *
name = input('File name: ')
print(load(open(name, 'rb')))
