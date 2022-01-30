import json
import os
from jagad.utils.constants import CONFIG_PATH
from jagad.terminal.console import print_warning
from jagad.exceptions import ConfigError

class Selector:
    def __init__(self, data: dict = {}) -> None:
        self.data = data
        self.output = None

    @property
    def get(self):
        return self.output

    def exists(self, key):
        for x in self.data:
            if x == key:
                return True
        return False

    def select(self, key):
        if self.exists(key):
            data = self.data[key]
            if isinstance(data, dict):
                return Selector(data)
            else:
                self.output = data
                return data

class Config:
    def __init__(self) -> None:
        self.CONFIG_PATH = CONFIG_PATH
        self.data = {}

    def find_path(self):
        result = []
        for path in self.CONFIG_PATH:
            if os.path.isfile(path):
                result.append(path)
        if len(result) == 0:
            raise ConfigError("No config found!")
        else:
            return result

    def read(self, files: list = []):
        temp = {}
        if len(files) == 0:
            files = self.find_path()
        for file in files:
            if os.path.isfile(file):
                with open(file, "r") as File:
                    content = File.read()
                    try:
                        data = json.loads(content)
                        temp.update(data)
                    except (json.JSONDecodeError, json.decoder.JSONDecodeError) as err:
                        print_warning(f"Unable load configure on file '{file}'")
                        print_warning(f"Syntax error on line: {err.lineno}")
        self.data = temp
        return Selector(self.data)