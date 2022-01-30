from jagad.environments import Environments, Selector
from jagad.utils.constants import ROOT_PATH
from jagad.terminal.console import Terminal
from jagad.handler.commandHandler import CommandHandler
from jagad.exceptions import UserExit
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from pathlib import Path

class Prompt:
    def __init__(self) -> None:
        self.session = PromptSession()
        self.path = ""
        self.module = "'"
        self.message = []
        self.style = None

    def set_path(self, _path):
        self.path = _path
        return True

    def build_message(self):
        self.message = [
            ("class:username","jagad"),
            ("class:at","@"),
            ("class:framework", "framework"),
            ("class:colon",     ":"),
            # ("class:path",      self.path.replace(ROOT_PATH, "")),
            ("class:path",      self.path),
            ("class:dolar",     "$ ")
        ]

    def build_style(self):
        self.style = Style.from_dict({
            "":         "ansiwhite",
            "username": "ansigreen",
            "at":       "ansiwhite",
            "colon":    "ansiwhite",
            "dolar":    "ansiblue",
            "path":     "ansicyan underline"
        })

    def input(self):
        try:
            self.build_message()
            self.build_style()
            user_input = self.session.prompt(self.message, style=self.style)
            return user_input
        except KeyboardInterrupt: raise UserExit
        
class Shell:
    def __init__(self) -> None:
        self.completerList  = []
        self.prompt         = Prompt()
        self.environment    = Environments()
        self.terminal       = Terminal(self.environment)
        self.cmdhamdler     = CommandHandler(self.terminal)
        self.PATH           = Path(ROOT_PATH)

        self.cmdhamdler.action.onChangePath("POST", self.PATH)

    def changePath(self):
        new_path = self.cmdhamdler.action.onChangePath("GET")
        if new_path != self.PATH:
            if isinstance(new_path, bool):
                return False
            self.PATH = Path(f"{new_path}")
            return True
        else:
            return False

    def build_path(self):
        path_cwd = self.PATH
        if path_cwd == Path(ROOT_PATH):
            return "~"
        else:
            return str(path_cwd)

    def initalize(self):
        self.environment.run()
        self.selector = Selector(self.environment)
        self.selector.update("commands", self.completerList)

    def get_user_input(self):
        return self.prompt.input()

    def run(self):
        while True:
            self.changePath()
            try:
                # self.prompt.set_path(self.cmdhamdler)
                if self.cmdhamdler.action.get_module is None:
                    self.prompt.set_path("~")
                else:
                    self.prompt.set_path(self.cmdhamdler.action.get_module)
                user_input = self.get_user_input()
                command, argument = self.cmdhamdler.parse(user_input)
                self.cmdhamdler.handle_command(command[0], argument)
            except UserExit:
                self.terminal.quit()