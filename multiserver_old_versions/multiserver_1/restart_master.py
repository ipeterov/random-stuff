import paramiko

with open('master') as f:
    first_line = f.readline()

ip, port, user, path = first_line.split()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=ip, username=user, port=22)

# Shut down if it's up
stdin, stdout, stderr = client.exec_command('ps aux | grep master.py')
pid = None
for line in stdout:
    if 'grep' not in line:
        pid = line.split()[1]
        break
if pid:
    client.exec_command('kill {pid}'.format(pid=pid))
    print('Killed master.py on server {}@{}:{}'.format(user, ip, port))

# Start it
stdin, stdout, stderr = client.exec_command("sh -c 'nohup python3 {path}/master.py > /dev/null 2>&1 &'".format(path=path,))
print('Raised master.py on server {}@{}:{}'.format(user, ip, port))

client.close()
