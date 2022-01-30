import os
import sys
from jagad.exceptions import AttrError
from jagad.terminal.console import print_warning
from jagad.utils.typedata import (
    OptionEnv, OptionsDict, Options, File, Commands
)
from jagad.utils.constants import ROOT_PATH
from jagad.api.module import BaseModules

from modules.port_scanner.core import Core

class Apps(BaseModules):
    def __init__(self) -> None:
        self.options = Options()
        self.optienv = OptionEnv()
        self.core = Core()

    def initialize(self):
        option_target = OptionsDict()
        option_target.set_option("target")
        option_target.set_shortdesc("Set target")

        option_minrange = OptionsDict()
        option_minrange.set_option("min")
        option_minrange.set_shortdesc("Set min range port (e.g: 22)")
        option_minrange.set_values(int(22))

        option_maxrange = OptionsDict()
        option_maxrange.set_option("max")
        option_maxrange.set_shortdesc("Set max range port (e.g: 8080)")
        option_maxrange.set_values(int(8080))

        option_output = OptionsDict("output", os.path.join(ROOT_PATH, "share/portscanner"), "Set output path")

        self.options.set_opts(option_target)
        self.options.set_opts(option_minrange)
        self.options.set_opts(option_maxrange)
        self.options.set_opts(option_output)

        commands = Commands()
        commands.register("options", self.onOption)
        commands.register("set", self.onSet)
        commands.register("run", self.onRun)
        commands.register("reset", self.onReset)
        # commands.register("build", self.onBuild)
        self.optienv.set("commands", commands)
        return True

    def destroy(self):
        self.core.destroy()
        return True
        
    def onReset(self, argument: dict):
        self.core.reset()
        self.core.options = {}
        print("All in done.")
        return True
  
    def onSet(self, argument: dict):
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0 or argument_length == 1 or argument_length > 2:
            print(f"{argument['cmds']} <option> <value>")
            return False
        else:
            option = user_argument[0]
            value = user_argument[1]
            isExists = self.options.exists(option)
            if isExists:
                options = self.options.get_opts()
                index_value = options.index(isExists)
                old_value = options[index_value].value
                new_value = None
                if old_value is None:
                    new_value = value
                elif isinstance(old_value, File):
                    new_value = File(value)
                elif isinstance(old_value, int):
                    if value.isdigit():
                        new_value = int(value)
                    else:
                        print_warning(f"Invalid literal for int() with base 10")
                        return False
                        
                elif isinstance(old_value, bool):
                    if value.isdigit():
                        if value == "0" or value.lower() == "false":
                            new_value = bool(False)
                        elif value == "1" or value.lower() == "true":
                            new_value = bool(True)
                        else:
                            print_warning(f"Unknown value")
                            return False
                    else:
                        print_warning(f"Unknown value")
                        return False
                elif isinstance(old_value, str):
                    new_value = value
                new_option = OptionsDict(options[index_value].option, new_value, options[index_value].shortdesc)
                self.options.delete(index_value)
                self.options.set_opts(new_option)
            else:
                print (f"Option '{option}' is not defined")
            return False

    def onOption(self, argument: dict):
        specials = [
            {"key": "output", "type": "shortfile"},
            {"key": "target", "type": "normal"},
            {"key": "min", "type": "normal"},
            {"key": "max", "type": "normal"},
        ]
        for option in self.options.get_opts():
            key = option.option
            val = option.value
            try:
                self.optienv.set(key, val)
            except AttributeError as attr:
                raise AttrError(attr.args[0])
        user_argument = argument["user"]
        argument_length = len(user_argument)
        if argument_length == 0:
            self.optienv.pretty(specials=specials)
            return True
        else:
            first_argument = user_argument[0]
            self.optienv.pretty(first_argument, specials)
            return True

    def onRun(self, argument: dict = {}):
        # Run action
        self.core.reset()
        self.core.set_options(self.options.parse())
        isConnectionConnected = self.core.check_connection()
        if isConnectionConnected is True:
            print ("[+] Network connected")
            return True
        else:
            print ("[-] No network connection")
            return False