import subprocess

for line in open('node_list'):
    ip, port, user, path = line.split()
    command = 'rsync -av ./node_files/ {user}@{ip}:{path}'.format(user=user, ip=ip, path=path)
    print(command)
    process = subprocess.call(command.split())
