import os.path
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
            "stop": self.stop,
            "status": self.status
        }
        self.socket_server()

    def minecraft_server(self):
        if os.path.isfile("Minecraft/logs/latest.log"):
            os.remove("Minecraft/logs/latest.log")
        self.server = Popen("./start.sh", cwd="Minecraft", stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        self.running = True

    def run(self, command):
        if "Done" in self.log():
            self.server.stdin.write((command + "\r\n").encode("utf-8"))
            self.server.stdin.flush()
        else:
            return False

    def log(self):
        log_file_fath = os.path.join(os.getcwd(), "Minecraft/logs/latest.log")
        if self.running:
            if not self.outputted:
                if os.path.isfile("Minecraft/logs/latest.log"):
                    self.outputted = True
                else:
                    return ""
            return open(log_file_fath, "r").read()
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
            if self.run("stop") is False:
                return "not running"
            self.server.communicate()
            self.running = False
            self.outputted = False
            if os.path.isfile("Minecraft/logs/latest.log"):
                return open(os.path.join(os.getcwd(), "Minecraft/logs/latest.log"), "r").read()
            else:
                return ""
        else:
            return "Already stopped"

    def status(self):
        try:
            if self.server.poll() is not None and self.running:
                self.running = False
                self.outputted = False
                return "stopped"
        except AttributeError:
            pass
        if not self.running:
            return "stopped"
        if "Done" in self.log():
            return "running"
        return "starting"

    def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                s.close()


Minecraft()
