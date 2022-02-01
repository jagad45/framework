#!/usr/bin/env python3
import sys
import subprocess
import os
import shutil
import time
try:
    import platform
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "platform"], stdout=subprocess.DEVNULL)
    print (f"[!] Please restart script!")
    sys.exit()
    
try:
    import requests
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "requests"], stdout=subprocess.DEVNULL)
    print (f"[!] Please restart script!")
    sys.exit()
    
# Executable path
EXECUTABLE_GIT = ""
EXECUTABLE_PYTHON = sys.executable


symbols = "|/-\|"
index = 0

def animation(text, delay=0.1):
    try:
        global index, symbols
        if index >= len(symbols):
            index = 0
        symbol = symbols[index]
        print(f"[{symbol}] {text}", end="\r")
        index += 1
        time.sleep(delay)
    except: pass

def check_connection():
    try:
        requests.get("https://google.com")
        return True
    except:
        print ("[!] Internet connection required.")
        sys.exit()

def check_system():
    print (("=" * 5) + "System Information" + "=" * 5)
    distros = []
    platform_uname = platform.uname()
    platform_version = platform_uname.version
    # Reference compatible distro: https://github.com/v1s1t0r1sh3r3/airgeddon/blob/master/airgeddon.sh
    known_compatible_distro = [
        "Wifislax",
		"Kali",
		"Parrot",
		"Backbox",
		"BlackArch",
		"Cyborg",
		"Ubuntu",
		"Mint",
		"Debian",
		"SuSE",
		"CentOS",
		"Gentoo",
		"Fedora",
		"Red Hat",
		"Arch",
		"OpenMandriva",
		"Pentoo",
		"Manjaro",
    ]
    for known_distro in known_compatible_distro:
        print (f"[!] Checking distro {known_distro}" + " " * 10, end="\r")
        if known_distro in platform_version:
            distros.append(known_distro)
    if len(distros) == 0:
        print ("[-] No distro known, please see issue.")
        sys.exit()
    else:
        distro = ",".join(distros)
        print (f"[+] Distro: {distro}" + " " * 50)

    print (f"[+] Machine: {platform_uname.machine}")
    print (f"[+] Processor: {platform_uname.processor}")
    print (f"[+] Release: {platform_uname.release}")
    print (f"[+] Name: {platform_uname.node}")
    print (f"[+] Version: {platform_uname.version}")
    
def check_executable():
    print (("=" * 5) + "Executable Information" + ("=" * 5))
    print (f"[+] Python Version: {platform.python_version()}")
    print (f"[+] Python Compile: {platform.python_compiler()}")
    print (f"[+] Python Build Type: {platform.python_build()[0]}")
    print (f"[+] Python Build Date: {platform.python_build()[1]}")
    if platform.python_branch() != "":
        print (f"[+] Python Branch: {platform.python_branch()}")

