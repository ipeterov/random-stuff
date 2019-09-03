import objsocket
import queue
import threading
import pickle

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

    def __init__(self, task_port, result_port, node_addresses):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.active_task_stream = False
        self.controller = _ControllerConnection(task_port, result_port, self)
        self.nodes = [_NodeConnection(ip, port, self) for ip, port in node_addresses]

    def start(self):
        self.controller.start()
        for node in self.nodes:
            node.start()

    def grab_result(self, result):
        '''Эту функцию будет вызывать _NodeConnection чтобы передать результаты в Master'''
        self.results.put(result)
        self.tasks.task_done()

    def give_task(self):
        '''Эту функцию будет вызывать _NodeConnection чтобы взять задание из Master'''
        return self.tasks.get()

    def put_task(self, task):
        '''Эту функцию будет вызывать _ControllerConnection чтобы положить задание в очередь Master'''
        self.tasks.put(task)

    def get_result(self):
        '''Эту функцию будет вызывать _ControllerConnection чтобы взять результат из очереди Master'''
        try:
            return self.results.get(timeout=1)
        except queue.Empty:
            return None


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

class _NodeConnection:
    def __init__(self, ip, port, master):
        self.ip = ip
        self.port = port
        self.master = master
        self.sock = objsocket.objsocket()
        self.thread = threading.Thread(target=self.main)

    def start(self):
        self.thread.start()

    def main(self):
        sucsessful = self.sock.connect(self.ip, self.port)
        if sucsessful:
            print('Connected to node {ip}:{port}.'.format(ip=self.ip, port=self.port))
        else:
            print('Node {ip}:{port} is unavailible.'.format(ip=self.ip, port=self.port))
            return

        while True:
            task = self.master.give_task()
            self.sock.send_obj(task)
            print('Sent task {}'.format(task))
            result = self.sock.recv_obj()
            print('Got result')
            self.master.grab_result(result)


class Node:
    '''
    Класс, который получает задания от Master и возвращает ответы.
    '''

    def __init__(self, function, port):
        self.sock = objsocket.objsocket()
        self.sock.bind_and_listen(port)
        self.function = function

    def start(self):
        while True:
            connection, address = self.sock.accept()
            print('Connected to master {}'.format(address))

            while True:
                try:
                    task = connection.recv_data()
                except objsocket.EndOfInputException:
                    print('Disconnected from master {}'.format(address))
                    connection.close()
                    break

                task = pickle.loads(task)
                print('Got task {}'.format(task))
                connection.send_obj(self.function(task))
                print('Sent result')
