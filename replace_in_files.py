import os


ROOT_DIR = os.getcwd()
OLD = 'tkinter'
NEW = 'tkinter'


def replace_in_file(filename, old, new):
	with open(filename) as f:
		lines = f.readlines()

	with open(filename, 'w') as f:
		for line in lines:
			new_line = line.replace(old, new)
			f.write(new_line)


for root, subdirs, files in os.walk(ROOT_DIR):
	for file in files:
		if not file.endswith('.py'):
			continue

		filename = f'{root}/{file}'

		replace_in_file(filename, OLD, NEW)