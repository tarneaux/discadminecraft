import os
from setup_wizard import Wizard
import argparse
import json
import sys


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A Discord bot for Minecraft server control.")
        self.define_args()
        self.args = self.parser.parse_args()
        if not os.path.isfile("config.json") or self.args.setup:
            config = Wizard().start()
            json.dump(config, open("config.json", "w"))
        config = json.load(open("config.json", "r"))
        os.system(sys.executable + " " + config["server_command"])

    def define_args(self):
        self.parser.add_argument("-s", "--setup", dest="setup", action="store_true", help="Setup a new server.")


Main()
