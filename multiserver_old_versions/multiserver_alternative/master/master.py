import multiserver

task_port, result_port = 9088, 9089
nodes = [('', 9090), ('168.235.86.179', 9090)]

print('Starting multiserver master...')

master = multiserver.Master(task_port, result_port, nodes)
master.start()

print('Started.')
