from multiserver.jsonsocket import JSONSocket, ConnectionLostError

import threading
import queue
import time


class ConnectionManager:

    def __init__(self, port, connection_class, max_pending_connections=100):
        self.thread = threading.Thread(target=self.mainloop)
        self.connection_class = connection_class
        self._connections = {}
        self.socket = JSONSocket()
        self.socket.bind_and_listen(port, max_pending_connections)

    @property
    def connections(self):
        for key in self._connections.copy():
            if self._connections[key].is_dead:
                del self._connections[key]
        return self._connections

    def get_connection_addresses(self):
        return list(self.connections.keys())

    def start(self):
        self.thread.start()

    def mainloop(self):
        while True:
            socket, address = self.socket.accept()
            self.connections[address] = self.connection_class(socket, self)
            self.connections[address].start()


class ServerConnection:

    def __init__(self, socket, manager):
        self.manager = manager
        self.socket = socket
        self.thread = threading.Thread(target=self.main_loop)
        self.keep_alive = True
        self.is_dead = False

    def start(self):
        self.thread.start()

    def stop(self):
        self.keep_alive = False
        self.thread.join()

    def response(self, message):
        pass

    def on_connection_closed(self):
        pass

    def main_loop(self):
        while self.keep_alive:
            try:
                message = self.socket.receive()
                response = self.response(message)
                #~ print('got response')
                self.socket.send(response)
                #~ print('sent response')

            except ConnectionLostError:
                break

        self.socket.close()
        self.on_connection_closed()
        self.is_dead = True

#~ class ClientConnectionOld:
#~
    #~ def __init__(self, server_addresses):
        #~ self.lock = threading.RLock()
        #~ self.server_addresses = server_addresses
        #~ self.current_server = None
#~
    #~ def assure_that_connected(self):
        #~ if self.current_server == None:
            #~ self.socket = JSONSocket()
            #~ while True:
                #~ for ip, port in self.server_addresses:
                    #~ if self.socket.connect(ip, port):
                        #~ self.current_server = ip, port
                        #~ return True
#~
    #~ def get_response(self, message):
        #~ with self.lock:
            #~ try:
                #~ self.assure_that_connected()
                #~ self.socket.send(message)
                #~ return self.socket.receive()
            #~ except ConnectionLostError:
                #~ self.current_server = None
                #~ return self.get_response(message)

class ClientConnection:

    def __init__(self, server_address=None):
        if server_address != None:
            self.change_server(server_address)

    def change_server(self, new_server):
        self.server_address = new_server
        self.is_connected = False

    def assure_that_connected(self):
        if not self.is_connected:
            self.socket = JSONSocket()
            while not self.socket.connect(*self.server_address):
                pass # Will block until connect method returns True

    def get_response(self, message):
        try:
            self.assure_that_connected()
            self.socket.send(message)
            return self.socket.receive()
        except ConnectionLostError:
            self.current_server = None
            return self.get_response(message)
