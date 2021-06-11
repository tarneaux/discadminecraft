import socket
from threading import Thread
from subprocess import Popen


class Minecraft:
    def __init__(self):
        self.log = None
        self.previous_log = None
        socket_thread = Thread(target=self.socket_server)
        socket_thread.start()

    def minecraft_server(self):
        self.log = Popen(["./start.sh"], cwd="Minecraft", shell=True)
        self.previous_log = self.log

    def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 25556))
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    data = conn.recv(1024)
                    if not data:
                        break
                    if data == b"ping":
                        conn.sendall(b"pong")


Minecraft()
