import os
from pathlib import Path
from jagad.api.module import BaseAction
from jagad.utils.typedata import Commands
from jagad.utils.constants import ROOT_PATH
from jagad.terminal.colors import Fore
from jagad.terminal.console import print, print_error, print_warning
from jagad.handler.module import Manager

class Action(BaseAction):
    def __init__(self) -> None:
        self.cmds    = Commands()
        self.manager = Manager()
        self.path    = None
        self.module  = None

    @property
    def get_module(self):
        return self.module

    def initialize(self):
        self.manager.initalize()
        self.cmds.register("ls", self.onWalk)
        self.cmds.register("cd", self.onChangeDirectory)
        self.cmds.register("mkdir", self.onMakeDir)
        self.cmds.register("use", self.onUse)
        self.cmds.register("back", self.onBack)

    def onChangePath(self, method: str = "GET", path: str = ""):
        if method.lower() == "get":
            return self.path
        elif method.lower() == "post":
            self.path = path
            return True

    def onBack(self, argument: dict):
        if self.module is None:
            print_warning(f"Module is not defined!")
            return False
        else:
            try:
                print ("Destroying module...")
                self.manager.apps.destroy()
            except AttributeError: pass
            self.manager.reset()
            self.module = None
            return False

    def show_files(self, path: Path = None, indent: int = 2):
        if path is None:
            path = self.path
        listdir = os.listdir(path)
        output = ""
        for dirs in listdir:
            if os.path.isdir(dirs):
                output += Fore.BLUE
            else:
                output += Fore.WHITE
            output += dirs
            output += " " * indent
        print(output)
        return True

    def onWalk(self, argument: dict = {}):
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0:
            if isinstance(self.path, Path) is False:
                path = Path(self.path)
            else:
                path = self.path
            self.show_files(path)
        else:
            first_argument = user_argument[0]
            if first_argument == "":
                if isinstance(self.path, Path) is False:
                    path = Path(self.path)
                else:
                    path = self.path
                self.show_files(path)
                return True
            else:
                join_path = os.path.join(self.path, first_argument)
                if os.path.isdir(join_path):
                    self.show_files(join_path)
                    return True
                elif os.path.isfile(join_path):
                    print(f"{first_argument}: is a file, can't open directory")
                    return False
                else:
                    print(f"{first_argument}: no such file or directory")
                    return False

    def onChangeDirectory(self, argument: dict = {}):
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0:
            new_path = Path(ROOT_PATH)
            self.path = new_path
        else:
            first_argument = user_argument[0]
            if first_argument == ".": return True
            elif first_argument == "..":
                new_path = Path(self.path.parent)
                self.path = new_path
                return True
            else:
                join_path = os.path.join(self.path, first_argument)
                if os.path.isdir(join_path):
                    new_path = Path(join_path)
                    self.path = new_path
                    return True
                elif os.path.isfile(join_path):
                    print(f"{first_argument}: is a file, can't change directory")
                    return False
                else:
                    print(f"{first_argument}: no such file or directory")
                    return False

    def onMakeDir(self, argument: dict = {}):
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0:
            print(f"{argument['cmds']}: program error!")
            return False
        else:
            for dirs in user_argument:
                dirs = os.path.join(self.path, dirs)
                if os.path.isdir(dirs):
                    print_warning(f"{dirs}: directory already exists")
                elif os.path.isfile(dirs):
                    print_warning(f"{dirs}: is a file")
                else:
                    os.mkdir(dirs)
            return True

    def onUse(self, argument: dict = {}):
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0:
            print(f"{argument['cmds']} <type> <value>")
            return False
        else:
            use_type = user_argument[0]
            if use_type == "module":
                try:
                    val = user_argument[1]
                    isExists = self.manager.exists(val)
                    if isExists:
                        isActived = self.manager.run(val)
                        if isActived is True:
                            self.module = val
                            return True
                        else: return False
                    else:
                        print (f"{val}: module not found")
                        return False
                except IndexError:
                    print(f"{argument['cmds']} module <value>")
                    return False
                