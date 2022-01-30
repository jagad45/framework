import os
from configparser import ConfigParser
from jagad.terminal.colors import Fore

FRAMEWORK_PATHS = [
    "/usr/share/jagad7/framework", "/usr/share/jagad-framework",
    "/opt/jagad7framework", os.getcwd()
]

MODULE_PATH = [os.path.join(path, "modules") for path in FRAMEWORK_PATHS]
CONFIG_PATH = [os.path.join(path, "config.json") for path in FRAMEWORK_PATHS]
ROOT_PATH = f"{os.getcwd()}/system"
BIN_PATH = f"{ROOT_PATH}/bin"