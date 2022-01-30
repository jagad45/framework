import os
import threading
import hashlib
import time
from jagad.utils.converter import convert_hashrate
from jagad.utils.typedata import Options, File
from jagad.terminal.console import print_warning
from jagad.terminal.colors import Fore

symbols = "|/-\|"
def animation_loading(text, index):
    global symbols
    if index >= len(symbols):
        index = 0
    symbol = symbols[index]
    print(f"{Fore.WHITE}[{Fore.GREEN}{symbol}{Fore.WHITE}] {text}", end="\r")
    index += 1
    time.sleep(0.05)
    return index

class Core:
    def __init__(self) -> None:
        self.supported_algo     = {
            "md4": "bde52cb31de33e46245e05fbdbd6fb24",
            "md5": "0cc175b9c0f1b6a831c399e269772661",
            "sha1": "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8",
            "blake2b": "333fcb4ee1aa7c115355ec66ceac917c8bfd815bf7587d325aec1864edd24e34d5abe2c6b1b5ee3face62fed78dbef802f2a85cb91d455a8f5249d330853cb3c",
            "blake2s": "4a0d129873403037c2cd9b9048203687f6233fb6738956e0349bd4320fec3e90",
            "sha384": "d752c2c51fba0e29aa190570a9d4253e44077a058d3297fa3a5630d5bd012622f97c28acaed313b5c83bb990caa7da85",
            "sha256": "cd2eb0837c9b4c962c22d2ff8b5441b7b45805887f051d39bf133b583baf6860",
            "sha512": "9057ff1aa9509b2a0af624d687461d2bbeb07e2f37d953b1ce4a9dc921a7f19c45dc35d7c5363b373792add57d0d7dc41596e1c585d6ef7844cdf8ae87af443f",
        }

        self.options            = {}
        self.password_string    = ""
        self.threads            = []
        self.isrunning          = True
        self.wordlist_index     = 0
        self.running_speed      = 0
        self.running_speeds     = []

    def reset(self):
        self.password_string    = ""
        self.threads            = []
        self.isrunning          = True
        self.wordlist_index     = 0
        self.running_speed      = 0
        self.running_speeds     = []

    def paste_options(self, parsed: dict):
        self.options = parsed

    def destroy(self):
        for th in self.threads:
            th.join()

    def check_algo(self):
        options = self.options["type"]
        if options.lower() in self.supported_algo:
            return True
        else:
            print_warning(f"Hash type not sopported!")
            return False

    def splitlines_wordlist(self, text: str):
        animation_index = 0
        for data in text.split("\n"):
            self.options["wordlist"].append(data)

    def read_wordlist_content(self, file):
        chunksize = self.options["chunksize"]
        encoding = self.options["encoding"]
        data = ""
        while True:
            try:
                temp = file.read(chunksize)
                if not temp: break
                else:
                    try:
                        data += temp
                    except (UnicodeDecodeError):
                        data += temp.decode(encoding)
                    except TypeError:
                        data += temp.decode()
            except UnicodeDecodeError:
                print_warning(f"Can't decode content, try change raw to 0 (false)")
                break
        if data == "":
            return False
        else:
            th = threading.Thread(target=self.splitlines_wordlist, args=(data, ))
            th.setDaemon(True)
            th.start()
            animation_index = 0
            while th.is_alive():
                animation_index = animation_loading("Append text to wordlist", animation_index)
            th.join()

            return True

    def read_wordlist(self):
        pathlist = self.options["filename"]
        if isinstance(pathlist, File):
            pathlist = pathlist.value

        isRaw = self.options["raw"]
        if os.path.isfile(pathlist) is True:
            read_mode = "r"
            if isRaw == 0 or isRaw == "0":
                read_mode += "b"
            animation_index = 0
            with open(pathlist, read_mode) as file:
                th = threading.Thread(target=self.read_wordlist_content, args=(file, ))
                th.setDaemon(True)
                th.start()
                while th.is_alive():
                    animation_index = animation_loading("Reading wordlist...", animation_index)
                file.close()
                try:
                    th.join()
                    return True
                except LookupError as err:
                    print (f"{err}")
                    return False
        else:
            print_warning(f"File '{pathlist}' no such file")
            return False

    def check_wordlist(self):
        value = self.options["wordlist"]
        value_length = len(value)
        if value_length == 0:
            status = self.read_wordlist()
            return status
        else:
            return True

    def validate_hash(self):
        target_hash = self.options["target"]
        hash_type = self.options["type"]
        if target_hash is None:
            print_warning(f"Target hash is not defined")
            return False
        else:
            algo_sample = self.supported_algo[hash_type.lower()]
            if len(target_hash) == len(algo_sample):
                return True
            else:
                print_warning(f"Invalid hash type")
                return False

    def calculate_speed(self):
        while self.isrunning:
            current_index = self.wordlist_index
            time.sleep(1)
            self.running_speed = (self.wordlist_index - current_index)
            if self.running_speed in self.running_speeds:
                continue
            else:
                self.running_speeds.append(self.running_speed)

    def print_status(self):
        while self.isrunning:
            print (f"{Fore.WHITE}[{Fore.CYAN}RUN{Fore.WHITE}] job: {len(self.threads)} process: {self.wordlist_index} speed: {convert_hashrate(self.running_speed)}H/s time: {int(time.time() - self.start_time)}s" + " " * 5, end="\r")
            time.sleep(0.1)

    def start(self):
        wordlist = self.options["wordlist"]
        algo = self.options["type"].lower()
        target = self.options["target"]
        while self.isrunning:
            if self.wordlist_index >= len(wordlist):
                self.isrunning = False
                break
            else:
                try:
                    password = wordlist[self.wordlist_index]
                    jobhash = hashlib.new(algo)
                    jobhash.update(password.encode())
                    sample = jobhash.hexdigest()
                    if target == sample:
                        self.password_string = password
                        self.isrunning = False
                    self.wordlist_index += 1
                except IndexError:
                    self.isrunning = False
                    
    def run(self):
        print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Target: {self.options['target']}")
        print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Algorithm: {self.options['type']}")
        print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Total threads: {os.cpu_count()}")
        print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Total wordlist: {len(self.options['wordlist'])}")
        
        max_worker = os.cpu_count()
        self.start_time = time.time()
        for x in range(max_worker):
            th = threading.Thread(target=self.start)
            th.setDaemon(True)
            th.start()
            self.threads.append(th)
        th_speed = threading.Thread(target=self.calculate_speed)
        th_speed.setDaemon(True)
        th_speed.start()

        th_status = threading.Thread(target=self.print_status)
        th_status.setDaemon(True)
        th_status.start()

        self.threads.append(th_speed)
        self.threads.append(th_status)

        self.destroy()
        current_value = 0
        for speed in self.running_speeds:
            current_value += speed
        try:
            average_speed = int(current_value / len(self.running_speeds))
        except ZeroDivisionError:
            average_speed = 0
            hashlib.algorithms_available
        try:
            print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Min speed: {convert_hashrate(min(self.running_speeds))}H/s" + " " * 60)
            print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Max speed: {convert_hashrate(max(self.running_speeds))}H/s")
            print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Average speed: {convert_hashrate(average_speed)}H/s")
        except ValueError:
            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}] Min speed: unknown" + " " * 60)
            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}] Max speed: unknown")
            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}] Average speed: unknown")
        print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Time elapsed: {int(time.time() - self.start_time)}s")
        if self.password_string != "":
            print(f"{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] Password: {self.password_string}")
        else:
            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}] Password: not found")
        return True