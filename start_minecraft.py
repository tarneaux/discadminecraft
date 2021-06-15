import socket
from subprocess import Popen, PIPE, STDOUT


class Minecraft:
    def __init__(self):
        print("Server started.")
        print("My IP is: " + socket.getfqdn())
        self.previous_log = ""
        self.running = False
        self.outputted = False
        self.answers = {
            "ping": (lambda: "pong"),
            "log": self.log,
            "start": self.start,
            "previous_log": (lambda: self.previous_log),
            "stop": self.stop
        }
        self.socket_server()

    def minecraft_server(self):
        self.server = Popen("./start.sh", cwd="Minecraft", stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        self.running = True

    def run(self, command):
        if "Done" in self.log():
            self.server.stdin.write((command + "\r\n").encode("utf-8"))
            self.server.stdin.flush()

    def log(self):
        if self.running:
            while not self.outputted:
                while not self.server.stdout.readline():
                    pass
                self.outputted = True
            return open("/home/max/Servers/discadminecraft/Minecraft/logs/latest.log", "r").read()
        else:
            return ""

    def start(self):
        if not self.running:
            self.minecraft_server()
            return "started"
        else:
            return "running"

    def stop(self):
        if self.running:
            self.run("stop")
            self.server.communicate()
            self.running = False
            self.outputted = False
            return self.log()
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
                        data = conn.recv(64).decode("utf-8")

                        if data.startswith("run:"):
                            data += conn.recv(1024).decode("utf-8")
                            self.run(data[4:])
                        elif data in self.answers:
                            conn.sendall(self.answers[data]().encode("utf-8"))
                        else:
                            conn.sendall(b"unknown")
            except KeyboardInterrupt:
                print("Stopping Minecraft server...")
                if self.running:
                    self.stop()
                pass


Minecraft()
