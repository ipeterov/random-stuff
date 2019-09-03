import pickle
name = input('File name: ')
info = pickle.load(open(name, 'rb'))
output_file = open(str(name) + '.txt', 'w')
if type(info) == dict:
    for key in info:
        output_file.write(str(info[key]) + '\n')
else:
    for item in info:
        output_file.write(str(item) + '\n')
