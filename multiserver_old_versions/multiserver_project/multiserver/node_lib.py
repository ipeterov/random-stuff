import multiprocessing
import threading
import os
import sys
import json
import boto3
import importlib
import time

from multiserver.jsonsocket import JSONSocket, ConnectionLostError
from multiserver.util import time_since_epoch, open_url, URLError

from virtualenvapi.util import get_env_path
from virtualenvapi.manage import VirtualEnvironment


class Node:

    def __init__(self, master_addresses, process_count=None, package_cache_dirs=None, amazon_s3_bucket='ipeterov'):

        # This will throw an exception if run not from virtualenv
        self.env = VirtualEnvironment()

        self.s3_client = boto3.client('s3')
        self.amazon_s3_bucket = amazon_s3_bucket

        self.thread = threading.Thread(target=self.main)
        self.is_alive = True

        self.current_master = None
        self.master_addresses = master_addresses

        if package_cache_dirs == None:
            package_cache_dirs = ['/var/tmp/multiserver/', '~/.multiserver/tmp/']

        for directory in package_cache_dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except (PermissionError, OSerror) as e:
                    continue
            self.package_cache_dir = directory
            break

        # Multiprocessing
        if process_count == None:
            self.process_count = multiprocessing.cpu_count()
        else:
            self.process_count = process_count

        self.manager = multiprocessing.Manager()
        self.tasks = multiprocessing.Queue()
        self.answers = multiprocessing.Queue()
        self.package_lock = multiprocessing.Lock()
        self.master_addresses_lock = multiprocessing.Lock()
        self.processes = [_NodeProcess(self) for i in range(self.process_count)]

        # Amazon
        try:
            self.instance_id = open_url('http://instance-data/latest/meta-data/instance-id')
            self.instance_type = open_url('http://instance-data/latest/meta-data/instance-type')
        except URLError:
            self.is_amazon = False
        else:
            self.is_amazon = True
            with open('/proc/uptime', 'r') as f:
                self.approx_term_time = time_since_epoch() - float(f.readline().split()[0]) + 3600 # 3600 так как инстансы работают час


    def main(self):
        while self.is_alive:

            socket = JSONSocket()

            with self.master_addresses_lock:
                for ip, port in self.master_addresses:
                    if socket.connect(ip, port):
                        self.current_master = ip, port
                        break
                else:
                    continue

            startup_msg = {'header': 'start', 'process_count': len(self.processes), 'is_amazon': self.is_amazon}
            if self.is_amazon:
                startup_msg['instance_id'] = self.instance_id
                startup_msg['instance_type'] = self.instance_type
                startup_msg['approx_term_time'] = self.approx_term_time

            try:
                socket.send(startup_msg)
            except ConnectionLostError:
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

                    if not self.answers.empty():
                        socket.send(self.answers.get())

                except ConnectionLostError:
                    self.current_master = None
                    socket.close()
                    break

    def start(self):
        self.thread.start()
        for process in self.processes:
            process.start()

    def stop(self):
        for process in self.processes:
            process.terminate()
        self.is_alive = False
        self.thread.join()

    def give_task(self):
        return self.tasks.get()

    def grab_answer(self, result):
        self.answers.put(result)

    def add_master_address(self, address):
        with self.master_addresses_lock:
            self.master_addresses.append(address)

    def remove_master_address(self, address):
        with self.master_addresses_lock:
            self.master_addresses.remove(address)

    def ensure_package(self, package_filename, package_name, package_version):
        with self.package_lock:
            if (package_name, package_version) not in self.env.installed_packages:

                full_package_path = os.path.join(self.package_cache_dir, package_filename)

                self.s3_client.download_file(self.amazon_s3_bucket, package_filename, full_package_path)

                self.env.install(full_package_path, upgrade=True)


class _NodeProcess:
    def __init__(self, master):
        self.master = master
        self.process = multiprocessing.Process(target=self.main)
        self.modules = {}

    def terminate(self):
        self.process.terminate()

    def start(self):
        self.process.start()

    def main(self):

        # Processes have no output
        sys.stdout = open(os.devnull, 'w')

        while True:
            json_task = self.master.give_task()
            task = json.loads(json_task)

            module_name = '.'.join((task['package_name'], task['module_name']))

            self.master.ensure_package(task['package_filename'], task['package_name'], task['package_version'])
            self.modules[module_name] = importlib.import_module(module_name)

            function = getattr(self.modules[module_name], task['function_name'])

            args = json.loads(task['args_json'])

            t = time.perf_counter()
            result = function(*args)
            t = time.perf_counter() - t

            answer = {
                'header': 'result',
                'json_task': json_task,
                'result': result,
                'time': t,
            }
            answer.update(task)

            self.master.grab_answer(answer)

