import os

class NoModuleError(Exception):
    def __init__(self, filename="", name="", message=""):
        self._name = name
        self._file = filename
        self._msg = message
        self._dir = os.path.split(filename)

    def __str__(self) -> str:
        return f"{self._name}: error exception '{self._msg}'"

    def get_message(self):
        module = os.path.basename(self._dir[0])
        return f"{module}: {self._msg}"

class ThreadingError(Exception):
    def __init__(self, message = "") -> None:
        self.message = message

    def __str__(self) -> str:
        print (self.message)

    def get_message(self):
        return self.message

class PrettyError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AttrError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ConfigError(Exception):
    pass

class UserExit(Exception):
    pass