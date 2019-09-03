import multiserver

task_port, result_port, master_port = 9088, 9089, 9090
nodes = ['127.0.0.1', '', 'localhost', '168.235.86.179']

print('Starting multiserver master...')

master = multiserver.Master(task_port, result_port, master_port, nodes)
master.start()
