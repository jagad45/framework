import os
from pathlib import Path
import traceback
from typing import Any
from typing import Callable

from jagad.exceptions import PrettyError
from jagad.terminal.colors import Fore
from jagad.terminal.console import print_error, print_warning

class File(object):
    def __init__(self, filename: str) -> None:
        self.name = filename
        # self.filename = file

        self._path = Path(filename)
        
    @property
    def value(self):
        return self.name

    def exists(self):
        return self._path.exists()

    def isfile(self):
        return self._path.is_file()

    def isdir(self):
        return self._path.is_dir()

    def parent(self):
        return self._path.parent

    def parents(self):
        return self._path.parents
        
    def basename(self):
        return os.path.basename(self._path)
        
class OptionsDict:
    def __init__(self, option: str = "", values: Any = None, shortdesc: str = "") -> None:
        self._dict = {}

        self.set_option(option)
        self.set_values(values)
        self.set_shortdesc(shortdesc)

    @property
    def option(self):
        return self._dict["option"]

    @property
    def value(self):
        return self._dict["values"]
    
    @property
    def shortdesc(self):
        return self._dict["shortdesc"]

    def set_option(self, option: str = ""):
        self._dict["option"] = option
        return True
        
    def set_values(self, values: Any = None):
        self._dict["values"] = values
        return True
        
    def set_shortdesc(self, desc: str):
        self._dict["shortdesc"] = desc
        return True
        
class Options:
    def __init__(self) -> None:
        self.opts = []

    def exists(self, opt):
        for opts in self.opts:
            option = opts.option
            if opt == option: return opts
        return False

    def parse(self):
        data = {}
        for opts in self.opts:
            data[opts.option] = opts.value
        return data

    def set_opts(self, opt: OptionsDict):
        self.opts.append(opt)

    def delete(self, index):
        try:
            del self.opts[index]
            return True
        except IndexError:
            return False
        
    def get_opts(self):
        return self.opts

class OptionEnv:
    def __init__(self) -> None:
        self.env = {}
        self.whitelist = ["start", "run", "commands"]

    def set_whitelist(self, data):
        if isinstance(data, list) or isinstance(data, tuple):
            self.whitelist.extend(data)
        else:
            self.whitelist.append(data)

    def exists(self, key: str):
        if key in self.env: return True
        else: return False

    def set(self, option: str, value: Any = None):
        self.env[option] = value

    def get(self, env: str):
        if self.exists(env):
            return self.env[env]
        else:
            return False

    def block_pretty(self, env: list = [], specials: list = [], indent: int = 4):
        output = ""
        for key in self.env:
            if key in self.whitelist: continue
            else:
                current_value = ""
                env_value = self.env[key]
                if env_value is None:
                    current_value += Fore.RED
                    current_value += f"{env_value}"
                else:
                    current_value += Fore.GREEN
                    if len(specials) >= 1:
                        for items in specials:
                            if isinstance(items, dict):
                                try:
                                    keyx = items["key"]
                                    ktype = items["type"]
                                    if keyx == key:
                                        if ktype == "length":
                                            current_value += f"{len(env_value)}"
                                        elif ktype == "integer":
                                            current_value += f"{len(env_value)}"
                                        elif keyx == key and ktype == "shortfile":
                                            try:
                                                filename = env_value.value
                                            except AttributeError:
                                                filename = env_value
                                            current_value += f"{os.path.basename(filename)}" 
                                        else:
                                            current_value += f"{env_value}"
                                        break
                                except KeyError:
                                    current_value += f"{env_value}"
                                    break
                            else:
                                print_warning(f"'{items}' is a not dictionary")
                                break
                    else:
                        current_value += f"{env_value}"
            current_value += Fore.WHITE
            output += f"{key}:{current_value}"
            output += f" " * indent
        print(output)

    def pretty(self, env: str = "", specials: list = [], indent: int = 4):
        if env == "":
            envs = list(self.env)
            self.block_pretty(envs, specials, indent)
        elif self.exists(env):
            self.block_pretty([env], specials, indent)
        else:
            raise PrettyError(f"{env}: keyword not found")

class Commands:
    def __init__(self) -> None:
        self.obj = []

    @property
    def list(self):
        return self.obj

    def exists(self, command: str):
        for obj in self.obj:
            if command == obj["command"]:
                return True
        return False

    def register(self, command: str, callback: Callable, parameter: tuple = None):
        data = {
            "command": command,
            "callback": callback,
            "params": parameter
        }
        self.obj.append(data)

    def execute(self, command: str, argument: tuple = None):
        for obj in self.obj:
            try:
                if command == obj["command"]:
                    arg = {
                        "user": argument,
                        "root": obj["params"],
                        "cmds": obj["command"]
                    }
                    callback = obj["callback"]
                    callback(arg)
                    return True
            except TypeError as err:
                print_error(f"{err}", _quit=True)
                return False
            except RecursionError:
                print_error(f"Unable to call handler, function not found", _quit=True)
                return False