import os
import sys
import json
import traceback
import importlib.util
from pathlib import Path
from glob import glob

from jagad.utils.constants import MODULE_PATH
from jagad.exceptions import NoModuleError
from jagad.terminal.console import print, print_error, print_warning, Terminal
from jagad.utils.typedata import Commands

class Scanner(object):
    def __init__(self) -> None:
        super().__init__()
        self.PACKAGES = []

    @property
    def get_package(self):
        return self.PACKAGES

    def get_module_dirs(self):
        results = []
        for module in MODULE_PATH:
            if os.path.isdir(module):
                for module_path in os.listdir(module):
                    join_path = os.path.join(module, module_path)
                    if os.path.isdir(join_path):
                        results.append(join_path)
        return results

    def get_package_files(self, exception: bool = True):
        for module_dir in self.get_module_dirs():
            package_file = os.path.join(module_dir, "module.json")
            if os.path.isfile(package_file):
                self.PACKAGES.append(package_file)
            else:
                if exception is True:
                    raise NoModuleError(package_file, os.path.basename(module_dir), "filename package not found")
                else:
                    yield NoModuleError(package_file, os.path.basename(module_dir), "filename package not found").get_message()
    
class Manager:
    def __init__(self) -> None:
        self.scanner = Scanner()
        self.terminal = Terminal()
        self.running = False
        self.module = None
        self.apps = None
        self.data = {"modules": []}

    @property
    def get_data(self):
        return self.data

    @property
    def get_modules(self):
        return self.data["modules"]

    def reset(self):
        self.running = False
        self.module = None
        self.apps = None

    def exists(self, module_name: str):
        mdl = self.getModule(module_name)
        if mdl is False or mdl is None: return mdl
        else: return True

    def run_command(self, command: str, arguments: tuple = None):
        if self.apps is None and self.module is None: return False
        else:
            try:
                optienv = self.apps.optienv
                isExists = optienv.exists("commands")
                if isExists is False:
                    return False
                else:
                    commands = optienv.get("commands")
                    if isinstance(commands, Commands):
                        if commands.exists(command):
                            commands.execute(command, arguments)
                            return True
                        else:
                            return False
                    else:
                        print_error(f"Module error, unknown command type!")
                        return False
            except AttributeError as attr:
                traceback.print_exc()
                print_error(f"Unable to call virtual environment, please read docs example.")
                return False
                
    def getModule(self, module_name: str):
        for module in self.data["modules"]:
            try:
                package = module["package"]
                if module_name == package:
                    return module
            except KeyError:
                print_error(f"Error searching packages, key 'package' not found in line ")
                return None
        return False

    def load_package(self, filename: str):
        if os.path.isfile(filename):
            with open(filename, "r") as File:
                content = File.read()
                try:
                    data = json.loads(content)
                    data["path"] = filename
                    self.data["modules"].append(data)
                    return True
                except (json.JSONDecodeError, json.decoder.JSONDecodeError) as error:
                    module = os.path.basename(os.path.split(filename)[0])
                    print_error(f"{module}: Syntax error in line {error.lineno}")
                    return False
        else:
            return NoModuleError(filename, None, "filename package not found").get_message()

    def openfile(self, filename: str, mode: str = "r", buffer=1024):
        try:
            data = ""
        except UnicodeDecodeError:
            print_error(f"Can't decode content from file")

    def initalize(self):
        error = self.scanner.get_package_files(False)
        for err in error:
            print_error(err)
        for package in self.scanner.get_package:
            self.load_package(package)

    def process_module(self):
        try:
            self.apps = self.module.Apps()
            return self.apps.run()
        except Exception as err:
            if isinstance(err, AttributeError):
                print_error(f"Unable to run module, message: {err}")
            elif isinstance(err, ModuleNotFoundError):
                print_error(f"Unable to run module, no dependences installed '{err.name}'")
            else:
                print_error(f"Syntax error, message: {err}")
            self.reset()
            return False

    def run(self, module: str):
        if self.running is False:
            getmod = self.getModule(module)
            try:
                script = getmod["script"]
                script_init = script["main"]
            except KeyError:
                script_init = "__init__.py"
            module_dirname = os.path.dirname(getmod["path"])
            module_path = os.path.join(module_dirname, script_init)
            if os.path.isfile(module_path):
                source = ""
                with open(module_path, "r") as File:
                    while True:
                        data = File.read(1024)
                        if not data: break
                        else:
                            source += data
                module_spec = importlib.util.spec_from_loader(module, loader=False)
                self.module = importlib.util.module_from_spec(module_spec)
                try:
                    exec(source, self.module.__dict__)
                    isProcess = self.process_module()
                    if isProcess is True:
                        self.running = True
                        return True
                    else: 
                        self.reset()
                        return False
                except Exception as err:
                    if isinstance(err, NameError):
                        print_error(f"Syntax error, type: NameError, message: {err}")
                    else:
                        # traceback.print_exc()
                        print_error(f"Syntax error, message: {err}")
                    self.reset()
                    return False
            else:
                print_error(f"{module}: No such file or directory '{os.path.basename(module_path)}' on path '{module_dirname}'")
                self.reset()
                return False
        else:
            print_warning(f"Module '{self.mdl}' already running...")
            i = input(f"Did you change module? (Y/n): ")
            if i.lower() == "y":
                try:
                    self.module.destroy()
                except AttributeError: pass
                self.reset()
                return self.run(module)
            else:
                self.reset()
                return False