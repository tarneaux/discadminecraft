import os
import setup_wizard
import argparse
import json


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A Discord bot for Minecraft server control.")
        self.define_args()
        self.args = self.parser.parse_args()
        if not os.path.isfile("config.json") or self.args.setup:
            data = setup_wizard.wizard()
            with open("config.json", "w") as write_file:
                json.dump(data, write_file)

    def define_args(self):
        self.parser.add_argument("-s, --setup", dest="setup", action="store_true", help="Setup a new server.")


Main()
