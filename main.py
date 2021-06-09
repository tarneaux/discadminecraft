import os

import setup_wizard
import argparse

class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A Discord bot for Minecraft server control.")
        self.define_args()
        self.args = self.parser.parse_args()
        print(self.args.setup)
        if not os.path.isfile(".setup_done") or self.args.setup:
            setup_wizard.Wizard()

    def define_args(self):
        self.parser.add_argument("-s, --setup", dest="setup", action="store_true", help="Setup a new server.")

Main()
