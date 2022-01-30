# Generates ANSI character codes to printing colors to terminals
# Copyright Jonathan Hartley 2013. BSD 3-Clause license
# Copyright Billal Fauzan 2022. GNU General Public License
import os

CSI = "\033["

def code_to_chars(code):
    if os.name != "":
        return f"{CSI}{code}m"
    else:
        return ""

class AnsiCodes(object):
    def __init__(self):
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))

class AnsiFore(AnsiCodes):
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37
    RESET   = 39

class AnsiForeLight(AnsiCodes):
    BLACK   = 90
    RED     = 91
    GREEN   = 92
    BLUE    = 94
    MAGENTA = 95
    CYAN    = 96
    WHITE   = 97

Fore = AnsiFore()
ForeLight = AnsiForeLight()