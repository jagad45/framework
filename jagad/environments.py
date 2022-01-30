# This module CRUD (Create, Read, Update, and Delete) environment from files
# This module using Fernet and ZLIB for encrypt data environment
# WARNING: Module no implemented

import os
import time
from threading import Thread
from jagad.crypto.envcrypt import encrypt_data, decrypt_data
from jagad.terminal.console import print, print_error, print_warning
from jagad.exceptions import ThreadingError

class Environments:
    def __init__(self) -> None:
        self.FILENAME = os.path.join(os.getcwd(), ".config.lnx")
        self.environment = {}
        self.threads = {
            "read": {
                "object": None, "running": True
            },
            "write": {
                "object": None, "running": True
            }
        }

    @property
    def data(self):
        return self.environment

    def destroy(self):
        if self.threads["read"]["object"] is None:
            raise ThreadingError("read: Thread not running")
        if self.threads["write"]["object"] is None:
            raise ThreadingError("write: Thread not running")
        self.threads["read"]["running"] = False
        self.threads["write"]["running"] = False
        self.threads["read"]["object"].join()
        self.threads["write"]["object"].join()
        return True

    def build_default(self):
        if len(self.environment) != 1:
            print ("Build new")
            self.environment["client"] = {}
            self.environment["client"]["USER"] = "banaspati"
            self.environment["client"]["PASS"] = "1442"
            self.environment["client"]["REQUIRE_PASSWORD"] = False
            self.environment["server"] = {}
            return True

    def read(self):
        while self.threads["read"]["running"]:
            if os.path.isfile(self.FILENAME):
                with open(self.FILENAME, "rb") as File:
                    content = File.read()
                    data = decrypt_data(content)
                    File.close()
                    if data is False:
                        # print_error (f"Can't load environment file, decode error!", _quit=True)
                        self.build_default()
                    else:
                        self.environment = data
            else:
                self.build_default()
            time.sleep(2)

    def write(self):
        while self.threads["write"]["running"]:
            data = encrypt_data(self.environment)
            File = open(self.FILENAME, "wb")
            File.write(data)
            File.close()
            time.sleep(2)

    def run(self):
        # enable looping thread read and write
        self.threads["read"]["running"] = True
        self.threads["write"]["running"] = True

        # Initialize thread process
        thread = Thread(target=self.read)
        thwrite = Thread(target=self.write)
        try:
            thread.setDaemon(True)
            thwrite.setDaemon(True)
        except AttributeError:
            thread.daemon = True
            thwrite.daemon = True
        thread.start()
        time.sleep(2)
        thwrite.start()

        # Setup thread and save data to variable threads
        self.threads["read"]["object"] = thread
        self.threads["write"]["object"] = thwrite

class Selector:
    def __init__(self, _env: Environments) -> None:
        self.env = _env

    @property
    def get_all(self):
        return self.env.environment

    def is_connected(self):
        if len(self.env.data) == 0:
            return False
        else:
            return True

    def exists(self, key):
        keys = self.env.environment.keys()
        return (True if key in keys else False)

    def update(self, key, value):
        self.env.environment[key] = value
        return True

    def delete(self, key):
        if self.exists(key):
            self.env.environment.pop(key)
            return True
        else:
            return False