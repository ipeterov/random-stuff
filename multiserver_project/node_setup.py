from invoke import run
import os
import shutil

def insert_if_not_in(filename, line, index):

    if not line.endswith('\n'):
        line = line + '\n'

    with open(filename, 'r') as f:
        contents = [item for item in f.readlines() if item.strip()]

    if line not in contents:
        contents.insert(index, line)
    contents = "".join(contents)

    with open(filename, 'w') as f:
        print(contents)
        f.write(contents)

def copy_create_dirs(src, dst):
    try:
        shutil.copyfile(src, dst)
    except FileNotFoundError:
        os.mkdir(os.path.dirname(dst))
        shutil.copyfile(src, dst)
        run('chown {} {} -R'.format(username, os.path.dirname(dst)))


REQUIRED_PYTHON_PATH = '/usr/bin/python3.4'
REQUIRED_PACKAGES = ['virtualenv', 'boto3', 'virtualenv-api']
REQUIRED_FILES = ['node.py', 'node_config.json']
REQUIRED_FOLDERS = ['multiserver']
DEFAULT_INSTALL_PATH = '/home/{}/.multiserver'
DEFAULT_SCREEN_NAME = 'multiserver_node'


username = input('Username [{}]: '.format(os.getlogin()))
if not username:
    username = os.getlogin()

default_install_path = DEFAULT_INSTALL_PATH.format(username)
install_path = input('Installation path [{}]: '.format(default_install_path))
if not install_path:
    install_path = default_install_path

if os.path.exists(install_path):
    if input('Path already exists. Remove all files there and reinstall or abort installation? ([y]/else): ') in ('', 'y'):
        reinstall = True
    else:
        raise Exception('Installation aborted.')
else:
    reinstall = False

env_path = os.path.join(install_path, 'venv')
env_python_path = os.path.join(env_path, 'bin/python')

autolaunch = input('Add node autolaunch? ([y]/else): ') in ('', 'y')
if autolaunch:

    screen_name = input('Screen name? [{}]: '.format(DEFAULT_SCREEN_NAME))
    if not screen_name:
        screen_name = DEFAULT_SCREEN_NAME

    node_py_path = os.path.join(install_path, 'src/node.py')

    autolaunch_line = "su - {username} -c 'screen -dmS {screen_name} {python_path} {node_py_path}'".format(
        username=username,
        screen_name=screen_name,
        python_path=env_python_path,
        node_py_path=node_py_path
    )


sure = input('Are you sure? (y/else): ')
if sure == 'y':
    # Install requirements
    for package in REQUIRED_PACKAGES:
        run('pip3 install {}'.format(package))

    # Delete old installation if reinstalling
    if reinstall:
        shutil.rmtree(install_path)

    # Create virtualenv
    run('virtualenv -p {} {} --system-site-packages'.format(REQUIRED_PYTHON_PATH, env_path))

    # Make folder structure
    for f in REQUIRED_FILES:
        copy_create_dirs(f, os.path.join(install_path, 'src', f))

    for f in REQUIRED_FOLDERS:
        shutil.copytree(f, os.path.join(install_path, 'src', f))

    # Make user owner of the folder
    run('chown {} {} -R'.format(username, install_path))

    # Add autolaunch to rc.local
    if autolaunch:
        insert_if_not_in('/etc/rc.local', autolaunch_line, -1)
