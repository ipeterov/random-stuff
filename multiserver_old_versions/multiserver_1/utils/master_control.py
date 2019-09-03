import paramiko

actions = set(('shutdown', 'restart'))

def get_action():
    command = input('What to do with master {}: '.format(actions))
    temp_action = None
    for action in actions:
        if command == action:
            return action
        elif command in action:
            if not temp_action:
                temp_action = action
            else:
                print('Command can be interpreted in multiple ways, retry.')
                return get_action()
    else:
        if not temp_action:
            print('Command not in possible actions, retry.')
            return get_action()
        else:
            return temp_action

def kill_master(client):
    # Shut down if it's up
    stdin, stdout, stderr = client.exec_command('ps aux | grep master.py')
    pids = []

    for line in stdout:
        if 'grep' not in line:
            #~ print(line)
            pids.append(line.split()[1])

    for pid in pids:
        client.exec_command('kill {pid}'.format(pid=pid))
        print('Killed master.py with pid {} on server {}@{}:{}/{}'.format(pid, user, ip, task_port, result_port))

def raise_master(clent):
    # Start it
    stdin, stdout, stderr = client.exec_command("sh -c 'nohup python3 {path}/master.py > /dev/null 2>&1 &'".format(path=path,))
    print('Raised master.py on server {}@{}:{}/{}'.format(user, ip, task_port, result_port))

action = get_action()

with open('master') as master:
    ip, task_port, result_port, user, path = master.readline().split()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=ip, username=user, port=22)

if action == 'shutdown':
    kill_master(client)
elif action == 'restart':
    kill_master(client)
    raise_master(client)

client.close()
