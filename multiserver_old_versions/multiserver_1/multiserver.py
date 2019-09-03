from jsonsocket import *
import time, datetime, calendar
import queue
import threading
import multiprocessing
import urllib.request, urllib.error
import os
import sys
import json
import boto3
import importlib
import pip
import contextlib


@contextlib.contextmanager
def working_dir(directory):
    curdir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(curdir)

def time_since_epoch():
    return calendar.timegm(time.gmtime())


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
            #~ print('Connected to controller at {}'.format(address))

            task_thread = threading.Thread(target=self.task_stream, args=(connection, ))
            result_thread = threading.Thread(target=self.result_stream, args=(connection, ))

            task_thread.start()
            result_thread.start()
            task_thread.join()
            result_thread.join()

            #~ print('Disconnected from controller')
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


class Master:
    '''
    Класс, который получает задачи от чего-нибудь вроде Controller,
    распределяет их по Node-ам, получает результаты и посылает их
    обратно в Controller.
    '''

    def __init__(self, controller_port, manager_port, result_log=open('result_log', 'a')):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.controller = _ControllerConnection(controller_port, self)
        self.node_manager = _NodeManager(manager_port, self)
        self.result_log = result_log
        self.tasks_at_nodes = 0

    def start(self):
        self.controller.start()
        self.node_manager.start()
        #~ print('Started master')

    def grab_result(self, result):
        '''Эту функцию вызывает _NodeConnection чтобы передать результаты в Master'''
        self.result_log.write(str(result) + '\n')
        self.result_log.flush()
        self.results.put(result)
        self.tasks_at_nodes -= 1

    def give_task(self):
        '''Эту функцию вызывает _NodeConnection чтобы взять задание из Master'''
        try:
            task = self.tasks.get_nowait()
            self.tasks_at_nodes += 1
        except queue.Empty:
            task = None
        return task

    def put_task(self, task):
        '''Эту функцию вызывает _ControllerConnection чтобы положить задание в очередь Master'''
        self.tasks.put(task)

    def get_result(self):
        '''Эту функцию вызывает _ControllerConnection чтобы взять результат из очереди Master'''
        try:
            result = self.results.get_nowait()
        except queue.Empty:
            result = None
        return result

    def on_controller_disconnect(self):
        with self.tasks.mutex: self.tasks.queue.clear()
        with self.results.mutex: self.results.queue.clear()
        #~ print('Task and result queues have been cleared')

    def nodes_tps(self):
        return [(ip, self.node_manager.nodes[ip].get_tps()) for ip in self.node_manager.nodes]

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
            if ip in self.nodes:
                if self.nodes[ip].stop():
                    pass
                    #~ print('Stopped old node with ip {}'.format(ip))
                #~ else:
                    #~ print('Old node with ip {} was already dead'.format(ip))
            self.nodes[ip] = _NodeConnection(conn, self.master, self, ip)
            self.nodes[ip].start()
            #~ print('Connected to node at {}:{}'.format(addr[0], addr[1]))


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
                message = self.socket.receive()

                if message['header'] == 'task_request':
                    # Выдача задания
                    task = self.master.give_task()
                    if task == None:
                        self.socket.send({'header': 'no_task'})
                    else:
                        self.in_progress.add(task)
                        self.socket.send({'header': 'task', 'task': task})
                        #~ print('Sent task')

                elif message['header'] == 'result':
                    # Принятие результата
                    #~ print('Got result')
                    self.in_progress.discard(message['task'])
                    self.master.grab_result(message)
                    self.times.append(message['time'])

                elif message['header'] == 'start':
                    # Начальное сообщение
                    self.process_count = message['process_count']
                    self.amazon = message['amazon']
                    if self.amazon:
                        self.approx_term_time = message['approx_term_time']
                        self.instance_id = message['instance_id']
                        self.instance_type = message['instance_type']

            except ConnectionLostError:
                break

        self.socket.close()
        #~ print('Disconnected from node with addr {}'.format(addr))
        if self.requeue_tasks():
            pass
            #~ print('Returned some tasks back to master')


