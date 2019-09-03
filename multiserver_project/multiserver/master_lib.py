from multiserver.connection_lib import ServerConnection, ConnectionManager

import queue
import threading
import time
import json
import MySQLdb

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

class Master:

    def __init__(self, controller_port, manager_port, db_user='root', db_password='05011998', db_name='results'):

        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.init_db(self.db_name)

        self.controller_manager = ControllerManager(controller_port, self)
        self.node_manager = NodeManager(manager_port, self)

        self.tasks = queue.Queue()
        self.tasks_at_nodes = 0

        self.db_cursor.execute('SELECT chunk_id, length, tasks_done FROM chunk_infos', tuple())
        self.db_connection.commit()

        self.chunks = {}
        self.old_chunks = {chunk_id: {'length': length, 'tasks_done': tasks_done} for chunk_id, length, tasks_done in self.db_cursor}

        self.db_exec_queue = queue.Queue()
        self.db_thread = threading.Thread(target=self.exec_db_tasks)

    def wait_until_ready(self, chunk_id):
        if chunk_id in self.chunks:
            self.chunks[chunk_id]['done_event'].wait()
        elif chunk_id in self.old_chunks:
            return
        else:
            raise Exception('Wrong chunk_id')

    def exec_db_tasks(self):
        while True:
            exec_tuple = self.db_exec_queue.get()
            self.db_cursor.execute(*exec_tuple)
            self.db_connection.commit()

    def start(self):
        self.controller_manager.start()
        self.node_manager.start()
        self.db_thread.start()

    def grab_chunk_info(self, chunk_id, length, tasks_done):
        exec_tuple = ('INSERT INTO chunk_infos VALUES (%s, %s, %s)', (chunk_id, length, tasks_done))
        self.db_exec_queue.put(exec_tuple)

    def grab_result(self, result):
        'Эту функцию вызывает NodeConnection чтобы передать результаты в Master'

        result['body']['result_json'] = json.dumps(result['body']['result'], sort_keys=True)

        chunk_id = result['body']['chunk_id']

        self.chunks[chunk_id]['tasks_done'] += 1

        result_list = [result['body'][key] for key in (
            'package_name',
            'package_version',
            'module_name',
            'function_name',
            'result_json',
            'chunk_id',
            'task_id',
            'time'
        )]

        exec_tuple = ('INSERT INTO results VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', result_list)
        self.db_exec_queue.put(exec_tuple)

        exec_tuple = ('UPDATE chunk_infos SET tasks_done=%s WHERE chunk_id=%s', (self.chunks[chunk_id]['tasks_done'], chunk_id))
        self.db_exec_queue.put(exec_tuple)

        if self.chunks[chunk_id]['tasks_done'] == self.chunks[chunk_id]['length']:
            self.chunks[chunk_id]['done_event'].set()

        self.tasks_at_nodes -= 1

    def give_task(self):
        'Эту функцию вызывает NodeConnection чтобы взять задание из Master'
        try:
            task = self.tasks.get_nowait()
            self.tasks_at_nodes += 1
        except queue.Empty:
            task = None
        return task

    def put_task(self, task, from_node=False):
        'Эту функцию вызывает ControllerConnection чтобы положить задание в очередь Master'
        self.tasks.put(task)
        if from_node:
            self.tasks_at_nodes -= 1

    def init_db(self, filename):
        self.db_connection = MySQLdb.connect(user=self.db_user, passwd=self.db_password)
        self.db_cursor = self.db_connection.cursor()

        self.db_cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.db_name))

        self.db_connection.select_db(self.db_name)

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                package_name text,
                package_version text,
                module_name text,
                function_name text,
                result text,
                chunk_id text,
                task_id text,
                time text
            )
        ''')

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunk_infos (
                chunk_id text,
                length text,
                tasks_done text
            )
        ''')

        self.db_connection.commit()

    def nodes_tps(self):
        return [(ip, self.node_manager.connections[ip].get_tps()) for ip in self.node_manager.connections]

    def tasks_left(self):
        return self.tasks.qsize()

class NodeManager(ConnectionManager):
    def __init__(self, port, master):
        super().__init__(port, NodeConnection)

        self.master = master

class NodeConnection(ServerConnection):
    def __init__(self, socket, manager):
        super().__init__(socket, manager)

        self.in_progress = {}
        self.times = []

    def response(self, message):
        if message['header'] == 'task_request':
            # Выдача задания
            task = self.manager.master.give_task()
            if task == None:
                return {'header': 'no_task'}
            else:
                self.in_progress[task['body']['task_id']] = task
                return {'header': 'task', 'body': task['body']}

        elif message['header'] == 'result':
            # Принятие результата
            if message['body']['task_id'] in self.in_progress:
                del self.in_progress[message['body']['task_id']]
            self.manager.master.grab_result(message)
            self.times.append(message['body']['time'])

        elif message['header'] == 'start':
            # Начальное сообщение
            self.process_count = message['body']['process_count']
            self.amazon = message['body']['is_amazon']
            if self.amazon:
                self.approx_term_time = message['body']['approx_term_time']
                self.instance_id = message['body']['instance_id']
                self.instance_type = message['body']['instance_type']

    def on_connection_close(self):
        self.requeue_tasks()

    def requeue_tasks(self):
        if self.in_progress:
            for key in self.in_progress:
                self.manager.master.put_task(self.in_progress[key])
            return True
        else:
            return False

    def get_tps(self):
        if self.times:
            return (1 / (sum(self.times) / len(self.times))) * self.process_count
        else:
            return 0

class ControllerManager(ConnectionManager):
    def __init__(self, port, master):
        super().__init__(port, ControllerConnection)
        self.master = master

class ControllerConnection(ServerConnection):
    def response(self, message):
        if message['header'] == 'task':
            self.manager.master.put_task(message)

        elif message['header'] == 'finish_notice_request':
            self.manager.master.wait_until_ready(message['body']['chunk_id'])
            return {'header': 'finish_notice', 'body': message['body']}

        elif message['header'] == 'chunk_info':
            length = int(message['body']['length'])

            self.manager.master.grab_chunk_info(chunk_id=message['body']['id'], length=length, tasks_done=0)
            self.manager.master.chunks[message['body']['id']] = {'length': length, 'tasks_done': 0, 'done_event': threading.Event()}
