import socket
import queue
import threading
import pickle

class Master:
    def __init__(self, tasks, node_addresses):
        self.tasks = queue.Queue()
        for task in tasks:
            self.tasks.put(task)
        self.nodes = [_NodeConnection(ip, port, self) for ip, port in node_addresses]
        self.results = []

    def get_results(self):
        for node in self.nodes:
            node.thread.start()
        self.tasks.join()
        return self.results

class _NodeConnection:
    def __init__(self, ip, port, master):
        self.ip = ip
        self.port = port
        self.master = master
        self.sock = socket.socket()
        self.thread = threading.Thread(target=self.main)

    def main(self):
        try:
            self.sock.connect((self.ip, self.port))
            print('Connected to node {ip}:{port}.'.format(ip=self.ip, port=self.port))
        except socket.error:
            print('Node {ip}:{port} is unavailible.'.format(ip=self.ip, port=self.port))
            return

        while not self.master.tasks.empty():
            task = self.master.tasks.get()
            self.sock.send(pickle.dumps(task))
            result = pickle.loads(self.sock.recv(4096))
            self.master.results.append(result)
            self.master.tasks.task_done()
        else:
            self.sock.send(pickle.dumps('finish'))


class Node:
    def __init__(self, function, port):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(1)
        self.function = function

    def start(self):
        while True:
            connection, address = self.sock.accept()

            while True:
                task = pickle.loads(connection.recv(4096))
                if task == 'finish':
                    connection.close()
                    break
                connection.send(pickle.dumps(self.function(task)))
