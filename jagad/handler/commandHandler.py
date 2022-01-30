import os
from jagad.exceptions import UserExit
from jagad.terminal.console import Terminal, print_warning
from jagad.terminal.console import print
from jagad.utils.constants import BIN_PATH
from jagad.handler.commandAction import Action
from jagad.utils.config import Config
from pathlib import Path

class CommandHandler:
    def __init__(self, terminal: Terminal) -> None:
        self.action = Action()
        self.action.run()

        self._config = Config()
        self.config = self._config.read()

        self.terminal = terminal
        self.commands = None
        self.parameters = None
        self.path = None

    def parse(self, text: str):
        text_split = text.split(" ")
        if len(text_split) == 0:
            return None, []
        elif len(text_split) == 1:
            return text_split[:1], tuple([])
        elif len(text_split) >= 2:
            return text_split[:1], tuple(text_split[1:])

    def find_syscmd(self):
        path = Path(BIN_PATH)
        results = [os.path.basename(gen).replace(".py", "") for gen in path.glob("*.py")]
        return results

    def execute(self, file, argument: tuple = ()):
        argument_length = len(argument)
        try:
            python_executable = self.config.select("executable").select("python").select("path")
            if os.path.isfile(python_executable):
                print_warning("Can't use executable file, change default path")
            else:
                python_executable = "python3"
        except AttributeError:
            python_executable = "python3"
        if argument_length == 0:
            os.system(f"{python_executable} {file}")
        else:
            join_argument = " ".join(argument)
            os.system(f"{python_executable} {file} {join_argument}")

    def handle_command(self, command: str, arguments: tuple):
        cmd = command.strip()
        if cmd == "": return False
        elif cmd == "exit":
            raise UserExit
        else:
            isExists = self.action.cmds.exists(cmd)
            if isExists:
                self.action.cmds.execute(cmd, arguments)
            else:
                command_file = os.path.join(BIN_PATH, f"{cmd}.py")
                if os.path.isfile(command_file):
                    self.execute(command_file, arguments)
                    return True
                elif self.action.manager.run_command(command, arguments):
                    return True
                else:
                    print(f"{cmd}: command not found")
                    return False