class Node:
    '''
    Класс, который получает задания от Master и возвращает ответы.
    '''

    def __init__(self, master_addresses, process_count=None, package_cache_dirs=None):

        self.is_alive = True
        self.master_addresses = master_addresses
        self.tasks = multiprocessing.Queue()
        self.results = multiprocessing.Queue()
        self.thread = threading.Thread(target=self.main)
        self.main_lock = multiprocessing.Lock()
        self.master_addresses_lock = multiprocessing.Lock()
        self.manager = multiprocessing.Manager()
        self.s3_client = boto3.client('s3')
        self.current_master = None

        if package_cache_dirs == None:
            package_cache_dirs = ['/var/tmp/multiserver/', '~/.multiserver/tmp']

        for directory in package_cache_dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except (PermissionError, OSerror) as e:
                    continue
            self.package_cache_dir = directory
            sys.path.append(directory)
            break

        try:
            self.instance_id = urllib.request.urlopen('http://instance-data/latest/meta-data/instance-id').read().decode("utf-8")
            self.instance_type = urllib.request.urlopen('http://instance-data/latest/meta-data/instance-type').read().decode("utf-8")
        except urllib.error.URLError:
            self.amazon = False
        else:
            #~ print('This is Amazon EC2 instance. ID is {}, type is {}.'.format(self.instance_id, self.instance_type))
            with open('/proc/uptime', 'r') as f:
                self.approx_term_time = time_since_epoch() - float(f.readline().split()[0]) + 3600 # 3600 так как инстансы работают час
            self.amazon = True

        if process_count == None:
            self.process_count = multiprocessing.cpu_count()
        else:
            self.process_count = process_count

        self.processes = [_NodeProcess(self) for i in range(self.process_count)]

        self.installed_packages = self.manager.dict({obj.key: {'version': obj.version} for obj in pip.get_installed_distributions()})

    def main(self):
        while self.is_alive:
            socket = JSONSocket()

            with self.master_addresses_lock:
                for ip, port in self.master_addresses:
                    if socket.connect(ip, port):
                        self.current_master = ip, port
                        #~ print('Connected to master at {}:{}'.format(ip, port))
                        break
                else:
                    continue

            startup_msg = {'header': 'start', 'process_count': len(self.processes), 'amazon': self.amazon}
            if self.amazon:
                startup_msg['instance_id'] = self.instance_id
                startup_msg['instance_type'] = self.instance_type
                startup_msg['approx_term_time'] = self.approx_term_time

            try:
                socket.send(startup_msg)
            except ConnectionLostError:
                #~ print('Disconnected')
                self.current_master = None
                socket.close()
                continue

            while self.is_alive:
                try:
                    if self.tasks.empty():
                        socket.send({'header': 'task_request'})
                        answer = socket.receive()
                        if answer['header'] == 'task':
                            task = answer['task']
                            self.tasks.put(task)
                        elif answer['header'] == 'no_task':
                            pass

                    if not self.results.empty():
                        socket.send(self.results.get())

                except ConnectionLostError:
                    #~ print('Disconnected')
                    self.current_master = None
                    socket.close()
                    break

    def start(self):
        self.thread.start()
        for process in self.processes:
            process.start()
        #~ print('Started node with {} processes'.format(len(self.processes)))

    def stop(self):
        for process in self.processes:
            process.terminate()
        self.is_alive = False
        self.thread.join()

    def give_task(self):
        return self.tasks.get()

    def grab_result(self, result):
        self.results.put(result)

    def add_master_address(self, address):
        with self.master_addresses_lock:
            self.master_addresses.append(address)

    def remove_master_address(self, address):
        with self.master_addresses_lock:
            self.master_addresses.remove(address)

    def ensure_package(self, package_filename, package_name, package_version):
        with self.main_lock:
            if package_name not in self.installed_packages or self.installed_packages[package_name]['version'] != package_version:

                self.s3_client.download_file('ipeterov', package_filename, os.path.join(self.package_cache_dir, package_filename))

                with working_dir(self.package_cache_dir):
                    pip.main(['install', '--upgrade', package_filename])
                self.installed_packages[package_name] = {'version': package_version}


class _NodeProcess:
    def __init__(self, master):
        self.master = master
        self.process = multiprocessing.Process(target=self.main)
        self.modules = {}
        self.is_alive = True

    def stop(self):
        self.is_alive = False
        self.process.join()

    def terminate(self):
        self.process.terminate()

    def start(self):
        self.process.start()

    def main(self):
        #~ sys.stdout = open(os.devnull, 'w') # processes have no output

        while self.is_alive:
            json_task = self.master.give_task()
            task = json.loads(json_task)

            full_name = '.'.join((task['package_name'], task['module_name']))

            self.master.ensure_package(task['package_filename'], task['package_name'], task['package_version'])
            self.modules[full_name] = importlib.import_module(full_name)

            function = getattr(self.modules[full_name], task['function_name'])

            t = time.perf_counter()

            self.master.grab_result(
                {
                    'header': 'result',
                    'result': function(*task['args']),
                    'task': json_task,
                    'time': time.perf_counter() - t
                }
            )

if __name__ == '__main__':
    pass
