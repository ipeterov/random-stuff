from multiserver.jsonsocket import JSONSocket, ConnectionLostError
from multiserver.util import time_since_epoch

import queue
import threading
import time
import sqlite3


class Master:

    def __init__(self, controller_port, manager_port, db_name='results.db'):
        self.tasks = queue.Queue()
        #~ self.results = queue.Queue()
        self.db_exec_queue = queue.Queue()
        self.thread = threading.Thread(target=self.main)
        self.controller = _ControllerConnection(controller_port, self)
        self.node_manager = _NodeManager(manager_port, self)
        self.tasks_at_nodes = 0
        self.db_name = db_name

    def main(self):
        self.init_db(self.db_name)
        while True:
            exec_tuple = self.db_exec_queue.get()
            self.db_cursor.execute(*exec_tuple)
            self.db_connection.commit()

    def start(self):
        self.controller.start()
        self.node_manager.start()
        self.thread.start()

    def grab_result(self, result):
        'Эту функцию вызывает _NodeConnection чтобы передать результаты в Master'

        result_list = [result[key] for key in (
            'package_name',
            'package_version',
            'module_name',
            'function_name',
            'args_json',
            'result',
            'time'
        )]

        exec_tuple = ('INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?)', result_list)

        self.db_exec_queue.put(exec_tuple)
        #~ self.results.put(result)
        self.tasks_at_nodes -= 1

    def give_task(self):
        'Эту функцию вызывает _NodeConnection чтобы взять задание из Master'
        try:
            task = self.tasks.get_nowait()
            self.tasks_at_nodes += 1
        except queue.Empty:
            task = None
        return task

    def put_task(self, task):
        'Эту функцию вызывает _ControllerConnection чтобы положить задание в очередь Master'
        self.tasks.put(task)

    def get_result(self):
        'Эту функцию вызывает _ControllerConnection чтобы взять результат из очереди Master'
        try:
            result = self.results.get_nowait()
        except queue.Empty:
            result = None
        return result

    def init_db(self, filename):
        self.db_connection = sqlite3.connect(filename)
        self.db_cursor = self.db_connection.cursor()
        try: # FIXME
            self.db_cursor.execute('''
                CREATE TABLE results (
                    package_name text,
                    package_version text,
                    module_name text,
                    function_name text,
                    args_json text,
                    result text,
                    time text
                )
            ''')
        except sqlite3.OperationalError:
            pass
        self.db_connection.commit()

    def on_controller_disconnect(self):
        with self.tasks.mutex: self.tasks.queue.clear()
        with self.results.mutex: self.results.queue.clear()

    def nodes_tps(self):
        return [(ip, self.node_manager.nodes[ip].get_tps()) for ip in self.node_manager.nodes]


class _ControllerConnection:

    def __init__(self, port, master):
        self.master = master
        self.thread = threading.Thread(target=self.main)
        self.address = None

        self.socket = JSONSocket()
        self.socket.bind_and_listen(port)

    def start(self):
        self.thread.start()

    def main(self):
        while True:
            connection, self.address = self.socket.accept()
            self.active_stream = True

            task_thread = threading.Thread(target=self.task_stream, args=(connection, ))
            result_thread = threading.Thread(target=self.result_stream, args=(connection, ))

            task_thread.start()
            result_thread.start()
            task_thread.join()
            result_thread.join()

            self.master.on_controller_disconnect()
            self.address = None

    def task_stream(self, connection):
        while self.active_stream:
            try:
                task = connection.receive_string()
            except ConnectionLostError:
                connection.close()
                self.active_stream = False
                break
            self.master.put_task(task)

    def result_stream(self, connection):
        while self.active_stream:
            result = self.master.get_result()
            if result != None:
                try:
                    connection.send(result)
                except ConnectionLostError:
                    connection.close()
                    self.active_stream = False
                    break


class _NodeManager:
    def __init__(self, manager_port, master):
        self.master = master
        self.thread = threading.Thread(target=self.main)
        self.nodes = {} # {ip: node}
        self.sock = JSONSocket()
        self.sock.bind_and_listen(manager_port, 100)

    def start(self):
        self.thread.start()

    def main(self):
        while True:
            conn, addr = self.sock.accept()
            ip = addr[0]
            self.nodes[ip] = _NodeConnection(conn, self.master, self, ip)
            self.nodes[ip].start()


class _NodeConnection:
    def __init__(self, socket, master, manager, ip):
        self.socket = socket
        self.master = master
        self.manager = manager
        self.ip = ip
        self.thread = threading.Thread(target=self.main)
        self.is_alive = True
        self.in_progress = set()
        self.times = []

    def start(self):
        self.start_time = time.perf_counter()
        self.thread.start()

    def stop(self):
        self.is_alive = False
        self.thread.join()

    def requeue_tasks(self):
        if self.in_progress:
            for task in self.in_progress:
                self.master.put_task(task)
            return True
        else:
            return False

    def get_tps(self):
        return (1 / (sum(self.times) / len(self.times))) * self.process_count

    def main(self):
        addr = self.socket.getpeername()
        while self.is_alive:
            try:
                answer = self.socket.receive()

                if answer['header'] == 'task_request':
                    # Выдача задания
                    task = self.master.give_task()
                    if task == None:
                        self.socket.send({'header': 'no_task'})
                    else:
                        self.in_progress.add(task)
                        self.socket.send({'header': 'task', 'task': task})

                elif answer['header'] == 'result':
                    # Принятие результата
                    self.in_progress.discard(answer['json_task'])
                    self.master.grab_result(answer)
                    self.times.append(answer['time'])

                elif answer['header'] == 'start':
                    # Начальное сообщение
                    self.process_count = answer['process_count']
                    self.amazon = answer['is_amazon']
                    if self.amazon:
                        self.approx_term_time = answer['approx_term_time']
                        self.instance_id = answer['instance_id']
                        self.instance_type = answer['instance_type']

            except ConnectionLostError:
                break

        self.socket.close()
        self.requeue_tasks()
