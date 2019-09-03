import objsocket
import queue
import threading
import pickle
import time

class Controller:
    '''
    Это класс написанный для примера, в реальности на его месте
    скорее всего будет программа на VB.net, которая будет подбирать
    параметры. Она должна будет посылать по сокетам то же, что и этот
    класс.
    '''

    def _init__(self, ip, task_port, result_port):
        self.task_socket = objsocket.objsocket()
        self.result_socket = objsocket.objsocket()

        self.task_socket.connect(ip, task_port)
        self.result_socket.connect(ip, result_port)

    def main(self):
        tasks = ['spam', 'eggs', 'ham']
        for i in range(3):
            task_socket.send_obj(tasks.pop())
            answer = result_socket.recv_obj()
            print(answer)

class Master:
    '''
    Класс, который получает задачи от чего-нибудь вроде Controller,
    распределяет их по Node-ам, получает результаты и посылает их
    обратно в Controller.
    '''

    def __init__(self, task_port, result_port, manager_port, allowed_node_addrs):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.active_task_stream = False
        self.controller = _ControllerConnection(task_port, result_port, self)
        self.node_manager = _NodeManager(manager_port, allowed_node_addrs, self)

    def start(self):
        self.controller.start()
        self.node_manager.start()

    def grab_result(self, result):
        '''Эту функцию вызывает _NodeConnection чтобы передать результаты в Master'''
        self.results.put(result)
        self.tasks.task_done()

    def give_task(self):
        '''Эту функцию вызывает _NodeConnection чтобы взять задание из Master'''
        try:
            task = self.tasks.get_nowait()
        except queue.Empty:
            task = None

        return task

    def reuse_task(self, task):
        '''Эту функцию вызывает _NodeConnection чтобы вернуть задание в Master в случае обрыва соединения с Node'''
        self.tasks.put(task)

    def put_task(self, task):
        '''Эту функцию будет вызывать _ControllerConnection чтобы положить задание в очередь Master'''
        self.tasks.put(task)

    def get_result(self):
        '''Эту функцию будет вызывать _ControllerConnection чтобы взять результат из очереди Master'''
        try:
            return self.results.get(timeout=1)
        except queue.Empty:
            return None

class _NodeManager:
    def __init__(self, manager_port, allowed_node_ips, master):
        self.master = master
        self.allowed_node_ips = allowed_node_ips

        self.thread = threading.Thread(target=self.main)
        self.nodes = {} # {ip: node, }

        self.sock = objsocket.objsocket()
        self.sock.bind_and_listen(manager_port, len(allowed_node_ips))

    def start(self):
        self.thread.start()

    def main(self):
        while True:
            conn, addr = self.sock.accept()
            ip = addr[0]
            print('Node with addr {} is trying to connect.'. format(addr))
            if ip in self.allowed_node_ips:
                if ip in self.nodes:
                    if self.nodes[ip].stop():
                        print('Stopped old node with ip {}'.format(ip))
                    else:
                        print('Old node with ip {} was already dead'.format(ip))
                node_connection = _NodeConnection(conn, self.master, self)
                self.nodes[ip] = node_connection
                node_connection.start()
                print('Connected to node at {}'.format(ip))
            else:
                print('Refused')


class _NodeConnection:
    def __init__(self, sock, master, manager):
        self.master = master
        self.sock = sock
        self.thread = threading.Thread(target=self.main)
        self.is_alive = True
        self.is_dead = False

    def start(self):
        self.thread.start()

    def stop(self):
        if not self.is_dead:
            self.is_alive = False
            while not self.is_dead:
                time.sleep(1)
            return True
        else:
            return False

    def main(self):
        while self.is_alive:
            task = self.master.give_task()

            if task == None:
                time.sleep(1)

            try:
                self.sock.send_obj(task)
            except objsocket.ServerUnavailibleException:
                print('Disconnected from node.')
                if task != None:
                    self.master.reuse_task(task)
                    print('Task returned to queue')
                break

            if task != None:
                print('Sent task {}'.format(task))

            try:
                result = self.sock.recv_obj()
            except objsocket.EndOfInputException:
                print('Disconnected from node.')
                if task != None:
                    self.master.reuse_task(task)
                    print('Task returned to queue')
                break

            if task != None:
                print('Got result')
                self.master.grab_result(result)

        self.is_dead = True

class _ControllerConnection:
    def __init__(self, task_port, result_port, master):
        self.master = master
        self.thread = threading.Thread(target=self.main)

        self.task_socket = objsocket.objsocket()
        self.result_socket = objsocket.objsocket()

        self.task_socket.bind_and_listen(task_port)
        self.result_socket.bind_and_listen(result_port)

    def start(self):
        self.thread.start()

    def main(self):
        while True:
            task_connection, task_adress = self.task_socket.accept()
            self.master.active_task_stream = True
            print('Connected to task_socket {}'.format(task_adress))
            result_connection, result_adress = self.result_socket.accept()
            print('Connected to result_socket {}'.format(result_adress))

            task_thread = threading.Thread(target=self._task_stream, args=(task_connection, ))
            result_thread = threading.Thread(target=self._result_stream, args=(result_connection, ))

            task_thread.start()
            result_thread.start()

            task_thread.join()
            result_thread.join()

    def _task_stream(self, task_connection):
        while True:
            try:
                task = task_connection.recv_obj()
            except objsocket.EndOfInputException:
                task_connection.close()
                self.master.active_task_stream = False
                print('Disconnected from task_socket')
                break
            print('Got task from cont {}'.format(task))
            self.master.put_task(task)

    def _result_stream(self, result_connection):
        while True:
            result = self.master.get_result()
            if result == None:
                pass
                if not self.master.active_task_stream:
                    result_connection.close()
                    print('Disconnected from result_socket and closed connection to cont')
                    break
            else:
                result_connection.send_obj(result)
                print('Sent result to cont')


class Node:
    '''
    Класс, который получает задания от Master и возвращает ответы.
    '''

    def __init__(self, function, master_ip, master_port):
        self.function = function
        self.master_ip = master_ip
        self.master_port = master_port

    def start(self):
        while True:
            sock = objsocket.objsocket()
            successful = sock.connect(self.master_ip, self.master_port)
            if successful:
                print('Connected to master {}@{}'.format(self.master_ip, self.master_port))
            else:
                time.sleep(1)
                continue

            while True:
                try:
                    task = sock.recv_data()
                except objsocket.EndOfInputException:
                    print('Disconnected from master {}@{}'.format(self.master_ip, self.master_port))
                    sock.close()
                    break

                task = pickle.loads(task)
                if task != None:
                    print('Got task {}'.format(task))
                    sock.send_obj(self.function(task))
                    print('Sent result')
                else:
                    sock.send_obj(None)
