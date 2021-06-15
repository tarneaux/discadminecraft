import socket
import time
from threading import Thread
from subprocess import Popen, PIPE, STDOUT


class Minecraft:
    def __init__(self):
        print("Server started.")
        print("My IP is: " + socket.getfqdn())
        self.log = ""
        self.previous_log = ""
        self.running = False
        self.answers = {
            "ping": (lambda: "pong"),
            "log": (lambda: self.log),
            "start": self.start,
            "previous_log": (lambda: self.previous_log),
            "stop": self.stop
        }
        self.socket_server()

    def minecraft_server(self):
        self.server = Popen("./start.sh", cwd="Minecraft", stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        self.log = ""
        self.running = True
        while self.server.poll() == None:
            self.log += self.server.stdout.readline().decode("utf-8")
            self.server.stdout.flush()
        print(time.strftime("%H:%M:%S"))
        self.running = False
        self.previous_log = self.log

    def run(self, command):
        if self.running:
            self.server.stdin.write((command + "\r\n").encode("utf-8"))
            self.server.stdin.flush()

    def start(self):
        if not self.running:
            minecraft_thread = Thread(target=self.minecraft_server)
            minecraft_thread.start()
            return "started"
        else:
            return "running"

    def stop(self):
        if self.running:
            self.run("stop")
            while self.running:
                pass
            return self.log
        else:
            return "Already stopped"

    def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 25556))
            try:
                while True:
                    s.listen()
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(1024).decode("utf-8")

                        if data.startswith("run:"):
                            self.run(data[4:])
                        elif data in self.answers:
                            conn.sendall(self.answers[data]().encode("utf-8"))
                        else:
                            conn.sendall(b"unknown")
            except KeyboardInterrupt:
                print("Stopping Minecraft server...")
                if self.running:
                    self.run("stop")
                    while self.running:
                        pass
                pass
Minecraft()
