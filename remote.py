import socket
from time import sleep


class Client:
    def __init__(self, host):
        self.host = host

    def __enter__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self.host, 25556))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._s.close()

    def sendall(self, text: str):
        self._s.sendall(text.encode("utf-8"))

    def recvall(self, bs=256):
        data = b""
        while True:
            part = self._s.recv(bs)
            data += part
            if len(part) < bs:
                break
        data = data.decode("utf-8")
        if data.endswith("\n"):
            data = data[:-1]
        return data


class NotRunningError(Exception):
    pass


class AlreadyStoppedError(Exception):
    pass


class Remote:
    def __init__(self, host):
        self.host = host
        self.client = Client(self.host)

    def log(self):
        with self.client as c:
            c.sendall("log")
            return c.recvall()

    def previous_log(self):
        with self.client as c:
            c.sendall("previous_log")
            return c.recvall()

    def start(self):
        with self.client as c:
            c.sendall("start")
            return c.recvall()

    def stop(self):
        with self.client as c:
            c.sendall("stop")
            response = c.recvall()
            return response

    def run(self, command: str):
        if command:
            command = "run:" + command
            with self.client as c:
                c.sendall(command)
            sleep(1)

    def status(self):
        with self.client as c:
            c.sendall("status")
            return c.recvall()
