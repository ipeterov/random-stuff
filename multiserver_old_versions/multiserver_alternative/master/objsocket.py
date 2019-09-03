import pickle
import struct
from socket import *

class EndOfInputException(Exception):
    pass

class ServerUnavailibleException(Exception):
    pass

class objsocket:
    def __init__(self, sock=None):
        if not sock:
            self.sock = socket()
        else:
            self.sock = sock

    def bind_and_listen(self, port):
        self.sock.bind(('', port))
        self.sock.listen(1)

    def accept(self):
        try:
            conn, addr = self.sock.accept()
        except error:
            raise ServerUnavailibleException()

        return objsocket(conn), addr

    def connect(self, ip, port):
        try:
            self.sock.connect((ip, port))
            return True
        except ConnectionRefusedError:
            return False

    def send_obj(self, obj):
        data = pickle.dumps(obj)
        self.send_data(data)

    def recv_obj(self):
        data = self.recv_data()
        return pickle.loads(data)

    def send_data(self, data):
        length = len(data)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(data)

    def recv_data(self):
        lengthbuf = self._recvall(4)
        if not lengthbuf:
            raise EndOfInputException('Session ended!')
        length, = struct.unpack('!I', lengthbuf)
        return self._recvall(length)

    def _recvall(self, count):
        buf = b''
        while count:
            newbuf = self.sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def close(self):
        self.sock.close()
