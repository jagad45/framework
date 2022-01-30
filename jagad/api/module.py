from typing import Callable
from jagad.utils.typedata import Commands, Options, OptionEnv
from jagad.terminal.console import print, print_error, print_warning
from jagad.exceptions import AttrError

class BaseAction(object):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self):
        pass

    def run(self):
        self.initialize()
    
class BaseModules(object):
    def __init__(self) -> None:
        super().__init__()

        self.options = Options()
        self.optienv = OptionEnv()

    @property
    def connected(self):
        return True

    def set_starter(self, callback: Callable):
        self.optienv.set("start", callback)
        return True

    def register(self):
        for options in self.options.get_opts():
            option = options.option
            value = options.value
            try:
                self.optienv.set(option, value)
            except AttributeError as attr:
                raise AttrError(attr.args[0])

    def destroy(self):
        # Fungsi yang akan menghandle perintah 'quit' atau 'back'
        raise NotImplementedError

    def initialize(self):
        # Fungsi yang akan dijalankan pertama kali di dalam module
        raise NotImplementedError
    
    def run(self):
        try:
            self.initialize()
            self.register()
            return True
        except NotImplementedError:
            print_error("No implemented script! failed to call function initialize")
            return False