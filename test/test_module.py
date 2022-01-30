# Fix error module not found
import os
import sys
sys.path.append(os.getcwd())

from modules.hash_cracker.apps import Apps
from jagad.utils.typedata import File

if __name__ == "__main__":
    apps = Apps()
    apps.run()
    options = apps.options.get_opts()
    while True:
        user_input = input("> ")
        text_split = user_input.split(" ")
        if text_split[0] == "o":
            try:
                output = apps.optienv.get(text_split[1])
                if isinstance(output, File):
                    print (output.filename)
                else:
                    print (output)
            except IndexError:
                special = [
                    {"key": "target", "type": "normal"},
                    {"key": "wordlist", "type": "shortfile"}
                ]
                apps.optienv.pretty(specials=special)
        elif text_split[0] == "s":
            pass