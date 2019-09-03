import multiprocessing
import threading
import os
import sys
import json
import boto3
import importlib
import time

from multiserver.connection_lib import ClientConnection
from multiserver.util import time_since_epoch, open_url, URLError

from virtualenvapi.util import get_env_path
from virtualenvapi.manage import VirtualEnvironment


class Node:

    def __init__(self, master_address, process_count=None, package_cache_dirs=None, amazon_s3_bucket='ipeterov'):

        # This will throw an exception if run not from virtualenv
        self.env = VirtualEnvironment()

        self.s3_client = boto3.client('s3')
        self.amazon_s3_bucket = amazon_s3_bucket

        self.thread = threading.Thread(target=self.main_loop)
        self.keep_alive = True

        self.master_connection = ClientConnection(master_address)

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


    def main_loop(self):
        while self.keep_alive:

            startup_msg = {'header': 'start', 'body': {'process_count': len(self.processes), 'is_amazon': self.is_amazon}}
            if self.is_amazon:
                startup_msg['body']['instance_id'] = self.instance_id
                startup_msg['body']['instance_type'] = self.instance_type
                startup_msg['body']['approx_term_time'] = self.approx_term_time

            response = self.master_connection.get_response(startup_msg)

            while self.keep_alive:
                if self.tasks.empty():
                    response = self.master_connection.get_response({'header': 'task_request'})
                    if response['header'] == 'task':
                        self.tasks.put(response)
                    elif response['header'] == 'no_task':
                        pass

                if not self.answers.empty():
                    response = self.master_connection.get_response(self.answers.get())

    def start(self):
        self.thread.start()
        for process in self.processes:
            process.start()

    def stop(self):
        for process in self.processes:
            process.terminate()
        self.keep_alive = False
        self.thread.join()

    def give_task(self):
        return self.tasks.get()

    def grab_answer(self, result):
        self.answers.put(result)

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
            task = self.master.give_task()

            module_name = '.'.join((task['body']['package_name'], task['body']['module_name']))

            self.master.ensure_package(task['body']['package_filename'], task['body']['package_name'], task['body']['package_version'])
            self.modules[module_name] = importlib.import_module(module_name)

            function = getattr(self.modules[module_name], task['body']['function_name'])

            t = time.perf_counter()
            result = function(*task['body']['args'])
            t = time.perf_counter() - t

            answer = {
                'header': 'result',
                'body': {
                    'result': result,
                    'time': t
                }
            }
            answer['body'].update(task['body'])

            self.master.grab_answer(answer)

