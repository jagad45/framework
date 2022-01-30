import socket
from threading import Thread

class Core:
    def __init__(self) -> None:
        self.options = {}
        self.threads = []

        self.DEFAULT_HOSTNAME = "8.8.8.8"

    def destroy(self):
        for thread in self.threads:
            thread.join()

    def reset(self):
        self.destroy()
        self.threads = []
        self.options = {}

    def set_options(self, option: dict):
        self.options = option

    def check_connection(self):
        try:    
            try:
                hostname = self.options["target"]
            except KeyError:
                hostname = self.DEFAULT_HOSTNAME
            print (f"[!] Test connection, use hostname {hostname} and port 80 (http only)")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((hostname, 80))
            return True
        except socket.timeout:
            print ("[-] Can't connect internet, read timeout")
            return False
        except OSError:
            print ("[-] Can't connect internet, network error")
            return False