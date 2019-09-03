import paramiko

actions = set(('shutdown', 'restart'))

def get_action():
    command = input('What to do with nodes {}: '.format(actions))
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

def kill_node(client):
    # Shut down if it's up
    stdin, stdout, stderr = client.exec_command('ps aux | grep node.py')
    pids = []

    for line in stdout:
        if 'grep' not in line:
            pids.append(line.split()[1])

    for pid in pids:
        client.exec_command('kill {pid}'.format(pid=pid))
        print('Killed node.py with pid {} on server {}@{}:{}'.format(pid, user, ip, port))

def raise_node(clent):
    # Start it
    stdin, stdout, stderr = client.exec_command("sh -c 'nohup python3 {path}/node.py > /dev/null 2>&1 &'".format(path=path,))
    print('Raised node.py on server {}@{}:{}'.format(user, ip, port))

action = get_action()

with open('node_list') as nodes:
    for line in nodes:
        ip, port, user, path = line.split()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, port=22)

        if action == 'shutdown':
            kill_node(client)
        elif action == 'restart':
            kill_node(client)
            raise_node(client)

        client.close()
