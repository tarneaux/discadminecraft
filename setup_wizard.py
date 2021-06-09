import requests
import os
import shutil
import psutil

class Wizard:
    def __init__(self):
        print("Welcome to the discadminecraft setup.\n"
              "This tool will guide you to get your Minecraft/Discord server running.")

    def setup_minecraft_server(self):
        if os.path.isdir("Minecraft"):
            print("WARNING! You seem to already have a server in the Minecraft directory! If you continue, you'll wipe the entire server, including worlds!")
            while True:
                choice = input("Do you want to continue? ['y','n']:")
                if choice == "y":
                    print("Please enter 'yy' if you want to delete the server.")
                elif choice == "yy":
                    print("Continuing.")
                    break
                else:
                    print("Stopping the Minecraft server setup.")
                    return
        print("Installing Minecraft server.")
        print("How do you want to install the server?\n"
              "[1] Download a paper server\n"
              "[2] Enter download link for given server")
        while True:
            choice = self._get_choice("12")
            if choice == "1":
                if os.path.isdir("Minecraft"):
                    shutil.rmtree('Minecraft')
                self.download_paper()
                break
            elif choice == "2":
                if os.path.isdir("Minecraft"):
                    shutil.rmtree('Minecraft')
                self.download_from_link()
                break

    def download_from_link(self):
        while True:
            link = input("Download link? (This should end with .jar) ")
            if link.endswith(".jar"):
                try:
                    r = requests.get(link)
                    if not r.ok:
                        print("Whoops, we couldn't download that. Please verify the URL is right.")
                        continue
                    os.mkdir("Minecraft")
                    open('Minecraft/server.jar', 'wb').write(r.content)
                    self.set_ram()
                    break
                except requests.exceptions.MissingSchema:
                    print("The URL should start with https:// or http://.")
                except requests.exceptions.ConnectionError:
                    print("Whoops, we couldn't download that. Please verify the URL is right.")
            else:
                print("invalid link.")

    def download_paper(self):
        print("Downloading paper server.")
        r = requests.get("https://papermc.io/api/v2/projects/paper")
        versions = r.json()["versions"]
        version_groups = r.json()["version_groups"]
        choosen_version = input("Please enter a Minecraft version. Latest is " + versions[-1] + ". ")
        if choosen_version == "":
            choosen_version = versions[-1]
        while not(choosen_version in versions or choosen_version in version_groups):
            print("Oops, this version doesn't seem like it's supported by paper. The available versions are:\n" + str(versions))
            choosen_version = input("Please enter a Minecraft version. ")
            if choosen_version == "":
                choosen_version = versions[-1]
        r = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + choosen_version)
        latest_build = str(r.json()["builds"][-1])
        print("Downloading paper build " + latest_build + "...")
        r = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + choosen_version + "/builds/" + latest_build + "/downloads/paper-" + choosen_version + "-" + latest_build + ".jar")
        os.mkdir("Minecraft")
        open('Minecraft/server.jar', 'wb').write(r.content)
        self.set_ram()

    def set_ram(self):
        while True:
            gigs = int(input("How much RAM do you want to allocate to your minecraft server? (in Gb)"))
            if gigs > psutil.virtual_memory().total / 1000000000:
                print("You don't have that much RAM!")
            elif gigs > psutil.virtual_memory().available / 1000000000:
                print("Currently there's not that much memory available. Do you want to continue anyway? (available: " + str(int(psutil.virtual_memory().available / 1000000000)) + "Gb)")
                if self._get_choice("yn") == "y":
                    break
            else:
                break
        open('Minecraft/start.sh', 'w').write("java -jar server.jar -Xmx" + str(gigs) + "G -Xms" + str(gigs) + "G nogui")

    def _get_choice(self, allowedValues: str):
        allowedValues = [char for char in allowedValues]
        while True:
            choice = input(str(allowedValues) + ":")
            if choice in allowedValues:
                return choice
