import json
from socket import *


class ConnectionLostError(Exception):
    pass

class MessageTooBigError(Exception):
    pass


class JSONSocket:
    def __init__(self, sock=None, prefix_length=4):
        if sock == None:
            self.sock = socket()
        else:
            self.sock = sock
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.prefix_length = prefix_length

    def bind_and_listen(self, port, number=1):
        self.sock.bind(('', port))
        self.sock.listen(number)

    def getpeername(self):
        return self.sock.getpeername()

    def accept(self):
        try:
            conn, addr = self.sock.accept()
        except error:
            raise ServerUnavailibleException()

        return JSONSocket(conn), addr

    def connect(self, ip, port):
        try:
            self.sock.connect((ip, port))
            return True
        except OSError:
            return False

    def send_string(self, string):
        encoded = string.encode('utf-8')
        self._send_bytes(encoded)

    def receive_string(self):
        encoded = self._receive_bytes()
        return encoded.decode('utf-8')

    def send(self, obj):
        data = json.dumps(obj, sort_keys=True)
        self.send_string(data)

    def receive(self):
        data = self.receive_string()
        return json.loads(data)

    def _send_bytes(self, data):
        length = len(data)
        if length > 2**(self.prefix_length*8):
            raise MessageTooBigError

        try:
            self.sock.sendall(length.to_bytes(self.prefix_length, byteorder='little'))
            self.sock.sendall(data)
        except BrokenPipeError:
            raise ConnectionLostError

    def _receive_bytes(self):
        lengthbuf = self._recvall(self.prefix_length)
        if not lengthbuf:
            raise ConnectionLostError
        length = int.from_bytes(lengthbuf, byteorder='little')
        return self._recvall(length)

    def _recvall(self, count):
        try:
            buf = b''
            while count:
                newbuf = self.sock.recv(count)
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
            return buf
        except ConnectionResetError:
            raise ConnectionLostError

    def close(self):
        self.sock.close()