class SetupGit:
    def __init__(self) -> None:
        self.KNOWN_GIT_PATH = [
            "/usr/bin/git",
            "/bin/git",
            "/usr/local/bin/git",
            os.path.join(os.path.expanduser("~"), ".local/bin/git")
        ]
        self.METADATA = {
            "windows":
            {
                "x64": "https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.1/Git-2.35.1-64-bit.exe",
                "x86": "https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.1/Git-2.35.1-32-bit.exe"
            }
        }

    def check_system(self):
        platform_system = platform.system()
        if platform_system.lower() == "linux" or platform_system.lower() == "windows": return True
        else:
            print (f"[-] System '{platform_system}' not supported.")
            sys.exit()

    def check_git(self, user_path: str = None):
        global EXECUTABLE_GIT
        paths = []
        known_path = []
        if user_path is None:
            paths.extend(self.KNOWN_GIT_PATH)
        else:
            paths.append(user_path)

        for filename in paths:
            if os.path.isfile(filename):
                known_path.append(filename)
            elif os.path.isdir(filename):
                print (f"[-] {os.path.basename(filename)}: Is a directory")
        
        if len(known_path) == 0:
            print ("[-] No git installed found!")
            return self.install_git()
        else:
            running = True
            print ("===Choice a git path===")
            for index, filename in enumerate(known_path):
                print (f"  {index + 1}). {filename}")
            print ("  0). Manual")
            while running:
                user_select = input("[>] Select: ")
                if user_select == "0" or user_select == "00":
                    user_fileinput = input("[?] Paste path: ")
                    if os.path.isfile(user_fileinput):
                        print ("[+] Success to set github path")
                        EXECUTABLE_GIT = user_fileinput
                        running = False
                    elif os.path.isdir(user_fileinput):
                        basename = os.path.basename(user_fileinput)
                        if basename == "":
                            basename = user_fileinput
                        print (f"[-] {basename}: Is a directory")
                        continue
                    else:
                        print ("[-] Invalid path")
                        continue
                if user_select.isdigit():
                    user_select = int(user_select) - 1
                    if user_select > len(known_path):
                        print ("[-] Invalid number")
                    else:
                        git_path = known_path[user_select]
                        EXECUTABLE_GIT = git_path
                        running = False
                else:
                    print ("[-] Invalid number")
        print (f"[!] Use git path: {EXECUTABLE_GIT}")
        return True

    def install_git(self):
        commands = []
        winurls = ""
        platform_system = platform.system()
        if platform_system.lower() == "linux":
            check_system()    
            check_executable()
            platform_version = platform.uname().version
            if "Ubuntu" in platform_version:
                commands.append("add-apt-repository ppa:git-core/ppa")
                commands.append("sudo apt-get update -y")
                commands.append("sudo apt-get install git")
            elif "Fedora" in platform_version:
                print ("=== Choice Fedora Version ===")
                print ("  1). Up to Fedora 21")
                print ("  2). Fedora 22 and later")
                while True:
                    user_input = input("[?] Select: ")
                    if user_input == "1" or user_input == "01":
                        commands.append("yum install git")
                        break
                    elif user_input == "2" or user_input == "02":
                        commands.append("dnf install git")
                        break
                    else: continue
            elif "" in platform_version:
                commands.append("emerge --ask --verbose dev-vcs/git")
        elif platform_system.lower() == "windows":
            print ("=== Choice architecture type ===")
            print ("  1). 64 bit architecture")
            print ("  2). 32 bit architecture")
            while True:
                user_select = input("[?] Select: ")
                if user_select == "1" or user_select == "01":
                    winurls = self.METADATA["windows"]["x64"]
                    break
                elif user_select == "2" or user_select == "02":
                    winurls = self.METADATA["windows"]["x86"]
                    break
                else: continue
        else:
            print ("[!] Your system can't supported.")
            sys.exit()

        if len(commands) == 0:
            print (f"[+] Please download gitbash from {winurls}")
            print ("[+] After install gitbash, please restart this script.")
            input("[*] Enter to exit...")
            sys.exit()
        else:
            print ("=== Git install commands ==")
            print ("[!] Please install manual if you choice type 'n'")
            print ("[!] Super User required!")
            for cmds in commands:
                print (f"[+] Commands: {cmds}")
                run_y = input("[?] Run this command? (Y/n): ")
                if run_y.lower() == "y":
                    subprocess.check_call(f"{cmds}")
                else: continue

            return self.check_git()

class SetupTools:
    def __init__(self) -> None:
        global EXECUTABLE_GIT
        self.GITURL = "https://github.com/jagad45/framework"
        if EXECUTABLE_GIT == "":
            setupgit = SetupGit()
            if setupgit.check_git(): pass

    def clone_github(self):
        global EXECUTABLE_GIT
        gitout = self.GITURL.split("/")[-1]
        if os.path.isdir(gitout):
            user_input = input("[*] Framework found! Delete old framework? (Y/n): ")
            if user_input.lower() == "y":
                shutil.rmtree(gitout)
            else:
                sys.exit()
        try:
            devnull = subprocess.DEVNULL
        except:
            devnull = open(os.devnull, "w")
        print (f"[+] Cloning from github and save to {gitout}...")
        try:
            subprocess.check_call([EXECUTABLE_GIT, "clone", self.GITURL], stdout=devnull, stderr=devnull, stdin=devnull)
        except subprocess.CalledProcessError:
            check_connection()
            print ("[-] Failed clone from github, please check internet connection.")
            sys.exit()
        print ("[+] Success to clone tools")

    def setup_requirements(self):
        global EXECUTABLE_PYTHON
        try:
            devnull = subprocess.DEVNULL
        except:
            devnull = open(os.devnull, "w")
        gitout = self.GITURL.split("/")[-1]
        print ("[+] Installing requirements...")
        requirement_filepath = os.path.join(os.getcwd(), gitout, "requirements.txt")
        if os.path.isfile(requirement_filepath):
            try:
                subprocess.check_call([EXECUTABLE_PYTHON, "-m", "pip", "install", "-r", requirement_filepath], stdout=devnull, stderr=devnull, stdin=devnull)
            except subprocess.CalledProcessError:
                check_connection()
                print ("[-] Install failed, please check your system supported.")
                sys.exit()
        else:
            print ("[-] No requirements file error")
            sys.exit()

    def move_tools(self):
        gitout = self.GITURL.split("/")[-1]
        user_input = input("[?] Move tools? (Y/n): ")
        if user_input.lower() == "y":
            move_path = input("[?] Paste path to move: ")
            shutil.move(gitout, move_path)
            print ("[+] Success to move tools.")

if __name__ == "__main__":
    try:
        setupgit = SetupGit()
        setupgit.check_git()
        setuptools = SetupTools()
        setuptools.clone_github()
        setuptools.setup_requirements()
        setuptools.move_tools()
        print ("[+] All in done.")
    except KeyboardInterrupt:
        print ("[!] User quit")
        sys.exit()