import os
import sys
from jagad.exceptions import AttrError
from jagad.terminal.console import print_warning
from jagad.utils.typedata import (
    OptionEnv, OptionsDict, Options, File, Commands
)
from jagad.api.module import BaseModules

class Apps(BaseModules):
    def __init__(self) -> None:
        self.options = Options()
        self.optienv = OptionEnv()

    def initialize(self):
        option_target = OptionsDict()
        option_target.set_option("target")
        option_target.set_shortdesc("Set target")

        option_pathlist = OptionsDict()
        option_pathlist.set_option("filename")
        option_pathlist.set_shortdesc("Set subdomain list")
        option_pathlist.set_values(File("system/wordlist/subdomains.lst"))

        option_chunksize = OptionsDict()
        option_chunksize.set_option("chunksize")
        option_chunksize.set_shortdesc("Set reading chunk")
        option_chunksize.set_values(int(2048))

        option_isRaw = OptionsDict()
        option_isRaw.set_option("raw")
        option_isRaw.set_shortdesc("Set raw/byte mode, if use mode byte change raw value to 'False' or 0")
        option_isRaw.set_values(int(1))

        option_wordlist = OptionsDict("wordlist", list(), "Wordlist from filename")

        option_type = OptionsDict("output", "system/share/subdobrute/output/result.txt", "Set output path")
        option_encoding = OptionsDict("encoding", "utf-8", "Set content encoding")

        self.options.set_opts(option_target)
        self.options.set_opts(option_pathlist)
        self.options.set_opts(option_wordlist)
        self.options.set_opts(option_chunksize)
        self.options.set_opts(option_isRaw)
        self.options.set_opts(option_type)
        self.options.set_opts(option_encoding)

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
            {"key": "target", "type": "normal"},
            {"key": "filename", "type": "shortfile"},
            {"key": "wordlist", "type": "length"},
            {"key": "chunksize", "type": "normal"},
            {"key": "raw", "type": "normal"},
            {"key": "output", "type": "normal"},
            {"key": "encoding", "type": "normal"},
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
        pass