# Copyright Billal Fauzan 2022. GNU General Public License
import sys
from jagad.terminal.colors import Fore, ForeLight
from jagad.utils.timeutils import get_timenow, get_timestamp, FORMAT_GET_TIME

COLOR_RED       = Fore.RED
COLOR_GREEN     = Fore.GREEN
COLOR_BLUE      = Fore.BLUE
COLOR_YELLOW    = Fore.YELLOW
COLOR_CYAN      = Fore.CYAN
COLOR_NORMAL    = Fore.RESET

TAB     = "\t"
NEWLINE = "\n"

class TerminalCodes:
    NORMAL  = 0
    INFO    = 1
    WARNING = 2
    ERROR   = 3
    RUNNING = 4
    PROCESS = 5

class Terminal:
    def __init__(self, environments = None) -> None:
        self.environment = environments

    def quit(self):
        if self.environment is not None:
            self.environment.destroy()
        sys.exit()

    def console(self, message: str, code: int = 0, _time: bool = False, _quit: bool = False):
        terminal_status = ""
        terminal_timer  = ""
        if code == TerminalCodes.NORMAL:
            pass
        elif code == TerminalCodes.INFO:
            terminal_status += f"{COLOR_NORMAL}["
            terminal_status += f"{COLOR_GREEN}INFO"
            terminal_status += f"{COLOR_NORMAL}] "
        elif code == TerminalCodes.WARNING:
            terminal_status += f"{COLOR_NORMAL}["
            terminal_status += f"{COLOR_YELLOW}WARNING"
            terminal_status += f"{COLOR_NORMAL}] "
        elif code == TerminalCodes.ERROR:
            terminal_status += f"{COLOR_NORMAL}["
            terminal_status += f"{COLOR_RED}ERROR"
            terminal_status += f"{COLOR_NORMAL}] "
        elif code == TerminalCodes.PROCESS:
            terminal_status += f"{COLOR_NORMAL}["
            terminal_status += f"{COLOR_CYAN}PROCESS"
            terminal_status += f"{COLOR_NORMAL}] "
        elif code == TerminalCodes.RUNNING:
            terminal_status += f"{COLOR_NORMAL}[ "
            terminal_status += f"{COLOR_GREEN}RUNNING"
            terminal_status += f"{COLOR_NORMAL}] "
        else: terminal_status = ""

        if _time is True:
            terminal_timer += f"{COLOR_NORMAL}["
            terminal_timer += f"{COLOR_CYAN}{get_timenow(FORMAT_GET_TIME)}"
            terminal_timer += f"{COLOR_NORMAL}] "
        output = f"{terminal_timer}{terminal_status}{message}{NEWLINE}{COLOR_NORMAL}"
        sys.stdout.write(output)
        sys.stdout.flush()
        if _quit:
            self.quit()

def print(s):
    Terminal().console(s, TerminalCodes.NORMAL, False, False)

def print_warning(s, _time: bool = False, _quit: bool = False):
    Terminal().console(s, TerminalCodes.WARNING, _time, _quit)

def print_error(s, _time: bool = False, _quit: bool = False):
    Terminal().console(s, TerminalCodes.ERROR, _time, _quit)