import subprocess

with open('node_list') as nodes:
    print('Syncing nodes...')
    for line in nodes:
        ip, port, user, path = line.split()
        command = 'rsync -av ./node_files/ {user}@{ip}:{path}'.format(user=user, ip=ip, path=path)
        process = subprocess.call(command.split())
    print('Nodes synchronised.\n')

with open('master') as master:
    print('Syncing master...')
    ip, task_port, result_port, user, path = master.readline().split()
    command = 'rsync -av ./master_files/ {user}@{ip}:{path}'.format(user=user, ip=ip, path=path)
    process = subprocess.call(command.split())
    print('Master synchronised.')
